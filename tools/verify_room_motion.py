"""Scoped animation checks with isolated Godot profiles and owner fingerprints."""
import datetime, hashlib, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/('room-motion-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
OUT.mkdir(parents=True)
OWNER=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {p.relative_to(OWNER).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in OWNER.rglob('*') if p.is_file()}
before=fingerprint();(OUT/'owner-before.json').write_text(json.dumps(before))
env=os.environ.copy();env['APPDATA']=str(OUT/'scratch/roaming');env['LOCALAPPDATA']=str(OUT/'scratch/local')
Path(env['APPDATA']).mkdir(parents=True);Path(env['LOCALAPPDATA']).mkdir(parents=True)
godot='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe'
uid=OUT/'uids.gd'
uid.write_text('extends SceneTree\nfunc _initialize():\n\tfor path in ["res://scripts/ambient_fronds.gd","res://scripts/room_transition_art.gd","res://tests/test_room_transition_art.gd","res://tests/preview_room_transitions.gd","res://tests/test_room_transition_integration.gd"]:\n\t\tif not FileAccess.file_exists(path+".uid"):\n\t\t\tFileAccess.open(path+".uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")\n\tquit()\n')
jobs=[('uids',['--headless','-s',str(uid)],''),
      ('logic',['--headless','-s','res://tests/test_room_transition_art.gd'],'ROOM TRANSITIONS: 0 failures'),
      ('scrap',['--headless','-s','res://tests/test_room_scrap.gd'],'ROOM SCRAP failures=0'),
      ('repair',['--headless','-s','res://tests/test_hull_repair.gd'],'HULL REPAIR PASS'),
      ('fitting',['--headless','-s','res://tests/test_construction_fitting_routes.gd'],'CONSTRUCTION FITTING ROUTES: PASS'),
      ('integration',['--headless','-s','res://tests/test_room_transition_integration.gd'],'ROOM TRANSITION INTEGRATION: 0 failures'),
      ('native',['--screen','2','-s','res://tests/preview_room_transitions.gd'],'0 failures'),
      ('ocean',['--screen','2','-s','res://tests/test_ocean_life.gd'],'OCEAN LIFE: PASS')]
for flag,names in [('--native-only',{'native'}),('--visual-only',{'native','ocean'}),('--logic-only',{'uids','logic'}),('--integration-only',{'integration'}),('--uids-only',{'uids'})]:
    if flag in sys.argv:jobs=[job for job in jobs if job[0] in names]
results=[]
try:
    for label,args,marker in jobs:
        log=OUT/(label+'.log')
        with log.open('w') as stream:
            result=subprocess.run([godot,'--path',str(ROOT),*args],env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=120)
        lines=log.read_text(errors='replace').splitlines()
        okay=result.returncode==0 and any(marker in line for line in lines) and not any('SCRIPT ERROR' in line or ('ERROR:' in line and 'resources still in use at exit' not in line) for line in lines)
        results.append({'job':label,'pass':okay,'exit':result.returncode})
        print(label,'PASS' if okay else 'FAIL',flush=True)
        if not okay:
            print('\n'.join(line for line in lines if 'ERROR' in line or 'failure' in line),flush=True);break
finally:
    after=fingerprint();deltas=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
    (OUT/'owner-after.json').write_text(json.dumps(after))
    (OUT/'summary.json').write_text(json.dumps({'results':results,'owner_unchanged':before==after,'owner_files':len(before),'owner_deltas':deltas},indent=2))
    print('Owner profile unchanged:',before==after,'files:',len(before),'Evidence:',OUT,flush=True)
raise SystemExit(0 if before==after and len(results)==len(jobs) and all(r['pass'] for r in results) else 1)
