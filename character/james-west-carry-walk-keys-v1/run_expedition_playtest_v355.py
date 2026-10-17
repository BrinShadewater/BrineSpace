import os,json,hashlib,tempfile,subprocess,shutil
from pathlib import Path
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1/release-expedition-playtest-v355';o=r/'output/james-release-closeout-v351';qa=o/'native-qa';out=r/'output/james-expedition-playtest-v355';out.mkdir(exist_ok=True)
profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fp():return {str(x.relative_to(profile)):hashlib.sha256(x.read_bytes()).hexdigest() for x in profile.rglob('*') if x.is_file()}
before=fp();scratch=Path(tempfile.mkdtemp(prefix='brine-james-release-'));env=os.environ.copy();env['APPDATA']=str(scratch)
expected=json.loads((o/'release-validation.json').read_text())['hashes']
for name,digest in expected.items():assert hashlib.file_digest((qa/name).open('rb'),'sha256').hexdigest()==digest
override=qa/'override.cfg';assert not override.exists();override.write_text('[autoload]\nJamesExpeditionPlaytest="*'+(p/'expedition_playtest.gd').as_posix()+'"\n')
try:
    with (out/'native.log').open('w',encoding='utf8') as log:code=subprocess.run([str(qa/'BrineSpace.exe')],cwd=qa,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=900).returncode
    source=scratch/'Godot/app_userdata/BrineSpace/expedition355'
    if source.exists():shutil.copytree(source,out/'captures',dirs_exist_ok=True)
finally:
    override.unlink(missing_ok=True)
    after=fp();delta=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
    log=(out/'native.log').read_text(errors='replace');report={'exitCode':locals().get('code',124),'scratch':str(scratch),'ownerUnchanged':not delta,'profileDelta':delta,'packageHashes':expected,'qaOverrideRemoved':not override.exists(),'summary':[x for x in log.splitlines() if 'JAMES ' in x or 'ERROR:' in x]};(out/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps({**report,"summary":report["summary"][:8],"errorCount":sum("ERROR:" in line for line in report["summary"])}))
