from pathlib import Path
import json,shutil
P=Path(__file__).resolve().parent
records=[];checks=0;captures=0;guards=[]
out=P/'continue-native';out.mkdir(exist_ok=True)
for label in ['bare','helmet']:
    e=json.loads((P/f'continue-{label}-evidence.json').read_text());v=json.loads((P/f'continue-{label}-validation.json').read_text())
    assert e['failures']==0 and v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
    checks+=e['checks'];captures+=e['captures'];guards.append(v)
    for r in e['records']:
        filename=Path(r['capture']).name;shutil.copy2(P/f'continue-{label}-native'/filename,out/filename)
        r['capture']='res://character/james-seated-read-phases-v1/continue-native/'+filename;records.append(r)
(P/'continue-evidence.json').write_text(json.dumps({'checks':checks,'failures':0,'captures':captures,'records':records,'scope':'Two bounded three-case native gear lanes; actual fresh scene disk Continue at partial draw, held reading and interrupted held-to-stow. Combined original six-case job timed out before final completion and remains archived; not treated as success.'},indent=2))
(P/'continue-validation.json').write_text(json.dumps({'exitCode':0,'timedOut':False,'realProfileUnchanged':True,'profileDelta':[],'laneGuards':guards},indent=2))
print(json.dumps({'checks':checks,'captures':captures,'terminalLanes':len(guards)}))
