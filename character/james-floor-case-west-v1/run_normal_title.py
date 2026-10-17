from pathlib import Path
import os,json,hashlib,tempfile,subprocess,shutil
from PIL import Image
r=Path.cwd();p=r/'character/james-floor-case-west-v1'
profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fp():return {str(f.relative_to(profile)):hashlib.sha256(f.read_bytes()).hexdigest() for f in profile.rglob('*') if f.is_file()}
before=fp()
guard=json.loads((p/'normal_checkpoint_probe-validation.json').read_bytes())
assert guard['exitCode']==0 and guard['realProfileUnchanged']
source_root=Path(guard['scratch'])/'Godot/app_userdata/BrineSpace'
assert 'brine-james-native-' in str(source_root)
cases={}
for mode in ['bare','helmet']:
    for phase in ['before','after','midpoint','terminal','idle']:
        label=mode+'-normal-checkpoint-v1-'+phase
        source=p/'arrival-captures'/(label+'-saved-source.png')
        # Godot's binding hashes hexadecimal raw RGBA, then SHA256 of that text.
        rgba=hashlib.sha256(Image.open(source).convert('RGBA').tobytes().hex().encode()).hexdigest()
        disk=source_root/(label+'.save')
        cases[label]={'save':str(disk),'sha256':hashlib.sha256(disk.read_bytes()).hexdigest(),'sourceRgba':rgba}
spec={'cases':cases,'frozen':{str(f.relative_to(r)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [p/'normal_title_continue.gd',r/'scripts/main.gd',r/'scripts/grid_canvas.gd',r/'scripts/run_save.gd',r/'scripts/james_cargo_actor.gd',r/'scripts/james_cargo_player.gd',r/'scripts/james_cargo_workshop.gd',r/'scripts/james_cargo_checkpoint.gd']}}
(p/'normal-title-inputs.json').write_text(json.dumps(spec,indent=2)+'\n')
results=[]
for label,item in cases.items():
    scratch=Path(tempfile.mkdtemp(prefix='brine-james-native-'))
    user=scratch/'Godot/app_userdata/BrineSpace';user.mkdir(parents=True)
    shutil.copy2(item['save'],user/'brine_loop.save')
    if (profile/'room_layouts.json').exists():shutil.copy2(profile/'room_layouts.json',user/'room_layouts.json')
    env=os.environ.copy();env['APPDATA']=str(scratch)
    cmd=['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(r),'-s','res://character/james-floor-case-west-v1/normal_title_continue.gd','--rendering-method','gl_compatibility','--',label]
    with (p/(label+'-title.log')).open('w',encoding='utf8') as log:
        proc=subprocess.Popen(cmd,env=env,stdout=log,stderr=subprocess.STDOUT)
        try:code=proc.wait(timeout=300)
        except subprocess.TimeoutExpired:proc.kill();proc.wait();code=124
    after=fp()
    delta=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
    entry={'label':label,'exitCode':code,'scratch':str(scratch),'realProfileUnchanged':not delta,'profileDelta':delta}
    results.append(entry)
    (p/'normal-title-validation.json').write_text(json.dumps({'results':results},indent=2)+'\n')
    print(json.dumps(entry),flush=True)
    if code or delta:raise SystemExit(code or 2)
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in spec['frozen'].items())
assert all(hashlib.sha256(Path(c['save']).read_bytes()).hexdigest()==c['sha256'] for c in cases.values())
print('Ten fresh engine/title Continue cases complete; frozen inputs and owner profile unchanged.',flush=True)
