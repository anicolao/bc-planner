"""Recheck persisted feedback evidence without running a parser or a game."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
import prove_feedback as proof
from services.replay_feedback import FeedbackLimits, FeedbackRejected, project_replay_feedback


def main():
    here = Path(__file__).resolve().parent
    public = json.loads((here / 'verification.json').read_bytes())
    provenance = json.loads((here / 'observer/provenance.json').read_bytes())
    bridge_report = proof.bridge.read_json(proof.BRIDGE / 'integration-report.json')
    before = json.loads((here / 'observer/originals-before.json').read_bytes())
    after = json.loads((here / 'observer/originals-after.json').read_bytes())
    assert before == after == proof.snapshot(bridge_report)
    assert proof.bridge.sha(proof.REPO / 'services/replay_feedback.py') == provenance['projector_sha256']
    assert proof.bridge.sha(proof.BRIDGE / 'integration-report.json') == provenance['source_bridge_report_sha256']
    context = provenance['opaque_demonstration_context']
    full_data = (here / 'observer/query-full.json').read_bytes()
    capped_data = (here / 'observer/query-capped.json').read_bytes()
    full, capped = json.loads(full_data), json.loads(capped_data)
    assert full['matching_record_count'] == full['returned_record_count'] == len(full['records']) == 455
    assert dict(Counter(row['kind'] for row in full['records'])) == full['matching_counts_by_kind']
    assert capped['records'] == full['records'][:32]
    assert capped['matching_record_count'] == full['matching_record_count']
    assert full['source_replay']['sha256'] == bridge_report['match']['replay_sha256']
    for data, process in zip((full_data, capped_data), provenance['query_processes']):
        assert proof.digest(data) == process['stdout_sha256']
        assert len(data) == process['stdout_bytes'] and process['exit_code'] == 0
        proof.source_data_hashes[id(data)] = proof.digest(data)
    sources = {'feedback.json': (full_data, full),
               'feedback-window-complete.json': (full_data, full),
               'feedback-source-capped.json': (capped_data, capped),
               'feedback-byte-capped.json': (full_data, full)}
    for name, (data, source) in sources.items():
        actual = (here / name).read_bytes()
        out = proof.check_public(actual, source, data, context, bridge_report)
        limits = FeedbackLimits(**out['limits'])
        assert project_replay_feedback(data, **context, limits=limits) == actual
        assert len(actual) == public['outputs'][name]['bytes']
        assert proof.digest(actual) == public['outputs'][name]['sha256']
    assert public['new_matches'] == 0 and public['heldout_gate'] == 'closed'
    for line in (here / 'SHA256SUMS').read_text().splitlines():
        expected, name = line.split('  ', 1)
        assert '/' not in name and name in {'README.md', 'verification.json', *sources}
        assert hashlib.sha256((here / name).read_bytes()).hexdigest() == expected
    print('PASS: persisted query hashes, original artifact seals, exact projected prefixes, '
          'version binding, metadata stripping, output bounds, coverage and shareable checksums; '
          'no parser or game invoked.')


if __name__ == '__main__':
    main()
