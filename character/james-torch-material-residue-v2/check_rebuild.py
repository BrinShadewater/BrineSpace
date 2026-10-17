from pathlib import Path
import hashlib,subprocess,json,sys
P=Path(__file__).resolve().parent
files=list((P/'frames').rglob('*.png'))+[P/'bare-manifest.json',P/'helmet-manifest.json',P/'material-config.json']
before={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
with (P/'rebuild.log').open('w') as log:subprocess.run([sys.executable,str(P/'build.py')],check=True,stdout=log,stderr=subprocess.STDOUT)
after={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files};assert before==after
e={'files':len(files),'byteIdentical':True,'frozenSourceReferences':696};(P/'rebuild-evidence.json').write_text(json.dumps(e,indent=2)+'\n');print(json.dumps(e))
