from pathlib import Path
import os,subprocess,json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[1]
real=Path(os.environ['APPDATA'])/'Godot/app_userdata/BrineSpace'
def fingerprint():
    return {str(f.relative_to(real)):hashlib.sha256(f.read_bytes()).hexdigest() for f in real.rglob('*') if f.is_file()}
before=fingerprint();(P/'owner-before.json').write_text(json.dumps(before,indent=2))
scratch=ROOT/'output/crew-walk-v2-isolated';scratch.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['APPDATA']=str(scratch)
godot='C:/Users/Alex/Desktop/Projects/Godot_v4.7.2/Godot_v4.7.2-stable_win64.exe'
results=[]
try:
    for name,native in [('test_crew_walk_v2',False),('test_veld_walk_integration',False),('playtest_crew_walk_v2',True),('playtest_crew_walk_v2_station',True)]:
        cmd=[godot,'--path',str(ROOT),'--script','res://tests/'+name+'.gd']
        if not native:cmd.insert(1,'--headless')
        with (P/(name+'.log')).open('w') as log:
            r=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=180)
        text=(P/(name+'.log')).read_text(errors='replace');errors=[line for line in text.splitlines() if 'Error' in line or 'ERROR' in line or 'FAIL' in line or 'CREW WALK' in line or 'VELD WALK' in line]
        results.append(dict(test=name,returncode=r.returncode,summary=errors));print(results[-1],flush=True)
        if r.returncode:break
finally:
    after=fingerprint();changed=[k for k in before.keys()|after.keys() if before.get(k)!=after.get(k)]
    (P/'owner-after.json').write_text(json.dumps(after,indent=2));(P/'test-results.json').write_text(json.dumps(dict(tests=results,ownerProfileChanges=changed),indent=2));print('Owner profile changed files:',changed,flush=True)
