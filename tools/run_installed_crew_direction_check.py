from pathlib import Path
import os,hashlib,json,subprocess
p=Path('character/crew-installed-direction-check-v1');p.mkdir(exist_ok=True);o=Path('output/crew-installed-direction-check-v1');o.mkdir(parents=True,exist_ok=True);real=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fp():return {str(f.relative_to(real)):hashlib.sha256(f.read_bytes()).hexdigest() for f in real.rglob('*') if f.is_file()}
before=fp();env=os.environ.copy();env['APPDATA']=str((o/'appdata').resolve());Path(env['APPDATA']).mkdir(exist_ok=True)
try:
 with (o/'native.log').open('w') as log:r=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(Path.cwd()),'-s','tools/preview_installed_crew_directions.gd'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=100)
finally:
 after=fp();(o/'owner-before.json').write_text(json.dumps(before));(o/'owner-after.json').write_text(json.dumps(after));print('Owner profile unchanged:',before==after)
print('Native exit:',r.returncode)
