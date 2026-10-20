import pathlib,subprocess,json,time,argparse
p=argparse.ArgumentParser()
p.add_argument("--root",required=True)
p.add_argument("--evidence-dir",default=str(pathlib.Path(__file__).resolve().parents[1]))
p.add_argument("--execute",action="store_true")
a=p.parse_args()
if not a.execute:p.error("Execution requires explicit --execute and a separately authorized game budget")
evidence=pathlib.Path(a.evidence_dir).resolve()
out=pathlib.Path(a.root).resolve();catalog=json.loads((evidence/'bc23-public-source-catalog.json').read_text());results=[]
# Fail closed after any prior invocation, including a partial run.
with (out/'.execution-started').open('x') as guard:guard.write('Public smoke reproduction started. Do not remove to retry.\n')
builds=[]
for c in catalog['candidates']:
 key=c['catalogKey'];target='work/build-'+key
 cmd=[str(out/'bcenv'),'build','--source','public-sources/'+key+'/java','--package',c['package'],'--output',target,'--timeout','120']
 p=subprocess.run(cmd,capture_output=True,text=True);(out/('build-'+key+'-launcher.log')).write_text(p.stdout+p.stderr)
 artifact=out/'root/workspace'/target/'artifact.json';data=json.loads(artifact.read_text()) if artifact.exists() else {}
 builds.append({'candidate':key,'status':data.get('status','launcher-failure'),'returncode':p.returncode})
 (out/'build-summary.json').write_text(json.dumps(builds,indent=2)+'\n')
verified={r['candidate'] for r in json.loads((out/'build-summary.json').read_text()) if r['status']=='verified'}
assert 'lectureplayer' in verified
schedule=[('lectureplayer','A','lectureplayer','lectureplayer')]
for c in catalog['candidates']:
 key=c['catalogKey']
 if key=='lectureplayer' or key not in verified:continue
 schedule.extend([(key,'A',key,'lectureplayer'),(key,'B','lectureplayer',key)])
assert len(schedule)<=12
for key,side,a,b in schedule:
 match=f'smoke-{key}-{side}';cmd=[str(out/'bcenv'),'run','--team-a','work/build-'+a,'--team-b','work/build-'+b,'--map','/opt/battlecode23/maps/DefaultMap.map23','--output','work/'+match,'--timeout','120']
 start=time.time();p=subprocess.run(cmd,capture_output=True,text=True)
 (out/(match+'-launcher.log')).write_text(p.stdout+p.stderr)
 path=out/'root/workspace/work'/match/'result.json';artifact=json.loads(path.read_text()) if path.exists() else {}
 summary=out/'root/workspace/work'/match/'replay-summary.json';replay=json.loads(summary.read_text()) if summary.exists() else {}
 result={'candidate':key,'side':side,'returncode':p.returncode,'elapsedSeconds':time.time()-start,'status':artifact.get('status','launcher-failure'),'resultPath':str(path.relative_to(out)) if path.exists() else None,'replaySummaryPath':str(summary.relative_to(out)) if summary.exists() else None,'engineSha256':artifact.get('engine_sha256'),'mapSha256':artifact.get('map_sha256'),'replaySha256':artifact.get('replay',{}).get('sha256')}
 results.append(result);(out/'match-summary.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(result),flush=True)
