from pathlib import Path
import os,json,hashlib,subprocess,sys,time
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-east-grounded-flat-probe-v1';P=R/'character/veld-carry-east-original-master-v1/standing-step-video-v4-grounded'
O.mkdir(exist_ok=True);assert not (O/'validation.json').exists(),'Preserve prior interval'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def profile():
 p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
paths={R/'scripts/crew_sprite_player.gd',R/'tests/test_veld_east_grounded_flat_probe_v1.gd',R/'tests/test_veld_east_grounded_flat_probe_v1.gd.uid',Path(__file__),P/'full-source-record.json',P/'build_source_clip.py',P/'refined-flat-phase-study.json',P/'support-window-diagnostic.json',P/'audit_support_windows.py',P/'refined-flat-sole-diagnostic.json'}
bindings=json.loads((P/'full-source-record.json').read_text(encoding='utf-8'))['bindings'];paths.update(R/name for name in bindings)
for manifest in P.glob('*-phase-manifest.json'):
 paths.add(manifest)
 for state in json.loads(manifest.read_text(encoding='utf-8'))['states']:paths.update(R/ref[6:] for ref in state['frameFiles'])
def inputs():return {x.relative_to(R).as_posix():sha(x) for x in sorted(paths)}
before=profile();art=inputs();env=os.environ.copy();env['APPDATA']=str(O/'veld-east-grounded-flat-scratch');Path(env['APPDATA']).mkdir(exist_ok=True)
for name,d in [('profile-before',before),('inputs-before',art)]: (O/f'{name}.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
t=time.monotonic()
with (O/'native.log').open('w',encoding='utf-8') as log:
 code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_east_grounded_flat_probe_v1.gd','--resolution','900x620'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
after=profile();art_after=inputs();changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));log=(O/'native.log').read_text(encoding='utf-8')
passed=code==0 and ',0 failures;' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and not changes and art==art_after
report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-t,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(art),'targetedInputsUnchanged':art==art_after,'scope':'Actual distance-driven full21-pose two-cycle two-hypothesis stride trial, both gears/three scales. No final rigid contact/stride/start-stop or normal integration acceptance.'}
for name,d in [('profile-after',after),('inputs-after',art_after),('validation',report)]: (O/f'{name}.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report));print('\n'.join(log.splitlines()[-5:]));raise SystemExit(0 if passed else 1)
