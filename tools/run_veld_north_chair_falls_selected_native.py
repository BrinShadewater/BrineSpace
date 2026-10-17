"""Scratch-only native world interruption and fresh disk checkpoint verification."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/veld-north-chair-falls-selected-native-v1'
def fingerprint():
    profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {p.relative_to(profile).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file() and 'logs' not in p.relative_to(profile).parts}
def main():
    godot=Path(sys.argv[1]);assert godot.is_file();OUT.mkdir(exist_ok=True)
    prior=[p for p in OUT.iterdir() if p.is_file()]
    if prior:
        archive=OUT/f'interval-before-{time.time_ns()}';archive.mkdir()
        for p in prior:shutil.copy2(p,archive/p.name)
    inputs=[ROOT/'scripts/veld_npc.gd',ROOT/'scripts/veld_death_motion.gd',ROOT/'scripts/crew_life.gd',ROOT/'scripts/run_save.gd',ROOT/'scripts/crew_sprite_player.gd',ROOT/'scripts/room_flooding.gd',ROOT/'tests/test_veld_north_chair_falls_selected_native.gd']
    inputs+=[ROOT/'scripts/grid_canvas.gd',ROOT/'character/veld-seated-north-selected-v1/bare-manifest.json',ROOT/'character/veld-seated-north-selected-v1/helmet-manifest.json']
    inputs+=list((ROOT/'character/veld-seated-north-coherent-v1/frames').rglob('*.png'))
    inputs+=list((ROOT/'character/veld-lounge-early-fall-north-v1/frames').rglob('*.png'))
    inputs+=[ROOT/'character/veld-lounge-early-fall-north-v1/bare-manifest.json',ROOT/'character/veld-lounge-early-fall-north-v1/helmet-manifest.json']
    inputs+=[ROOT/'character/veld-seated-north-coherent-v1/bare-manifest.json',ROOT/'character/veld-seated-north-coherent-v1/helmet-manifest.json']
    for folder in ['veld-lounge-fall-north-v1','veld-lounge-partial-fall-north-v1','veld-lounge-late-fall-north-v1']:
        inputs+=list((ROOT/'character'/folder/'frames').rglob('*.png'))
        inputs+=[ROOT/'character'/folder/'bare-manifest.json',ROOT/'character'/folder/'helmet-manifest.json']
    bindings={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    (OUT/'inputs-before.json').write_text(json.dumps(bindings,indent=2)+'\n')
    before=fingerprint();(OUT/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
    env=os.environ.copy();scratch=OUT/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
    started=time.monotonic();epoch=time.time()
    with (OUT/'native.log').open('w',encoding='utf-8') as log:
        try:code=subprocess.run([str(godot),'--path',str(ROOT),'--script','res://tests/test_veld_north_chair_falls_selected_native.gd','--resolution','1280x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1600).returncode
        except subprocess.TimeoutExpired:code=-1
    after=fingerprint();(OUT/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
    after_bindings={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    (OUT/'inputs-after.json').write_text(json.dumps(after_bindings,indent=2)+'\n')
    changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    text=(OUT/'native.log').read_text(encoding='utf-8');photo=OUT/'helmet-held3-after-room.png'
    fresh=photo.exists() and photo.stat().st_mtime>=epoch
    runtime=code==0 and '0 failures;28 fresh disk restores' in text and not any(e in text for e in ['SCRIPT ERROR','ERROR:','Artwork unavailable:']) and fresh
    report={'passed':runtime and not changes and bindings==after_bindings,'targetedInputsUnchanged':bindings==after_bindings,'targetedInputCount':len(bindings),'runtimePassed':runtime,'returnCode':code,'seconds':round(time.monotonic()-started,2),'scratchAPPDATA':str(scratch),'realProfileFileCount':len(before),'realProfileChanges':changes,'freshScreenshot':fresh}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
    print('\n'.join(line for line in text.splitlines() if any(k in line for k in ['NORTH CHAIR FALLS SELECTED','VELD BUNK BODY RESUME','SCRIPT ERROR','ERROR:',' at:']))[-2500:])
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
