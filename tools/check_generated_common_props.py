"""Run the generated-common native integration fixture with isolated saves and fingerprints."""
import os,json,hashlib,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/"output/generated-common-install-2026-09-27"
out.mkdir(parents=True,exist_ok=True)
owner=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {p.relative_to(owner).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(owner.rglob('*')) if p.is_file()}
before=fingerprint()
(out/'owner-before.json').write_text(json.dumps(before,indent=2))
env=os.environ.copy()
env['APPDATA']=str(out/'scratch/roaming')
env['LOCALAPPDATA']=str(out/'scratch/local')
env['BRINE_COMMON_TEST']='isolated'
Path(env['APPDATA']).mkdir(parents=True,exist_ok=True)
Path(env['LOCALAPPDATA']).mkdir(parents=True,exist_ok=True)
godot='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe'
code=1
try:
    with (out/'native.log').open('w',encoding='utf-8') as log:
        proc=subprocess.run([godot,'--path',str(root),'--script','res://tests/test_generated_common_props.gd'],cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=240)
        code=proc.returncode
finally:
    after=fingerprint()
    (out/'owner-after.json').write_text(json.dumps(after,indent=2))
    print('Owner profile unchanged:',before==after)
    text=(out/'native.log').read_text(encoding='utf-8',errors='replace')
    for line in text.splitlines():
        if any(s in line for s in ['ERROR','Error','rotation','GENERATED COMMON']):print(line[:400])
    print('Exit:',code,'Log:',out/'native.log')
    if 'SCRIPT ERROR' in text or 'ERROR:' in text or 'GENERATED COMMON PROPS:' not in text:code=1
sys.exit(code)
