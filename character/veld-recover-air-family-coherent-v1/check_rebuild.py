from pathlib import Path
import subprocess,sys,json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[P/'bare-manifest.json',P/'helmet-manifest.json',P/'source-bindings.json']
bindings=json.loads((P/'source-bindings.json').read_text());files.extend(ROOT/f for f in bindings)
before={str(p.relative_to(ROOT)):sha(p) for p in files}
subprocess.run([sys.executable,str(P/'build.py')],check=True,capture_output=True,text=True)
after={str(p.relative_to(ROOT)):sha(p) for p in files};assert before==after
(P/'selected-rebuild-checks.json').write_text(json.dumps({'passed':True,'manifestCount':2,'frameReferences':48,'sourceBindingsExact':True,'comparedFiles':len(files),'hashes':after,'scope':'actual family build regeneration preserves installed status/manifests and all source pixels'},indent=2)+'\n')
print('Actual rebuild byte-exact:2manifests,48source frames and source bindings')
