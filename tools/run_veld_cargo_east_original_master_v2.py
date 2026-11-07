from pathlib import Path
import os,json,hashlib,subprocess,sys,time
R=Path(__file__).resolve().parent.parent;P=R/'character/veld-cargo-east-original-master-v2';O=R/'output/veld-cargo-east-original-master-v2';O.mkdir(exist_ok=True);assert not(O/'validation.json').exists(),'Preserve prior interval'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def profile():
 p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
paths={R/'scripts/crew_sprite_player.gd',R/'tests/test_veld_cargo_east_original_master_v2.gd',R/'tests/test_veld_cargo_east_original_master_v2.gd.uid',P/'build_shared_case.py',P/'register_contacts.py',P/'contact-registration.json',P/'shared-case-registration.json',R/'character/veld-side-foundation-v1/east-standing.png',R/'character/veld-helmet-original-turntable-v1/v3-study/shells/005.png'}
paths.update(P.glob('raw-*.png'));paths.update(P.glob('prompt-*.txt'));paths.update(P.glob('whole-*.png'));paths.add(P/'shared-floor-case.png')
for folder in [P,R/'character/veld-east-held-original-master-v1']:
 for m in folder.glob('*-manifest.json'):
  paths.add(m)
  for state in json.loads(m.read_text(encoding='utf-8'))['states']:paths.update(R/ref[6:] for ref in state['frameFiles'])
paths.update((P/'atlas-contact-frames').glob('*.png'))
def inputs():return {x.relative_to(R).as_posix():sha(x) for x in sorted(paths)}
before=profile();art=inputs();env=os.environ.copy();env['APPDATA']=str(O/'veld-east-cargo-original-scratch');Path(env['APPDATA']).mkdir(exist_ok=True)
for name,data in [('profile-before',before),('inputs-before',art)]:(O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
t=time.monotonic()
with (O/'native.log').open('w',encoding='utf-8') as log:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_cargo_east_original_master_v2.gd','--resolution','760x600'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=90).returncode
after=profile();art_after=inputs();changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));log=(O/'native.log').read_text(encoding='utf-8');passed=code==0 and ',0 failures;' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and not changes and art==art_after
report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-t,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(art),'targetedInputsUnchanged':art==art_after,'scope':'Paired chronological held/unload/deposited idle/pickup/held, all sources at47/93/148, finite clocks/counts/root/ruler/exact held joins. Prescribed staged sprite player; not ordinary controller, world case ownership, save or final artistic acceptance.'}
for name,data in [('profile-after',after),('inputs-after',art_after),('validation',report)]:(O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report));print('\n'.join(log.splitlines()[-5:]));raise SystemExit(0 if passed else 1)
