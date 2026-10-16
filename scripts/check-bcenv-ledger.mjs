import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const kinds = new Set(['proposed', 'preregistered', 'started', 'artifact', 'deviation', 'decision', 'correction']);
const sha = /^[a-f0-9]{64}$/;
const commit = /^[a-f0-9]{40}$/;
const nonempty = value => typeof value === 'string' && value.trim().length > 0;
function requireFields(record, fields) {
  for (const field of fields) if (!nonempty(record[field])) throw Error(`missing text field: ${field}`);
}
function artifact(record) {
  requireFields(record, ['locator', 'sha256', 'producer', 'created_at', 'access']);
  if (!sha.test(record.sha256) || !Number.isFinite(Date.parse(record.created_at))) throw Error('invalid artifact hash/time');
}

export function validateLedger(text, previous = '') {
  if (!text.startsWith(previous)) throw Error('ledger is not an exact append of trusted base');
  if (!text.endsWith('\n')) throw Error('ledger must end with newline');
  const events = new Map();
  let lastTime = -Infinity;
  for (const [index, line] of text.slice(0, -1).split('\n').entries()) {
    try {
      const event = JSON.parse(line);
      const fields = ['event_id', 'experiment_id', 'recorded_at', 'kind', 'references', 'record', 'note'];
      if (Object.keys(event).length !== fields.length || fields.some(key => !(key in event))) throw Error('invalid envelope fields');
      if (!nonempty(event.event_id) || events.has(event.event_id)) throw Error('empty or duplicate event ID');
      if (!/^BCENV-[0-9]+$/.test(event.experiment_id) || !kinds.has(event.kind) || !nonempty(event.note)) throw Error('invalid event identity/kind/note');
      const time = Date.parse(event.recorded_at);
      if (typeof event.recorded_at !== 'string' || !event.recorded_at.endsWith('Z') || !Number.isFinite(time) || time < lastTime) throw Error('invalid or nonchronological UTC time');
      if (!Array.isArray(event.references) || new Set(event.references).size !== event.references.length) throw Error('invalid references');
      const refs = event.references.map(id => {
        const ref = events.get(id);
        if (!ref || ref.experiment_id !== event.experiment_id) throw Error('reference must name earlier event in same experiment');
        return ref;
      });
      const r = event.record;
      if (!r || typeof r !== 'object' || Array.isArray(r)) throw Error('record must be object');
      const need = kind => { if (!refs.some(ref => ref.kind === kind)) throw Error(`requires earlier ${kind} reference`); };
      switch (event.kind) {
        case 'proposed': requireFields(r, ['path', 'status']); break;
        case 'preregistered':
          need('proposed');
          requireFields(r, ['protocol_commit', 'protocol_path', 'protocol_sha256', 'rubric_sha256', 'authorization_reference', 'pins_review_reference', 'isolation_review_reference']);
          if (!commit.test(r.protocol_commit) || !sha.test(r.protocol_sha256) || !sha.test(r.rubric_sha256)) throw Error('invalid preregistration pins');
          break;
        case 'started': need('preregistered'); requireFields(r, ['run_id', 'arm', 'input_manifest_sha256']); if (!sha.test(r.input_manifest_sha256)) throw Error('invalid input manifest hash'); break;
        case 'artifact': need('started'); artifact(r); break;
        case 'deviation': requireFields(r, ['impact', 'handling']); if (!refs.length) throw Error('deviation requires affected event'); break;
        case 'decision':
          need('preregistered'); need('artifact');
          if (!['keep', 'reject', 'inconclusive'].includes(r.verdict)) throw Error('invalid verdict');
          requireFields(r, ['audit', 'mechanism', 'downstream', 'deviations', 'actual_cost', 'uncertainty', 'lessons', 'rationale']);
          break;
        case 'correction': if (!refs.length) throw Error('correction requires affected event'); requireFields(r, ['replacement_claim', 'reason']); break;
      }
      events.set(event.event_id, event);
      lastTime = time;
    } catch (error) { throw Error(`line ${index + 1}: ${error.message}`); }
  }
  return events.size;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const file = process.argv[2] ?? 'experiments/bcenv/ledger.jsonl';
    const base = process.argv[3];
    let previous = '';
    if (base) {
      // Reject unknown base revisions; a missing file is valid only for initial adoption.
      execFileSync('git', ['rev-parse', '--verify', `${base}^{commit}`], { stdio: 'pipe' });
      const files = execFileSync('git', ['ls-tree', '--name-only', base, '--', file], { encoding: 'utf8' });
      if (files.trim()) previous = execFileSync('git', ['show', `${base}:${file}`], { encoding: 'utf8' });
    }
    console.log(`Valid ledger: ${validateLedger(readFileSync(file, 'utf8'), previous)} events (${base ? 'trusted-base prefix checked' : 'structure only'}).`);
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
