import hashlib,json,os,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent.parent;O=P/'review/native';O.mkdir(parents=True,exist_ok=True)
real=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
 return {str(p.relative_to(real)):hashlib.sha256(p.read_bytes()).hexdigest() for p in real.rglob('*') if p.is_file() and p.suffix.lower()!='.log'} if real.exists() else {}
before=fingerprint();env=os.environ.copy();env['APPDATA']=str(P/'native/scratch-appdata');env['KRUSHER_NATIVE_OUTPUT']=str(O);start=time.monotonic();code=None
try:
 with (O/'engine.log').open('w',encoding='utf-8') as log:
  run=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(R),'--rendering-method','gl_compatibility','--resolution','960x600','-s','res://character/krusher-continuity-audit-v1/native/verify.gd'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=360);code=run.returncode
finally:
 after=fingerprint();changed=[q for q in set(before)|set(after) if before.get(q)!=after.get(q)];logtext=(O/'engine.log').read_text(errors='replace');logged=[s for s in logtext.splitlines() if 'SCRIPT ERROR' in s or s.startswith('ERROR:')]
 result={'engineExit':code,'seconds':round(time.monotonic()-start,2),'ownerFilesFingerprinted':len(before),'ownerFilesChanged':changed,'loggedErrors':logged[:8],'scratchAppData':env['APPDATA']};(O/'run-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
assert code==0 and not changed and not logged
report=json.loads((O/'report.json').read_text());print(json.dumps({'checks':report['checks'],'errors':report['errors'],'states':report['states'],'slots':report['slots']}));assert not report['errors']
