"""Offline composition probes; source/export/model/game outcomes are fixtures."""
from dataclasses import asdict
import hashlib
import io
import json
from pathlib import Path
import socket
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

SNAPSHOT = Path(sys.argv[1])
MANIFEST = json.loads(Path(sys.argv[2]).read_text())
RESULT_PATH = Path(sys.argv[3])
sys.argv = sys.argv[:1]
for record in MANIFEST['sources']:
    path = SNAPSHOT / record['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == record['sha256'], record['path']
    assert len(path.read_bytes()) == record['bytes'], record['path']
sys.path.insert(0, str(SNAPSHOT))
from services.controller import (ControllerLimits, ExecRequest, FrozenContext, ResultRequest,
    SubmitRequest, TOOL_NAMES, launch_real, run_synthetic)
from services.controller_ledger import (ArtifactError, CapturingSandboxAdapter,
    DurableScrimmageAdapter, ExportedExecReply, SourceArtifactStore, SourceExport)
from services.ledger import DurableLedger, LedgerError
from services.responses_transport import (MODEL, OfflineInputCount, OfflineResponsesTransport)

SOURCE = b'package bot; public class RobotPlayer { /* synthetic source, never compiled */ }\n'
MUTATED = b'package bot; public class RobotPlayer { /* mutation after trusted capture */ }\n'
PRIVATE = 'PRIVATE_FIXTURE_DIAGNOSTIC_MUST_NOT_REACH_CANDIDATE'
FAKE_HANDLE = 'a_' + 'f' * 32
CONTEXT = FrozenContext(b'synthetic controller system\r\n  exact bytes\n',
                        b'OFFLINE FIXTURE ONLY: test six-tool protocol continuity.\n')
RESULTS = {}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('utf-8')


def source_zip(data):
    sink = io.BytesIO()
    with zipfile.ZipFile(sink, 'w', compression=zipfile.ZIP_STORED) as archive:
        entry = zipfile.ZipInfo('bot/RobotPlayer.java', date_time=(2020, 1, 1, 0, 0, 0))
        entry.external_attr = 0o100644 << 16
        archive.writestr(entry, data)
    return sink.getvalue()


def call_output(body):
    return [json.loads(item['output']) for item in body['input']
            if item.get('type') == 'function_call_output']


def first_field(body, key):
    return next(item[key] for item in call_output(body) if key in item)


def tool(turn, name, arguments):
    return {'type': 'function_call', 'id': f'fc_{turn}', 'status': 'completed',
            'call_id': f'call_{turn}', 'name': name, 'arguments': json.dumps(arguments)}


def provider_response(turn, output):
    return encoded({'object': 'response', 'status': 'completed', 'model': MODEL,
                    'service_tier': 'default', 'error': None, 'incomplete_details': None,
                    'output': output, 'usage': {'input_tokens': 100, 'output_tokens': 16,
                     'total_tokens': 116, 'input_tokens_details': {'cached_tokens': 0},
                     'output_tokens_details': {'reasoning_tokens': 8}}})


def final(turn):
    return provider_response(turn, [{'type': 'message', 'id': f'msg_final_{turn}',
        'role': 'assistant', 'phase': 'final_answer', 'status': 'completed',
        'content': [{'type': 'output_text', 'annotations': [],
                     'text': 'Offline fixture composition complete; no game or inference ran.'}]}])


class FixtureCounter:
    def __init__(self):
        self.bodies = []

    def count_input(self, body):
        self.bodies.append(body)
        return OfflineInputCount(hashlib.sha256(body).hexdigest(), 100)


class FixtureExchange:
    """The step functions are trusted test scripts, never generated model code."""
    def __init__(self, steps):
        self.steps = list(steps)
        self.requests = []
        self.bodies = []

    def respond(self, request):
        self.requests.append(request)
        body = json.loads(request.body)
        self.bodies.append(body)
        assert body['model'] == MODEL
        assert body['reasoning'] == {'effort': 'high'}
        assert body['instructions'].encode('utf-8') == CONTEXT.system
        assert body['input'][0]['content'].encode('utf-8') == CONTEXT.task
        assert tuple(spec['name'] for spec in body['tools']) == TOOL_NAMES
        assert all(spec['type'] == 'function' and spec['strict'] for spec in body['tools'])
        assert body['parallel_tool_calls'] is False
        assert body['store'] is False and body['stream'] is False
        assert body['truncation'] == 'disabled'
        ids = [item['id'] for item in body['input'] if 'id' in item]
        assert len(ids) == len(set(ids))
        step = self.steps.pop(0)
        if isinstance(step, Exception):
            raise step
        result = step(body) if callable(step) else step
        if result is None:
            return final(request.attempt)
        name, arguments = result
        turn = request.attempt
        return provider_response(turn, [
            {'type': 'reasoning', 'id': f'rs_{turn}', 'summary': [],
             'encrypted_content': f'OPAQUE_FIXTURE_STATE_{turn}'},
            {'type': 'message', 'id': f'msg_comment_{turn}', 'role': 'assistant',
             'status': 'completed', 'phase': 'commentary',
             'content': [{'type': 'output_text', 'text': 'Synthetic step only.', 'annotations': []}]},
            tool(turn, name, arguments)])


class MemoryExportBackend:
    """In-memory workspace and trusted byte export; exec NEVER launches anything."""
    def __init__(self):
        self.files = {'src/bot/RobotPlayer.java': SOURCE}
        self.exports = []
        self.exec_requests = []
        self.override = None

    def write(self, request):
        self.files[request.path] = request.content

    def read(self, request):
        return self.files[request.path][request.offset:request.offset + request.limit]

    def exec(self, request):
        assert type(request) is ExecRequest
        assert request.argv == ('fixture-package-only',)
        assert request.cwd == 'src'
        self.exec_requests.append(request)
        if self.override is not None:
            return self.override
        data = self.files['src/bot/RobotPlayer.java']
        self.exports.append(data)
        return ExportedExecReply('succeeded', b'synthetic byte export; no compilation',
                                 source=SourceExport('bot', source_zip(data)))


WRITE = ('workspace_write', {'path': 'src/bot/RobotPlayer.java', 'content': SOURCE.decode()})
READ = ('workspace_read', {'path': 'src/bot/RobotPlayer.java', 'offset': 0, 'limit': len(SOURCE)})
EXEC = ('workspace_exec', {'argv': ['fixture-package-only'], 'cwd': 'src', 'timeout_seconds': 1})
MUTATE = ('workspace_write', {'path': 'src/bot/RobotPlayer.java', 'content': MUTATED.decode()})


class FullCompositionSmoke(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='bcenv-offline-composition-')
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'actual-sqlite.db'
        self.ledger = DurableLedger(self.path, clock=lambda: 1000)
        self.store = SourceArtifactStore()
        self.backend = MemoryExportBackend()
        self.sandbox = CapturingSandboxAdapter(self.backend, self.store, 'owner-a', 'run-a')
        self.adapter = DurableScrimmageAdapter(self.ledger, self.store, 'owner-a', 'run-a')
        self.counter = FixtureCounter()
        self.socket_guard = patch.object(socket, 'socket', side_effect=AssertionError('network forbidden'))
        self.process_guard = patch.object(subprocess, 'Popen', side_effect=AssertionError('execution forbidden'))
        self.socket_guard.start(); self.process_guard.start()
        self.addCleanup(self.socket_guard.stop); self.addCleanup(self.process_guard.stop)

    def run_steps(self, steps, *, transport=None, sandbox=None, adapter=None):
        if transport is None:
            self.exchange = FixtureExchange(steps)
            transport = OfflineResponsesTransport(self.exchange, self.counter)
        report = run_synthetic(CONTEXT, transport, sandbox or self.sandbox, adapter or self.adapter)
        self.assertEqual(report.initial_sha256, CONTEXT.sha256)
        self.assertNotIn(PRIVATE, repr(report))
        self.assertNotIn('OPAQUE_FIXTURE_STATE_', repr(report))
        return transport, report

    def rows(self, query):
        with sqlite3.connect(self.path) as database:
            return database.execute(query).fetchall()

    def submit_step(self, body):
        return 'scrimmage_submit', {'artifact_id': first_field(body, 'artifact_id'), 'package': 'bot'}

    def finish_and_result_step(self, body):
        # Explicit trusted test event. No worker, compilation, game or model ran.
        identifier = first_field(body, 'submission_id')
        lease = self.ledger.reserve_job('owner-a', identifier, 'synthetic-fixture-worker')
        self.assertEqual(lease.source.files[0].data, SOURCE)
        self.ledger.finish('owner-a', identifier, lease.worker, lease.generation,
            {'status': 'complete', 'validated_complete': True,
             'summary': {'games': 1, 'wins': 1, 'draws': 0, 'losses': 0},
             'private_worker_diagnostic': PRIVATE, 'private_path': '/fixture/private'})
        return 'scrimmage_result', {'submission_id': identifier}

    def test_01_full_continuity_immutable_export_and_durable_completion(self):
        steps = [WRITE, READ, EXEC, MUTATE, self.submit_step, self.finish_and_result_step,
                 lambda body: ('scrimmage_replay', {'submission_id': first_field(body, 'submission_id')}), None]
        transport, report = self.run_steps(steps)
        self.assertEqual((report.status, report.turns, report.tool_calls), ('complete', 8, 7))
        self.assertEqual(self.backend.files['src/bot/RobotPlayer.java'], MUTATED)
        self.assertEqual(self.backend.exports, [SOURCE])
        self.assertEqual(self.rows('SELECT state FROM jobs'), [('complete',)])
        self.assertEqual(self.rows('SELECT data FROM source_files'), [(SOURCE,)])
        results = [item['result'] for item in map(json.loads, report.transcript) if 'result' in item]
        self.assertEqual(results[1]['text'].encode(), SOURCE)
        self.assertEqual(results[-2]['summary'], {'games': 1, 'wins': 1, 'draws': 0, 'losses': 0})
        self.assertEqual(results[-1]['reason'], 'replay_withheld')
        self.assertNotIn('validated_complete', repr(results))
        submission = next(item['submission_id'] for item in results if 'submission_id' in item)
        reopened = DurableLedger(self.path, clock=lambda: 1000)
        self.assertEqual(reopened.result('owner-a', submission)['status'], 'complete')
        self.assertEqual(len(transport.attempts), 8)
        self.assertTrue(all(item.outcome == 'reported' for item in transport.attempts))
        self.assertEqual(sum(item.reserved_input_tokens for item in transport.attempts), 128000)
        self.assertEqual(sum(item.reserved_output_tokens for item in transport.attempts), 64000)
        self.assertEqual(self.counter.bodies, [request.body for request in self.exchange.requests])
        self.assertEqual(len(self.exchange.bodies[-1]['input']), 1 + 7 * 4)
        RESULTS['full_continuity'] = {'status': report.status, 'model_fixture_attempts': 8,
            'tool_calls': 7, 'all_six_tools': True, 'captured_source_immutable_after_workspace_mutation': True,
            'sqlite_jobs': 1, 'sqlite_state': 'complete', 'reopened_result_complete': True,
            'completion_evidence': 'fabricated trusted fixture; no game was run',
            'reserved_input_tokens': 128000, 'reserved_output_tokens': 64000,
            'observed_fixture_input_tokens': 800, 'observed_fixture_output_tokens': 128,
            'initial_context_sha256': report.initial_sha256,
            'captured_source_sha256': hashlib.sha256(SOURCE).hexdigest()}

    def test_02_failed_export_does_not_mint_handle_or_create_job(self):
        self.backend.override = ExportedExecReply('succeeded', source=SourceExport('bot', b'bad archive'))
        transport, report = self.run_steps([EXEC,
            ('scrimmage_submit', {'artifact_id': FAKE_HANDLE, 'package': 'bot'}), None])
        self.assertEqual(report.status, 'complete')
        results = [item['result'] for item in map(json.loads, report.transcript) if 'result' in item]
        self.assertEqual(results, [{'status': 'infrastructure_failure', 'reason': 'adapter_failure'},
                                   {'status': 'rejected', 'reason': 'unknown_handle'}])
        self.assertEqual(self.rows('SELECT count(*) FROM jobs'), [(0,)])
        self.assertEqual(len(transport.attempts), 3)
        self.assertEqual(sum(item.reserved_input_tokens for item in transport.attempts), 48000)
        RESULTS['failed_export'] = {'minted_authority': False, 'sqlite_jobs': 0,
            'error_codes': [item['reason'] for item in results], 'retained_attempts': 3,
            'reserved_input_tokens': 48000, 'reserved_output_tokens': 24000}

    def test_03_cross_owner_and_cross_run_handles_are_denied(self):
        transport, report = self.run_steps([WRITE, EXEC, self.submit_step, None])
        self.assertEqual(report.status, 'complete')
        results = [item['result'] for item in map(json.loads, report.transcript) if 'result' in item]
        handle = next(item['artifact_id'] for item in results if 'artifact_id' in item)
        identifier = next(item['submission_id'] for item in results if 'submission_id' in item)
        codes = []
        for owner, run in (('owner-b', 'run-a'), ('owner-a', 'run-b')):
            other = DurableScrimmageAdapter(self.ledger, self.store, owner, run)
            for action, request in ((other.submit, SubmitRequest(handle, 'bot')),
                                    (other.result, ResultRequest(identifier)),
                                    (other.replay, ResultRequest(identifier))):
                with self.assertRaises(ArtifactError) as caught:
                    action(request)
                codes.append(caught.exception.code)
        with self.assertRaises(LedgerError) as caught:
            self.ledger.result('owner-b', identifier)
        self.assertEqual(caught.exception.code, 'not_found')
        self.assertEqual(codes, ['unknown_artifact', 'unknown_submission', 'unknown_submission'] * 2)
        self.assertEqual(self.rows('SELECT count(*) FROM jobs'), [(1,)])
        RESULTS['cross_scope'] = {'adapter_denials': codes, 'ledger_cross_owner_denial': 'not_found',
                                 'sqlite_jobs_unchanged': 1, 'retained_model_attempts': len(transport.attempts),
                                 'authentication_claim': 'host fixture scopes only, no authenticated service'}

    def test_04_unknown_model_outcome_retains_budget_and_never_autoretries(self):
        transport, first = self.run_steps([TimeoutError(PRIVATE), None])
        self.assertEqual(first.status, 'transport_failure')
        self.assertEqual(len(self.exchange.requests), 1)
        self.assertEqual(transport.attempts[0].outcome, 'unknown')
        self.assertEqual(self.rows('SELECT count(*) FROM jobs'), [(0,)])
        # The test operator explicitly re-enters the exact failed initial turn.
        # Neither transport nor controller performs an automatic retry.
        transport, second = self.run_steps([], transport=transport)
        self.assertEqual(second.status, 'complete')
        self.assertEqual([item.outcome for item in transport.attempts], ['unknown', 'reported'])
        self.assertEqual(self.exchange.requests[0].body, self.exchange.requests[1].body)
        self.assertNotIn(PRIVATE, repr(transport.attempts))
        self.assertEqual(sum(item.reserved_input_tokens for item in transport.attempts), 32000)
        self.assertEqual(sum(item.reserved_output_tokens for item in transport.attempts), 16000)
        RESULTS['unknown_model_outcome'] = {'first_status': first.status, 'explicit_retry_status': second.status,
            'automatic_retries': 0, 'outcomes': ['unknown', 'reported'],
            'reserved_input_tokens': 32000, 'reserved_output_tokens': 16000, 'sqlite_jobs': 0}

    def test_05_launch_stays_closed_with_composed_adapters(self):
        transport = OfflineResponsesTransport(FixtureExchange([None]), self.counter)
        with self.assertRaisesRegex(RuntimeError, '^real_launch_unsupported$'):
            launch_real(transport=transport, workspace=self.sandbox, scrimmage=self.adapter, enabled=True)
        self.assertEqual(self.rows('SELECT count(*) FROM jobs'), [(0,)])
        RESULTS['launch_gate'] = 'real_launch_unsupported'


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FullCompositionSmoke)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    RESULT_PATH.write_text(json.dumps({'schema': 'bcenv.full-composition-smoke.v1',
        'scope': 'offline fixtures + actual temporary SQLite; no inference, compilation or game',
        'source_manifest': MANIFEST, 'tests_run': result.testsRun,
        'success': result.wasSuccessful(), 'cases': RESULTS,
        'sqlite_version': sqlite3.sqlite_version, 'python_version': sys.version,
        'limits': ['host-supplied scopes are not authentication', 'no sandbox/isolation proof',
                   'completion evidence fabricated', 'fixture token counts are not tokenizer measurements',
                   'model attempt accounting remains process-local', 'no provider network or credentials']},
        indent=2, sort_keys=True) + '\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
