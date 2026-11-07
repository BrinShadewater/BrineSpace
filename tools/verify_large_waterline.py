"""Large equipment clipping and native waterline review in an isolated profile."""
import datetime,hashlib,json,os,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/('large-waterline-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
OUT.mkdir(parents=True)
OWNER=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():return {p.relative_to(OWNER).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in OWNER.rglob('*') if p.is_file()}
before=fingerprint();(OUT/'owner-before.json').write_text(json.dumps(before))
env=os.environ.copy();env['APPDATA']=str(OUT/'scratch/roaming');env['LOCALAPPDATA']=str(OUT/'scratch/local')
scratch=Path(env['APPDATA'])/'Godot/app_userdata/BrineSpace';scratch.mkdir(parents=True)
if (OWNER/'room_layouts.json').exists():shutil.copy2(OWNER/'room_layouts.json',scratch/'room_layouts.json')
uid=OUT/'uids.gd';uid.write_text('extends SceneTree\nfunc _initialize():\n\tfor path in ["res://tests/review_large_waterline.gd","res://scripts/large_wet_equipment.gd","res://tests/test_large_waterline.gd"]:\n\t\tif not FileAccess.file_exists(path+".uid"):\n\t\t\tFileAccess.open(path+".uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")\n\tquit()\n')
godot='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe'
results=[]
try:
    for name,args,marker in [('uids',['--headless','-s',str(uid)],''),('geometry',['--headless','-s','res://tests/test_large_waterline.gd'],'LARGE WATERLINE GEOMETRY: 0 failures'),('native',['--screen','2','-s','res://tests/review_large_waterline.gd'],'LARGE WATERLINE REVIEW: 0 failures')]:
        log=OUT/(name+'.log')
        with log.open('w') as stream:result=subprocess.run([godot,'--path',str(ROOT),*args],env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=180)
        lines=log.read_text(errors='replace').splitlines()
        okay=result.returncode==0 and any(marker in line for line in lines) and not any('SCRIPT ERROR' in line or ('ERROR:' in line and 'resources still in use at exit' not in line) for line in lines)
        results.append({'job':name,'pass':okay,'exit':result.returncode});print(name,'PASS' if okay else 'FAIL',flush=True)
        excerpts=[line for line in lines if line.startswith('{"') or 'LARGE WATERLINE REVIEW' in line or 'ERROR' in line]
        print('\n'.join(excerpts[:20]),flush=True)
        if not okay:break
finally:
    after=fingerprint();deltas=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    (OUT/'owner-after.json').write_text(json.dumps(after))
    (OUT/'summary.json').write_text(json.dumps({'results':results,'owner_files':len(before),'owner_unchanged':before==after,'owner_deltas':deltas,'layouts_copied':(scratch/'room_layouts.json').exists()},indent=2))
    print('Owner unchanged:',before==after,'Evidence:',OUT,flush=True)
raise SystemExit(0 if before==after and len(results)==3 and all(r['pass'] for r in results) else 1)
