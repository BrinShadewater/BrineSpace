"""Export the tested frozen James snapshot plus the installed North timing only."""
import hashlib,json,os,shutil,subprocess,tempfile,sys
from pathlib import Path
root=Path.cwd();old=root/'output/james-release-closeout-v351';out=root/'output/james-release-closeout-v365';out.mkdir(exist_ok=True)
frozen=out/'frozen-project'
if '--resume-copied' in sys.argv:
    assert frozen.exists() and not (out/'build-validation.json').exists()
else:
    assert not frozen.exists(),'Preserve an existing build; inspect it before any retry'
    print('Copying tested frozen project and its established import cache.',flush=True)
    shutil.copytree(old/'frozen-project',frozen)
changes=['character/james-cargo-north-v1/bare-manifest.json','character/james-cargo-north-v1/helmet-manifest.json','character/james-cargo-material-joined-v1/bare-manifest.json','character/james-cargo-material-joined-v1/helmet-manifest.json']
rows=[]
for name in changes:
    original=(old/'frozen-project'/name).read_bytes();replacement=(root/name).read_bytes()
    (frozen/name).write_bytes(replacement)
    rows.append({'path':name,'beforeSha256':hashlib.sha256(original).hexdigest(),'afterSha256':hashlib.sha256(replacement).hexdigest()})
installed=json.loads((root/'character/james-west-carry-walk-keys-v1/north-unload-installed-rise-v364/installation.json').read_text())
for field in ['sourceFrameHashes','joinedSourceFrameHashes']:
    for name,digest in installed[field].items():
        assert hashlib.sha256((frozen/name).read_bytes()).hexdigest()==digest,'Frozen artwork differs: '+name
(out/'frozen-inputs.json').write_text(json.dumps({'baseline':str(old/'frozen-project'),'frozenProject':str(frozen),'changes':rows,'originalArtworkVerified':180,'scope':'Physical V351 tested snapshot plus four paired North rise timing manifests only. Authoring registration is not a runtime dependency and is excluded. Established cache copied physically. No later shared UI/character runtime changes included.'},indent=2)+'\n')
profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():return {str(f.relative_to(profile)):hashlib.sha256(f.read_bytes()).hexdigest() for f in profile.rglob('*') if f.is_file()}
before=fingerprint();scratch=Path(tempfile.mkdtemp(prefix='brine-james-release-'));env=os.environ.copy();env['APPDATA']=str(scratch)
env['GIT_DIR']=subprocess.check_output(['git','rev-parse','--absolute-git-dir'],cwd=root,text=True).strip();env['GIT_WORK_TREE']=str(frozen);env['GIT_OPTIONAL_LOCKS']='0'
env['PATH']='C:/Python314'+os.pathsep+env['PATH']
print('Exporting the isolated James timing revision with the maintained exporter.',flush=True)
with (out/'build-driver.log').open('w',encoding='utf8') as log:
    code=subprocess.run(['powershell','-NoProfile','-File',str(frozen/'tools/export_release.ps1'),'-ProjectRoot',str(frozen),'-OutputPath',str(out/'deliverable/BrineSpace.exe')],cwd=frozen,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=1800).returncode
after=fingerprint();delta=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
report={'exitCode':code,'scratch':str(scratch),'ownerUnchanged':not delta,'profileDelta':delta,'changes':rows}
(out/'build-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'exitCode':code,'ownerUnchanged':not delta,'selectedChanges':len(rows)}),flush=True)
raise SystemExit(0 if code==0 and not delta else 1)
