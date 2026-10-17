"""Run floor-details native art review with an isolated owner profile."""
import datetime,hashlib,json,os,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/('floor-details-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));OUT.mkdir()
OWNER=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():return {p.relative_to(OWNER).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in OWNER.rglob('*') if p.is_file()}
before=fingerprint();(OUT/'owner-before.json').write_text(json.dumps(before))
env=os.environ.copy();env['APPDATA']=str(OUT/'scratch/roaming');env['LOCALAPPDATA']=str(OUT/'scratch/local')
scratch=Path(env['APPDATA'])/'Godot/app_userdata/BrineSpace';scratch.mkdir(parents=True)
if (OWNER/'room_layouts.json').exists():shutil.copy2(OWNER/'room_layouts.json',scratch/'room_layouts.json')
godot='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe'
results=[]
uid=OUT/'uids.gd'
uid.write_text('extends SceneTree\nfunc _initialize():\n\tfor path in ["res://tests/review_floor_details.gd.uid","res://assets/environment/floor-details-v1/floor_details_view.gd.uid"]:\n\t\tif not FileAccess.file_exists(path): FileAccess.open(path,FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")\n\tquit()\n')
with (OUT/'uids.log').open('w') as stream:subprocess.run([godot,'--path',str(ROOT),'--headless','-s',str(uid)],env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=30,check=True)
try:
    for name,script,marker in [('native','res://tests/review_floor_details.gd','FLOOR DETAILS REVIEW: 0 failures')]:
        log=OUT/(name+'.log')
        with log.open('w') as stream:r=subprocess.run([godot,'--path',str(ROOT),'--screen','2','-s',script],env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=180)
        lines=log.read_text(errors='replace').splitlines()
        okay=r.returncode==0 and any(marker in line for line in lines) and not any('SCRIPT ERROR' in line or ('ERROR:' in line and 'resources still in use at exit' not in line) for line in lines)
        results.append(dict(job=name,passed=okay,exit=r.returncode));print(name,'PASS' if okay else 'FAIL',flush=True)
        print('\n'.join(line for line in lines if 'ERROR' in line or marker in line),flush=True)
        if not okay:break
finally:
    after=fingerprint();deltas=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    (OUT/'owner-after.json').write_text(json.dumps(after));(OUT/'summary.json').write_text(json.dumps(dict(results=results,owner_files=len(before),owner_unchanged=before==after,owner_deltas=deltas),indent=2))
    print('Owner unchanged:',before==after,'Evidence:',OUT,flush=True)
raise SystemExit(0 if len(results)==1 and all(r['passed'] for r in results) else 1)
