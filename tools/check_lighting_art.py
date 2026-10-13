"""Lighting gates; every Godot process gets a fresh isolated profile."""
import datetime,hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'/('lighting-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
OUT.mkdir(parents=True)
OWNER=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {p.relative_to(OWNER).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(OWNER.rglob('*')) if p.is_file()}
def environment(name):
    env=os.environ.copy()
    env['APPDATA']=str(OUT/name/'roaming');env['LOCALAPPDATA']=str(OUT/name/'local')
    Path(env['APPDATA']).mkdir(parents=True);Path(env['LOCALAPPDATA']).mkdir(parents=True)
    return env
before=fingerprint();(OUT/'owner-before.json').write_text(json.dumps(before,indent=2))
GODOT='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe'
results=[]
try:
    paths=['scripts/lighting_art.gd','tests/test_lighting_art.gd','tests/test_lighting_art_review.gd','tests/test_lighting_game_review.gd']
    uid=OUT/'uids.gd'
    uid.write_text('extends SceneTree\nfunc _initialize():\n\tfor path in '+json.dumps(['res://'+p for p in paths])+':\n\t\tif not FileAccess.file_exists(path+".uid"):\n\t\t\tvar file=FileAccess.open(path+".uid",FileAccess.WRITE)\n\t\t\tfile.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\\n")\n\tquit()\n')
    with (OUT/'uids.log').open('w') as log:
        subprocess.run([GODOT,'--headless','--path',str(ROOT),'-s',str(uid)],env=environment('uids'),stdout=log,stderr=subprocess.STDOUT,check=True,timeout=60)
    for test in (sys.argv[1:] or ['test_lighting_art','test_effects_quality','test_light_emergency','test_reliability','test_lighting_art_review']):
        native=test in ['test_lighting_art_review','test_lighting_game_review']
        command=[GODOT,'--screen','2'] if native else [GODOT,'--headless']
        command+=['--path',str(ROOT),'-s','res://tests/'+test+'.gd']
        if native:command+=['--','--capture-dir='+str(ROOT/'assets/sea-life-v1/lighting/review/native')]
        with (OUT/(test+'.log')).open('w') as log:
            try:code=subprocess.run(command,env=environment(test),stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
            except subprocess.TimeoutExpired:code=-1
        lines=(OUT/(test+'.log')).read_text(errors='replace').splitlines()
        ok=code==0 and not any('SCRIPT ERROR' in l for l in lines) and any('failures=0' in l or '0 failures' in l for l in lines)
        results.append(dict(test=test,ok=ok,exit=code))
        print(test,'PASS' if ok else 'FAIL',flush=True)
        if not ok:
            print('\n'.join(l[:500] for l in lines if any(x in l for x in ['ERROR','Error','FAIL','failures'])),flush=True)
            break
finally:
    after=fingerprint();unchanged=before==after
    (OUT/'owner-after.json').write_text(json.dumps(after,indent=2))
    (OUT/'summary.json').write_text(json.dumps(dict(results=results,owner_unchanged=unchanged),indent=2))
    print('Owner profile unchanged:',unchanged,'Logs:',OUT,flush=True)
sys.exit(0 if unchanged and all(r['ok'] for r in results) else 1)
