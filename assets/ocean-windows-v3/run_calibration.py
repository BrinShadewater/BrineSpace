"""Run the offline Godot texture exporter in a scratch profile."""
import hashlib,json,os,subprocess
from pathlib import Path
PACK=Path(__file__).resolve().parent
ROOT=PACK.parents[1]
owner=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def hashes():
    return {str(p.relative_to(owner)):hashlib.sha256(p.read_bytes()).hexdigest() for p in owner.rglob('*') if p.is_file()}
before=hashes()
env=os.environ.copy();env['APPDATA']=str(PACK/'scratch-appdata');env['BRINE_WINDOW_TEST']='isolated'
with (PACK/'calibration.log').open('w') as log:
    result=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--headless','--path',str(ROOT),'-s','res://tools/build_window_render_assets.gd'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=90)
after=hashes()
(PACK/'calibration-verification.json').write_text(json.dumps({'exit_code':result.returncode,'owner_unchanged':before==after,'changed':[k for k in before if k in after and before[k]!=after[k]],'added':[k for k in after if k not in before],'removed':[k for k in before if k not in after]},indent=2))
print((PACK/'calibration.log').read_text(errors='replace')[-1800:])
raise SystemExit(result.returncode)
