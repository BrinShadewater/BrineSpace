"""Validate current staged Bill West water bridges under scratch APPDATA."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/bill-land-water-material-west-v6';OUT.mkdir(exist_ok=True)
def fingerprint():
 profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {p.relative_to(profile).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file() and 'logs' not in p.relative_to(profile).parts}
def targeted_fingerprint():
 paths=json.loads((ROOT/'character/bill-land-water-material-west-v6/input-paths.json').read_text(encoding='utf-8'))
 return {name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in paths}
def main():
 godot=Path(sys.argv[1]);assert godot.is_file()
 archive=OUT/f'interval-before-{time.time_ns()}'
 previous=[OUT/name for name in ['native.log','validation.json','profile-before.json','profile-after.json','helmet-459-candidate-room.png','records.json','targeted-before.json','targeted-after.json','bare-diagnosis.json','helmet-diagnosis.json','bare-route.json','helmet-route.json'] if (OUT/name).exists()]
 if previous:
  archive.mkdir()
  for path in previous:shutil.copy2(path,archive/path.name)
 targeted_before=targeted_fingerprint();(OUT/'targeted-before.json').write_text(json.dumps(targeted_before,indent=2)+'\n',encoding='utf-8')
 before=fingerprint();(OUT/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
 env=os.environ.copy();scratch=OUT/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
 command=[str(godot),'--path',str(ROOT),'--script','res://tests/test_bill_land_water_material_west_v6.gd','--resolution','1280x900']
 if "--one-case" in sys.argv:command.extend(["--","--one-case"])
 started=time.monotonic();start_epoch=time.time()
 if (OUT/'native.log').exists():
  (OUT/f'native-before-{time.time_ns()}.log').write_bytes((OUT/'native.log').read_bytes())
 with (OUT/'native.log').open('w',encoding='utf-8') as log:
  try:result=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=480);code=result.returncode
  except subprocess.TimeoutExpired:code=-1
 targeted_after=targeted_fingerprint();(OUT/'targeted-after.json').write_text(json.dumps(targeted_after,indent=2)+'\n',encoding='utf-8')
 targeted_changes=[name for name in targeted_before.keys()|targeted_after.keys() if targeted_before.get(name)!=targeted_after.get(name)]
 after=fingerprint();(OUT/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n',encoding='utf-8')
 changes=[name for name in before.keys()|after.keys() if before.get(name)!=after.get(name)]
 text=(OUT/'native.log').read_text(encoding='utf-8');passed=code==0 and 'BILL LAND WATER MATERIAL WEST V6:' in text and '0 failures' in text and 'SCRIPT ERROR' not in text and 'ERROR:' not in text and 'Artwork unavailable:' not in text
 photo=OUT/'helmet-459-candidate-room.png';fresh_photo=photo.exists() and photo.stat().st_mtime>=start_epoch
 capture_passed=passed and fresh_photo
 passed=capture_passed and not changes and not targeted_changes
 report={'capturePassed':capture_passed,'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-started,2),'scratchAPPDATA':str(scratch),'realProfileScope':'all non-log files','realProfileFileCount':len(before),'realProfileChanges':changes,'nativeScreenshot':fresh_photo,'targetedInputCount':len(targeted_before),'targetedChanges':targeted_changes}
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(report));print('\n'.join(line for line in text.splitlines() if any(key in line for key in ['BILL CARRY RETURN EAST','BILL WATER','SCRIPT ERROR','ERROR:',' at:']))[-2000:]);return 0 if passed else 1
if __name__=='__main__':raise SystemExit(main())


