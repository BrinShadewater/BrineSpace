import os,hashlib,json,tempfile,shutil,subprocess,sys
from pathlib import Path
r=Path.cwd();o=r/'output/james-release-closeout-v365';f=o/'frozen-project';b=o/'deliverable';p=r/'character/james-west-carry-walk-keys-v1/release-build-review-v365'
assert json.loads((o/'build-validation.json').read_text())['exitCode']==0
profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fp():return {str(x.relative_to(profile)):hashlib.sha256(x.read_bytes()).hexdigest() for x in profile.rglob('*') if x.is_file()}
before=fp();scratch=Path(tempfile.mkdtemp(prefix='brine-james-release-'));env=os.environ.copy();env['APPDATA']=str(scratch)
retry='--retry-native' in sys.argv
empty=o/'audit-empty';empty.mkdir(exist_ok=True);qa=o/'native-qa';qa.mkdir(exist_ok=True)
for name in ['BrineSpace.exe','BrineSpace.pck','build_info.json']:
    if not retry:shutil.copy2(b/name,qa/name)
    else:
        assert hashlib.file_digest((b/name).open('rb'),'sha256').digest()==hashlib.file_digest((qa/name).open('rb'),'sha256').digest()
shutil.copy2(f/'assets/runtime-release.json',o/'expected-manifest.json')
fixture=r/'character/james-west-carry-walk-keys-v1/release-build-review-v351/release_smoke.gd';(qa/'override.cfg').write_text('[autoload]\nJamesReleaseSmoke="*'+fixture.as_posix()+'"\n')
results=[]
if retry:
    previous=json.loads((o/'release-validation.json').read_text());assert previous['checks'][0]['exitCode']==0
    results=[dict(previous['checks'][0],reused=True)]
    archive=o/'failed-native-start';archive.mkdir(exist_ok=True)
    for name in ['release-validation.json','native-release.log']:(archive/name).write_bytes((o/name).read_bytes())
try:
    command=['C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe','--headless','--path',str(empty),'--script',str(r/'tools/audit_release_assets.gd'),'--',str(b/'BrineSpace.pck'),str(o/'expected-manifest.json')]
    code=0
    if not retry:
        with (o/'asset-audit.log').open('w',encoding='utf8') as log:code=subprocess.run(command,env=env,cwd=empty,stdout=log,stderr=subprocess.STDOUT,timeout=600).returncode
        results.append({'check':'exact-packed-asset-audit','exitCode':code})
    if code==0:
        with (o/'native-release.log').open('w',encoding='utf8') as log:code=subprocess.run([str(qa/'BrineSpace.exe'),'--rendering-method','gl_compatibility'],env=env,cwd=qa,stdout=log,stderr=subprocess.STDOUT,timeout=600).returncode
        results.append({'check':'actual-release-new-game-saved-continue-f8','exitCode':code})
    user=scratch/'Godot/app_userdata/BrineSpace'
    for name in ['release-game.png','release-report.png','release-continue.png']:
        if (user/name).is_file():shutil.copy2(user/name,p/name)
finally:
    (qa/'override.cfg').unlink(missing_ok=True)
    after=fp();delta=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
    hashes={name:hashlib.file_digest((b/name).open('rb'),'sha256').hexdigest() for name in ['BrineSpace.exe','BrineSpace.pck']}
    logs={name:[x for x in (o/name).read_text(errors='replace').splitlines() if 'RELEASE ' in x or 'ERROR:' in x] for name in ['asset-audit.log','native-release.log'] if (o/name).exists()}
    report={'checks':results,'scratch':str(scratch),'realProfileUnchanged':not delta,'profileDelta':delta,'hashes':hashes,'logs':logs,'qaOverrideRemoved':not (qa/'override.cfg').exists()};(o/'release-validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True)
sys.exit(0 if all(x['exitCode']==0 for x in results) and len(results)==2 and not delta else 1)
