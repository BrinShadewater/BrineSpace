"""Run one Margot check with isolated APPDATA and verify the real profile is untouched."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/margot-polish-native';OUT.mkdir(parents=True,exist_ok=True)
label=sys.argv[1]
if not label.replace('-','').isalnum():raise SystemExit('Invalid label')
real=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {str(p.relative_to(real)):hashlib.sha256(p.read_bytes()).hexdigest() for p in real.rglob('*') if p.is_file()} if real.exists() else {}
before=fingerprint();env=os.environ.copy();scratch=OUT/'appdata'/label
env['APPDATA']=str(scratch);dest=scratch/'Godot/app_userdata/BrineSpace';dest.mkdir(parents=True,exist_ok=True)
if (real/'room_layouts.json').exists():shutil.copy2(real/'room_layouts.json',dest/'room_layouts.json')
godot=env.get('BRINE_GODOT','C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe')
log=OUT/(label+'.log');code=1
try:
    with log.open('w',encoding='utf-8') as output:
        run=subprocess.run([godot,'--path',str(ROOT),*sys.argv[2:]],env=env,stdout=output,stderr=subprocess.STDOUT,timeout=240)
        code=run.returncode
finally:
    after=fingerprint();unchanged=before==after
    changed=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)]
    progress_unchanged=not any(Path(p).parts[0]!='logs' for p in changed)
    (OUT/(label+'-profile-check.json')).write_text(json.dumps({'unchanged':unchanged,'progressUnchanged':progress_unchanged,'changed':changed,'before':before,'after':after},indent=2),encoding='utf-8')
    print('Real saved progress unchanged:',progress_unchanged,'all profile files unchanged:',unchanged,'exit:',code)
    if not progress_unchanged:raise SystemExit('Real saved data changed during test; inspect saved fingerprints')
lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
for line in [s for s in lines if any(k in s for k in ['ERROR','SCRIPT','PASS','FAIL','failures='])][:18]:print(line)
print('Log:',log)
raise SystemExit(code)
