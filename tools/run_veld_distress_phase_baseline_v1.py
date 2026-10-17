"""Scoped native corridor/retreat regressions with isolated profiles and owner fingerprints."""
from pathlib import Path
import os,sys,hashlib,json,subprocess,time
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-distress-phase-baseline-v1'
TESTS=[('test_veld_walk_integration.gd','VELD WALK INTEGRATION'),('test_crew_swim_packs.gd','CREW SWIM PACKS'),('test_carry_turn_handoff.gd','CREW TURN HANDOFF')]
def fingerprint():
 p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {f.relative_to(p).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file() and 'logs' not in f.relative_to(p).parts}
def main():
 O.mkdir(exist_ok=True);before=fingerprint();(O/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8');results=[]
 for name,marker in TESTS:
  env=os.environ.copy();scratch=O/'scratch-appdata'/Path(name).stem;scratch.mkdir(parents=True,exist_ok=True);env['APPDATA']=str(scratch)
  log=O/(name+'.log');started=time.monotonic()
  with log.open('w',encoding='utf-8') as stream:
   try:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://output/veld-distress-phase-regressions-v1/baseline/'+name,'--resolution','1280x900'],env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=180).returncode
   except subprocess.TimeoutExpired:code=-1
  text=log.read_text(encoding='utf-8');result={'test':name,'passed':code==0 and marker in text and 'ERROR:' not in text,'returnCode':code,'seconds':round(time.monotonic()-started,2),'logSha256':hashlib.sha256(log.read_bytes()).hexdigest()};results.append(result);print(json.dumps(result),flush=True)
 after=fingerprint();(O/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n',encoding='utf-8');changes=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
 report={'passed':all(r['passed'] for r in results) and not changes,'results':results,'realProfileFileCount':len(before),'realProfileChanges':changes}
 (O/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
