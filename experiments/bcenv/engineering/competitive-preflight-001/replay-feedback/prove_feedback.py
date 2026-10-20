"""Read the one existing public-game replay; never compile or launch a game."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
OBSERVER = HERE / 'observer'
BRIDGE = Path('/workspace/shared/bc23-service-integration')
REPO = Path('/workspace/shared/bcenv-lecture')
sys.path.insert(0, str(BRIDGE))
sys.path.insert(0, str(REPO))
import bridge
from services.replay_feedback import FeedbackLimits, FeedbackRejected, project_replay_feedback

EXPECTED_COMMIT = '04c815954154a9be691bb531245f74e35cbd6edf'
JAVA = '/nix/store/84sr5jfh99mdgfwa0sa8nxifgy0vqicf-openjdk-8u504-b01/bin/java'
START, END = 35, 40  # Fixed before inspecting this window's rows.
JDK_WARNING = b"OpenJDK 64-Bit Server VM warning: Can't detect primordial thread stack location - find_vma failed\n"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write('\n')


def snapshot(report):
    result = {'bridge_runtime': bridge.runtime_fingerprint(),
              'job_files': bridge.inventory(BRIDGE / 'root/workspace/jobs'),
              'match_files': bridge.inventory(BRIDGE / 'root/workspace/matches'),
              'top_level_files': {p.name: bridge.sha(p) for p in sorted(BRIDGE.iterdir()) if p.is_file()}}
    assert result['bridge_runtime'] == report['runtime'], 'runtime drift'
    match = Path(report['match']['directory'])
    assert bridge.inventory(match) == report['match']['sealed_files'], 'match artifact drift'
    assert bridge.sha(match / 'replay.bc23') == report['match']['replay_sha256'], 'replay drift'
    return result


def query(report, record_limit, name):
    replay = report['match']['internal'] + '/replay.bc23'
    command = ['/usr/bin/unshare', '--user', '--map-root-user', '--net', '--',
               '/usr/sbin/chroot', str(BRIDGE / 'root'), JAVA,
               '-Xmx512m', '-XX:-UsePerfData', '-Djava.io.tmpdir=/tmp',
               '-cp', '/opt/bcenv/replay-classes:/opt/battlecode23/engine.jar',
               'ReplayQuery', replay, str(START), str(END), 'all', str(record_limit)]
    output, errors = OBSERVER / (name + '.json'), OBSERVER / (name + '.stderr')
    started = time.monotonic()
    with output.open('xb') as stdout, errors.open('xb') as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr,
                                   env={'PATH': '/usr/bin:/bin', 'LANG': 'C'},
                                   start_new_session=True)
        try:
            code = process.wait(timeout=60)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            raise RuntimeError('parser_timeout') from None
    assert code == 0, 'parser_nonzero_exit'
    data = output.read_bytes()
    assert len(data) <= 4_194_304, 'query_input_limit'
    value = json.loads(data)
    assert value['status'] == 'complete' and value['source_stream_complete']
    assert value['spec_version'] == '3.0.13'
    assert value['source_replay']['sha256'] == report['match']['replay_sha256']
    return data, value, {'command': command, 'exit_code': code,
                         'elapsed_seconds': round(time.monotonic() - started, 6),
                         'stdout_sha256': digest(data), 'stdout_bytes': len(data),
                         'stderr_sha256': bridge.sha(errors), 'stderr_bytes': errors.stat().st_size,
                         'stderr_classification': 'jdk_stack_location_warning' if errors.read_bytes() == JDK_WARNING
                                                  else 'empty' if errors.stat().st_size == 0 else 'other_diagnostic'}


def check_public(data, source, source_data, context, report):
    out = json.loads(data)
    assert set(out) == {'schema', 'status', 'spec_version', 'submission_id', 'job_id',
                        'own_team_id', 'query', 'matches', 'records', 'coverage', 'limits'}
    assert out['spec_version'] == '3.0.13'
    assert out['submission_id'] == context['submission_id'] and out['job_id'] == context['job_id']
    assert out['own_team_id'] == 1
    assert len(data) <= out['limits']['max_output_encoded_bytes']
    assert len(out['records']) <= out['limits']['max_records']
    coverage = out['coverage']
    assert coverage['source_stream_complete'] is True
    assert coverage['all_schema_fields_validated'] is False
    assert coverage['matching_record_count'] == source['matching_record_count']
    assert coverage['matching_counts_by_kind'] == source['matching_counts_by_kind']
    assert coverage['source_returned_record_count'] == len(source['records'])
    assert coverage['returned_record_count'] == len(out['records'])
    assert coverage['source_truncated'] == source['truncated']
    assert coverage['truncated'] == (len(out['records']) < source['matching_record_count'])
    assert coverage['selected_records_complete'] == (len(out['records']) == source['matching_record_count'])
    assert coverage['projection_truncated'] == (len(out['records']) < len(source['records']))
    expected = deepcopy(source['records'][:len(out['records'])])
    for row in expected:
        team = row['team_id']
        row['team_slot'] = None if team is None else 'own' if team == 1 else 'opponent'
    assert out['records'] == expected, 'raw row values or prefix changed'
    for actual, original in zip(out['matches'], source['matches']):
        assert actual == {k: v for k, v in original.items() if k != 'map'}
    secrets = [b'/workspace', b'/nix/store', b'/opt/', b'http://', b'https://',
               b'source_replay', b'sha256', b'package', b'raw_log', b'hidden_schedule',
               report['engine_sha256'].encode(), report['match']['replay_sha256'].encode(),
               report['map_sha256'].encode(), report['candidate']['package'].encode(),
               report['public_fixture']['package'].encode()]
    secrets += [match['map'].encode() for match in source['matches']]
    for secret in secrets:
        assert secret not in data, 'private metadata leaked'
    assert data == json.dumps(out, sort_keys=True, separators=(',', ':')).encode()
    assert digest(source_data) == source_data_hashes[id(source_data)], 'source query bytes changed'
    return out


source_data_hashes = {}


def main():
    assert not (HERE / 'verification.json').exists(), 'already_recorded'
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
    assert commit == EXPECTED_COMMIT, 'unexpected_projector_commit'
    report = bridge.read_json(BRIDGE / 'integration-report.json')
    assert report['new_games'] == 1 and report['engine_version'] == '3.0.13'
    assert report['heldout_gate'] == 'closed' and report['public_source_edits'] is False
    before = snapshot(report)
    write_json(OBSERVER / 'originals-before.json', before)
    # Revalidate the persisted positive chain/negative controls without engine execution.
    with (OBSERVER / 'bridge-offline-tests.txt').open('xb') as output:
        offline = subprocess.run([sys.executable, '-B', '-m', 'unittest', 'test_bridge.py', '-v'],
            cwd=BRIDGE, stdout=output, stderr=subprocess.STDOUT, timeout=60,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
    assert offline.returncode == 0, 'persisted_bridge_verification_failed'
    full_data, full, full_process = query(report, 10000, 'query-full')
    capped_data, capped, capped_process = query(report, 32, 'query-capped')
    source_data_hashes.update({id(full_data): digest(full_data), id(capped_data): digest(capped_data)})
    assert full['selected_records_complete'] is True, 'window_exceeded_source_cap'
    assert full['returned_record_count'] == full['matching_record_count']
    assert dict(Counter(row['kind'] for row in full['records'])) == full['matching_counts_by_kind']
    assert capped['records'] == full['records'][:32]
    assert capped['matching_record_count'] == full['matching_record_count']
    assert capped['matching_counts_by_kind'] == full['matching_counts_by_kind']
    assert capped['truncated'] is True
    assert all(m['all_requested_positive_rounds_present'] for m in full['matches'])
    context = {'submission_id': 's_' + uuid.uuid4().hex, 'job_id': 'j_' + uuid.uuid4().hex,
               'own_team_id': 1, 'expected_spec_version': '3.0.13'}
    variants = [('feedback.json', full_data, full, FeedbackLimits(max_records=64, max_output_encoded_bytes=32768)),
                ('feedback-window-complete.json', full_data, full, FeedbackLimits()),
                ('feedback-source-capped.json', capped_data, capped, FeedbackLimits(max_records=64, max_output_encoded_bytes=32768)),
                ('feedback-byte-capped.json', full_data, full, FeedbackLimits(max_records=64, max_output_encoded_bytes=4096))]
    results = {}
    for name, data, source, limits in variants:
        encoded = project_replay_feedback(data, **context, limits=limits)
        out = check_public(encoded, source, data, context, report)
        with (HERE / name).open('xb') as output:
            output.write(encoded)
        results[name] = {'bytes': len(encoded), 'sha256': digest(encoded),
                         'coverage': out['coverage'],
                         'returned_counts_by_kind': dict(Counter(row['kind'] for row in out['records'])),
                         'returned_team_slots': sorted({row['team_slot'] for row in out['records'] if row['team_slot']})}
    # Negative checks alter only in-memory query copies, never replay originals.
    negative = []
    cases = [('wrong_expected_version', full, {**context, 'expected_spec_version': '2.0.3'}),
             ('incomplete_source', {**full, 'source_stream_complete': False}, context)]
    corrupt = deepcopy(full)
    corrupt['records'][-1]['kind'] = 'private_future_record'
    cases.append(('corrupt_tail_beyond_projection_cap', corrupt, context))
    for name, value, ctx in cases:
        try:
            project_replay_feedback(json.dumps(value).encode(), **ctx, limits=FeedbackLimits(max_records=1))
        except FeedbackRejected as error:
            assert error.code == 'invalid_evidence'
            negative.append({'case': name, 'result': 'rejected', 'reason': error.code})
        else:
            raise AssertionError('accepted negative case')
    injected = deepcopy(full)
    marker = 'PRIVATE_METADATA_INJECTION_MARKER'
    injected['opponent'] = {'package': marker, 'path': marker}
    for row in injected['records']:
        row['metadata'] = {'schedule': [marker, {'raw_log': marker}]}
    assert project_replay_feedback(json.dumps(injected).encode(), **context,
        limits=variants[0][3]) == (HERE / 'feedback.json').read_bytes()
    after = snapshot(report)
    assert before == after, 'originals_changed'
    write_json(OBSERVER / 'originals-after.json', after)
    write_json(OBSERVER / 'provenance.json', {
        'source_bridge_report_sha256': bridge.sha(BRIDGE / 'integration-report.json'),
        'source_replay_sha256': report['match']['replay_sha256'],
        'source_replay_bytes': (Path(report['match']['directory']) / 'replay.bc23').stat().st_size,
        'engine_sha256': report['engine_sha256'],
        'projector_commit': commit, 'projector_sha256': bridge.sha(REPO / 'services/replay_feedback.py'),
        'producer': report['runtime'], 'query_processes': [full_process, capped_process],
        'originals_equal': before == after, 'opaque_demonstration_context': context})
    verification = {
        'schema': 'bcenv.bc2023.feedback-integration-evidence.v1',
        'scope': 'Offline projection from one previously completed public game; no new matches.',
        'expected_spec_version': '3.0.13', 'projector_commit': commit,
        'new_matches': 0, 'heldout_gate': 'closed', 'facade_integration': False,
        'source_window': {'round_start': START, 'round_end': END, 'robot_id': None},
        'source_stream_complete': True, 'source_query_records_complete': True,
        'source_matching_record_count': full['matching_record_count'],
        'source_matching_counts_by_kind': full['matching_counts_by_kind'],
        'source_window_rounds_present': True, 'all_schema_fields_validated': False,
        'original_artifacts_unchanged': True, 'private_metadata_absence_checks': 'passed',
        'exact_raw_prefix_and_coverage_checks': 'passed', 'nested_injection_check': 'passed',
        'persisted_bridge_checks': {'passed': 8, 'new_engine_runs': 0},
        'negative_checks': negative, 'outputs': results,
        'producer_diagnostics': {'classification': full_process['stderr_classification'],
                                 'processes': 2, 'raw_stderr_retained_privately': True,
                                 'parser_exit_codes': [full_process['exit_code'], capped_process['exit_code']]},
        'limitations': ['Core replay validation is not full FlatBuffers verification.',
                       'Hashes detect drift but do not establish an isolation or authenticity boundary.',
                       'No new game, heldout evaluation, service deployment or model learning loop was run.',
                       'Gameplay can reveal recognizable behavior even after identity metadata is removed.',
                       'The fixed window and prefix are not representative sampling or causal analysis.']}
    write_json(HERE / 'verification.json', verification)
    print(json.dumps({'status': 'verified', 'new_matches': 0,
        'source_records': full['matching_record_count'],
        'outputs': {name: {'bytes': value['bytes'], 'records': value['coverage']['returned_record_count'],
                          'truncation_reasons': value['coverage']['truncation_reasons']}
                    for name, value in results.items()}}, sort_keys=True))


if __name__ == '__main__':
    main()
