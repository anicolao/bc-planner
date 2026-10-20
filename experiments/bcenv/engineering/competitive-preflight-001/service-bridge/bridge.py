"""Scratch-only trusted/public integration probe; no server or heldout access.

One fixed public match, fixed runtime/map/launcher, and source ZIPs are the only
submission inputs. All host commands below are service-owned constants. The
existing user/network-namespace chroot is copied unchanged, not security-audited.
This does not enable the permanently closed real-heldout gate.
"""
from dataclasses import dataclass
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time
import uuid
import zipfile

from service_facade import ScrimmageFacade, accept_source_zip, require_heldout_attestation, BoundaryUnverified

BASE = Path(__file__).resolve().parent
ROOT = BASE / 'root'
WORKSPACE = ROOT / 'workspace'
PUBLIC = Path('/workspace/shared/bc23-public-smoke/root/workspace/public-sources')
ENGINE_SHA256 = '2b6db98e312e0e509d599acc46bffbb55c2569de0f12c8214a85ee57625f15f2'
MAP_SHA256 = 'a53211fc3fb4cc6427693f6f65b0732cc4bdf9ecb90f911ffbd71b5af82bb910'
JAVA = '/nix/store/84sr5jfh99mdgfwa0sa8nxifgy0vqicf-openjdk-8u504-b01/bin/java'
JAVAC = '/nix/store/84sr5jfh99mdgfwa0sa8nxifgy0vqicf-openjdk-8u504-b01/bin/javac'
ENGINE = '/opt/battlecode23/engine.jar'
MAP = '/opt/battlecode23/maps/DefaultMap.map23'
ENGINE_VERSION = '3.0.13'


class EvidenceInvalid(ValueError):
    pass


def need(condition, code):
    if not condition:
        raise EvidenceInvalid(code)


def sha(path, maximum=64 * 1024 * 1024):
    path = Path(path)
    need(not path.is_symlink() and path.is_file(), 'not_regular_file')
    need(path.stat().st_size <= maximum, 'file_limit')
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            result.update(block)
    return result.hexdigest()


def identity(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def inventory(path, maximum=1024):
    result = {}
    for item in sorted(Path(path).rglob('*')):
        need(not item.is_symlink(), 'symlink')
        if item.is_file():
            need(len(result) < maximum, 'inventory_limit')
            result[item.relative_to(path).as_posix()] = sha(item)
        else:
            need(item.is_dir(), 'special_file')
    return result


def read_json(path):
    path = Path(path)
    need(not path.is_symlink() and path.is_file() and path.stat().st_size <= 1048576, 'json_limit')
    with path.open() as stream:
        return json.load(stream)


def write_new(path, value):
    with Path(path).open('x') as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write('\n')


def source_zip(catalog_key):
    source = PUBLIC / catalog_key
    provenance = read_json(BASE / 'provenance' / catalog_key / 'provenance.json')
    need(sha(BASE / 'provenance' / catalog_key / 'LICENSE') == provenance['licenseSha256'], 'license_identity')
    files = inventory(source / 'java')
    expected = {item['path']: item['sha256'] for item in provenance['sourceFiles']}
    need(files == expected, 'public_source_drift')
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, (source / 'java' / name).read_bytes())
    return stream.getvalue(), provenance


def stage(accepted, private_id):
    # IDs are minted by this trusted process, never a submitted path argument.
    need(private_id.replace('_', '').isalnum(), 'job_id')
    job = WORKSPACE / 'jobs' / private_id
    job.mkdir(mode=0o700, parents=True, exist_ok=False)
    source = job / 'source'
    source.mkdir(mode=0o700)
    for item in accepted.files:
        target = source / item.path
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(item.data)
    expected = {item.path: hashlib.sha256(item.data).hexdigest() for item in accepted.files}
    need(inventory(source) == expected, 'staged_source_drift')
    return job, '/workspace/jobs/' + private_id, expected


def invoke(arguments, private_log):
    """Only fixed service recipes call this function; never client-supplied argv."""
    started = time.monotonic()
    with Path(private_log).open('xb') as output:
        process = subprocess.Popen([str(BASE / 'bcenv'), *arguments], stdout=output,
            stderr=subprocess.STDOUT, env={'PATH': '/usr/bin:/bin', 'LANG': 'C'}, start_new_session=True)
        try:
            returncode = process.wait(timeout=180)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
            return {'status': 'timeout', 'elapsed_seconds': round(time.monotonic() - started, 3)}
    return {'status': 'succeeded' if returncode == 0 else 'failed', 'exit_code': returncode,
            'elapsed_seconds': round(time.monotonic() - started, 3), 'log_sha256': sha(private_log)}


def check_process(record, directory, log, *, stderr=None):
    need(record['status'] == 'succeeded' and record['exit_code'] == 0, 'process_not_successful')
    need(record['log'] == log and record['log_sha256'] == sha(directory / log, 8388608), 'process_log_drift')
    if stderr:
        need(record['stderr_log'] == stderr and record['stderr_sha256'] == sha(directory / stderr, 8388608), 'stderr_drift')


@dataclass(frozen=True)
class BuildBinding:
    directory: Path
    internal: str
    package: str
    accepted_identity: str
    source_files: tuple
    binary_files: tuple
    source_identity: str
    binary_identity: str
    sealed_files: tuple


def validate_build(directory, internal, accepted, expected_source):
    data = read_json(directory / 'artifact.json')
    need(data['schema'] == 'bcenv.artifact.v1' and data['kind'] == 'build' and data['season'] == '2023', 'build_schema')
    need(data['status'] == 'verified' and data['package'] == accepted.package, 'build_not_verified')
    need(data['engine_sha256'] == ENGINE_SHA256, 'build_engine_mismatch')
    need(inventory(directory / 'source') == expected_source == data['source_files'], 'source_drift')
    need(identity(expected_source) == data['source_sha256'], 'source_identity_mismatch')
    binaries = inventory(directory / 'classes')
    need(binaries and binaries == data['binary_files'] and identity(binaries) == data['binary_sha256'], 'binary_drift')
    need(len(data['steps']) == 2, 'build_steps')
    check_process(data['steps'][0], directory, 'compile.log')
    check_process(data['steps'][1], directory, 'verify.log')
    compile_command = [JAVAC, '-source', '8', '-target', '8', '-encoding', 'UTF-8', '-proc:none',
                       '-classpath', ENGINE, '-d', internal + '/classes']
    compile_command += [internal + '/source/' + name for name in sorted(expected_source)]
    need(data['steps'][0]['command'] == compile_command, 'compile_command_mismatch')
    need(data['steps'][1]['command'] == [JAVA, '-cp', ENGINE, 'battlecode.instrumenter.Verifier',
                                       accepted.package, internal + '/classes'], 'verifier_command_mismatch')
    return BuildBinding(directory, internal, accepted.package, accepted.content_sha256,
        tuple(sorted(expected_source.items())), tuple(sorted(binaries.items())),
        data['source_sha256'], data['binary_sha256'], tuple(sorted(inventory(directory).items())))


def build(accepted, private_id):
    job, internal, expected_source = stage(accepted, private_id)
    output = job / 'build'
    invocation = invoke(['build', '--source', internal + '/source', '--package', accepted.package,
                         '--output', internal + '/build', '--timeout', '60'], job / 'build-launcher.log')
    if invocation['status'] != 'succeeded':
        return None, job, invocation
    binding = validate_build(output, internal + '/build', accepted, expected_source)
    return binding, job, invocation


def validate_match(directory, internal, candidate, opponent):
    # Expected input identities are held by the parent observer, not reloaded
    # from a manifest an executing game could edit.
    for binding in (candidate, opponent):
        need(tuple(sorted(inventory(binding.directory).items())) == binding.sealed_files, 'sealed_build_drift')
    result = read_json(directory / 'result.json')
    need(result['schema'] == 'bcenv.artifact.v1' and result['kind'] == 'match' and result['season'] == '2023', 'match_schema')
    need(result['status'] == 'completed', 'match_incomplete')
    need(result.get('winner') in ('A', 'B'), 'missing_winner')
    need(result['engine_sha256'] == ENGINE_SHA256 and result['engine_version'] == ENGINE_VERSION, 'match_engine_mismatch')
    need(result['map_sha256'] == MAP_SHA256 == sha(directory / 'maps/DefaultMap.map23'), 'map_drift')
    need(inventory(directory / 'maps') == {'DefaultMap.map23': MAP_SHA256}, 'unexpected_maps')
    for slot, binding in (('A', candidate), ('B', opponent)):
        expected = {'source_sha256': binding.source_identity, 'binary_sha256': binding.binary_identity,
                    'package': binding.package}
        need(result['teams'][slot] == expected and inventory(directory / ('team-' + slot)) == dict(binding.binary_files), 'match_input_drift')
    need(set(result['teams']) == {'A', 'B'}, 'extra_team')
    config = result['config']
    fixed = {'bc.server.mode': 'headless', 'bc.server.wait-for-client': 'false', 'bc.server.websocket': 'false',
        'bc.game.map-path': internal + '/maps', 'bc.server.robot-player-to-system-out': 'false',
        'bc.server.debug': 'false', 'bc.engine.debug-methods': 'false', 'bc.engine.enable-profiler': 'false',
        'bc.engine.show-indicators': 'true', 'bc.game.team-a': 'A', 'bc.game.team-b': 'B',
        'bc.game.team-a.url': internal + '/team-A', 'bc.game.team-b.url': internal + '/team-B',
        'bc.game.team-a.package': candidate.package, 'bc.game.team-b.package': opponent.package,
        'bc.game.maps': 'DefaultMap', 'bc.server.validate-maps': 'true', 'bc.server.alternate-order': 'false',
        'bc.server.save-file': internal + '/replay.bc23'}
    need(config == fixed, 'match_config_mismatch')
    check_process(result['process'], directory, 'engine.log')
    expected_command = [JAVA, '-Xmx512m'] + ['-D' + key + '=' + value for key, value in fixed.items()]
    expected_command += ['-cp', ENGINE, 'battlecode.server.Main', '-c=-']
    need(result['process']['command'] == expected_command, 'engine_command_mismatch')
    check_process(result['extraction'], directory, 'replay-summary.json', stderr='replay-extractor.log')
    need(result['extraction']['command'] == [JAVA, '-Xmx512m', '-cp', '/opt/bcenv/replay-classes:' + ENGINE,
                                            'ReplaySummary', internal + '/replay.bc23'], 'extractor_command_mismatch')
    replay = result['replay']
    need(replay['path'] == 'replay.bc23' and replay['summary'] == 'replay-summary.json', 'replay_path_mismatch')
    need(replay['sha256'] == sha(directory / 'replay.bc23') and
         replay['summary_sha256'] == sha(directory / 'replay-summary.json'), 'replay_drift')
    summary = read_json(directory / 'replay-summary.json')
    need(summary['format'] == 'bcenv.bc2023.replay-summary.v1' and summary['status'] == 'complete' and
         summary['spec_version'] == ENGINE_VERSION and summary['game_footer_present'] is True and
         summary['extracted_fields_valid'] is True, 'replay_incomplete')
    need(len(summary['teams']) == 2 and {team['slot']: team['package'] for team in summary['teams']} ==
         {'A': candidate.package, 'B': opponent.package}, 'replay_team_mismatch')
    need({team['slot']: team['team_id'] for team in summary['teams']} == {'A': 1, 'B': 2}, 'replay_team_id_mismatch')
    need(len(summary['matches']) == 1, 'replay_match_count')
    game = summary['matches'][0]
    winner = result['winner']
    winner_id = 1 if winner == 'A' else 2
    need(summary['winner_slot'] == winner == game['winner_slot'] and
         summary['winner_team_id'] == winner_id == game['winner_team_id'], 'winner_mismatch')
    need(game['map'] == 'DefaultMap' and game['index'] == 0 and game['max_rounds'] == 2000, 'replay_map_mismatch')
    need(all(game[key] is True for key in ('match_footer_present', 'round_ids_contiguous',
         'round_records_cover_reported_rounds', 'resource_records_cover_observed_rounds')), 'replay_coverage')
    rounds = game['total_rounds']
    need(type(rounds) is int and 1 <= rounds <= 2000 and game['round_events'] == rounds == game['last_round_id'], 'round_evidence')
    evidence = {'status': 'complete', 'validated_complete': True,
                'summary': {'games': 1, 'wins': int(winner == 'A'), 'draws': 0, 'losses': int(winner == 'B')}}
    # Kept only in observer records. Public projection drops every such field.
    evidence.update(opponent=opponent.package, internal_path=str(directory), raw_logs=str(directory / 'engine.log'))
    return evidence, {'winner_slot': winner, 'rounds': rounds,
        'replay_sha256': replay['sha256'], 'summary_sha256': replay['summary_sha256'],
        'sealed_files': inventory(directory), 'parser_limitations': summary['limitations'],
        'all_schema_fields_validated': summary['all_schema_fields_validated']}


def runtime_fingerprint():
    need(sha(ROOT / ENGINE.lstrip('/')) == ENGINE_SHA256, 'runtime_engine_drift')
    need(sha(ROOT / MAP.lstrip('/')) == MAP_SHA256, 'runtime_map_drift')
    with zipfile.ZipFile(ROOT / ENGINE.lstrip('/')) as engine:
        need(engine.read('battlecode_version').decode().strip() == ENGINE_VERSION, 'runtime_version_mismatch')
    return {'launcher': sha(BASE / 'bcenv'), 'opt_files': inventory(ROOT / 'opt', maximum=8192),
            'facade': sha(BASE / 'service_facade.py'), 'bridge': sha(BASE / 'bridge.py')}


def demonstration():
    os.umask(0o077)
    need(not (BASE / 'integration-report.json').exists(), 'demonstration_already_recorded')
    initial_runtime = runtime_fingerprint()
    facade = ScrimmageFacade()
    zip_data, candidate_provenance = source_zip('beaverbois')
    receipt = facade.submit(zip_data, candidate_provenance['package'])
    need(receipt['status'] == 'accepted', 'unexpected_intake_rejection')
    submission_id = receipt['submission_id']
    candidate_source = facade.accepted_submission(submission_id)
    candidate, candidate_job, compile_run = build(candidate_source, submission_id)
    need(candidate is not None, 'candidate_compile_failed')
    fixture_zip, fixture_provenance = source_zip('lectureplayer')
    opponent_source = accept_source_zip(fixture_zip, fixture_provenance['package'])
    opponent, opponent_job, opponent_run = build(opponent_source, 'fixture_' + uuid.uuid4().hex)
    need(opponent is not None, 'fixture_compile_failed')
    match_id = 'match_' + uuid.uuid4().hex
    match = WORKSPACE / 'matches' / match_id
    match.parent.mkdir(mode=0o700, exist_ok=True)
    internal_match = '/workspace/matches/' + match_id
    match_run = invoke(['run', '--team-a', candidate.internal, '--team-b', opponent.internal,
                        '--map', MAP, '--output', internal_match, '--timeout', '120'], BASE / 'match-launcher.log')
    need(match_run['status'] == 'succeeded', 'public_match_failed')
    evidence, match_binding = validate_match(match, internal_match, candidate, opponent)
    result = facade.record_result(submission_id, evidence)
    need(result['status'] == 'complete', 'result_projection_failed')
    encoded = json.dumps(result, sort_keys=True, separators=(',', ':')).encode()
    need(len(encoded) <= 4096 and all(value not in encoded for value in (b'/workspace', b'lectureplayer', b'USQualifiers', b'engine.log')), 'public_data_leak')
    write_new(BASE / 'public-result.json', result)
    negatives = []
    bad_zip = io.BytesIO()
    with zipfile.ZipFile(bad_zip, 'w') as archive:
        archive.writestr('../escape.java', b'class Escape {}')
    bad_receipt = facade.submit(bad_zip.getvalue(), 'escape')
    need(bad_receipt['status'] == 'rejected' and facade.accepted_submission(bad_receipt['submission_id']) is None, 'bad_zip_accepted')
    negatives.append({'case': 'traversal_zip', 'public_result': bad_receipt, 'compiler_invoked': False})
    invalid = io.BytesIO()
    with zipfile.ZipFile(invalid, 'w') as archive:
        archive.writestr('broken/RobotPlayer.java', b'package broken; public class RobotPlayer { not valid Java; }')
    bad_receipt = facade.submit(invalid.getvalue(), 'broken')
    need(bad_receipt['status'] == 'accepted', 'invalid_java_layout_rejected')
    invalid_source = facade.accepted_submission(bad_receipt['submission_id'])
    invalid_binding, invalid_job, invalid_run = build(invalid_source, bad_receipt['submission_id'])
    bad_build = read_json(invalid_job / 'build/artifact.json')
    need(invalid_binding is None and bad_build['status'] == 'failed' and len(bad_build['steps']) == 1 and
         bad_build['steps'][0]['status'] == 'failed' and bad_build['steps'][0]['exit_code'] != 0 and
         'launch_error' not in bad_build['steps'][0], 'expected_compiler_rejection')
    rejected = facade.record_result(bad_receipt['submission_id'], {'status': 'rejected', 'reason': 'compile_rejected'})
    negatives.append({'case': 'invalid_java', 'public_result': rejected, 'compiler_invoked': True,
                      'invocation': invalid_run, 'artifact': str(invalid_job / 'build/artifact.json')})
    negative_root = BASE / 'negative-copies'
    negative_root.mkdir(mode=0o700)
    tampered_build = negative_root / 'tampered-build'
    shutil.copytree(candidate.directory, tampered_build)
    target = tampered_build / 'classes' / next(iter(dict(candidate.binary_files)))
    with target.open('ab') as stream:
        stream.write(b'tamper')
    try:
        validate_build(tampered_build, candidate.internal, candidate_source, dict(candidate.source_files))
    except EvidenceInvalid as error:
        need(str(error) == 'binary_drift', 'wrong_tamper_reason')
        negatives.append({'case': 'tampered_real_build_copy', 'validation': 'rejected', 'reason': str(error)})
    else:
        raise EvidenceInvalid('tampered_build_accepted')
    missing = negative_root / 'missing-winner'
    shutil.copytree(match, missing)
    modified = read_json(missing / 'result.json')
    modified['winner'] = None
    (missing / 'result.json').write_text(json.dumps(modified, sort_keys=True))
    try:
        validate_match(missing, internal_match, candidate, opponent)
    except EvidenceInvalid as error:
        need(str(error) == 'missing_winner', 'wrong_missing_winner_reason')
        negatives.append({'case': 'missing_winner_real_match_copy', 'validation': 'rejected', 'reason': str(error)})
    else:
        raise EvidenceInvalid('missing_winner_accepted')
    for item in negatives[-2:]:
        new = facade.submit(zip_data, candidate_source.package)
        item['public_result'] = facade.record_result(new['submission_id'], {'status': 'infrastructure_failure', 'reason': 'invalid_evidence'})
        need('summary' not in item['public_result'], 'failure_became_loss')
    try:
        require_heldout_attestation()
    except BoundaryUnverified:
        heldout_gate = 'closed'
    else:
        raise EvidenceInvalid('heldout_gate_open')
    need(runtime_fingerprint() == initial_runtime, 'runtime_changed')
    validate_match(match, internal_match, candidate, opponent)
    report = {'schema': 'bcenv.public-service-integration.scratch.v1',
        'scope': 'One NEW real public-source match; no reuse of historical match outputs for positive result.',
        'new_games': 1, 'public_source_edits': False, 'engine_version': ENGINE_VERSION,
        'engine_sha256': ENGINE_SHA256, 'map_sha256': MAP_SHA256,
        'runtime': initial_runtime, 'candidate': {'package': candidate.package,
            'provenance': candidate_provenance, 'accepted_sha256': candidate.accepted_identity,
            'build_source_sha256': candidate.source_identity, 'build_binary_sha256': candidate.binary_identity,
            'sealed_files': dict(candidate.sealed_files), 'job': str(candidate_job), 'invocation': compile_run},
        'public_fixture': {'package': opponent.package, 'provenance': fixture_provenance,
            'accepted_sha256': opponent.accepted_identity, 'sealed_files': dict(opponent.sealed_files),
            'job': str(opponent_job), 'invocation': opponent_run},
        'match': {'directory': str(match), 'internal': internal_match, 'invocation': match_run, **match_binding},
        'public_result': result, 'public_result_bytes': len(encoded), 'negative_checks': negatives,
        'heldout_gate': heldout_gate, 'replay_publication': 'withheld',
        'remaining_gaps': ['Experimental existing namespace/chroot, not independently audited agent/tool/host isolation.',
            'No durable queue/ownership/authentication/service transport; facade and observer state are process-local.',
            'No model inference/controller integration or supported provider transport.',
            'No sanitized replay publication through the service; full tactical learning loop remains unproved.',
            'Core replay fields and ordering validated; parser is not a full FlatBuffers schema verifier.',
            'No hidden opponents, strength ranking, tournament-equivalence or statistical performance claim.',
            'Runtime and build hashes detect drift under this trusted observer; they are not signatures or filesystem enforcement.']}
    write_new(BASE / 'integration-report.json', report)
    print(json.dumps({'status': result['status'], 'new_games': 1, 'negative_checks': len(negatives),
        'public_result': result, 'report': str(BASE / 'integration-report.json')}, sort_keys=True))


if __name__ == '__main__':
    demonstration()
