from pathlib import Path
import os,sys,json,hashlib,subprocess,time
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-workshop-west-start-master-v1'
def profile():
    p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {x.relative_to(p).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
O.mkdir(exist_ok=True)
assert not (O/'validation.json').exists(),'Preserve old interval; use distinct run instead'
paths=[R/'character/veld-carry-west-start-master-v1/workshop_motion_preview.gd',R/'scripts/james_cargo_workshop.gd',R/'character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd',R/'rooms/underwater/salvage-workshop-v1/workshop_view.gd',R/'scripts/crew_sprite_player.gd',R/'tests/test_veld_workshop_west_start_master_v1.gd',R/'scripts/veld_npc.gd',R/'scripts/bill_npc.gd',R/'scripts/grid_canvas.gd',R/'scenes/main.tscn',R/'scripts/main.gd',R/'character/veld-cargo-north-master-family-v1/rise-join-v3/floor-case-canvas.png',R/'character/veld-cargo-north-master-family-v1/rise-join-v3/workshop_preview.gd',R/'scripts/crew_life.gd',R/'character/veld-cargo-east-master-family-v1/workshop_motion_preview.gd']
for folder in ['veld-cargo-north-master-family-v1/rise-join-v3','veld-cargo-north-master-family-v1','veld-cargo-east-master-family-v1','veld-unload-east-consistent-v1','veld-pickup-east-consistent-v1','veld-carry-west-start-master-v1','veld-cargo-turns-master-family-v1/half-turn-candidate-v1','veld-cargo-turns-master-family-v1/north-west-candidate-v4']:
    for gear in ['bare','helmet']:
        p=R/f'character/{folder}/{gear}-manifest.json';paths.append(p)
        for s in json.loads(p.read_text(encoding='utf-8'))['states']:paths.extend(R/x[6:] if x.startswith('res://') else p.parent/x for x in s['frameFiles'])
paths=sorted(set(paths))
def inputs():return {x.relative_to(R).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
before=profile();art=inputs()
for name,value in [('profile-before',before),('inputs-before',art)]:
    (O/f'{name}.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
env=os.environ.copy();scratch=O/'veld-workshop-source-scratch';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
start=time.monotonic();epoch=time.time()
with (O/'native.log').open('w',encoding='utf-8') as log:
    try:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_workshop_west_start_master_v1.gd','--resolution','1280x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=240).returncode
    except subprocess.TimeoutExpired:code=-1
after=profile();art_after=inputs()
for name,value in [('profile-after',after),('inputs-after',art_after)]:
    (O/f'{name}.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
log=(O/'native.log').read_text(encoding='utf-8');fresh=(O/'journeys.json').exists() and (O/'journeys.json').stat().st_mtime>=epoch
passed=code==0 and 'VELD WORKSHOP WEST START:' in log and ',0 failures' in log and not any(x in log for x in ['SCRIPT ERROR','ERROR:','Artwork unavailable:']) and fresh and not changes and art==art_after
report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-start,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(art),'targetedInputsUnchanged':art==art_after,'freshCapture':fresh,'scope':'actual workshop generated route/grid source, normal actor versus fixture-only coordinated subclass/staged master sources, both gears; no normal selection/natural chooser/ownership/interruption/Continue acceptance'}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report));print('\n'.join(log.splitlines()[-6:]));raise SystemExit(0 if passed else 1)
