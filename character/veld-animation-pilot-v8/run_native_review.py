"""Native probe wrapper: isolate APPDATA and fingerprint the real profile."""
from pathlib import Path
import os,hashlib,json,subprocess
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
REAL=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {str(p.relative_to(REAL)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(REAL.rglob('*')) if p.is_file()} if REAL.exists() else {}
before=fingerprint()
scratch=HERE/'native-review/scratch-appdata';scratch.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['APPDATA']=str(scratch)
with (HERE/'native-review/native.log').open('w') as log:
    result=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(ROOT),'--rendering-method','gl_compatibility','-s','res://tools/review_veld_pilot.gd','--','--v8'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120)
after=fingerprint()
report={'returncode':result.returncode,'profile_unchanged':before==after,'profile_files_before':len(before),'profile_files_after':len(after),'changed_paths':[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]}
(HERE/'native-review/isolation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
assert before==after,'Real profile changed during isolated probe; inspect evidence.'
raise SystemExit(result.returncode)
