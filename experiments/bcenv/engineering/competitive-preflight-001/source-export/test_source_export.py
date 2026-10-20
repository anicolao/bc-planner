"""Actual isolated export + typed capture + SQLite, all synthetic, zero games."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
import hashlib
import json
from pathlib import Path
import sqlite3
import time
import unittest
from unittest.mock import patch

from export_backend import (COLLECTOR_ARGV, EXPORT_ARGV, FIXTURE_PACKAGE,
                            ExportingFixtureBackend, PYTHON)
from probe_adapter import BASE
from services.controller import (ControllerLimits, ExecReply, ExecRequest, FrozenContext,
    ReadRequest, ResultRequest, SubmitRequest, TOOL_NAMES, ToolCall, TurnReply,
    WriteRequest, launch_real, run_synthetic)
from services.controller_ledger import (ArtifactError, CapturingSandboxAdapter,
    DurableScrimmageAdapter, SourceArtifactStore)
from services.ledger import DurableLedger
from services.scrimmage import accept_source_zip

SOURCE = b'package fixturebot; public class RobotPlayer {}\n'
PATH = 'src/fixturebot/RobotPlayer.java'
FAKE = 'a_' + 'f' * 32


def request(argv, *, wall=2, cap=16384, cwd='.'):
    return ExecRequest(tuple(argv), cwd, wall, 268435456, cap)


class SourceExportTests(unittest.TestCase):
    def setUp(self):
        self.backend = ExportingFixtureBackend()
        self.store = SourceArtifactStore()
        self.adapter = CapturingSandboxAdapter(self.backend, self.store, 'synthetic-owner', 'synthetic-run')
        reply = self.execute('''import os,shutil
for entry in os.scandir('/workspace/src'):
 if entry.is_dir(follow_symlinks=False):shutil.rmtree(entry.path)
 else:os.unlink(entry.path)
os.mkdir('/workspace/src/fixturebot')
open('/workspace/src/fixturebot/RobotPlayer.java','wb').write(''' + repr(SOURCE) + ''')
''')
        self.assertEqual(reply.status, 'succeeded', reply.stderr)
        self.assertIsNone(reply.artifact_id)

    def execute(self, code, **kwargs):
        return self.adapter.exec(request((PYTHON, '-I', '-B', '-c', code), **kwargs))

    def capture(self):
        result = self.adapter.exec(request(EXPORT_ARGV))
        self.assertEqual(result.status, 'succeeded', result.stderr)
        self.assertRegex(result.artifact_id, r'^a_[0-9a-f]{32}$')
        return result, self.store.resolve('synthetic-owner', 'synthetic-run', result.artifact_id)

    def reject(self):
        count = len(self.store._artifacts)
        result = self.adapter.exec(request(EXPORT_ARGV))
        self.assertIn(result.status, ('failed', 'timeout'))
        self.assertIsNone(result.artifact_id)
        self.assertEqual(len(self.store._artifacts), count)
        self.assertLessEqual(len(result.stdout) + len(result.stderr), 128)
        self.assertNotIn(b'PK\x03\x04', result.stdout)
        return result

    def test_real_export_validates_and_private_zip_is_not_tool_output(self):
        result, snapshot = self.capture()
        accepted = accept_source_zip(snapshot.archive, snapshot.package)
        self.assertEqual(snapshot.package, FIXTURE_PACKAGE)
        self.assertEqual(accepted.files[0].path, 'fixturebot/RobotPlayer.java')
        self.assertEqual(accepted.files[0].data, SOURCE)
        self.assertEqual(accepted.content_sha256, snapshot.content_sha256)
        self.assertEqual(result.stdout, b'source export validated\n')
        self.assertNotIn(SOURCE, result.stdout)
        self.assertIs(type(snapshot.archive), bytes)

    def test_snapshot_stays_frozen_after_candidate_mutation(self):
        old_result, old = self.capture()
        old_bytes = old.archive
        self.adapter.write(WriteRequest(PATH, SOURCE + b'// changed\n'))
        unused, new = self.capture()
        self.assertNotEqual(old.content_sha256, new.content_sha256)
        self.assertEqual(old.archive, old_bytes)
        self.assertEqual(accept_source_zip(old.archive, old.package).files[0].data, SOURCE)
        self.assertIs(self.store.resolve('synthetic-owner', 'synthetic-run', old_result.artifact_id), old)
        with self.assertRaises(FrozenInstanceError):
            old.package = 'forged'

    def test_duplicate_capture_is_deterministic_bytes(self):
        first, old = self.capture()
        second, new = self.capture()
        self.assertNotEqual(first.artifact_id, second.artifact_id)
        self.assertEqual(old.archive, new.archive)

    def test_owner_and_run_scope_cannot_resolve_handle(self):
        result, unused = self.capture()
        for owner, run in [('other-owner', 'synthetic-run'), ('synthetic-owner', 'other-run')]:
            with self.assertRaises(ArtifactError) as caught:
                self.store.resolve(owner, run, result.artifact_id)
            self.assertEqual(caught.exception.code, 'unknown_artifact')

    def test_candidate_stdout_cannot_mint_handle(self):
        result = self.execute('print(' + repr(json.dumps({'artifact_id': FAKE,
            'source': '/workspace/src/fixturebot/RobotPlayer.java', 'archive': 'forged'})) + ')')
        self.assertEqual(result.status, 'succeeded')
        self.assertIsNone(result.artifact_id)
        self.assertEqual(len(self.store._artifacts), 0)

    def test_reserved_operation_is_exact_and_has_no_path_parameter(self):
        for argv in (EXPORT_ARGV + ('/outside',), (EXPORT_ARGV[0] + '-extra',)):
            result = self.adapter.exec(request(argv))
            self.assertEqual(result.status, 'failed')
            self.assertIsNone(result.artifact_id)
        result = self.adapter.exec(request(EXPORT_ARGV, cwd='src'))
        self.assertEqual(result.status, 'failed')
        self.assertIsNone(result.artifact_id)
        self.assertEqual(len(self.store._artifacts), 0)

    def test_collector_requires_readonly_workspace_and_is_immutable(self):
        result = self.adapter.exec(request(COLLECTOR_ARGV))
        self.assertEqual(result.status, 'failed')
        self.assertIsNone(result.artifact_id)
        result = self.execute('''import json
try:open('/opt/source_collector.py','ab').write(b'corrupt');print('mutated')
except OSError as e:print(e.errno)
''')
        self.assertEqual(result.stdout, b'30\n')
        self.capture()

    def test_outside_symlink_leaf_rejected(self):
        self.execute('import os;os.unlink("/workspace/' + PATH + '");os.symlink(' +
            repr(str(BASE / 'host-canary.txt')) + ',"/workspace/' + PATH + '")')
        self.reject()
        self.assertEqual((BASE / 'host-canary.txt').read_text(), 'NEW-SYNTHETIC-EXPORT-OUTSIDE-CANARY\n')

    def test_symlink_directory_rejected(self):
        self.execute('import os;os.symlink("/workspace/docs","/workspace/src/fixturebot/linked")')
        self.reject()

    def test_hardlink_rejected(self):
        self.execute('import os;os.link("/workspace/' + PATH + '","/workspace/src/fixturebot/Other.java")')
        self.reject()

    def test_fifo_rejected_without_blocking(self):
        self.execute('import os;os.mkfifo("/workspace/src/fixturebot/Fifo.java")')
        start = time.monotonic()
        self.reject()
        self.assertLess(time.monotonic() - start, 1)

    def test_empty_source_rejected(self):
        self.adapter.write(WriteRequest(PATH, b''))
        self.reject()

    def test_invalid_unicode_and_nul_rejected(self):
        for data in (b'\xff', b'package fixturebot;\x00'):
            self.adapter.write(WriteRequest(PATH, data))
            self.reject()

    def test_non_java_name_rejected(self):
        self.adapter.write(WriteRequest('src/fixturebot/extra.txt', b'not java'))
        self.reject()

    def test_wrong_package_tree_rejected(self):
        self.execute('import os;os.mkdir("/workspace/src/other");open("/workspace/src/other/X.java","wb").write(b"x")')
        self.reject()

    def test_intake_reserved_identifier_rejected(self):
        self.adapter.write(WriteRequest('src/fixturebot/class.java', b'class invalid {}'))
        self.reject()

    def test_file_size_limit(self):
        self.execute('open("/workspace/' + PATH + '","wb").write(b"x"*524289)')
        self.reject()

    def test_file_count_limit(self):
        self.execute('''
for n in range(128):open('/workspace/src/fixturebot/C'+str(n)+'.java','wb').write(b'x')
''')
        self.reject()

    def test_archive_size_limit(self):
        self.execute('''
for n in range(3):open('/workspace/src/fixturebot/C'+str(n)+'.java','wb').write(b'x'*400000)
''')
        self.reject()
        self.assertLess(self.backend.last_export['output_bytes_retained'], 128)

    def test_depth_limit(self):
        self.execute('import os;os.makedirs("/workspace/src/fixturebot/"+"/".join(["deep"]*17))')
        self.reject()

    def test_private_collector_output_limit_is_enforced(self):
        reply = self.backend._runner._run(COLLECTOR_ARGV, cap=128, _collector=True)
        self.assertEqual(reply.status, 'failed')
        self.assertEqual(self.backend._runner.last_execution['stop_reason'], 'output_limit')
        self.assertLessEqual(len(reply.stdout) + len(reply.stderr), 128)
        self.assertEqual(len(self.store._artifacts), 0)

    def test_export_timeout_never_publishes_handle(self):
        with patch.object(self.backend._runner, '_run', return_value=ExecReply('timeout', b'PKpartial')):
            self.backend._runner.last_execution = {'synthetic_injection': 'timeout'}
            self.reject()

    def test_malformed_collector_result_never_publishes_handle(self):
        with patch.object(self.backend._runner, '_run', return_value=ExecReply('succeeded', b'PKinvalid')):
            self.backend._runner.last_execution = {'synthetic_injection': 'malformed_archive'}
            self.reject()

    def test_uncertain_exec_cleanup_permanently_blocks_export(self):
        with patch('probe_adapter.selectors.DefaultSelector', side_effect=RuntimeError('synthetic_setup_error')):
            with self.assertRaisesRegex(RuntimeError, 'synthetic_setup_error'):
                self.execute('import time;time.sleep(2)')
        reply = self.reject()
        self.assertEqual(reply.stderr, b'workspace_cleanup_unverified\n')

    def test_uncertain_read_cleanup_blocks_export(self):
        with patch('probe_adapter.selectors.DefaultSelector', side_effect=RuntimeError('synthetic_setup_error')):
            with self.assertRaisesRegex(RuntimeError, 'synthetic_setup_error'):
                self.adapter.read(ReadRequest(PATH, 0, 128))
        self.assertEqual(self.reject().stderr, b'workspace_cleanup_unverified\n')

    def test_operation_lock_waits_for_candidate_exit_before_capture(self):
        marker = BASE / 'writable' / 'scratch' / ('lock-' + str(time.time_ns()))
        code = 'import time;open(' + repr('/workspace/scratch/' + marker.name) + ',"w").write("started");'
        code += 'time.sleep(.3);open("/workspace/' + PATH + '","wb").write(' + repr(SOURCE + b'// after exit\n') + ')'
        with ThreadPoolExecutor(max_workers=2) as pool:
            pending = pool.submit(self.execute, code)
            deadline = time.monotonic() + 1
            while not marker.exists() and time.monotonic() < deadline:
                time.sleep(.01)
            self.assertTrue(marker.exists())
            start = time.monotonic()
            captured = pool.submit(self.capture)
            self.assertEqual(pending.result(timeout=2).status, 'succeeded')
            unused, snapshot = captured.result(timeout=2)
            self.assertGreater(time.monotonic() - start, .2)
        self.assertEqual(accept_source_zip(snapshot.archive, snapshot.package).files[0].data,
                         SOURCE + b'// after exit\n')

    def test_hostile_candidate_teardown_precedes_capture(self):
        name = 'export-heartbeat-' + str(time.time_ns())
        marker = BASE / 'writable' / 'scratch' / name
        reply = self.execute('''import os,ctypes,time
os.setsid();ctypes.CDLL(None).prctl(1,0,0,0,0)
os.close(0);os.close(1);os.close(2)
end=time.monotonic()+3
with open('/workspace/scratch/''' + name + '''','ab',buffering=0) as f:
 while time.monotonic()<end:f.write(b'x');time.sleep(.025)
''', wall=1)
        self.assertEqual(reply.status, 'timeout')
        self.assertTrue(marker.exists())
        before = marker.stat().st_size
        self.capture()
        time.sleep(.2)
        self.assertEqual(marker.stat().st_size, before)
        self.assertLess(before, 50)

    def test_actual_six_tool_controller_export_submit_feedback_zero_games(self):
        path = BASE / ('synthetic-ledger-' + str(time.time_ns()) + '.sqlite')
        ledger = DurableLedger(path, clock=lambda: 1000)
        service = DurableScrimmageAdapter(ledger, self.store, 'synthetic-owner', 'synthetic-run')
        context = FrozenContext(b'fixed synthetic system', b'fixed synthetic task')
        def call(identifier, name, args):
            return ToolCall(identifier, name, json.dumps(args))
        def results(request):
            return [item['result'] for raw in request.transcript
                    if 'result' in (item := json.loads(raw))]
        class Transport:
            def next_turn(self, turn):
                assert turn.tool_names == TOOL_NAMES and len(turn.tool_names) == 6
                if turn.turn == 1:
                    return TurnReply((
                        call('write', 'workspace_write', {'path': PATH, 'content': SOURCE.decode()}),
                        call('read', 'workspace_read', {'path': PATH, 'offset': 0, 'limit': 128}),
                        call('export', 'workspace_exec', {'argv': list(EXPORT_ARGV), 'cwd': '.', 'timeout_seconds': 2})))
                if turn.turn == 2:
                    return TurnReply((call('submit', 'scrimmage_submit', {
                        'artifact_id': results(turn)[-1]['artifact_id'], 'package': FIXTURE_PACKAGE}),))
                if turn.turn == 3:
                    identifier = results(turn)[-1]['submission_id']
                    return TurnReply((call('result', 'scrimmage_result', {'submission_id': identifier}),
                                      call('replay', 'scrimmage_replay', {'submission_id': identifier})))
                return TurnReply(final_text='synthetic export complete; zero games')
        report = run_synthetic(context, Transport(), self.adapter, service,
                               limits=ControllerLimits(max_turns=4))
        self.assertEqual((report.status, report.tool_calls), ('complete', 6))
        output = results(report)
        self.assertEqual([item['status'] for item in output],
                         ['complete', 'complete', 'succeeded', 'accepted', 'accepted', 'unavailable'])
        self.assertEqual(output[-1]['reason'], 'replay_withheld')
        self.assertEqual(report.initial_sha256, context.sha256)
        with sqlite3.connect(path) as connection:
            self.assertEqual(connection.execute('SELECT state FROM jobs').fetchall(), [('queued',)])
        self.assertFalse(any('summary' in item or 'wins' in item for item in output))
        with self.assertRaises(RuntimeError):
            launch_real()


if __name__ == '__main__':
    unittest.main(verbosity=2)
