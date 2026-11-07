"""Real default lounge contact review; staged sprites and isolated profile only."""
from pathlib import Path
import os,sys,subprocess,json,hashlib,time,shutil
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'output/observation-sofa-depth-v1'
def fingerprint():
    profile=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {p.relative_to(profile).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in profile.rglob('*') if p.is_file() and 'logs' not in p.relative_to(profile).parts}
def main():
    godot=Path(sys.argv[1]);assert godot.is_file();OUT.mkdir(exist_ok=True)
    prior=[p for p in OUT.iterdir() if p.is_file()]
    if prior:
        archive=OUT/f'interval-before-{time.time_ns()}';archive.mkdir()
        for p in prior:shutil.copy2(p,archive/p.name)
    before=fingerprint();(OUT/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
    env=os.environ.copy();scratch=OUT/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
    started=time.monotonic();epoch=time.time()
    with (OUT/'native.log').open('w',encoding='utf-8') as log:
        try:code=subprocess.run([str(godot),'--path',str(ROOT),'--script','res://tests/test_observation_sofa.gd','--resolution','1280x900'],env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180).returncode
        except subprocess.TimeoutExpired:code=-1
    after=fingerprint();(OUT/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
    changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    log=(OUT/'native.log').read_text(encoding='utf-8');photo=OUT/'native.log'
    fresh=photo.exists() and photo.stat().st_mtime>=epoch
    runtime=code==0 and '0 failures' in log and not any(e in log for e in ['SCRIPT ERROR','ERROR:','Artwork unavailable:']) and fresh
    report={'passed':runtime and not changes,'runtimePassed':runtime,'returnCode':code,'seconds':round(time.monotonic()-started,2),'scratchAPPDATA':str(scratch),'realProfileFileCount':len(before),'realProfileChanges':changes,'freshLog':fresh}
    (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
    print('\n'.join(line for line in log.splitlines() if any(k in line for k in ['OBSERVATION SOFA','SCRIPT ERROR','ERROR:',' at:']))[-2000:])
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())

