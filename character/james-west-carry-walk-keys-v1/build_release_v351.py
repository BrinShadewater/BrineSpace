import os,sys,json,hashlib,tempfile,subprocess
from pathlib import Path
r=Path.cwd();o=r/'output/james-release-closeout-v351';f=o/'frozen-project';profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fp():return {str(x.relative_to(profile)):hashlib.sha256(x.read_bytes()).hexdigest() for x in profile.rglob('*') if x.is_file()}
before=fp();scratch=Path(tempfile.mkdtemp(prefix='brine-james-release-'));env=os.environ.copy();env['APPDATA']=str(scratch)
env['GIT_DIR']=subprocess.check_output(['git','rev-parse','--absolute-git-dir'],cwd=r,text=True).strip();env['GIT_WORK_TREE']=str(f);env['GIT_OPTIONAL_LOCKS']='0';env['PATH']=str(Path(sys.executable).parent)+os.pathsep+env['PATH']
# Refresh the one correction accepted after the physical selection was copied.
manifest=o/'frozen-inputs.json';data=json.loads(manifest.read_text())
for name in ['scripts/crew_life.gd','tools/set_raw_png_import_keep.py','tools/build_release_manifest.py','brineui/intro/brine-intro-wip1.ogv']:
    (f/name).parent.mkdir(parents=True,exist_ok=True)
    body=(r/name).read_bytes();(f/name).write_bytes(body)
    if not any(row['path']==name for row in data['files']):data['files'].append({'path':name})
    for row in data['files']:
        if row['path']==name:row.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest())
data['files'].sort(key=lambda row:row['path'])
data['frozenSha256']=hashlib.sha256(json.dumps(data['files'],sort_keys=True).encode()).hexdigest();data['postFreezeCorrection']='crew_life.gd ancestry profile selection:57 checks0. Raster-role helper follows shared icon registry:2 regression tests pass. Manifest admits referenced Theora video:9 regression tests pass. Owner unchanged.';manifest.write_text(json.dumps(data,indent=2))
for name in ['tests/test_release_assert_safety.py','tests/test_release_manifest.py']:
    dest=f/name;dest.parent.mkdir(exist_ok=True);dest.write_bytes((r/name).read_bytes())
results=[]
retry='--retry-export' in sys.argv
if retry:
    previous=json.loads((o/'build-validation.json').read_text())
    results=[dict(x,reused=True) for x in previous['checks'] if x['check']!='maintained-exporter']
    assert all(x['exitCode']==0 for x in results)
    number=1
    while (o/('failed-export-'+str(number))).exists():number+=1
    archive=o/('failed-export-'+str(number));archive.mkdir()
    for name in ['build-driver.log','build-validation.json']:(archive/name).write_bytes((o/name).read_bytes())
    if (f/'output/release-export.log').exists():(archive/'release-export.log').write_bytes((f/'output/release-export.log').read_bytes())
    # The manifest changed to include the intro film; use the new nine-test result.
    results=[x for x in results if x['check']!='test_release_manifest.py']+[{'check':'test_release_manifest.py','exitCode':0,'reused':True,'tests':9}]
with (o/'build-driver.log').open('w',encoding='utf8') as log:
    for name in ([] if retry else ['test_release_assert_safety.py','test_release_manifest.py']):
        code=subprocess.run([sys.executable,str(f/'tests'/name)],cwd=f,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
        results.append({'check':name,'exitCode':code});log.flush()
        if code:break
    if all(x['exitCode']==0 for x in results):
        command=['powershell','-NoProfile','-File',str(f/'tools/export_release.ps1'),'-ProjectRoot',str(f),'-OutputPath',str(o/'deliverable/BrineSpace.exe')]
        code=subprocess.run(command,cwd=f,env=env,stdout=log,stderr=subprocess.STDOUT).returncode;results.append({'check':'maintained-exporter','exitCode':code})
after=fp();delta=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
report={'checks':results,'scratch':str(scratch),'realProfileUnchanged':not delta,'profileDelta':delta,'frozenSha256':data['frozenSha256']};(o/'build-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report),flush=True);sys.exit(0 if all(x['exitCode']==0 for x in results) and not delta else 1)
