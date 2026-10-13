"""Isolated supported settling audit plus held-bunk/water mortality regressions."""
from pathlib import Path
import os,sys,json,hashlib,time,subprocess,shutil
R=Path(__file__).resolve().parent.parent;O=R/'output/veld-bunk-body-settle-v1'
def fingerprint():
    root=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
    return {p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and 'logs' not in p.relative_to(root).parts}
def main():
    O.mkdir(exist_ok=True)
    prior=[p for p in O.iterdir() if p.is_file()]
    if prior:
        archive=O/f'interval-before-{time.time_ns()}';archive.mkdir()
        for p in prior:shutil.copy2(p,archive/p.name)
    inputs=[R/p for p in ['scripts/veld_npc.gd','scripts/veld_death_motion.gd','scripts/crew_life.gd','scripts/crew_sprite_player.gd','tests/test_veld_bunk_body_settle.gd','tests/test_veld_bunk_body_settle_held.gd','tests/test_veld_water_death_entry.gd','character/veld-bunk-body-master-v1/bare-manifest.json','character/veld-bunk-body-master-v1/helmet-manifest.json']]+list((R/'character/veld-bunk-body-master-v1/frames').rglob('*.png'))
    bound={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
    (O/'inputs-before.json').write_text(json.dumps(bound,indent=2)+'\n')
    before=fingerprint();(O/'profile-before.json').write_text(json.dumps(before,indent=2)+'\n')
    env=os.environ.copy();scratch=O/'scratch-appdata';scratch.mkdir(exist_ok=True);env['APPDATA']=str(scratch)
    started=time.monotonic();epoch=time.time();runs=[]
    for name,test,headless,marker in [('native','test_veld_bunk_body_settle',False,'80 partial actor deaths,320 actor-file restores'),('held-regression','test_veld_bunk_body_settle_held',False,'8actual deaths,32source/restore samples'),('water-regression','test_veld_water_death_entry',True,'64 oxygen deaths')]:
        launch=[sys.argv[1],'--path',str(R),'--script',f'res://tests/{test}.gd']+(['--headless'] if headless else ['--resolution','1280x900'])
        t=time.monotonic()
        with (O/f'{name}.log').open('w',encoding='utf-8') as log:
            try:code=subprocess.run(launch,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=300).returncode
            except subprocess.TimeoutExpired:code=-1
        text=(O/f'{name}.log').read_text(encoding='utf-8');passed=code==0 and '0 failures' in text and marker in text and not any(e in text for e in ['SCRIPT ERROR','ERROR:','Artwork unavailable:'])
        runs.append({'name':name,'code':code,'passed':passed,'seconds':round(time.monotonic()-t,2)})
        print(name,code,passed,flush=True)
        if not passed:break
    after=fingerprint();(O/'profile-after.json').write_text(json.dumps(after,indent=2)+'\n')
    after_inputs={p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs};(O/'inputs-after.json').write_text(json.dumps(after_inputs,indent=2)+'\n')
    changes=sorted(k for k in before.keys()|after.keys() if before.get(k)!=after.get(k))
    fresh=(O/'records.json').exists() and (O/'records.json').stat().st_mtime>=epoch
    report={'passed':len(runs)==3 and all(r['passed'] for r in runs) and not changes and bound==after_inputs and fresh,'runs':runs,'seconds':round(time.monotonic()-started,2),'realProfileFileCount':len(before),'realProfileChanges':changes,'targetedInputCount':len(bound),'targetedInputsUnchanged':bound==after_inputs,'freshRecords':fresh,'scratchAPPDATA':str(scratch)}
    (O/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
    for run in runs:
        text=(O/f'{run["name"]}.log').read_text(encoding='utf-8')
        print('\n'.join(line for line in text.splitlines() if any(k in line for k in ['VELD BUNK BODY','VELD LIVE WATER DEATH ENTRY','SCRIPT ERROR','ERROR:']))[-1600:])
    return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
