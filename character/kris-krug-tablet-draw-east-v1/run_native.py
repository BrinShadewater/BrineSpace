from pathlib import Path
import hashlib,json,os,subprocess,time

ROOT=Path(__file__).resolve().parent;REPO=ROOT.parent.parent
real=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {str(p.relative_to(real)):hashlib.sha256(p.read_bytes()).hexdigest() for p in real.rglob('*') if p.is_file() and p.suffix.lower()!='.log'} if real.exists() else {}
before=fingerprint();out=ROOT/'native/output';out.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['APPDATA']=str(ROOT/'native/scratch-appdata');env['KRIS_OUTPUT']=str(out)
started=time.monotonic()
with (out/'engine.log').open('w',encoding='utf-8') as log:
    run=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(REPO),'--rendering-method','gl_compatibility','--resolution','1024x640','-s','res://character/kris-krug-tablet-draw-east-v1/native/review.gd'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=40)
after=fingerprint();changed=[p for p in set(before)|set(after) if before.get(p)!=after.get(p)]
text=(out/'engine.log').read_text(encoding='utf-8',errors='replace');relevant=[s for s in text.splitlines() if 'KRIS_NATIVE' in s or 'ERROR' in s or 'Error' in s]
result={'engine_exit':run.returncode,'seconds':round(time.monotonic()-started,2),'scratch_appdata':env['APPDATA'],'owner_files_fingerprinted':len(before),'owner_files_changed':changed,'logged_errors':[s for s in relevant if 'KRIS_NATIVE' not in s]}
(out/'run-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result));print('\n'.join(relevant))
raise SystemExit(run.returncode or bool(changed) or bool(result['logged_errors']))
