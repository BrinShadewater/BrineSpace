from pathlib import Path
import os,sys,json,hashlib,subprocess,time
R=Path(__file__).resolve().parent.parent;O=R/'output/bill-land-water-title-checkpoint-west-v1';O.mkdir(exist_ok=True)
def fingerprint():
 p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {f.relative_to(p).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file() and 'logs' not in f.relative_to(p).parts}
before=fingerprint();(O/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
env=os.environ.copy();scratch=O/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
godot=Path(sys.argv[1]);assert godot.is_file();intervals=[]
for name in ['seal','bare-81','bare-432','helmet-81','helmet-432']:
 cmd=[str(godot),'--path',str(R)]
 if name=='seal':cmd+=['--headless','--script','res://character/bill-land-water-material-west-v3/seal_title_checkpoints.gd']
 else:cmd+=['--script','res://tests/test_bill_land_water_title_checkpoint_west_v1.gd','--resolution','1280x900','--',name]
 log=O/(name+'.log');started=time.monotonic();epoch=time.time()
 with log.open('w',encoding='utf-8') as f:
  try:code=subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,timeout=180).returncode
  except subprocess.TimeoutExpired:code=-1
 text=log.read_text(encoding='utf-8');passed=code==0 and 'SCRIPT ERROR' not in text and 'ERROR:' not in text and ('BILL TITLE CHECKPOINT SEAL:' in text if name=='seal' else 'BILL LAND WATER TITLE CHECKPOINT WEST V1:' in text and '0 failures' in text)
 record={'name':name,'returnCode':code,'seconds':round(time.monotonic()-started,2),'passed':passed,'nativeScreenshot':False}
 if name!='seal':
  image=O/f'{name}-title-future-candidate-room.png';record['nativeScreenshot']=image.exists() and image.stat().st_mtime>=epoch;record['passed']=passed and record['nativeScreenshot']
 intervals.append(record);print(json.dumps(record),flush=True)
 if not record['passed']:
  print('\n'.join(x for x in text.splitlines() if any(k in x for k in ['SCRIPT ERROR','ERROR:',' at:','BILL ']))[-2200:],flush=True);break
after=fingerprint();(O/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
changes=[f for f in before.keys()|after.keys() if before.get(f)!=after.get(f)]
report={'passed':len(intervals)==5 and all(x['passed'] for x in intervals) and not changes,'intervals':intervals,'scratchAPPDATA':str(scratch),'realProfileFileCount':len(before),'realProfileChanges':changes,'scope':'Sealing plus four independent native processes, each actual title/loading Continue callbacks and normal checksum pending restore, staged fixture gate/source/view admission. Not production installation.'}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'passed':report['passed'],'ownerFiles':len(before),'ownerChanges':changes}),flush=True)
raise SystemExit(0 if report['passed'] else 1)
