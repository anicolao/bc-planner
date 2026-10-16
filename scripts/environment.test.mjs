import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
test('flake lock pins a Git revision and content hash', () => {
  const lock = JSON.parse(readFileSync('flake.lock'));
  assert.match(lock.nodes.nixpkgs.locked.rev, /^[0-9a-f]{40}$/);
  assert.match(lock.nodes.nixpkgs.locked.narHash, /^sha256-/);
});
for (const name of ['nix-root','sync-environment','run-in-root','tailscale-runtime']) {
  test(`${name} has valid shell syntax`, () => {
    assert.equal(spawnSync('sh', ['-n', `scripts/${name}`]).status, 0);
  });
}
test('sync requires signatures and forbids local builds or lock mutation', () => {
  const s=readFileSync('scripts/sync-environment','utf8');
  assert.match(s,/--sigs-needed 1/); assert.match(s,/--max-jobs 0/);
  assert.match(s,/--no-write-lock-file/);
});
test('runner uses clean environment, no host-root bind', () => {
  const s=readFileSync('scripts/run-in-root','utf8');
  assert.match(s,/env -i/); assert.doesNotMatch(s,/--bind|mount --/);
});
