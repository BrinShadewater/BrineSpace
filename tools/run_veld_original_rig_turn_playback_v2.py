from pathlib import Path
import os,json,hashlib,subprocess,sys,time
R=Path(__file__).resolve().parent.parent;P=R/'character/veld-turn-north-east-original-rig-v2';O=R/'output/veld-original-rig-turn-playback-v2';O.mkdir(exist_ok=True);assert not(O/'validation.json').exists(),'Preserve prior native interval'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def profile():
    p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return{x.relative_to(p).as_posix():sha(x) for x in p.rglob('*') if x.is_file() and 'logs' not in x.relative_to(p).parts}
paths={R/'scripts/crew_sprite_player.gd',R/'tests/test_veld_original_rig_turn_playback_v2.gd',R/'tests/test_veld_original_rig_turn_playback_v2.gd.uid',P/'registration.json'}
paths.update(R/ref for ref in json.loads((P/'registration.json').read_text(encoding='utf-8'))['bindings']);paths.update(P.glob('prompt-*.txt'));paths.update(P.glob('raw-*.png'))
for folder,glob in [(P,'*-manifest.json'),(R/'character/veld-turn-north-east-helmet-aligned-v3','*-manifest.json')]:
    for m in folder.glob(glob):
        paths.add(m)
        for state in json.loads(m.read_text(encoding='utf-8'))['states']:paths.update(R/ref[6:] for ref in state['frameFiles'])
def inputs():return{x.relative_to(R).as_posix():sha(x) for x in sorted(paths)}
before=profile();art=inputs();env=os.environ.copy();env['APPDATA']=str(O/'veld-gather-turn-chain-scratch');Path(env['APPDATA']).mkdir(exist_ok=True)
for name,data in [('profile-before',before),('inputs-before',art)]:(O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
t=time.monotonic()
with(O/'native.log').open('w',encoding='utf-8') as log:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/test_veld_original_rig_turn_playback_v2.gd','--resolution','760x600'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=90).returncode
after=profile();art_after=inputs();changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k));log=(O/'native.log').read_text(encoding='utf-8');passed=code==0 and ',0 failures;' in log and 'SCRIPT ERROR' not in log and 'ERROR:' not in log and not changes and art==art_after
report={'passed':passed,'returnCode':code,'seconds':round(time.monotonic()-t,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(art),'targetedInputsUnchanged':art==art_after,'scope':'Actual2.8s gather/turn/reverse/spread player chronology paired gear47/93/148. Corrected North endpoint and actual player gather/turn/reverse/spread exact boundaries. Original-rig whole turn interiors, count metadata and exact East held join checked; artistic smoothness, gait/world/save acceptance separate.'}
for name,data in [('profile-after',after),('inputs-after',art_after),('validation',report)]:(O/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report));print('\n'.join(log.splitlines()[-5:]));raise SystemExit(0 if passed else 1)
