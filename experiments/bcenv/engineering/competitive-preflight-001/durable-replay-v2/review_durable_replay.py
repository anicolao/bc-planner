"""Independent deterministic offline review; no engine, network or provider.

Usage: python review_durable_replay.py COMPOSED_SOURCE V1_BASELINE_JSON
Source must contain route files over producer commit f3963b7. Existing reviewed
test helpers supply only a source ZIP, normalized result and synthetic raw rows.
The provider, concurrency, fault injection and composed transport are below.
"""
import sys
from pathlib import Path
ROOT = Path(sys.argv.pop(1)).resolve()
BASELINE = Path(sys.argv.pop(1)).resolve()
sys.path[:0] = [str(ROOT), str(ROOT / 'tests')]
from concurrent.futures import ProcessPoolExecutor
from contextlib import closing
from dataclasses import asdict, replace
import hashlib
import json
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from services.controller import (ControllerLimits, FrozenContext, TOOL_NAMES,
    ToolCall, TurnReply, TurnRequest, run_synthetic, tool_schemas)
from services.controller_ledger import (CapturingSandboxAdapter,
    ExportedExecReply, SourceArtifactStore, SourceExport)
from services.ledger import DurableLedger, LedgerError
from services.replay_protocol import ReplayReply, encoded, parse_request, project_reply, replay_fields
from services.replay_route import ReplayFixture, ReplayProviderReceipt, ReplayScrimmageAdapter, SyntheticReplayRoute
from services.replay_store import PreparedReplay, ReplayLimits, ReplayPolicy, ReplayStore
from services.responses_transport import OfflineResponsesTransport, TransportError
from test_ledger import archive, complete
from test_replay_feedback import fixture, SECRET
from test_responses_transport import FixtureCounter, FixtureExchange, function, message, response

POLICY = ReplayPolicy('2.0.3', '1' * 64, '2' * 64)
RAW = b'independent inert replay fixture; never an engine result'


def req(sid, operation='manifest', **kw):
    value = dict.fromkeys(replay_fields())
    value.update(submission_id=sid, operation=operation)
    if operation == 'manifest':
        value.update(manifest_offset=0, manifest_limit=8)
    value.update(kw)
    return parse_request(value)


class Provider:
    def __init__(self):
        self.calls, self.hook = [], None

    def query(self, request):
        self.calls.append(request)
        if self.hook:
            self.hook(request)
        q = request.query
        value = fixture(start=q.round_start, end=q.round_end, robot=q.robot_id, limit=10000)
        rows = value['records'][q.record_offset:q.record_offset + q.record_limit]
        end, total = q.record_offset + len(rows), value['matching_record_count']
        value.update(format='bcenv.bc2023.replay-query.v2', records=rows,
            spec_version=request.expected_spec_version,
            returned_record_count=len(rows), truncated=len(rows) < total,
            selected_records_complete=len(rows) == total, page_records_complete=True,
            page_end_offset=end, next_record_offset=end if end < total else None)
        value['query'].update(record_offset=q.record_offset, record_limit=q.record_limit)
        return ReplayProviderReceipt(encoded(value), request.source_sha256,
            request.expected_spec_version, request.producer_identity)


def initialize_child(args):
    path, policy = args
    try:
        store = ReplayStore(DurableLedger(path, clock=lambda: 1000), policy)
        return ('ok', store.submit('alice', 'run', 'key', archive(), 'bot')['submission_id'])
    except LedgerError as error:
        return ('error', error.code)


def reserve_child(args):
    path, request = args
    try:
        store = ReplayStore(DurableLedger(path, clock=lambda: 1000), POLICY)
        claim = store.reserve_page('alice', 'run', request.submission_id,
            replay_id=request.replay_id, round_start=request.round_start,
            round_end=request.round_end, robot_id=request.robot_id, record_limit=request.record_limit)
        return ('ok', claim.generation)
    except LedgerError as error:
        return ('error', error.code)


class Review(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'ledger.db'
        self.now = 1000
        self.open()

    def open(self, limits=None):
        self.ledger = DurableLedger(self.path, clock=lambda: self.now)
        self.store = ReplayStore(self.ledger, POLICY, limits=limits)
        self.provider = Provider()
        self.route = SyntheticReplayRoute(self.store, self.provider)

    def sql(self, query, args=()):
        with closing(sqlite3.connect(self.path)) as c, c:
            return c.execute(query, args).fetchall()

    def denied(self, code, fn, *args, **kw):
        with self.assertRaises(LedgerError) as caught:
            fn(*args, **kw)
        self.assertEqual(caught.exception.code, code)

    def running(self, owner='alice', run='run', key='key'):
        sid = self.store.submit(owner, run, key, archive(), 'bot')['submission_id']
        return sid, self.ledger.reserve_job(owner, sid, 'worker')

    def finish(self, **kw):
        sid, claim = self.running(**kw)
        self.route.complete_with_replay(kw.get('owner', 'alice'), kw.get('run', 'run'),
            claim, complete(), (ReplayFixture('one', RAW, 1),))
        return sid, claim

    def reply(self, request, owner='alice', run='run'):
        return project_reply(self.route.replay(owner, run, request), request)

    def window(self, sid, limit=5):
        rid = self.reply(req(sid))['replays'][0]['replay_id']
        return req(sid, 'window', replay_id=rid, round_start=35, round_end=40,
                   robot_id=43, record_limit=limit)

    def reserve(self, request):
        return self.store.reserve_page('alice', 'run', request.submission_id,
            replay_id=request.replay_id, round_start=request.round_start,
            round_end=request.round_end, robot_id=request.robot_id, record_limit=request.record_limit)

    def test_01_fresh_database_eight_process_init_submit(self):
        self.path = Path(self.temp.name) / 'race.db'
        with ProcessPoolExecutor(max_workers=8) as pool:
            values = list(pool.map(initialize_child, [(self.path, POLICY)] * 8))
        self.assertEqual({v[0] for v in values}, {'ok'})
        self.assertEqual(len({v[1] for v in values}), 1)
        self.assertEqual(self.sql('SELECT count(*) FROM jobs'), [(1,)])
        self.assertEqual(self.sql('SELECT count(*) FROM replay_job_runs'), [(1,)])
        self.assertEqual(len(self.sql("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'replay_%'")), 5)

    def test_02_incompatible_initializers_commit_one_complete_configuration(self):
        self.path = Path(self.temp.name) / 'mixed.db'
        alternate = replace(POLICY, producer_identity='3' * 64)
        with ProcessPoolExecutor(max_workers=8) as pool:
            values = list(pool.map(initialize_child, [(self.path, p) for p in [POLICY, alternate] * 4]))
        self.assertEqual(sum(v[0] == 'ok' for v in values), 4)
        self.assertEqual(sum(v == ('error', 'configuration_mismatch') for v in values), 4)
        self.assertEqual(self.sql('SELECT count(*) FROM jobs'), [(1,)])
        self.assertEqual(len(self.sql("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'replay_%'")), 5)

    def test_03_atomic_submit_binding_failure_has_no_payload_orphans(self):
        self.sql("CREATE TRIGGER abort_binding BEFORE INSERT ON replay_job_runs BEGIN SELECT RAISE(ABORT,'private'); END")
        self.denied('storage_unavailable', self.store.submit, 'alice', 'run', 'key', archive(), 'bot')
        for table in ('jobs', 'sources', 'source_files', 'replay_job_runs'):
            self.assertEqual(self.sql('SELECT count(*) FROM ' + table), [(0,)])

    def test_04_second_registration_failure_rolls_back_entire_completion(self):
        sid, claim = self.running()
        self.sql("CREATE TRIGGER abort_second BEFORE INSERT ON replay_sources WHEN NEW.registration_key='two' BEGIN SELECT RAISE(ABORT,'private'); END")
        self.denied('storage_unavailable', self.route.complete_with_replay, 'alice', 'run', claim,
            complete(), (ReplayFixture('one', RAW, 1), ReplayFixture('two', RAW + b'2', 2)))
        self.assertEqual(self.sql('SELECT state FROM jobs'), [('running',)])
        for table in ('replay_completions', 'replay_sources'):
            self.assertEqual(self.sql('SELECT count(*) FROM ' + table), [(0,)])

    def test_05_expired_exact_repeat_never_reruns_provider_or_changes_rows(self):
        sid, claim = self.finish()
        old = self.sql('SELECT * FROM replay_sources')
        self.now += 7200
        original = self.route.complete_with_replay('alice', 'run', claim, complete(), (ReplayFixture('one', RAW, 1),))
        self.assertEqual(original['status'], 'complete')
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.sql('SELECT * FROM replay_sources'), old)
        for owner, run, altered, evidence, fixtures, code in [
            ('bob', 'run', claim, complete(), (ReplayFixture('one', RAW, 1),), 'not_found'),
            ('alice', 'other', claim, complete(), (ReplayFixture('one', RAW, 1),), 'not_found'),
            ('alice', 'run', replace(claim, worker='other'), complete(), (ReplayFixture('one', RAW, 1),), 'stale_reservation'),
            ('alice', 'run', replace(claim, generation=claim.generation+1), complete(), (ReplayFixture('one', RAW, 1),), 'stale_reservation'),
            ('alice', 'run', claim, {'status':'infrastructure_failure','reason':'worker_unavailable'}, (ReplayFixture('one', RAW, 1),), 'terminal_conflict'),
            ('alice', 'run', claim, complete(), (ReplayFixture('one', RAW + b'x', 1),), 'terminal_conflict')]:
            self.denied(code, self.route.complete_with_replay, owner, run, altered, evidence, fixtures)
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.reply(req(sid))['reason'], 'replay_not_available')

    def test_06_legacy_and_other_run_guesses_have_no_existence_oracle(self):
        legacy = self.ledger.submit('alice', 'old', archive(), 'bot')['submission_id']
        bound, unused = self.finish()
        for sid in (legacy, bound, 's_' + 'f'*32):
            self.assertEqual(self.reply(req(sid), run='unrelated')['reason'], 'not_found')
        self.denied('not_found', self.store.result, 'alice', 'unrelated', legacy)
        self.assertEqual(len(self.provider.calls), 1)

    def test_07_legacy_finish_never_gains_replay(self):
        sid, claim = self.running()
        self.ledger.finish('alice', sid, claim.worker, claim.generation, complete())
        self.denied('terminal_conflict', self.route.complete_with_replay, 'alice', 'run', claim,
            complete(), (ReplayFixture('one', RAW, 1),))
        self.assertEqual(self.provider.calls, [])
        self.assertEqual(self.sql('SELECT count(*) FROM replay_sources'), [(0,)])

    def test_08_supported_clock_and_large_ttl_manifest_numbers(self):
        for index, now in enumerate((2**31, 2**53+3, 2**60-1)):
            self.path = Path(self.temp.name) / ('clock%d.db' % index)
            self.now = now
            self.open(replace(ReplayLimits(), source_ttl=2**49))
            sid, unused = self.finish()
            manifest = self.reply(req(sid))
            self.assertEqual(manifest['status'], 'available')
            self.assertEqual(manifest['replays'][0]['expires_at'], now + 2**49)

    def test_09_fractional_rollback_via_legacy_api_fences_page_durably(self):
        self.now = 1000.9
        sid, unused = self.finish()
        claim = self.reserve(self.window(sid))
        self.now = 1000.1
        self.denied('clock_regression', self.ledger.result, 'bob', sid)
        self.assertEqual(self.sql('SELECT state,lease_until FROM replay_attempts'), [('expired', None)])
        self.now = 1000.9
        self.open()
        self.denied('stale_reservation', self.store.finish_page, 'alice', 'run', claim, b'{}')

    def test_10_stale_generation_after_retry_cannot_publish(self):
        sid, unused = self.finish()
        request = self.window(sid)
        first = self.reserve(request)
        self.now = first.lease_until
        second = self.reserve(request)
        self.assertEqual(second.generation, first.generation + 1)
        self.denied('stale_reservation', self.store.finish_page, 'alice', 'run', first, b'{}')
        self.assertEqual(self.sql('SELECT state,attempt_count FROM replay_attempts'), [('running', 2)])
        self.store.finish_page('alice', 'run', second)

    def test_11_cross_submission_view_and_altered_reservation_never_publish(self):
        sid, unused = self.finish()
        first = self.reply(self.window(sid))
        other, unused = self.finish(key='other')
        self.assertEqual(self.reply(req(other, 'page', view_id=first['view_id'], record_offset=5))['reason'], 'not_found')
        claim = self.reserve(self.window(sid))
        for change in ({'job_id':'j_'+'e'*32}, {'source':RAW+b'x'}, {'source_sha256':'0'*64},
                       {'record_limit':6}, {'own_team_id':2}):
            self.denied('storage_integrity', self.store.finish_page, 'alice', 'run', replace(claim, **change), b'{}')
        self.assertEqual(self.sql("SELECT count(*) FROM replay_attempts WHERE state='running'"), [(1,)])

    def test_12_unknown_reservation_commit_has_no_provider_or_retry(self):
        sid, unused = self.finish()
        request = self.window(sid)
        original = self.store.reserve_page
        def uncertain(*a, **kw):
            original(*a, **kw)
            raise LedgerError('storage_unavailable')
        with patch.object(self.store, 'reserve_page', side_effect=uncertain) as mocked:
            self.assertEqual(self.reply(request)['reason'], 'storage_unavailable')
            self.assertEqual(mocked.call_count, 1)
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.sql('SELECT state,attempt_count FROM replay_attempts'), [('running', 1)])

    def test_13_actual_commit_uncertainty_preserves_unknown_outcome(self):
        sid, unused = self.finish()
        request = self.window(sid)
        original = self.ledger._connect
        class Connection:
            def __init__(inner, real): inner.real = real
            def __getattr__(inner, name): return getattr(inner.real, name)
            def commit(inner):
                inner.real.commit()
                raise sqlite3.OperationalError('private uncertain commit')
        with patch.object(self.ledger, '_connect', side_effect=lambda: Connection(original())):
            self.assertEqual(self.reply(request)['reason'], 'storage_unavailable')
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.sql('SELECT state,attempt_count FROM replay_attempts'), [('running', 1)])

    def test_14_unknown_completion_commit_exact_inspection_no_second_provider(self):
        sid, claim = self.running()
        original = self.store.complete
        def uncertain(*a, **kw):
            original(*a, **kw)
            raise LedgerError('storage_unavailable')
        fixtures = (ReplayFixture('one', RAW, 1),)
        with patch.object(self.store, 'complete', side_effect=uncertain) as mocked:
            self.denied('storage_unavailable', self.route.complete_with_replay, 'alice', 'run', claim, complete(), fixtures)
            self.assertEqual(mocked.call_count, 1)
        self.assertEqual(self.sql('SELECT state FROM jobs'), [('complete',)])
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.route.complete_with_replay('alice', 'run', claim, complete(), fixtures)['status'], 'complete')
        self.assertEqual(len(self.provider.calls), 1)

    def test_15_failed_page_preserves_first_fingerprint_and_charge(self):
        sid, unused = self.finish()
        request = self.window(sid)
        first = self.reply(request)
        fingerprint = self.sql('SELECT fingerprint FROM replay_attempts')[0][0]
        self.provider.hook = lambda unused: (_ for _ in ()).throw(RuntimeError(SECRET))
        self.assertEqual(self.reply(request)['reason'], 'invalid_evidence')
        self.assertEqual(self.sql('SELECT state,attempt_count,fingerprint FROM replay_attempts'), [('failed', 2, fingerprint)])
        self.provider.hook = None
        self.assertEqual(self.reply(request)['page'], first['page'])
        self.assertEqual(self.sql('SELECT state,attempt_count FROM replay_attempts'), [('complete', 3)])

    def test_16_logical_source_cap_equal_and_distinct_guesses_fail_equally(self):
        self.path = Path(self.temp.name) / 'caps.db'
        self.open(replace(ReplayLimits(), global_source_bytes=len(RAW)))
        self.finish()
        for key, raw in [('equal', RAW), ('distinct', b'x'*len(RAW))]:
            sid, claim = self.running(owner='bob', key=key)
            self.denied('resource_limit', self.route.complete_with_replay, 'bob', 'run', claim,
                complete(), (ReplayFixture('one', raw, 1),))
        self.assertEqual(self.sql('SELECT count(*),sum(size) FROM replay_sources'), [(1, len(RAW))])

    def test_17_source_integrity_changed_during_callback_never_releases_page(self):
        sid, unused = self.finish()
        request = self.window(sid)
        def corrupt(unused):
            self.sql('DROP TRIGGER immutable_source_files_update')
            self.sql('UPDATE source_files SET data=zeroblob(size)')
        self.provider.hook = corrupt
        result = self.reply(request)
        self.assertEqual(result['reason'], 'storage_integrity')
        self.assertNotIn('page', result)
        self.assertEqual(self.sql('SELECT state,fingerprint FROM replay_attempts'), [('running', None)])

    def test_18_exact_v1_registry_flat_strict_v2_and_transport_binding(self):
        baseline = json.loads(BASELINE.read_text())
        for name, limits in [('default', ControllerLimits()),
                             ('tightened', ControllerLimits(max_read_bytes=123,max_write_bytes=456,exec_wall_seconds=7))]:
            self.assertEqual([s.decode() for s in tool_schemas(limits)], baseline[name])
        schemas = tool_schemas(protocol='v2')
        exchange = FixtureExchange([response()])
        transport = OfflineResponsesTransport(exchange, FixtureCounter(), controller_protocol='v2')
        request = TurnRequest(FrozenContext(b'exact\r\nsystem', b'task\n'), TOOL_NAMES, schemas, (), 1)
        with self.assertRaisesRegex(TransportError, 'registry_changed'):
            transport.next_turn(replace(request, tool_schemas=tool_schemas()))
        self.assertEqual(exchange.requests, [])
        transport.next_turn(request)
        tools = json.loads(exchange.requests[0].body)['tools']
        self.assertEqual(tuple(t['name'] for t in tools), TOOL_NAMES)
        for t in tools:
            self.assertEqual(set(t), {'type','strict','name','parameters'})
            self.assertEqual(t['type'], 'function')
            self.assertIs(t['strict'], True)
            p = t['parameters']
            self.assertEqual(set(p['required']), set(p['properties']))
            self.assertIs(p['additionalProperties'], False)
            self.assertNotIn('anyOf', p)
        for key, field in tools[-1]['parameters']['properties'].items():
            if key not in ('submission_id','operation'):
                self.assertIn('null', field['type'])
        for selected, supplied in [('v1','v2'), ('v2','v1')]:
            t = OfflineResponsesTransport(FixtureExchange([]), FixtureCounter(), controller_protocol=selected)
            with self.assertRaisesRegex(TransportError, 'registry_changed'):
                t.next_turn(replace(request, tool_schemas=tool_schemas(protocol=supplied)))

    def test_19_strict_inactive_fields_boolean_offset_and_malformed_envelopes(self):
        sid, unused = self.finish()
        request = req(sid, manifest_limit=1)
        manifest = self.reply(request)
        manifest.update(total_replays=2, next_manifest_offset=True)
        with self.assertRaises(ValueError):
            project_reply(ReplayReply(encoded(manifest)), request)
        for change in ({'round_start':0}, {'manifest_limit':True}, {'raw_path':SECRET}, {'operation':'shell'}):
            args = asdict(request); args.update(change)
            with self.assertRaises(ValueError): parse_request(args)
        raw = encoded(self.reply(request))
        for broken in (b'['*33+b']'*33, raw.replace(b'"status":',b'"status":"available","status":'),
                       raw.replace(b'"total_replays":1', b'"total_replays":1e0'), raw+b' '*12288):
            with self.assertRaises((ValueError, UnicodeError)):
                project_reply(ReplayReply(broken), request)

    def test_20_v2_complete_envelope_cap_and_exact_aggregate_accounting(self):
        class Workspace:
            def read(inner, request): return b'"'*request.limit
        def run(protocol, limits, n=2):
            class Transport:
                def __init__(inner): inner.step=0
                def next_turn(inner, turn):
                    inner.step += 1
                    if inner.step > n: return TurnReply(final_text='done')
                    return TurnReply((ToolCall('x'*63+str(inner.step), 'workspace_read',
                        json.dumps({'path':'docs/data','offset':0,'limit':8192})),))
            return run_synthetic(FrozenContext(b's',b't'),Transport(),Workspace(),None,protocol=protocol,limits=limits)
        widened = replace(ControllerLimits(),max_tool_output_bytes=65536)
        v1, v2 = run('v1',widened), run('v2',widened)
        outputs = lambda report: [r for r in report.transcript if 'result' in json.loads(r)]
        self.assertGreater(len(outputs(v1)[0]), 16384)
        self.assertTrue(all(len(r)<=16384 for r in outputs(v2)))
        self.assertEqual(json.loads(outputs(v2)[0])['result']['reason'], 'tool_output_limit')
        exact = sum(map(len,outputs(v2)))
        self.assertEqual(run('v2',replace(widened,max_total_output_bytes=exact)).status,'complete')
        clipped=run('v2',replace(widened,max_total_output_bytes=exact-1))
        self.assertEqual(clipped.status,'output_limit')
        self.assertEqual(len(outputs(clipped)),1)

    def test_21_composed_offline_responses_capture_ledger_and_full_pagination(self):
        store = SourceArtifactStore()
        adapter = ReplayScrimmageAdapter(self.route,store,'alice','run')
        class Workspace:
            def read(inner, request): return b'synthetic fixture rules'
            def write(inner, request): return None
            def exec(inner, request): return ExportedExecReply('succeeded', source=SourceExport('bot',archive()))
        workspace=CapturingSandboxAdapter(Workspace(),store,'alice','run')
        outer=self
        class Exchange:
            def __init__(inner): inner.requests=[]; inner.pages=[]; inner.sid=None
            def respond(inner, request):
                body=json.loads(request.body); inner.requests.append(body)
                results=[json.loads(item['output']) for item in body['input'] if item.get('type')=='function_call_output']
                n=len(results)
                if n==0: name,args='workspace_read',{'path':'docs/rules','offset':0,'limit':100}
                elif n==1: name,args='workspace_write',{'path':'src/bot/RobotPlayer.java','content':'synthetic'}
                elif n==2: name,args='workspace_exec',{'argv':['inert'],'cwd':'.','timeout_seconds':1}
                elif n==3: name,args='scrimmage_submit',{'artifact_id':results[-1]['artifact_id'],'package':'bot'}
                elif n==4:
                    inner.sid=results[-1]['submission_id']
                    claim=outer.ledger.reserve_job('alice',inner.sid,'worker')
                    outer.route.complete_with_replay('alice','run',claim,complete(),(ReplayFixture('one',RAW,1),))
                    name,args='scrimmage_result',{'submission_id':inner.sid}
                elif n==5: name,args='scrimmage_replay',asdict(req(inner.sid))
                elif n==6:
                    name,args='scrimmage_replay',asdict(req(inner.sid,'window',
                        replay_id=results[-1]['replays'][0]['replay_id'],round_start=0,round_end=45,robot_id=None,record_limit=64))
                else:
                    last=results[-1]; inner.pages.append(last['page'])
                    offset=last['page']['coverage']['next_record_offset']
                    if offset is None: return response([message('done',item_id='final')])
                    # Restart durable adapter between pages; no process-local submission visibility needed.
                    outer.ledger=DurableLedger(outer.path,clock=lambda:outer.now)
                    outer.store=ReplayStore(outer.ledger,POLICY)
                    outer.route=SyntheticReplayRoute(outer.store,outer.provider)
                    adapter.route=outer.route
                    name,args='scrimmage_replay',asdict(req(inner.sid,'page',view_id=last['view_id'],record_offset=offset))
                return response([function(name,args,call_id='call_'+str(n),item_id='fc_'+str(n))])
        exchange=Exchange()
        transport=OfflineResponsesTransport(exchange,FixtureCounter(),controller_protocol='v2')
        context=FrozenContext(b'exact\r\n system\n',b'exact task\n')
        report=run_synthetic(context,transport,workspace,adapter,protocol='v2')
        self.assertEqual(report.status,'complete')
        pages=exchange.pages
        self.assertGreater(len(pages),1)
        expected=fixture(start=0,end=45,robot=None,limit=10000)
        self.assertEqual(sum(len(p['records']) for p in pages),expected['matching_record_count'])
        identity=lambda row: tuple(row[key] for key in ('kind','match_index','event_index','round','row_index'))
        self.assertEqual([identity(row) for page in pages for row in page['records']],
                         [identity(row) for row in expected['records']])
        offset=0
        for page in pages:
            self.assertEqual(page['query']['record_offset'],offset)
            offset+=len(page['records'])
        self.assertIsNone(pages[-1]['coverage']['next_record_offset'])
        self.assertEqual({c['name'] for row in report.transcript for c in json.loads(row).get('calls',[])},set(TOOL_NAMES))
        outputs=[row for row in report.transcript if 'result' in json.loads(row)]
        self.assertTrue(all(len(row)<=16384 for row in outputs))
        self.assertLessEqual(sum(map(len,outputs)),ControllerLimits().max_total_output_bytes)
        for row in outputs:
            self.assertNotIn(SECRET.encode(),row)
            for secret in (b'source_sha256',b'producer_identity',b'projector_identity',RAW):
                self.assertNotIn(secret,row)
        self.assertEqual(len({encoded(b['tools']) for b in exchange.requests}),1)
        self.assertTrue(all(b['instructions'].encode()==context.system for b in exchange.requests))
        print('COMPOSED_SYNTHETIC_EVIDENCE',json.dumps({'pages':len(pages),'records':offset,
            'tool_calls':report.tool_calls,'envelope_max':max(map(len,outputs)),
            'output_bytes':sum(map(len,outputs))},sort_keys=True))

    def test_22_eight_process_page_admission_charges_exactly_one_attempt(self):
        sid, unused = self.finish()
        request = self.window(sid)
        with ProcessPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(reserve_child, [(self.path, request)]*8))
        self.assertEqual(results.count(('ok', 1)), 1)
        self.assertEqual(results.count(('error', 'resource_limit')), 7)
        self.assertEqual(self.sql('SELECT count(*) FROM replay_views'), [(1,)])
        self.assertEqual(self.sql('SELECT state,attempt_count FROM replay_attempts'), [('running', 1)])

    def test_23_failed_attempt_quota_survives_restart_and_blocks_callback(self):
        self.path = Path(self.temp.name)/'attempts.db'
        limits = replace(ReplayLimits(), attempts_per_run=2)
        self.open(limits)
        sid, unused = self.finish()
        request = self.window(sid)
        def fail(unused): raise RuntimeError(SECRET)
        self.provider.hook = fail
        self.assertEqual(self.reply(request)['reason'], 'invalid_evidence')
        self.open(limits)
        self.provider.hook = fail
        self.assertEqual(self.reply(request)['reason'], 'invalid_evidence')
        self.assertEqual(self.reply(request)['reason'], 'resource_limit')
        self.assertEqual(len(self.provider.calls), 1)
        self.assertEqual(self.sql('SELECT state,attempt_count FROM replay_attempts'), [('failed', 2)])

    def test_24_expired_source_stays_charged_and_immutable(self):
        self.path = Path(self.temp.name)/'retention.db'
        limits = replace(ReplayLimits(), global_sources=1, source_ttl=1)
        self.open(limits)
        first, unused = self.finish()
        self.now += 1
        self.open(limits)
        self.assertEqual(self.reply(req(first))['reason'], 'replay_not_available')
        sid, claim = self.running(key='second')
        self.denied('resource_limit', self.route.complete_with_replay, 'alice', 'run', claim,
                    complete(), (ReplayFixture('two', RAW, 1),))
        self.assertEqual(self.sql('SELECT count(*) FROM replay_sources'), [(1,)])
        for table in ('replay_job_runs','replay_completions','replay_sources'):
            with self.assertRaises(sqlite3.IntegrityError): self.sql('DELETE FROM '+table)

    def test_25_default_v1_with_v2_adapter_still_withholds(self):
        artifacts=SourceArtifactStore()
        adapter=ReplayScrimmageAdapter(self.route,artifacts,'alice','run')
        class Workspace:
            def exec(inner, unused): return ExportedExecReply('succeeded',source=SourceExport('bot',archive()))
        workspace=CapturingSandboxAdapter(Workspace(),artifacts,'alice','run')
        class Transport:
            def next_turn(inner, turn):
                outputs=[json.loads(row)['result'] for row in turn.transcript if 'result' in json.loads(row)]
                if not outputs: name,args='workspace_exec',{'argv':['inert'],'cwd':'.','timeout_seconds':1}
                elif len(outputs)==1: name,args='scrimmage_submit',{'artifact_id':outputs[-1]['artifact_id'],'package':'bot'}
                elif len(outputs)==2: name,args='scrimmage_replay',{'submission_id':outputs[-1]['submission_id']}
                else: return TurnReply(final_text='done')
                return TurnReply((ToolCall('call'+str(len(outputs)),name,json.dumps(args)),))
        result=run_synthetic(FrozenContext(b's',b't'),Transport(),workspace,adapter)
        outputs=[json.loads(row)['result'] for row in result.transcript if 'result' in json.loads(row)]
        self.assertEqual(result.status,'complete')
        self.assertEqual(outputs[-1]['reason'],'replay_withheld')
        self.assertEqual(self.provider.calls,[])

    def test_26_minimum_payload_budget_keeps_exact_pagination_progress(self):
        self.path = Path(self.temp.name)/'payload.db'
        self.open(replace(ReplayLimits(),payload_bytes=4096))
        sid, unused = self.finish()
        request = self.window(sid,limit=64)
        count, pages = 0, 0
        while True:
            value=self.reply(request)
            self.assertEqual(value['status'],'available')
            self.assertLessEqual(len(encoded(value)),4096)
            page=value['page']; pages+=1
            self.assertEqual(page['query']['record_offset'],count)
            count+=len(page['records'])
            next_offset=page['coverage']['next_record_offset']
            if next_offset is None: break
            self.assertEqual(next_offset,count)
            self.assertGreater(len(page['records']),0)
            request=req(sid,'page',view_id=value['view_id'],record_offset=next_offset)
            self.assertLess(pages,30)
        self.assertEqual(count,26)
        self.assertGreater(pages,1)

    def test_27_explicit_3013_profile_is_bound_without_version_inference(self):
        self.path=Path(self.temp.name)/'profile.db'
        self.ledger=DurableLedger(self.path,clock=lambda:self.now)
        self.store=ReplayStore(self.ledger,replace(POLICY,spec_version='3.0.13'))
        self.provider=Provider(); self.route=SyntheticReplayRoute(self.store,self.provider)
        sid,unused=self.finish()
        self.assertEqual(self.reply(req(sid))['replays'][0]['spec_version'],'3.0.13')
        request=self.window(sid)
        self.assertEqual(self.reply(request)['page']['spec_version'],'3.0.13')
        real=self.provider.query
        with patch.object(self.provider,'query',side_effect=lambda query:replace(real(query),spec_version='2.0.3')):
            self.assertEqual(self.reply(request)['reason'],'invalid_evidence')


if __name__ == '__main__':
    unittest.main(verbosity=2)
