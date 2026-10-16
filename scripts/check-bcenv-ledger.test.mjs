import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { validateLedger } from './check-bcenv-ledger.mjs';
const hash = 'a'.repeat(64);
const proposal = {event_id:'p', experiment_id:'BCENV-1', recorded_at:'2026-10-16T00:00:00Z',kind:'proposed',references:[],record:{path:'proposal.json',status:'unrun'},note:'test fixture; not actual results'};
const encode = events => events.map(e => JSON.stringify(e)).join('\n') + '\n';
const event = (id, kind, references, record) => ({...proposal,event_id:id,kind,references,record});
const prereg = event('pre','preregistered',['p'],{protocol_commit:'a'.repeat(40),protocol_path:'p.json',protocol_sha256:hash,rubric_sha256:hash,authorization_reference:'approval',pins_review_reference:'review',isolation_review_reference:'review'});
const started = event('run','started',['pre'],{run_id:'r1',arm:'baseline',input_manifest_sha256:hash});
const result = event('result','artifact',['run'],{locator:'immutable:test',sha256:hash,producer:'test',created_at:proposal.recorded_at,access:'private'});
const decision = event('end','decision',['pre','result'],{verdict:'inconclusive',audit:'ok',mechanism:'unknown',downstream:'unmeasured',deviations:'none',actual_cost:'test only',uncertainty:'high',lessons:'fixture',rationale:'fixture'});
test('valid lifecycle and exact append',()=>assert.equal(validateLedger(encode([proposal,prereg,started,result,decision]),encode([proposal])),5));
test('repository proposal and template remain unrun',()=>{
  assert.ok(validateLedger(readFileSync(new URL('../experiments/bcenv/ledger.jsonl',import.meta.url),'utf8')) >= 1);
  for (const path of ['templates/experiment.json','proposals/BCENV-001.json']) {
    const record = JSON.parse(readFileSync(new URL(`../experiments/bcenv/${path}`,import.meta.url),'utf8'));
    assert.equal(record.status,'proposal'); assert.equal(record.launch_gates.authorization_reference,null);
    assert.deepEqual(record.results.run_manifest,[]); assert.equal(record.decision.verdict,null);
  }
});
test('rewrite or deletion fails trusted prefix',()=>assert.throws(()=>validateLedger(encode([{...proposal,note:'rewritten'}]),encode([proposal])),/exact append/));
test('duplicate IDs fail',()=>assert.throws(()=>validateLedger(encode([proposal,proposal])),/duplicate/));
test('start without preregistration fails',()=>assert.throws(()=>validateLedger(encode([proposal,{...started,references:['p']}])),/preregistered/));
test('preregistration needs valid immutable pins',()=>assert.throws(()=>validateLedger(encode([proposal,{...prereg,record:{...prereg.record,protocol_commit:'main'}}])),/pins/));
test('decision without outcome artifact fails',()=>assert.throws(()=>validateLedger(encode([proposal,prereg,{...decision,references:['pre']}])),/artifact/));
test('cross-experiment and forward references fail',()=>{
  assert.throws(()=>validateLedger(encode([proposal,{...prereg,experiment_id:'BCENV-2'}])),/same experiment/);
  assert.throws(()=>validateLedger(encode([prereg,proposal])),/earlier/);
});
test('corrections preserve original',()=>assert.equal(validateLedger(encode([proposal,event('c','correction',['p'],{replacement_claim:'corrected observation',reason:'new evidence'})]),encode([proposal])),2));
test('bad hashes, costs, timestamps and missing newline fail',()=>{
 assert.throws(()=>validateLedger(encode([proposal,prereg,started,{...result,record:{...result.record,sha256:'bad'}}])),/hash/);
 assert.throws(()=>validateLedger(encode([proposal,prereg,started,result,{...decision,record:{...decision.record,actual_cost:''}}])),/actual_cost/);
 assert.throws(()=>validateLedger(encode([proposal,{...prereg,recorded_at:'2020-01-01T00:00:00Z'}])),/chronological/);
 assert.throws(()=>validateLedger(encode([proposal]).trimEnd()),/newline/);
});
