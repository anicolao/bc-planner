import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtempSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
const script = fileURLToPath(new URL('./check-prompt-history.mjs', import.meta.url));
test('CI validates individual commits, adoption, deletion, and file modes', () => {
  const cwd = mkdtempSync(join(tmpdir(), 'prompt-history-'));
  const env = {...process.env};
  for (const k of Object.keys(env)) if (k.startsWith('GIT_')) delete env[k];
  env.XDG_CONFIG_HOME=join(cwd,'config');
  const git=(...args)=>execFileSync('git',args,{cwd,env,encoding:'utf8'}).trim();
  const commit=(text)=>{writeFileSync(join(cwd,'PROMPTS.md'),text);git('add','.');git('commit','-qm','fixture');return git('rev-parse','HEAD');};
  const check=(base,ok)=>{const r=spawnSync(process.execPath,[script,base,'HEAD'],{cwd,env,encoding:'utf8'});assert.equal(r.status===0,ok,r.stdout+r.stderr);};
  try {
    git('init','-q');git('config','user.name','Test');git('config','user.email','test@example.invalid');git('config','commit.gpgsign','false');
    git('commit','--allow-empty','-qm','pre-policy');const base=git('rev-parse','HEAD');
    check(base,false); const adoption=commit('first prompt\n');check(base,true);
    commit('first prompt\nsecond\n');check(base,true);
    git('commit','--allow-empty','-qm','missing prompt');commit('first prompt\nsecond\nthird\n');check(base,false);
    git('checkout','-q','-f','--detach',adoption);commit('rewritten\nappend\n');check(base,false);
    git('checkout','-q','-f','--detach',adoption);commit('first prompt\n \n');check(base,false);
    git('checkout','-q','-f','--detach',adoption);git('rm','PROMPTS.md');git('commit','-qm','deleted');check(base,false);
    git('checkout','-q','-f','--detach',adoption);writeFileSync(join(cwd,'PROMPTS.md'),'first prompt\nnext\n');git('add','.');git('update-index','--chmod=+x','PROMPTS.md');git('commit','-qm','executable');check(base,false);
    git('checkout','-q','-f','--detach',adoption);check('0'.repeat(40),true);
  } finally {rmSync(cwd,{recursive:true,force:true});}
});
