"""Scratch-only native world interruption and fresh disk checkpoint verification."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/veld-bunk-body-emergency-v1'
def fingerprint():
    profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {p.relative_to(profile).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file() and 'logs' not in p.relative_to(profile).parts}
def main():
    godot=Path(sys.argv[1]);assert godot.is_file();OUT.mkdir(exist_ok=True)
    prior=[p for p in OUT.iterdir() if p.is_file()]
    if prior:
        archive=OUT/f'interval-before-{time.time_ns()}';archive.mkdir()
        for p in prior:shutil.copy2(p,archive/p.name)
    inputs=[ROOT/p for p in ['scripts/veld_npc.gd','scripts/fire_safety.gd','scripts/room_scrap.gd','scripts/crew_life.gd','tests/test_veld_bunk_body_emergency.gd','tests/test_room_fire.gd']]
    inputs+=list((ROOT/'character/veld-bunk-body-master-v1/frames').rglob('*.png'))
    inputs+=[ROOT/'character/veld-bunk-body-master-v1/bare-manifest.json',ROOT/'character/veld-bunk-body-master-v1/helmet-manifest.json']
    frozen={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    (OUT/'inputs-before.json').write_text(json.dumps(frozen,indent=2)+'\n')
    before=fingerprint();(OUT/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
    env=os.environ.copy();scratch=OUT/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
    started=time.monotonic();epoch=time.time()
    with (OUT/'native.log').open('w',encoding='utf-8') as log:
        try:code=subprocess.run([str(godot),'--path',str(ROOT),'--script','res://tests/test_veld_bunk_body_emergency.gd','--resolution','1280x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=600).returncode
        except subprocess.TimeoutExpired:code=-1
    with (OUT/'shared-fire-regression.log').open('w',encoding='utf-8') as log:
        regression_code=subprocess.run([str(godot),'--headless','--path',str(ROOT),'--script','res://tests/test_room_fire.gd'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120).returncode
    bound_after={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    (OUT/'inputs-after.json').write_text(json.dumps(bound_after,indent=2)+'\n')
    after=fingerprint();(OUT/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
    changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    text=(OUT/'native.log').read_text(encoding='utf-8');photo=OUT/'records.json'
    fresh=photo.exists() and photo.stat().st_mtime>=epoch
    runtime=code==0 and '0 failures;22 fire rises,22 direct gear swaps,2 blocked scraps' in text and not any(e in text for e in ['SCRIPT ERROR','ERROR:','Artwork unavailable:']) and fresh
    regression=(OUT/'shared-fire-regression.log').read_text(encoding='utf-8')
    regression_passed=regression_code==0 and '0 failures' in regression and not any(e in regression for e in ['SCRIPT ERROR','ERROR:'])
    report={'passed':runtime and regression_passed and not changes and frozen==bound_after,'runtimePassed':runtime,'returnCode':code,'sharedFirePassed':regression_passed,'sharedFireReturnCode':regression_code,'targetedInputCount':len(frozen),'targetedInputsUnchanged':frozen==bound_after,'seconds':round(time.monotonic()-started,2),'scratchAPPDATA':str(scratch),'realProfileFileCount':len(before),'realProfileChanges':changes,'freshScreenshot':fresh}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
    print('\n'.join(line for line in text.splitlines() if any(k in line for k in ['VELD BUNK BODY EMERGENCY','SCRIPT ERROR','ERROR:',' at:']))[-2500:])
    print('\n'.join(line for line in regression.splitlines() if any(k in line for k in ['Room fire:','SCRIPT ERROR','ERROR:']))[-1000:])
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
