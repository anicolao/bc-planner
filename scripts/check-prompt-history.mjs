import { execFileSync } from 'node:child_process';

const git = (...args) => execFileSync('git', args, { stdio: ['ignore', 'pipe', 'pipe'] });
const entry = (ref) => git('ls-tree', ref, '--', 'PROMPTS.md').toString();
const blob = (ref) => entry(ref) ? git('show', `${ref}:PROMPTS.md`) : Buffer.alloc(0);
try {
  const [base, head = 'HEAD'] = process.argv.slice(2);
  if (!base || !/^[0-9a-f]{40,64}$/.test(base)) throw new Error('Supply a full base commit SHA (all zeros for a new branch).');
  const range = /^0+$/.test(base) ? head : `${base}..${head}`;
  const commits = git('rev-list', '--reverse', '--topo-order', range).toString().trim().split('\n').filter(Boolean);
  for (const commit of commits) {
    const parents = git('show', '-s', '--format=%P', commit).toString().trim().split(' ').filter(Boolean);
    const currentEntry = entry(commit);
    const previous = parents.map(blob);
    // Historical commits without a record on either side predate adoption.
    if (!currentEntry && previous.every(b => b.length === 0)) continue;
    if (!/^100644 blob [0-9a-f]+\tPROMPTS\.md\n$/.test(currentEntry)) throw new Error(`${commit}: record must be a regular non-executable file.`);
    const current = blob(commit);
    for (const old of previous.length ? previous : [Buffer.alloc(0)]) {
      if (!current.subarray(0, old.length).equals(old)) throw new Error(`${commit}: changed or removed existing prompt bytes.`);
      if (!current.subarray(old.length).toString('utf8').trim()) throw new Error(`${commit}: missing non-whitespace prompt append.`);
    }
  }
  if (!entry(head)) throw new Error('Checked head has no PROMPTS.md; policy adoption is required.');
  console.log(`Prompt history checked: ${commits.length} commits (pre-adoption history exempt).`);
} catch (error) {
  console.error(`Prompt history check failed: ${error.message}`);
  process.exitCode = 1;
}
