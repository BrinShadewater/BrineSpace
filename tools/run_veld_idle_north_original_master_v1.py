from pathlib import Path
import os,json,hashlib,subprocess,sys,time
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-idle-north-original-master-v1';P=R/'character/veld-idle-north-original-master-v1'
O.mkdir(exist_ok=True);assert not (O/'validation.json').exists(),'Preserve prior interval'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def profile():
 p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
paths={R/'scripts/crew_sprite_player.gd',R/'tests/test_veld_idle_north_original_master_v1.gd',P/'build.py',P/'registration.json'}
registration=json.loads((P/'registration.json').read_text())
paths.update(R/(ref[6:] if ref.startswith('res://') else ref) for ref in registration['bindings'])
for folder in [P,R/'character/veld-cardinal-actions-shared-original-helmet-v1']:
 for manifest in folder.glob('*manifest.json'):
  paths.add(manifest)
  for state in json.loads(manifest.read_text())['states']:paths.update(R/ref[6:] for ref in state['frameFiles'])
paths.update([P/'raw-clean-master-v1.png',P/'build_clean_master.py',P/'clean-master-reference.json',P/'execution-clean-master-v1.json',P/'execution-idle-v3.json',P/'raw-idle-v1.png',P/'raw-idle-v2.png',P/'prompt-clean-master-v1.txt',P/'prompt-idle-v1.txt',P/'prompt-idle-v2.txt',P/'prompt-idle-v3.txt',R/'character/veld-cargo-turns-master-family-v1/original-north-identity-reference.png'])
def inputs():return {x.relative_to(R).as_posix():sha(x) for x in sorted(paths)}
before=profile();art=inputs();env=os.environ.copy();env['APPDATA']=str(O/'veld-north-idle-scratch');Path(env['APPDATA']).mkdir(exist_ok=True)
for name,d in [('profile-before',before),('inputs-before',art)]: (O/f'{name}.json').write_text(json.dumps(d,indent=2)+'\n')
t=time.monotonic()
with (O/'native.log').open('w',encoding='utf-8') as log:
 code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_idle_north_original_master_v1.gd','--resolution','760x600'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
after=profile();art_after=inputs();changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));log=(O/'native.log').read_text(encoding='utf-8')
passed=code==0 and ',0 failures;' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and not changes and art==art_after
report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-t,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(art),'targetedInputsUnchanged':art==art_after,'scope':'North original-guided prepared-master idle with four breathing poses, six North states/both gears, explicit-modulo elapsed source clocks and exact idle/cargo/action source joins. No controller/world/save/case lifetime acceptance.'}
for name,d in [('profile-after',after),('inputs-after',art_after),('validation',report)]: (O/f'{name}.json').write_text(json.dumps(d,indent=2)+'\n')
print(json.dumps(report));print('\n'.join(log.splitlines()[-5:]));raise SystemExit(0 if passed else 1)
