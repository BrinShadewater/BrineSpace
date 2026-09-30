"""Run sea-life gates with fresh isolated profiles and native capture on screen 2."""
import hashlib,json,os,subprocess,sys,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
OUT=ROOT/'output'/('sea-life-'+stamp)
OUT.mkdir(parents=True)
owner=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {p.relative_to(owner).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(owner.rglob('*')) if p.is_file()}
before=fingerprint(); (OUT/'owner-before.json').write_text(json.dumps(before,indent=2))
godot='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe'
results=[]
tests=sys.argv[1:] or ['test_sea_life_assets','test_effects_quality','test_reliability','test_ocean_life','test_sea_life_assembly']
try:
    scripts=['scripts/ocean_life.gd','tests/test_sea_life_assets.gd','tests/test_sea_life_review.gd','tests/test_sea_life_assembly.gd']
    if any(not (ROOT/(s+'.uid')).exists() for s in scripts):
        # Native UID creation for new/unpaired scripts, never replacing one.
        uid_script=OUT/'assign_missing_uids.gd'
        uid_script.write_text('extends SceneTree\nfunc _initialize():\n\tfor path in '+json.dumps(['res://'+s for s in scripts])+':\n\t\tif not FileAccess.file_exists(path+".uid"):\n\t\t\tvar file=FileAccess.open(path+".uid",FileAccess.WRITE)\n\t\t\tfile.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")\n\tquit()\n')
        uid_env=os.environ.copy();uid_env['APPDATA']=str(OUT/'uids/roaming');uid_env['LOCALAPPDATA']=str(OUT/'uids/local')
        Path(uid_env['APPDATA']).mkdir(parents=True);Path(uid_env['LOCALAPPDATA']).mkdir(parents=True)
        with (OUT/'uids.log').open('w') as log:
            subprocess.run([godot,'--headless','--path',str(ROOT),'-s',str(uid_script)],env=uid_env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
    for test in tests:
        env=os.environ.copy(); env['APPDATA']=str(OUT/test/'roaming');env['LOCALAPPDATA']=str(OUT/test/'local')
        Path(env['APPDATA']).mkdir(parents=True);Path(env['LOCALAPPDATA']).mkdir(parents=True)
        native=test in ['test_ocean_life','test_sea_life_review','test_sea_life_assembly']
        cmd=[godot,'--screen','2'] if native else [godot,'--headless']
        cmd+=['--path',str(ROOT),'-s','res://tests/'+test+'.gd']
        if test in ['test_sea_life_review','test_sea_life_assembly']: cmd+=['--','--capture-dir='+str(ROOT/'assets/sea-life-v1/review/native')]
        with (OUT/(test+'.log')).open('w',encoding='utf-8') as log:
            try: code=subprocess.run(cmd,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=240).returncode
            except subprocess.TimeoutExpired: code=-1
        text=(OUT/(test+'.log')).read_text(errors='replace')
        ok=code==0 and 'SCRIPT ERROR' not in text and 'failures=0' in text or (code==0 and '0 failures' in text)
        results.append({'test':test,'ok':ok,'exit':code})
        print(test,'PASS' if ok else 'FAIL','exit',code,flush=True)
        if not ok:
            print('\n'.join(l[:500] for l in text.splitlines() if any(k in l for k in ['ERROR','Error','FAIL','failures'])),flush=True)
            break
finally:
    after=fingerprint(); (OUT/'owner-after.json').write_text(json.dumps(after,indent=2))
    unchanged=before==after
    (OUT/'summary.json').write_text(json.dumps({'results':results,'owner_unchanged':unchanged},indent=2))
    print('Owner profile unchanged:',unchanged,'Logs:',OUT,flush=True)
sys.exit(0 if unchanged and all(r['ok'] for r in results) else 1)
