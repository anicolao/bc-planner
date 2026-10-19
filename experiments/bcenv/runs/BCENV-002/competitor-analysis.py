import json,pathlib,collections,sys
root=pathlib.Path('work')
version=sys.argv[1]
results=[]
for name in ['default-A','default-B','small-A','small-B']:
 side=name[-1];team=1 if side=='A' else 2
 records=[];coverage=[]
 for lo,hi in [(1,50),(51,100),(101,150)]:
  q=json.loads((root/f'query-{version}-{name}-{lo:03d}-{hi:03d}'/'replay-query.json').read_text())
  assert q['selected_records_complete'] and not q['truncated'] and q['source_stream_complete'] and all(m['all_requested_positive_rounds_present'] for m in q['matches'])
  records.extend(q['records']);coverage.append({'range':[lo,hi],'records':q['returned_record_count'],'sha256':q['source_replay'].get('sha256')})
 counts=collections.Counter();positions=collections.defaultdict(dict); examples=[]
 for r in records:
  if r['kind']=='movement' and r['body_type']=='LAUNCHER':positions[r['round']][r['robot_id']]=r
  if r.get('team_id')==team:
   if r['kind']=='spawn':counts['spawn_'+r['body_type']]+=1
   if r['kind']=='death':counts['death_'+str(r['body_type'])]+=1
   if r['kind']=='action':counts[r['action']]+=1
 for roundnum,pos in sorted(positions.items()):
  for rid,r in pos.items():
   if r['team_id']!=team:continue
   enemies=[e for e in pos.values() if e['team_id']!=team]
   if not enemies:continue
   e=min(enemies,key=lambda e:(r['x']-e['x'])**2+(r['y']-e['y'])**2)
   d=(r['x']-e['x'])**2+(r['y']-e['y'])**2
   if d<=20:
    counts['launcher_geometric_engagement_observations']+=1
    if d<=8:
     counts['launcher_close_observations']+=1
     if len(examples)<10:examples.append({'round':roundnum,'candidate':rid,'opponent':e['robot_id'],'distance_squared':d,'event_index':r['event_index'],'candidate_row':r['row_index'],'opponent_row':e['row_index']})
 m=json.loads((root/f'{version}-{name}'/'replay-summary.json').read_text())['matches'][0]
 result=json.loads((root/f'{version}-{name}'/'result.json').read_text())
 row={'condition':name,'candidate_slot':side,'win':result['winner']==side,'total_rounds':m['total_rounds'],'first150':dict(counts),'close_fraction':counts['launcher_close_observations']/max(1,counts['launcher_geometric_engagement_observations']),'close_examples':examples,'coverage':coverage}
 results.append(row)
out={'version':version,'fixed_round_window':[1,150],'metric_semantics':'Geometric recorded position observations, not reconstructed visibility, attack success, damage, or causal combat attribution. Distances use records of each round without inferring vector execution order. Deaths include all causes.','conditions':results}
(root/f'{version}-analysis.json').write_text(json.dumps(out,indent=2)+'\n')
for r in results:print(r['condition'],'win',r['win'],'rounds',r['total_rounds'],'close',r['first150'].get('launcher_close_observations',0),'/',r['first150'].get('launcher_geometric_engagement_observations',0),'fraction',round(r['close_fraction'],4),'launcherDeaths',r['first150'].get('death_LAUNCHER',0),'launchAttacks',r['first150'].get('LAUNCH_ATTACK',0),'examples',r['close_examples'][:2])
