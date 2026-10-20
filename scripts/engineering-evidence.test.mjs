// Offline drift checks only: no engine, bot, sandbox or network execution.
// Matching records can be rewritten together; these are not security attestations.
import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, lstatSync } from 'node:fs';
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
for (const directory of ['public-opponents', 'service-bridge', 'replay-feedback', 'composition', 'full-composition', 'source-export', 'integration-baseline']) {
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
