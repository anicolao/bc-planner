import pathlib,json,shutil,hashlib,argparse
p=argparse.ArgumentParser()
p.add_argument("--store-root",required=True)
p.add_argument("--destination",required=True)
p.add_argument("--evidence-dir",default=str(pathlib.Path(__file__).resolve().parents[1]))
a=p.parse_args();evidence=pathlib.Path(a.evidence_dir).resolve();record=json.loads((evidence/"smoke-manifest.json").read_text())
srcroot=pathlib.Path(a.store_root).resolve()
out=pathlib.Path(a.destination).resolve();out.mkdir(exist_ok=False)
root=out/'root';(root/'nix/store').mkdir(parents=True);(root/'tmp').mkdir();(root/'dev').mkdir();(root/'dev/null').touch();(root/'workspace/work').mkdir(parents=True)
paths=record['runtime']
closure=record['closure']
for path in closure:
 p=pathlib.Path(path)
 assert path.startswith('/nix/store/') and len(p.parts)==4
 shutil.copytree(srcroot/path.lstrip('/'),root/path.lstrip('/'),symlinks=True)
engine=srcroot/paths['engine'].lstrip('/')/'share/battlecode23';adapter=srcroot/paths['adapter'].lstrip('/')/'lib/bcenv'
(root/'opt/bcenv/seasons/2023').mkdir(parents=True)
shutil.copytree(engine,root/'opt/battlecode23');shutil.copytree(adapter/'runtime',root/'opt/bcenv/runtime');shutil.copytree(adapter/'replay-classes',root/'opt/bcenv/replay-classes');shutil.copyfile(adapter/'seasons/2023/adapter.py',root/'opt/bcenv/seasons/2023/adapter.py')
catalog=json.loads((evidence/'bc23-public-source-catalog.json').read_text())
for c in catalog['candidates']:
 base=root/'workspace/public-sources'/c['catalogKey'];(base/'java').mkdir(parents=True)
 source=srcroot/c['sourceStorePath'].lstrip('/')
 shutil.copyfile(source/'LICENSE',base/'LICENSE');assert hashlib.sha256((base/'LICENSE').read_bytes()).hexdigest()==c['licenseSha256']
 for f in c['sourceFiles']:
  sourcepath=source/'src'/f['path'];target=base/'java'/f['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(sourcepath,target)
  assert hashlib.sha256(target.read_bytes()).hexdigest()==f['sha256']
 (base/'provenance.json').write_text(json.dumps(c,indent=2)+'\n')
(root/'opt/launch.py').write_text('import os,sys\nos.chdir("/workspace")\nos.environ.update('+repr({'HOME':'/workspace','BCENV_ENGINE_JAR':'/opt/battlecode23/engine.jar','BCENV_JAVA':paths['jdk']+'/bin/java','BCENV_JAVAC':paths['jdk']+'/bin/javac','BCENV_REPLAY_CLASSPATH':'/opt/bcenv/replay-classes:/opt/battlecode23/engine.jar'})+')\nos.execv('+repr(paths['python']+'/bin/python3')+',['+repr(paths['python']+'/bin/python3')+',"/opt/bcenv/seasons/2023/adapter.py"]+sys.argv[1:])\n')
(out/'bcenv').write_text('#!/bin/sh\nset -eu\nHERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)\nexec env -i PATH=/usr/sbin:/usr/bin:/bin LANG=C /usr/bin/unshare --user --map-root-user --net -- /usr/sbin/chroot "$HERE/root" '+paths['python']+'/bin/python3 /opt/launch.py "$@"\n');(out/'bcenv').chmod(0o755)
manifest={'schema':'bc23.public-compatibility-smoke.v1','purpose':'Public-source build/verifier/activity smoke only; no strength ranking','runtime':paths,'closure':closure,'isolation':'env -i; user/network namespace; chroot; no host binds','sourceCatalogSha256':hashlib.sha256((evidence/'bc23-public-source-catalog.json').read_bytes()).hexdigest(),'map':'DefaultMap','maxMatches':12,'scope':'One lecture self-play sanity match plus two side positions for each of five other packages versus lectureplayer. No strategy edits.','caveats':['Robot stdout is disabled by the unmodified adapter, so absence of exceptions cannot be established from suppressed logs.','Historical team placement does not authenticate exact server submissions.']}
(out/'smoke-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(out)
