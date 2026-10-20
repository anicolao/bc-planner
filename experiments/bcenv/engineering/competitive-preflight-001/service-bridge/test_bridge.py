"""Revalidate persisted REAL integration outputs. Never invokes an engine/game."""
import json
from pathlib import Path
import unittest

import bridge
from service_facade import accept_source_zip, public_result


class PersistedIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = bridge.read_json(bridge.BASE / 'integration-report.json')
        cls.bindings = {}
        cls.accepted = {}
        for key, name in (('candidate', 'beaverbois'), ('public_fixture', 'lectureplayer')):
            data, provenance = bridge.source_zip(name)
            accepted = accept_source_zip(data, provenance['package'])
            job = Path(cls.report[key]['job'])
            expected_source = {item.path: __import__('hashlib').sha256(item.data).hexdigest() for item in accepted.files}
            binding = bridge.validate_build(job / 'build', '/workspace/jobs/' + job.name + '/build', accepted, expected_source)
            cls.bindings[key] = binding
            cls.accepted[key] = accepted
        cls.match = Path(cls.report['match']['directory'])
        cls.internal = cls.report['match']['internal']

    def test_exactly_one_new_game_and_two_public_sources(self):
        self.assertEqual(self.report['new_games'], 1)
        self.assertFalse(self.report['public_source_edits'])
        self.assertIn('NEW real public-source match', self.report['scope'])
        self.assertEqual(self.report['engine_version'], '3.0.13')
        self.assertEqual(self.report['heldout_gate'], 'closed')

    def test_frozen_build_observer_seals_still_match(self):
        for key, binding in self.bindings.items():
            self.assertEqual(dict(binding.sealed_files), self.report[key]['sealed_files'])
            self.assertEqual(binding.accepted_identity, self.report[key]['accepted_sha256'])

    def test_real_match_replay_and_output_seals_still_match(self):
        evidence, sealed = bridge.validate_match(self.match, self.internal, self.bindings['candidate'], self.bindings['public_fixture'])
        self.assertEqual(sealed['sealed_files'], self.report['match']['sealed_files'])
        self.assertEqual(sealed['replay_sha256'], self.report['match']['replay_sha256'])
        self.assertEqual(public_result(self.report['public_result']['submission_id'], evidence), self.report['public_result'])

    def test_traversal_was_rejected_before_compile(self):
        case = next(item for item in self.report['negative_checks'] if item['case'] == 'traversal_zip')
        self.assertEqual(case['public_result']['status'], 'rejected')
        self.assertFalse(case['compiler_invoked'])
        self.assertFalse((bridge.WORKSPACE / 'jobs' / case['public_result']['submission_id']).exists())

    def test_invalid_java_was_real_compiler_failure_not_a_loss(self):
        case = next(item for item in self.report['negative_checks'] if item['case'] == 'invalid_java')
        data = bridge.read_json(Path(case['artifact']))
        self.assertTrue(case['compiler_invoked'])
        self.assertEqual(data['status'], 'failed')
        self.assertNotEqual(data['steps'][0]['exit_code'], 0)
        self.assertEqual(case['public_result']['reason'], 'compile_rejected')
        self.assertNotIn('summary', case['public_result'])

    def test_tampered_copy_of_real_build_is_rejected(self):
        binding = self.bindings['candidate']
        with self.assertRaisesRegex(bridge.EvidenceInvalid, '^binary_drift$'):
            bridge.validate_build(bridge.BASE / 'negative-copies/tampered-build', binding.internal,
                                  self.accepted['candidate'], dict(binding.source_files))

    def test_real_match_copy_without_winner_never_becomes_a_score(self):
        with self.assertRaisesRegex(bridge.EvidenceInvalid, '^missing_winner$'):
            bridge.validate_match(bridge.BASE / 'negative-copies/missing-winner', self.internal,
                                  self.bindings['candidate'], self.bindings['public_fixture'])
        case = next(item for item in self.report['negative_checks'] if item['case'] == 'missing_winner_real_match_copy')
        self.assertEqual(case['public_result']['status'], 'infrastructure_failure')
        self.assertNotIn('summary', case['public_result'])

    def test_pinned_runtime_and_public_response_are_unchanged_and_bounded(self):
        self.assertEqual(bridge.runtime_fingerprint(), self.report['runtime'])
        response = bridge.read_json(bridge.BASE / 'public-result.json')
        self.assertEqual(response, self.report['public_result'])
        data = json.dumps(response, sort_keys=True, separators=(',', ':')).encode()
        self.assertEqual(len(data), self.report['public_result_bytes'])
        self.assertLessEqual(len(data), 4096)
        for secret in (b'/workspace', b'lectureplayer', b'USQualifiers', b'engine.log'):
            self.assertNotIn(secret, data)


if __name__ == '__main__':
    unittest.main()
