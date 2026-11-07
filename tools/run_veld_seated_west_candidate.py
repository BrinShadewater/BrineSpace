"""Native selected proof with isolated APPDATA and complete non-log fingerprint."""
from pathlib import Path
import os,sys,json,hashlib,subprocess,time,shutil
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-seated-west-candidate-v1'
def fingerprint():
 p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {f.relative_to(p).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file() and 'logs' not in f.relative_to(p).parts}
def main():
 O.mkdir(exist_ok=True); prior=[O/f for f in ['native.log','validation.json','profile-before.json','profile-after.json','native.png'] if (O/f).exists()]
 if prior:
  archive=O/f'interval-{time.time_ns()}';archive.mkdir()
  for f in prior:shutil.move(str(f),str(archive/f.name))
 before=fingerprint();(O/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
 env=os.environ.copy();scratch=O/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
 started=time.monotonic()
 with (O/'native.log').open('w',encoding='utf-8') as log:
  try:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_seated_west_candidate.gd','--resolution','1280x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
  except subprocess.TimeoutExpired:code=-1
 after=fingerprint();(O/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
 changes=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
 text=(O/'native.log').read_text(encoding='utf-8');passed=code==0 and '0 failures' in text and 'ERROR:' not in text and not changes and (O/'native.png').exists()
 result={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-started,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'scratchAPPDATA':str(scratch),'normalLoader':False,'scope':'candidate seated paired pixels/clocks/exact reverse/snapshot admission/native148-82; candidate override in normal player, controlled Veld actor interruption hook; no normal selection/furniture/world service-loss/Continue proof'}
 (O/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result));print('\n'.join(s for s in text.splitlines() if any(k in s for k in ['VELD SEATED WEST CANDIDATE','ERROR:',' at:']))[-2200:])
 return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())



