from pathlib import Path
import os,json,hashlib,subprocess,sys,time
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-west-kneel-motion-v2';P=R/'character/veld-library-closeout-v1/west-kneel-motion-v2'
O.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def profile():
 p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
 return {x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
paths={R/'scripts/crew_sprite_player.gd',R/'scripts/grid_canvas.gd',R/'character/ACTIVE_ASSETS.json',R/'tests/test_veld_west_kneel_motion_v2.gd',R/'tests/test_veld_west_kneel_motion_v2.gd.uid',Path(__file__),P/'FAMILY_REVIEW.json',P/'build_family.py'}
paths.update(R/name for name in json.loads((P/'FAMILY_REVIEW.json').read_bytes())['bindings'])
standing=R/'character/veld-library-closeout-v1/west-standing-family-v1'
paths.update([standing/'bare-manifest.json',standing/'helmet-manifest.json'])
paths.update(R/name for name in json.loads((standing/'FAMILY_REVIEW.json').read_bytes())['bindings'])

def inputs():return {x.relative_to(R).as_posix():sha(x) for x in sorted(paths)}
before=profile();art=inputs();env=os.environ.copy();env['APPDATA']=str(O/'veld-west-kneel-motion-scratch');Path(env['APPDATA']).mkdir(exist_ok=True)
for name,data in [('profile-before',before),('inputs-before',art)]: (O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
t=time.monotonic()
with (O/'native.log').open('w',encoding='utf-8') as log:
 code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_west_kneel_motion_v2.gd','--resolution','800x620'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
after=profile();final=inputs();changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));log=(O/'native.log').read_text(encoding='utf-8')
passed=code==0 and 'checks, 0 failures;' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and not changes and art==final
report=dict(passed=passed,returnCode=code,seconds=round(time.monotonic()-t,2),realProfileFileCount=len(before),realProfileChanges=changes,targetedInputCount=len(art),targetedInputsUnchanged=art==final,scope='Complete142source and1s lower/rise57poses per gear, native player/pixel/return/restore checks; not motion or normal admission; no normal selection/controller/root/contact/disk Continue acceptance.')
for name,data in [('profile-after',after),('inputs-after',final),('validation',report)]: (O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(report));print('\n'.join(log.splitlines()[-8:]));raise SystemExit(0 if passed else 1)
