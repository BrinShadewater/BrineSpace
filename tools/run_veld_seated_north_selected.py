"""Observe paused lighting without changing source art or owner profile."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/veld-seated-north-selected-v1'
def fingerprint():
    profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {p.relative_to(profile).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file() and 'logs' not in p.relative_to(profile).parts}
def main():
    godot=Path(sys.argv[1]);assert godot.is_file();OUT.mkdir(exist_ok=True)
    prior=[p for p in OUT.iterdir() if p.is_file()]
    if prior:
        archive=OUT/f'interval-before-{time.time_ns()}';archive.mkdir()
        for p in prior:shutil.copy2(p,archive/p.name)
    before=fingerprint();(OUT/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
    watched=['scripts/grid_canvas.gd','scripts/crew_life.gd','scripts/crew_sprite_player.gd','scripts/crew_room_activity.gd','scripts/veld_npc.gd','scripts/bill_npc.gd','scripts/run_save.gd','rooms/whole-room/nursery_whole_view.gd','tests/test_veld_seated_north_selected.gd','tests/test_veld_seated_north_continue.gd']
    for gear in ['bare','helmet']:
        manifest='character/veld-seated-north-breathing-source-v1/'+gear+'-manifest.json';watched.append(manifest)
        watched.extend('character/veld-seated-north-breathing-source-v1/'+name for state in json.loads((ROOT/manifest).read_text())['states'] for name in state['frameFiles'])
    watched.extend(json.loads((ROOT/'character/veld-seated-north-selected-v1/source-bindings.json').read_text(encoding='utf-8'))['bindings'])
    watched.extend(['character/veld-seated-north-selected-v1/bare-manifest.json','character/veld-seated-north-selected-v1/helmet-manifest.json'])
    hashes=lambda:{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in watched}
    sources=hashes();env=os.environ.copy();scratch=OUT/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
    started=time.monotonic();epoch=time.time()
    with (OUT/'native.log').open('w',encoding='utf-8') as log:
        try:code=subprocess.run([str(godot),'--path',str(ROOT),'--script','res://tests/test_veld_seated_north_selected.gd','--resolution','1280x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300).returncode
        except subprocess.TimeoutExpired:code=-1
    after=fingerprint();(OUT/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
    changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));source_after=hashes()
    text=(OUT/'native.log').read_text(encoding='utf-8');photo=OUT/'final.png';fresh=photo.exists() and photo.stat().st_mtime>=epoch
    runtime=code==0 and '0 failures;' in text and not any(e in text for e in ['SCRIPT ERROR','ERROR:','Artwork unavailable:']) and fresh
    report={'passed':runtime and not changes and sources==source_after,'runtimePassed':runtime,'returnCode':code,'seconds':round(time.monotonic()-started,2),'scratchAPPDATA':str(scratch),'realProfileFileCount':len(before),'realProfileChanges':changes,'sourcesBefore':sources,'sourcesAfter':source_after,'freshScreenshot':fresh}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['sourcesBefore','sourcesAfter']}))
    print('\n'.join(line for line in text.splitlines() if any(k in line for k in ['VELD NORTH SELECTED','SCRIPT ERROR','ERROR:',' at:']))[-2000:])
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())

