import pathlib,json,subprocess,collections,hashlib,argparse
p=argparse.ArgumentParser();p.add_argument("--root",required=True);a=p.parse_args()
out=pathlib.Path(a.root).resolve();summary=json.loads((out/'match-summary.json').read_text());rows=[]
for m in summary:
 name='smoke-'+m['candidate']+'-'+m['side'];base=out/'root/workspace/work'/name;qout='work/query-'+name;query=out/'root/workspace'/qout/'replay-query.json'
 if m['status']!='completed':continue
 if not query.exists():
  cmd=[str(out/'bcenv'),'replay','query','--replay','work/'+name+'/replay.bc23','--round-start','1','--round-end','50','--limit','10000','--output',qout,'--timeout','120']
  p=subprocess.run(cmd,capture_output=True,text=True);(out/('query-'+name+'-launcher.log')).write_text(p.stdout+p.stderr)
  if p.returncode:rows.append({'match':name,'query_failure':p.returncode});continue
 q=json.loads(query.read_text());assert q['status']=='complete' and q['source_stream_complete'] and q['selected_records_complete'];assert q['matches'][0]['all_requested_positive_rounds_present']
 teams={}
 for team in [1,2]:
  records=[r for r in q['records'] if r.get('team_id')==team];actions=collections.Counter(r['action'] for r in records if r['kind']=='action');spawns=collections.Counter(r['body_type'] for r in records if r['kind']=='spawn')
  teams['A' if team==1 else 'B']={'spawn_count':sum(spawns.values()),'spawns_by_type':dict(spawns),'action_counts':dict(actions)}
 r={'match':name,'candidate':m['candidate'],'candidateSide':m['side'],'roundRange':[1,50],'queryReturnedRows':q['returned_record_count'],'queryComplete':True,'teams':teams,'querySha256':hashlib.sha256(query.read_bytes()).hexdigest(),'queryPath':str(query.relative_to(out))};rows.append(r)
 print(json.dumps({'match':name,'candidateActivity':teams[m['side']],'queryComplete':True}),flush=True)
(out/'activity-summary.json').write_text(json.dumps(rows,indent=2)+'\n')
