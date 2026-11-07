from pathlib import Path
import os,json,hashlib,subprocess,sys,time
R=Path(__file__).resolve().parent.parent;P=R/'character/veld-cargo-east-original-master-v3';Q=R/'character/veld-cargo-east-original-master-v2';O=R/'output/veld-cargo-east-original-master-v3';O.mkdir(exist_ok=True);assert not(O/'validation.json').exists(),'Preserve prior interval'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def profile():
 p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
paths={R/'scripts/crew_sprite_player.gd',R/'tests/test_veld_cargo_east_original_master_v3.gd',R/'tests/test_veld_cargo_east_original_master_v3.gd.uid',P/'registration.json',P/'cargo_prop.gd',P/'cargo_prop.gd.uid'}
paths.update(R/ref for ref in json.loads((P/'registration.json').read_text(encoding='utf-8'))['bindings']);paths.update(R/ref for ref in json.loads((R/'output/veld-cargo-east-original-master-v2/inputs-before.json').read_text(encoding='utf-8')))
def inputs():return {p.relative_to(R).as_posix():sha(p) for p in sorted(paths)}
before=profile();art=inputs();env=os.environ.copy();env['APPDATA']=str(O/'veld-east-cargo-prop-scratch');Path(env['APPDATA']).mkdir(exist_ok=True)
for name,data in [('profile-before',before),('inputs-before',art)]:(O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
t=time.monotonic()
with (O/'native.log').open('w',encoding='utf-8') as log:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_cargo_east_original_master_v3.gd','--resolution','900x400'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=90).returncode
after=profile();art_after=inputs();changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));log=(O/'native.log').read_text(encoding='utf-8');passed=code==0 and ',0 failures;' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and not changes and art==art_after
report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-t,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(art),'targetedInputsUnchanged':art==art_after,'scope':'Staged separate visual floorcase anchor/contact/take and prescribed root displacement at47/93/148, paired native source chronology, serialized visual snapshot restore/reject and storage retirement hook. Not ordinary navigation, walking contacts, RunSave/menu Continue, gameplay credit or final artistic acceptance.'}
for name,data in [('profile-after',after),('inputs-after',art_after),('validation',report)]:(O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report));print('\n'.join(log.splitlines()[-8:]));raise SystemExit(0 if passed else 1)
