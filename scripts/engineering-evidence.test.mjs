// Offline drift checks only: no engine, bot, sandbox or network execution.
// Matching records can be rewritten together; these are not security attestations.
import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, lstatSync, readdirSync } from 'node:fs';
import { resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../experiments/bcenv/engineering/competitive-preflight-001/', import.meta.url));
const digest = bytes => createHash('sha256').update(bytes).digest('hex');
function checkedFile(directory, name) {
  assert.match(name, /^[A-Za-z0-9_.+/-]+$/);
  assert.ok(!name.startsWith('/') && name.split('/').every(part => part !== '..' && part !== '.' && part !== ''));
  const base = resolve(root, directory);
  const filename = resolve(base, name);
  assert.ok(filename.startsWith(base + sep));
  let parent = base;
  for (const part of name.split('/')) {
    parent = resolve(parent, part);
    assert.equal(lstatSync(parent).isSymbolicLink(), false);
  }
  assert.equal(lstatSync(filename).isFile(), true);
  return readFileSync(filename);
}
for (const directory of ['public-opponents', 'service-bridge', 'replay-feedback', 'composition', 'full-composition', 'source-export', 'integration-baseline', 'replay-pages-v2', 'durable-replay-v2']) {
  test(`compact ${directory} checksum inventory matches committed bytes`, () => {
    const lines = checkedFile(directory, 'SHA256SUMS').toString('utf8').trimEnd().split('\n');
    const seen = new Set();
    assert.ok(lines.length > 0);
    for (const line of lines) {
      const match = /^([0-9a-f]{64})  (.+)$/.exec(line);
      assert.ok(match, 'invalid checksum row');
      assert.equal(seen.has(match[2]), false, 'duplicate checksum path');
      seen.add(match[2]);
      assert.equal(digest(checkedFile(directory, match[2])), match[1], match[2]);
    }
  });
}
test('published namespace sources match independently reviewed snapshot', () => {
  const report = JSON.parse(checkedFile('namespace-probe', 'bc23-sandbox-independent-review-results.json'));
  assert.equal(report.passed, 21);
  assert.equal(report.failed, 0);
  assert.equal(Object.keys(report.source_sha256).length, 5);
  for (const [name, sha256] of Object.entries(report.source_sha256)) {
    assert.match(sha256, /^[0-9a-f]{64}$/);
    assert.equal(digest(checkedFile('namespace-probe', name)), sha256, name);
  }
});
test('published feedback examples retain recorded bytes and closed launch scope', () => {
  const report = JSON.parse(checkedFile('replay-feedback', 'verification.json'));
  assert.equal(report.new_matches, 0);
  assert.equal(report.facade_integration, false);
  assert.equal(report.heldout_gate, 'closed');
  assert.equal(report.expected_spec_version, '3.0.13');
  for (const [name, expected] of Object.entries(report.outputs)) {
    const bytes = checkedFile('replay-feedback', name);
    assert.equal(bytes.length, expected.bytes);
    assert.ok(bytes.length <= 262144);
    const output = JSON.parse(bytes);
    assert.equal(output.spec_version, report.expected_spec_version);
    assert.ok(output.records.length <= 1024);
  }
});

test('full offline composition snapshot matches imported source manifest', () => {
  const directory = 'full-composition';
  const manifest = JSON.parse(checkedFile(directory, 'source-manifest.json'));
  assert.equal(manifest.schema, 'bcenv.offline-composition-sources.v1');
  assert.equal(manifest.sources.length, 5);
  for (const source of manifest.sources) {
    const bytes = checkedFile(directory, `snapshot/${source.path}`);
    assert.equal(bytes.length, source.bytes);
    assert.equal(digest(bytes), source.sha256);
  }
  const result = JSON.parse(checkedFile(directory, 'results.json'));
  assert.equal(result.schema, 'bcenv.full-composition-smoke.v1');
  assert.equal(result.tests_run, 5);
  assert.equal(result.success, true);
  assert.equal(result.cases.launch_gate, 'real_launch_unsupported');
  assert.equal(result.cases.full_continuity.all_six_tools, true);
  assert.equal(result.cases.failed_export.sqlite_jobs, 0);
  assert.deepEqual(result.source_manifest, manifest);
});

test('retained replay v2 pages have continuous bounded progress and honest scope', () => {
  const directory = 'replay-pages-v2';
  const report = JSON.parse(checkedFile(directory, 'verification.json'));
  assert.equal(report.new_games, 0);
  assert.equal(report.provider_calls, 0);
  assert.equal(report.original_replay_unchanged, true);
  assert.equal(report.actual_cli_page_passed, true);
  let totalPages = 0;
  for (const window of report.windows) {
    const prefix = `${window.round_start}-${window.round_end}-offset-`;
    const pages = readdirSync(resolve(root, directory, 'feedback'))
      .filter(name => name.startsWith(prefix))
      .map(name => {
        const bytes = checkedFile(directory, `feedback/${name}`);
        assert.ok(bytes.length <= window.projection_byte_limit);
        return JSON.parse(bytes);
      }).sort((a, b) => a.query.record_offset - b.query.record_offset);
    assert.equal(pages.length, window.pages);
    let offset = 0;
    pages.forEach((page, index) => {
      assert.equal(page.schema, 'bcenv.bc2023.replay-feedback.v2');
      assert.equal(page.query.record_offset, offset);
      assert.equal(page.query.round_start, window.round_start);
      assert.equal(page.query.round_end, window.round_end);
      assert.equal(page.coverage.matching_record_count, window.matching_records);
      assert.equal(page.coverage.returned_record_count, page.records.length);
      assert.ok(page.records.length > 0 && page.records.length <= window.projection_record_limit);
      offset += page.records.length;
      assert.equal(page.coverage.output_page_end_offset, offset);
      assert.equal(page.coverage.next_record_offset, index + 1 === pages.length ? null : offset);
    });
    assert.equal(offset, window.matching_records);
    totalPages += pages.length;
  }
  assert.equal(totalPages, 67);
});


test('durable replay publication preserves review hashes and closed scope', () => {
  const directory = 'durable-replay-v2';
  const review = JSON.parse(checkedFile(directory, 'bcenv-durable-replay-review-sources.json'));
  const integration = JSON.parse(checkedFile(directory, 'integration-checks.json'));
  const publication = JSON.parse(checkedFile(directory, 'publication.json'));
  for (const artifact of review.review_artifacts) {
    assert.equal(digest(checkedFile(directory, artifact.path)), artifact.sha256);
  }
  assert.equal(review.reviewed_files.length, 8);
  assert.equal(integration.trusted_module_sources.length, 11);
  for (const source of integration.trusted_module_sources) {
    const reviewed = review.reviewed_files.find(item => item.path === source.path);
    if (reviewed) assert.equal(source.sha256, reviewed.sha256);
  }
  assert.equal(integration.flake_checks_passed.length, 13);
  assert.equal(integration.python_tests_passed, 286);
  assert.deepEqual(integration.trusted_modules_found_in_package, []);
  assert.equal(publication.portable_rerun_passed, 27);
  assert.equal(publication.new_public_games, 0);
  assert.equal(publication.provider_calls, 0);
  assert.equal(publication.real_launch_supported, false);
  assert.equal(publication.composed_fixture.pages, 5);
  assert.equal(publication.composed_fixture.records, 196);
  assert.ok(publication.composed_fixture.maximum_envelope_bytes <= 16384);
  assert.ok(publication.composed_fixture.aggregate_output_bytes <= 131072);
});
