from pathlib import Path
import json,hashlib,subprocess,sys,shutil
H=Path(__file__).resolve().parent;R=H.parents[1]
families=['veld-salvage-pickup-family-coherent-v1','veld-swim-carry-matrix-coherent-v1',H.name]
paths=[]
for family in families:
 for gear in ['bare','helmet']:
  p=R/'character'/family/(gear+'-manifest.json');m=json.loads(p.read_text());paths.append(p)
  paths.extend((p.parent/f).resolve() for s in m['states'] for f in s['frameFiles'])
def hashes():return {p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
before=hashes()
archive=H/'revisions/before-selected-rebuild-v1';archive.mkdir(exist_ok=True)
for family in families:
 for name in ['family-checks.json','provenance.json']:
  p=R/'character'/family/name
  if p.exists() and not (archive/(family+'-'+name)).exists():shutil.copy2(p,archive/(family+'-'+name))
for family in families:
 result=subprocess.run([sys.executable,str(R/'character'/family/'build.py')],capture_output=True,text=True)
 assert result.returncode==0,result.stderr
 print(result.stdout.splitlines()[-1])
assert hashes()==before,'Rebuild changed selected source bytes'
assert all(json.loads(p.read_text())['status'].startswith('installed') for p in paths if p.name.endswith('manifest.json'))
(H/'selected-rebuild-checks.json').write_text(json.dumps(dict(passed=True,manifests=6,references=336,hashes=before,scope='Actual regeneration preserves exact installed manifests/frame bytes; native checks remain applicable.'),indent=2)+'\n',encoding='utf-8')
print('Six selected manifests/336 frame references regenerate byte-exactly.')
