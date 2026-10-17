from pathlib import Path
import os,sys,json,subprocess,hashlib,time,shutil
R=Path.cwd();H=R/'character/veld-swim-carry-turn-matrix-coherent-v1';real=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace';probe='--probe' in sys.argv;suffix='native-narrow-v1' if probe else 'native-routes-v1'
def fp():return {str(p.relative_to(real)):hashlib.sha256(p.read_bytes()).hexdigest() for p in real.rglob('*') if p.is_file()}
previous=[H/(suffix+tail) for tail in ['.log','-checks.json'] if (H/(suffix+tail)).exists()]
if previous:
 archive=H/f'revisions/{suffix}-before-{time.time_ns()}';archive.mkdir(parents=True)
 for p in previous:shutil.copy2(p,archive/p.name)
b=fp();(H/(suffix+'-profile-before.json')).write_text(json.dumps(b,indent=2));env=os.environ.copy();env['APPDATA']=str(R/'output/veld-water-material-scratch-cargo-turn-routes-v1');Path(env['APPDATA']).mkdir(exist_ok=True)
command=['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(R),'-s','res://tools/review_veld_cargo_turn_routes_v1.gd']+(['--','--probe'] if probe else [])
with (H/(suffix+'.log')).open('w',encoding='utf-8') as log:
 try:code=subprocess.run(command,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120).returncode
 except subprocess.TimeoutExpired:code=-1
a=fp();s=(H/(suffix+'.log')).read_text(encoding='utf-8');errors=[x.strip() for x in s.splitlines() if x.startswith(('SCRIPT ERROR:','ERROR:'))];report={'exit_code':code,'engine_errors':errors,'real_profile_changed_files':[k for k in set(a)|set(b) if a.get(k)!=b.get(k)],'scratch_appdata':env['APPDATA'],'candidateLoadedExplicitly':True,'installed':False,'narrowProbe':probe};(H/(suffix+'-checks.json')).write_text(json.dumps(report,indent=2)+'\n');print('\n'.join(x for x in s.splitlines() if 'VELD CARGO TURN ROUTES' in x or x.startswith(('SCRIPT ERROR:','ERROR:')))[:2000]);print('real profile changes',len(report['real_profile_changed_files']));assert not errors and code==0 and not report['real_profile_changed_files']
