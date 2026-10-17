from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
files=[P/f for f in ['bare-manifest.json','helmet-manifest.json','all-cardinal-poses.png','station-scale-contact.png']]
def fingerprint():return {f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
a=fingerprint();subprocess.run([sys.executable,str(P/'build.py')],check=True,stdout=subprocess.PIPE,text=True);b=fingerprint();assert a==b
(P/'rebuild-checks.json').write_text(json.dumps({'passed':True,'files':b,'scope':'actual family manifest/board rebuild; referenced frames unchanged, not actual NPC routing'},indent=2)+'\n',encoding='utf-8')
print('2family manifests/2pose boards actual rebuild byte-exact')
