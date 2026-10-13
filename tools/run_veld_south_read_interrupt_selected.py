"""Scratch-only native world interruption and fresh disk checkpoint verification."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/veld-south-read-interrupt-selected-v1'
def fingerprint():
    profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {p.relative_to(profile).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file() and 'logs' not in p.relative_to(profile).parts}
def main():
    godot=Path(sys.argv[1]);assert godot.is_file();OUT.mkdir(exist_ok=True)
    prior=[p for p in OUT.iterdir() if p.is_file()]
    if prior:
        archive=OUT/f'interval-before-{time.time_ns()}';archive.mkdir()
        for p in prior:shutil.copy2(p,archive/p.name)
    frozen_paths=[ROOT/p for p in ['scripts/grid_canvas.gd','scripts/veld_npc.gd','scripts/bill_npc.gd','scripts/crew_life.gd','scripts/crew_sprite_player.gd','scripts/run_save.gd','character/ACTIVE_ASSETS.json','tests/test_veld_south_read_interrupt_selected.gd','tests/test_veld_seated_south_selected.gd','tests/test_veld_seated_north_continue.gd']]
    for gear in ['bare','helmet']:
        manifest=ROOT/f'character/veld-seated-south-selected-v1/{gear}-manifest.json'
        frozen_paths.append(manifest)
        data=json.loads(manifest.read_text(encoding='utf-8'))
        for state in data['states']:
            for frame in state['frameFiles']:
                value=frame if isinstance(frame,str) else frame['path']
                frozen_paths.append(ROOT/value.removeprefix('res://'))
    frozen_paths=sorted(set(frozen_paths))
    frozen={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen_paths}
    (OUT/'inputs-before.json').write_text(json.dumps(frozen,indent=2)+'\n',encoding='utf-8')
    before=fingerprint();(OUT/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
    env=os.environ.copy();scratch=OUT/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
    started=time.monotonic();epoch=time.time()
    with (OUT/'native.log').open('w',encoding='utf-8') as log:
        try:code=subprocess.run([str(godot),'--path',str(ROOT),'--script','res://tests/test_veld_south_read_interrupt_selected.gd','--resolution','1280x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900).returncode
        except subprocess.TimeoutExpired:code=-1
    inputs_after={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen_paths}
    input_changes=sorted(k for k in frozen if frozen[k]!=inputs_after[k])
    (OUT/'inputs-after.json').write_text(json.dumps(inputs_after,indent=2)+'\n',encoding='utf-8')
    after=fingerprint();(OUT/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
    changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    text=(OUT/'native.log').read_text(encoding='utf-8');photo=OUT/'final.png'
    fresh=photo.exists() and photo.stat().st_mtime>=epoch
    runtime=code==0 and '0 failures; 56 interruptions' in text and not any(e in text for e in ['SCRIPT ERROR','ERROR:','Artwork unavailable:']) and fresh
    report={'passed':runtime and not changes and not input_changes,'frozenInputCount':len(frozen),'frozenInputChanges':input_changes,'runtimePassed':runtime,'returnCode':code,'seconds':round(time.monotonic()-started,2),'scratchAPPDATA':str(scratch),'realProfileFileCount':len(before),'realProfileChanges':changes,'freshScreenshot':fresh}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
    print('\n'.join(line for line in text.splitlines() if any(k in line for k in ['READ INTERRUPT','VELD SOUTH READ INTERRUPT SELECTED','SCRIPT ERROR','ERROR:',' at:']))[-2500:])
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
