from pathlib import Path
import os,sys,json,hashlib,subprocess,time
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-cargo-west-master-family-v1'
def profile():
    p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {x.relative_to(p).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
O.mkdir(exist_ok=True)
assert not (O/'validation.json').exists(),'Preserve old interval; use distinct run instead'
paths=[R/'scripts/crew_sprite_player.gd',R/'tests/test_veld_cargo_west_master_family.gd']
for folder in ['veld-cargo-west-master-family-v1','veld-unload-west-consistent-v1','veld-pickup-west-consistent-v1']:
    for gear in ['bare','helmet']:
        p=R/f'character/{folder}/{gear}-manifest.json';paths.append(p)
        for s in json.loads(p.read_text(encoding='utf-8'))['states']:paths.extend(R/x[6:] if x.startswith('res://') else p.parent/x for x in s['frameFiles'])
paths=sorted(set(paths))
def inputs():return {x.relative_to(R).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}
before=profile();art=inputs()
for name,value in [('profile-before',before),('inputs-before',art)]:
    (O/f'{name}.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
env=os.environ.copy();scratch=O/'veld-cargo-west-master-scratch';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
start=time.monotonic();epoch=time.time()
with (O/'native.log').open('w',encoding='utf-8') as log:
    try:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_cargo_west_master_family.gd','--resolution','760x600'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=240).returncode
    except subprocess.TimeoutExpired:code=-1
after=profile();art_after=inputs()
for name,value in [('profile-after',after),('inputs-after',art_after)]:
    (O/f'{name}.json').write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
log=(O/'native.log').read_text(encoding='utf-8');fresh=(O/'helmet-pickup-017-native.png').exists() and (O/'helmet-pickup-017-native.png').stat().st_mtime>=epoch
passed=code==0 and ',0 failures;72native presentations' in log and not any(x in log for x in ['SCRIPT ERROR','ERROR:','Artwork unavailable:']) and fresh and not changes and art==art_after
report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-start,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(art),'targetedInputsUnchanged':art==art_after,'freshCapture':fresh,'scope':'candidate standalone actual crew-player finite-clock/native rendering, unload/pickup/both gears; no normal selection/controller/world/prop ownership/save acceptance'}
(O/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report));print('\n'.join(log.splitlines()[-6:]));raise SystemExit(0 if passed else 1)
