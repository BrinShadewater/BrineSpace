"""Run the Bill staged basic swim-turn fixture under scratch APPDATA and retain real-profile fingerprints."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/bill-death-water-south-candidate-native-v1';OUT.mkdir(exist_ok=True)
def fingerprint():
 profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {p.relative_to(profile).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file() and 'logs' not in p.relative_to(profile).parts}
def main():
 godot=Path(sys.argv[1]);assert godot.is_file()
 archive=OUT/f'interval-before-{time.time_ns()}'
 previous=[OUT/name for name in ['native.log','validation.json','profile-before.json','profile-after.json','loaded-water-carry.png'] if (OUT/name).exists()]
 if previous:
  archive.mkdir()
  for path in previous:shutil.copy2(path,archive/path.name)
 before=fingerprint();(OUT/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
 env=os.environ.copy();scratch=OUT/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
 command=[str(godot),'--path',str(ROOT),'--script','res://tests/test_bill_death_water_south_candidates.gd','--resolution','1280x900']
 started=time.monotonic();start_epoch=time.time()
 if (OUT/'native.log').exists():
  (OUT/f'native-before-{time.time_ns()}.log').write_bytes((OUT/'native.log').read_bytes())
 with (OUT/'native.log').open('w',encoding='utf-8') as log:
  try:result=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180);code=result.returncode
  except subprocess.TimeoutExpired:code=-1
 after=fingerprint();(OUT/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n',encoding='utf-8')
 changes=[name for name in before.keys()|after.keys() if before.get(name)!=after.get(name)]
 text=(OUT/'native.log').read_text(encoding='utf-8');passed=code==0 and '0 failures' in text and 'SCRIPT ERROR' not in text
 photo=OUT/'loaded-water-carry.png';fresh_photo=photo.exists() and photo.stat().st_mtime>=start_epoch
 passed=passed and not changes and fresh_photo
 report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-started,2),'scratchAPPDATA':str(scratch),'realProfileScope':'all non-log files','realProfileFileCount':len(before),'realProfileChanges':changes,'nativeScreenshot':fresh_photo}
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report));print('\n'.join(line for line in text.splitlines() if any(key in line for key in ['BILL DEATH','BILL WATER','SCRIPT ERROR','ERROR:',' at:']))[-2000:]);return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())
