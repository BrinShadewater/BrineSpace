"""Verify the real local authoring builder reproduces candidate assets byte-exact."""
from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[P/'bare-manifest.json',P/'helmet-manifest.json']+sorted((P/'frames').rglob('*.png'))
before={f.relative_to(P).as_posix():sha(f) for f in files}
subprocess.run([sys.executable,str(P/'build.py')],check=True,stdout=subprocess.PIPE,text=True)
after={f.relative_to(P).as_posix():sha(f) for f in files}
assert before==after,'Builder altered candidate pixels or metadata'
(P/'rebuild-checks.json').write_text(json.dumps({'passed':True,'files':len(files),'manifestCount':2,'frameCount':12,'sha256':after,'scope':'actual deterministic local rebuild; no generation/runtime selection'},indent=2)+'\n')
print('2manifests/12frames actual local rebuild byte-exact')
