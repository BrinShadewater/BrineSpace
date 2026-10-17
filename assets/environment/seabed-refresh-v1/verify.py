"""Scoped isolated native and runtime checks; preserve owner saves."""
import datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
from PIL import Image,ImageDraw
PACK=Path(__file__).resolve().parent
ROOT=PACK.parents[2]
OWNER=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {p.relative_to(OWNER).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in OWNER.rglob('*') if p.is_file()}
before=fingerprint()
out=ROOT/'output'/('seabed-refresh-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
out.mkdir(parents=True,exist_ok=True)
(out/'owner-before.json').write_text(json.dumps(before))
env=os.environ.copy()
env['APPDATA']=str(out/'scratch/roaming');env['LOCALAPPDATA']=str(out/'scratch/local')
Path(env['APPDATA']).mkdir(parents=True,exist_ok=True)
Path(env['LOCALAPPDATA']).mkdir(parents=True,exist_ok=True)
godot='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe'
results=[]
try:
    # UID resources are paired with the new scripts without opening the editor.
    paths=['assets/environment/seabed-refresh-v1/seabed_refresh_view.gd','tests/preview_seabed_refresh.gd','tests/preview_seabed_refresh_sheet.gd']
    uid=out/'uids.gd'
    uid.write_text('extends SceneTree\nfunc _initialize():\n\tfor path in '+json.dumps(['res://'+p for p in paths])+':\n\t\tif not FileAccess.file_exists(path+".uid"):\n\t\t\tFileAccess.open(path+".uid",FileAccess.WRITE).store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")\n\tquit()\n')
    jobs=[('uids',['--headless','-s',str(uid)]),('runtime',['--headless','-s','res://tests/test_runtime_environment_art.gd']),('native',['--screen','2','-s','res://tests/preview_seabed_refresh.gd'])]
    if '--sheet' in sys.argv: jobs=[jobs[0],('density',['--screen','2','-s','res://tests/preview_seabed_refresh_sheet.gd'])]
    for label,args in jobs:
        log=out/(label+'.log')
        with log.open('w') as stream:
            result=subprocess.run([godot,'--path',str(ROOT),*args],env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=120)
        lines=log.read_text(errors='replace').splitlines()
        okay=result.returncode==0 and not any('SCRIPT ERROR' in line or ('ERROR:' in line and 'resources still in use at exit' not in line) for line in lines)
        if label!='uids':okay=okay and any('0 failures' in line for line in lines)
        results.append({'job':label,'pass':okay,'exit':result.returncode})
        print(label,'PASS' if okay else 'FAIL',flush=True)
        if not okay:
            print('\n'.join(line for line in lines if 'ERROR' in line or 'failure' in line),flush=True)
            break
finally:
    after=fingerprint()
    deltas=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
    (out/'owner-after.json').write_text(json.dumps(after))
    (out/'summary.json').write_text(json.dumps({'results':results,'owner_unchanged':before==after,'owner_files':len(before),'owner_deltas':deltas},indent=2))
    print('Owner profile unchanged:',before==after,'files:',len(before),flush=True)
raise SystemExit(0 if before==after and len(results)==len(jobs) and all(r['pass'] for r in results) else 1)
