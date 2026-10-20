"""Read-only proof against the single already persisted public game; zero games.

Requires the preserved bridge replay and the separately prepared pinned runtime
root. No downloads, compilation, provider calls or new matches occur here.
Use a fresh output directory; this script never overwrites proof artifacts.
"""
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

REPO = Path('/workspace/shared/bcenv-replay-page-v2')
BASE = Path('/workspace/shared/bc23-replay-page-v2-tests')
ROOT = BASE / 'root'
ORIGINAL = Path('/workspace/shared/bc23-service-integration/root/workspace/matches/'
                'match_1c05d0460ecc467b9fb68af72c8b9a25/replay.bc23')
EXPECTED = '62a5a7aee958455efc2a4d1dae7f0a11872d92048d845fec7a2001e75c4a59cd'
JDK = '/nix/store/84sr5jfh99mdgfwa0sa8nxifgy0vqicf-openjdk-8u504-b01/bin'
PYTHON = '/nix/store/h3l4z7p6wny3phbckwwhy1i2g52pdnj4-python3-3.13.15/bin/python3'
sys.path.insert(0, str(REPO))
from services.replay_feedback_v2 import ReplayPageQuery, FeedbackLimits, project_replay_feedback_page


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def encoded(value):
    return json.dumps(value, sort_keys=True, indent=2).encode() + b'\n'


def main():
    dest = Path(sys.argv[1])
    dest.mkdir()
    observer = dest / 'observer'
    observer.mkdir()
    (dest / 'feedback').mkdir()
    original = ORIGINAL.read_bytes()
    assert sha(original) == EXPECTED
    replay = ROOT / 'workspace/persisted-public.bc23'
    if not replay.exists():
        write(replay, original)
    assert replay.read_bytes() == original
    hashes = {name: sha((REPO / name).read_bytes()) for name in (
        'seasons/2023/replay/ReplayQuery.java', 'seasons/2023/replay/ReplaySummary.java',
        'services/replay_feedback_v2.py', 'seasons/2023/adapter.py')}
    prefix = ['/usr/bin/unshare', '--user', '--map-root-user', '--net', '--', '/usr/sbin/chroot', str(ROOT)]
    invocations = []

    def run_query(start, end, offset, limit, label, paged=True):
        args = [JDK + '/java', '-Xmx512m', '-XX:-UsePerfData', '-Djava.io.tmpdir=/tmp',
                '-cp', '/workspace/classes:/opt/battlecode23/engine.jar', 'ReplayQuery']
        if paged:
            args.append('--page')
        args.extend(['/workspace/persisted-public.bc23', str(start), str(end), 'all', str(limit)])
        if paged:
            args.append(str(offset))
        run = subprocess.run(prefix + args, capture_output=True, timeout=60,
                             env={'PATH': '/usr/bin:/bin', 'LANG': 'C'})
        write(observer / (label + '.json'), run.stdout)
        write(observer / (label + '.stderr'), run.stderr)
        assert run.returncode == 0
        value = json.loads(run.stdout)
        assert value['source_replay']['sha256'] == EXPECTED
        assert value['spec_version'] == '3.0.13' and value['source_stream_complete']
        invocations.append({'label': label, 'exit_code': run.returncode,
                            'stdout_bytes': len(run.stdout), 'stdout_sha256': sha(run.stdout),
                            'stderr_bytes': len(run.stderr), 'stderr_sha256': sha(run.stderr)})
        return run.stdout, value

    windows = []
    # Explicit choices recorded before querying; no outcome/side-based selection.
    for start, end in ((35, 40), (300, 301)):
        label = str(start) + '-' + str(end)
        _, complete = run_query(start, end, 0, 10000, label + '-v1-complete', paged=False)
        assert complete['selected_records_complete']
        expected_rows = complete['records']
        offset, collected, page_sizes, page_bytes = 0, [], [], []
        while True:
            data, source = run_query(start, end, offset, 31, label + '-offset-' + str(offset))
            output = project_replay_feedback_page(data,
                submission_id='s_' + 'c' * 32, job_id='j_' + 'd' * 32,
                own_team_id=1, expected_spec_version='3.0.13',
                expected_query=ReplayPageQuery(start, end, None, offset, 31),
                limits=FeedbackLimits(max_records=17, max_output_encoded_bytes=4096))
            value = json.loads(output)
            write(dest / 'feedback' / (label + '-offset-' + str(offset) + '.json'), output)
            for banned in (b'source_replay', b'sha256', b'package', b'map', b'/workspace', b'/nix',
                           b'raw_log', b'hidden_schedule'):
                assert banned not in output
            assert len(output) <= 4096 and len(value['records']) <= 17
            assert value['coverage']['matching_record_count'] == len(expected_rows)
            assert value['coverage']['matching_counts_by_kind'] == complete['matching_counts_by_kind']
            assert value['matches'] == [{k: v for k, v in m.items() if k != 'map'} for m in complete['matches']]
            rows = [{k: v for k, v in row.items() if k != 'team_slot'} for row in value['records']]
            assert rows == expected_rows[offset:offset + len(rows)]
            collected.extend(rows)
            page_sizes.append(len(rows)); page_bytes.append(len(output))
            next_offset = value['coverage']['next_record_offset']
            if next_offset is None:
                break
            assert next_offset == offset + len(rows) and next_offset > offset
            offset = next_offset
        assert collected == expected_rows
        windows.append({'round_start': start, 'round_end': end, 'matching_records': len(collected),
            'counts_by_kind': dict(Counter(row['kind'] for row in collected)),
            'pages': len(page_sizes), 'page_rows_min': min(page_sizes), 'page_rows_max': max(page_sizes),
            'page_bytes_max': max(page_bytes), 'concatenation_exact': True,
            'source_limit': 31, 'projection_record_limit': 17, 'projection_byte_limit': 4096})
    # Exercise the actual new adapter command with pinned Python and Java.
    project = ROOT / 'workspace/page-cli-project'
    (project / 'seasons/2023').mkdir(parents=True, exist_ok=True)
    (project / 'runtime').mkdir(exist_ok=True)
    shutil.copyfile(REPO / 'seasons/2023/adapter.py', project / 'seasons/2023/adapter.py')
    shutil.copyfile(REPO / 'runtime/artifacts.py', project / 'runtime/artifacts.py')
    cli_dir = '/workspace/cli-' + dest.name
    env = {'PATH': '/usr/bin:/bin', 'LANG': 'C', 'BCENV_JAVA': JDK + '/java',
           'BCENV_JAVAC': JDK + '/javac', 'BCENV_ENGINE_JAR': '/opt/battlecode23/engine.jar',
           'BCENV_REPLAY_CLASSPATH': '/workspace/classes:/opt/battlecode23/engine.jar'}
    run = subprocess.run(prefix + [PYTHON, '-B', '/workspace/page-cli-project/seasons/2023/adapter.py',
        'replay', 'page', '--replay', '/workspace/persisted-public.bc23', '--round-start', '35',
        '--round-end', '40', '--record-offset', '100', '--limit', '3', '--output', cli_dir],
        capture_output=True, timeout=60, env=env)
    write(observer / 'cli.stdout', run.stdout); write(observer / 'cli.stderr', run.stderr)
    assert run.returncode == 0
    receipt = json.loads((ROOT / cli_dir.lstrip('/') / 'query-result.json').read_bytes())
    assert receipt['status'] == 'completed' and receipt['kind'] == 'replay-page'
    assert ORIGINAL.read_bytes() == original and replay.read_bytes() == original
    report = {'status': 'passed', 'new_games': 0, 'provider_calls': 0,
              'original_replay_unchanged': True, 'source_replay_sha256': EXPECTED,
              'expected_spec_version': '3.0.13', 'source_code_sha256': hashes,
              'windows': windows, 'actual_cli_page_passed': True, 'invocations': invocations,
              'limits': 'Read-only engineering proof; no authorization/isolation/trial claim.'}
    write(dest / 'verification.json', encoded(report))
    print(json.dumps({'status': report['status'], 'windows': windows, 'query_invocations': len(invocations),
                      'actual_cli_page_passed': True, 'new_games': 0}, indent=2))


if __name__ == '__main__':
    main()
