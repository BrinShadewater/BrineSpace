from pathlib import Path
import os,json,hashlib,subprocess,sys,time
R=Path(__file__).resolve().parent.parent;P=R/'character/veld-turn-north-east-helmet-aligned-v3';O=R/'output/veld-north-east-helmet-aligned-v3';O.mkdir(exist_ok=True);assert not(O/'validation.json').exists(),'Preserve prior native interval'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def profile():
    p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return{x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
paths={R/'scripts/crew_sprite_player.gd',R/'tests/test_veld_north_east_helmet_aligned_v3.gd',R/'tests/test_veld_north_east_helmet_aligned_v3.gd.uid',P/'package_turn.py',P/'registration.json',P/'register_source.py'}
paths.update(R/ref for ref in json.loads((P/'registration.json').read_text())['bindings']);paths.update(P.glob('prompt-*.txt'));paths.update(P.glob('raw-*.png'))
for folder,glob in [(P,'*-manifest.json'),(R/'character/veld-turn-north-east-helmet-aligned-v2','*-manifest.json')]:
    for m in folder.glob(glob):
        paths.add(m)
        for state in json.loads(m.read_text())['states']:paths.update(R/ref[6:] for ref in state['frameFiles'])
def inputs():return{x.relative_to(R).as_posix():sha(x) for x in sorted(paths)}
before=profile();art=inputs();env=os.environ.copy();env['APPDATA']=str(O/'veld-helmet-yaw-v3-scratch');Path(env['APPDATA']).mkdir(exist_ok=True)
for name,data in [('profile-before',before),('inputs-before',art)]:(O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
t=time.monotonic()
with(O/'native.log').open('w',encoding='utf-8') as log:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_north_east_helmet_aligned_v3.gd','--resolution','760x600'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=90).returncode
after=profile();art_after=inputs();changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));log=(O/'native.log').read_text();passed=code==0 and ',0 failures;' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and not changes and art==art_after
report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-t,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(art),'targetedInputsUnchanged':art==art_after,'scope':'Actual finite sprite-player NE/EN turn chronology paired gear47/93/148. All bare body poses and gathered North/equipped East endpoints exact prior aliases. Whole helmet angular correction only; gait/gather/world/save acceptance separate.'}
for name,data in [('profile-after',after),('inputs-after',art_after),('validation',report)]:(O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(report));print('\n'.join(log.splitlines()[-5:]));raise SystemExit(0 if passed else 1)
