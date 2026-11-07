"""Run normal-loader bunk cases serially with frozen inputs and scratch APPDATA."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil,re
R=Path(__file__).resolve().parent.parent
P=R/'character/veld-bunk-selected-v1';O=R/'output/veld-bunk-selected-native-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fingerprint():
 profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {p.relative_to(profile).as_posix():sha(p) for p in profile.rglob('*') if p.is_file() and 'logs' not in p.relative_to(profile).parts}
def main():
 godot=Path(sys.argv[1]);assert godot.is_file();O.mkdir(exist_ok=True)
 specs=json.loads((P/'native-suites.json').read_text());epoch=time.time();start=time.monotonic()
 prior=[p for p in O.iterdir() if p.is_file()]
 if prior:
  archive=O/f'interval-before-{time.time_ns()}';archive.mkdir()
  for p in prior:shutil.copy2(p,archive/p.name)
 files=[R/'scripts'/name for name in ['grid_canvas.gd','veld_npc.gd','veld_death_motion.gd','crew_life.gd','run_save.gd','crew_sprite_player.gd','room_flooding.gd']]
 files+=[R/'character/ACTIVE_ASSETS.json',P/'native-suites.json',Path(__file__).resolve()]
 files+=[R/'tests'/(s['test']+'.gd') for s in specs]
 for folder in ['veld-bunk-body-master-v1','veld-bunk-early-fall-v1']:
  root=R/'character'/folder;files+=list((root/'frames').rglob('*.png'))
  files+=[root/'bare-manifest.json',root/'helmet-manifest.json']
 before={p.relative_to(R).as_posix():sha(p) for p in files};(O/'inputs-before.json').write_text(json.dumps(before,indent=2)+'\n')
 profile_before=fingerprint();(O/'profile-before.json').write_text(json.dumps(profile_before,indent=2)+'\n')
 env=os.environ.copy();scratch=O/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
 results=[]
 for spec in specs:
  out=R/'output'/spec['output'];out.mkdir(exist_ok=True)
  prior=[p for p in out.iterdir() if p.is_file()]
  if prior:
   archive=out/f'interval-before-{time.time_ns()}';archive.mkdir()
   for p in prior:shutil.copy2(p,archive/p.name)
  suite_started=time.monotonic();suite_epoch=time.time()
  with (out/'native.log').open('w',encoding='utf-8') as log:
   try:code=subprocess.run([str(godot),'--path',str(R),'--script','res://tests/'+spec['test']+'.gd','--resolution','1280x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=spec['timeout']).returncode
   except subprocess.TimeoutExpired:code=-1
  text=(out/'native.log').read_text(encoding='utf-8');record=out/'records.json'
  passed=code==0 and spec['success'] in text and not any(e in text for e in ['SCRIPT ERROR','ERROR:','Artwork unavailable:']) and record.exists() and record.stat().st_mtime>=suite_epoch
  counts=re.findall(r'VELD [^\n]*?: (\d+) checks,(\d+) failures;',text)
  result={**spec,'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-suite_started,2),'checks':int(counts[-1][0]) if counts else None,'failures':int(counts[-1][1]) if counts else None}
  results.append(result);(O/'progress.json').write_text(json.dumps(results,indent=2)+'\n')
  print(json.dumps(result),flush=True)
  if not passed:
   print('\n'.join(x for x in text.splitlines() if any(k in x for k in ['SCRIPT ERROR','ERROR:',' at:']))[-2200:],flush=True);break
 after={p.relative_to(R).as_posix():sha(p) for p in files};profile_after=fingerprint()
 (O/'inputs-after.json').write_text(json.dumps(after,indent=2)+'\n');(O/'profile-after.json').write_text(json.dumps(profile_after,indent=2)+'\n')
 changes=sorted(k for k in profile_before.keys()|profile_after.keys() if profile_before.get(k)!=profile_after.get(k))
 report={'passed':len(results)==len(specs) and all(s['passed'] for s in results) and before==after and not changes,'suites':results,'targetedInputsUnchanged':before==after,'targetedInputCount':len(before),'realProfileFileCount':len(profile_before),'realProfileChanges':changes,'scratchAPPDATA':str(scratch),'seconds':round(time.monotonic()-start,2),'normalLoaderOnly':True}
 (O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='suites'}),flush=True)
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
