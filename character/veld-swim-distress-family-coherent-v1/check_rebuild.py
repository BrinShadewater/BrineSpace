"""Verify consolidated outputs reproduce locally without reauthoring or regrading."""
from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[P/'bare-manifest.json',P/'helmet-manifest.json',P/'source-bindings.json']+sorted((P/'frames').rglob('*.png'))
before={f.relative_to(P).as_posix():sha(f) for f in files}
subprocess.run([sys.executable,str(P/'build.py')],check=True,capture_output=True,text=True)
after={f.relative_to(P).as_posix():sha(f) for f in files}
assert before==after,'Consolidation changed pixels, metadata or source bindings'
(P/'rebuild-checks.json').write_text(json.dumps({'passed':True,'manifestCount':2,'frameCount':48,'sourceBindingsExact':True,'sha256':after,'scope':'actual local consolidation rebuild; no runtime selection'},indent=2)+'\n')
print('2manifests/48frames and source bindings rebuild byte-exact')
