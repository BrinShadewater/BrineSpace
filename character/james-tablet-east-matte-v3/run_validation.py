import os,json,hashlib,tempfile,shutil,subprocess,sys
from pathlib import Path
root=Path.cwd();out=Path(sys.argv[1]); profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fp():return {str(p.relative_to(profile)):hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file()}
before=fp();scratch=Path(tempfile.mkdtemp(prefix='brine-james-native-'));env=os.environ.copy();env['APPDATA']=str(scratch)
if (profile/'room_layouts.json').exists():
 d=scratch/'Godot/app_userdata/BrineSpace';d.mkdir(parents=True);shutil.copy2(profile/'room_layouts.json',d/'room_layouts.json')
name=sys.argv[2];cmd=['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(root),'-s','res://'+out.as_posix()+'/'+name+'.gd','--rendering-method','gl_compatibility']
log_path=out/(name+'.log')
timed_out=False
with log_path.open('w',encoding='utf8') as stream:
 proc=subprocess.Popen(cmd,env=env,stdout=stream,stderr=subprocess.STDOUT)
 try: code=proc.wait(timeout=1800)
 except subprocess.TimeoutExpired:
  timed_out=True;proc.kill();proc.wait();code=124
log=log_path.read_text(encoding='utf8',errors='replace');after=fp();delta=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
report={'exitCode':code,'timedOut':timed_out,'scratch':str(scratch),'realProfileUnchanged':not delta,'profileDelta':delta,'summary':[x for x in log.splitlines() if 'JAMES ' in x or 'ERROR:' in x]};(out/(name+'-validation.json')).write_text(json.dumps(report,indent=2));print(json.dumps(report));sys.exit(code)

