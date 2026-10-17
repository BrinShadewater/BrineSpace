import hashlib,json,os,subprocess,tempfile
from pathlib import Path
root=Path.cwd();out=root/'character/james-west-carry-walk-keys-v1/north-unload-installed-rise-v364'
profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {str(f.relative_to(profile)):hashlib.sha256(f.read_bytes()).hexdigest() for f in profile.rglob('*') if f.is_file()}
before=fingerprint();scratch=Path(tempfile.mkdtemp(prefix='brine-james-normal-'));env=os.environ.copy();env['APPDATA']=str(scratch)
with (out/'normal.log').open('w',encoding='utf8') as log:
    code=subprocess.run(['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--path',str(root),'--script',str(out/'normal_probe.gd')],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300).returncode
after=fingerprint();delta=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
log=(out/'normal.log').read_text(errors='replace')
report={'exitCode':code,'scratch':str(scratch),'ownerUnchanged':not delta,'profileDelta':delta,'summary':[line for line in log.splitlines() if 'JAMES NORMAL' in line or 'ERROR:' in line]}
(out/'normal-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
