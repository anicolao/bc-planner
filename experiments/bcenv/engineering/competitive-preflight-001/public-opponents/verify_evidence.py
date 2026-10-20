"""Offline metadata verification only. Never launches a compiler, bot or engine."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for line in (root/'SHA256SUMS').read_text().splitlines():
 digest,name=line.split('  ',1);p=root/name
 assert p.is_file() and sha(p)==digest,name
catalog=json.loads((root/'bc23-public-source-catalog.json').read_text());expected={c['catalogKey']:c for c in catalog['candidates']}
assert len(expected)==6 and sum(len(c['sourceFiles']) for c in expected.values())==89
for key,c in expected.items():
 assert sha(root/'licenses'/(key+'-LICENSE'))==c['licenseSha256']
 base=root/'metadata'/('build-'+key);a=json.loads((base/'artifact.json').read_text())
 assert a['status']=='verified' and a['package']==c['package']
 assert a['source_files']=={f['path']:f['sha256'] for f in c['sourceFiles']}
 assert c['verification']['sourceSha256']==a['source_sha256']
 assert c['verification']['binarySha256']==a['binary_sha256']
 assert c['verification']['artifactSha256']==sha(base/'artifact.json')
 for step in a['steps']:
  assert step['status']=='succeeded' and step['exit_code']==0
  assert sha(base/step['log'])==step['log_sha256']
 limits=catalog['correctedServiceLimits'];m=c['metrics']
 assert m['file_count']<=limits['files'] and m['largest_file']['bytes']<=limits['maxFileBytes']
 assert m['total_source_bytes']<=limits['totalSourceBytes'] and m['zip_bytes']<=limits['archiveBytes']
 assert m['largest_member_compression_ratio']['ratio']<=limits['maxMemberCompressionRatio']
matches=json.loads((root/'match-summary.json').read_text());completed=0;failed=[]
for m in matches:
 base=root/'metadata'/('smoke-'+m['candidate']+'-'+m['side']);r=json.loads((base/'result.json').read_text())
 assert r['status']==m['status'] and r['engine_version']=='3.0.13'
 assert r['engine_sha256']==m['engineSha256'] and r['map_sha256']==m['mapSha256']
 assert sha(base/r['process']['log'])==r['process']['log_sha256']
 assert r['teams'][m['side']]['package']==expected[m['candidate']]['package']
 if r['status']=='completed':
  completed+=1;s=json.loads((base/'replay-summary.json').read_text())
  assert sha(base/'replay-summary.json')==r['replay']['summary_sha256']
  assert s['status']=='complete' and s['spec_version']=='3.0.13' and s['game_footer_present']
  for match in s['matches']:
   assert all(match[k] for k in ['match_footer_present','round_ids_contiguous','round_records_cover_reported_rounds','resource_records_cover_observed_rounds'])
 else:
  failed.append((m['candidate'],m['side'],r['status']))
  assert r['process']['status']=='timeout' and r['process']['exit_code']==-9
assert len(matches)==11 and completed==10 and failed==[('no_thoughts','A','timeout')]
activity=json.loads((root/'activity-summary.json').read_text());assert len(activity)==10
for q in activity:
 assert q['queryComplete'];t=q['teams'][q['candidateSide']]
 assert t['spawn_count']>0 and t['action_counts'].get('PICK_UP_RESOURCE',0)>0
 if q['candidate']!='lectureplayer':assert t['action_counts'].get('LAUNCH_ATTACK',0)>0
print('Verified compact metadata: 6 build/verifier passes, 10 complete games, 1 preserved timeout; no game executed.')
