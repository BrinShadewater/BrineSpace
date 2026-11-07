"""Focused existing death regressions; isolated profile, bounded logs."""
from pathlib import Path
import os,sys,json,hashlib,subprocess,time
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-sofa-fall-south-regressions-v1'
TESTS=[('test_veld_bunk_death.gd','VELD BUNK DEATH'),('test_veld_water_death_entry.gd','VELD LIVE WATER DEATH ENTRY'),('test_veld_lounge_partial_fall_north_native.gd','VELD PARTIAL LOUNGE NORTH FALL')]
def fingerprint():
    p=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {f.relative_to(p).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file() and 'logs' not in f.relative_to(p).parts}
def main():
    O.mkdir(exist_ok=True);before=fingerprint();results=[]
    frozen_paths=[R/p for p in ['scripts/veld_death_motion.gd','scripts/crew_sprite_player.gd','scripts/grid_canvas.gd','scripts/veld_npc.gd','scripts/run_save.gd']]+[R/'tests'/t[0] for t in TESTS]
    frozen={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen_paths}
    (O/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
    (O/'inputs-before.json').write_text(json.dumps(frozen,indent=2)+'\n',encoding='utf-8')
    for name,marker in TESTS:
        env=os.environ.copy();scratch=O/'scratch-appdata'/Path(name).stem;scratch.mkdir(parents=True,exist_ok=True);env['APPDATA']=str(scratch)
        log=O/(name+'.log');started=time.monotonic()
        with log.open('w',encoding='utf-8') as stream:
            try:code=subprocess.run([sys.argv[1],'--path',str(R),'--script','res://tests/'+name,'--resolution','1280x900'],env=env,stdout=stream,stderr=subprocess.STDOUT,timeout=600).returncode
            except subprocess.TimeoutExpired:code=-1
        text=log.read_text(encoding='utf-8');result={'test':name,'passed':code==0 and marker in text and '0 failures' in text and not any(x in text for x in ['ERROR:','SCRIPT ERROR','Artwork unavailable:']),'returnCode':code,'seconds':round(time.monotonic()-started,2),'logSha256':hashlib.sha256(log.read_bytes()).hexdigest()};results.append(result);print(json.dumps(result),flush=True)
        print('\n'.join(line for line in text.splitlines() if marker in line or 'ERROR' in line)[-1400:],flush=True)
    after=fingerprint();changes=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
    current={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in frozen_paths};inputs=[k for k in frozen if frozen[k]!=current[k]]
    (O/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n',encoding='utf-8');(O/'inputs-after.json').write_text(json.dumps(current,indent=2)+'\n',encoding='utf-8')
    report={'passed':all(r['passed'] for r in results) and not changes and not inputs,'results':results,'frozenInputCount':len(frozen),'frozenInputChanges':inputs,'realProfileFileCount':len(before),'realProfileChanges':changes}
    (O/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
