from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-carry-cardinal-natural-v2'
d=json.loads((O/'journeys.json').read_text());v=json.loads((O/'validation.json').read_text());assert v['passed'] and d['failures']==0
banks=['bill-carry-east-gait-v3','bill-carry-start-east-v4','bill-carry-south-gait-v2','bill-carry-start-south-v1','bill-carry-west-gait-v2','bill-carry-start-west-v2','bill-carry-north-gait-v1','bill-carry-start-north-v1','bill-carry-turn-identity-matrix-v5','bill-unload-north-rise-v1']
catalog={};inputs={}
for gear in ['bare','helmet']:
 catalog[gear]={}
 for bank in banks:
  f=R/f'character/{bank}/{gear}-manifest.json';inputs[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
  for s in json.loads(f.read_text())['states']:
   catalog[gear][s['id']]=s['frameFiles']
checks=0;proof=[]
def check(ok,message):
 global checks
 checks+=1
 assert ok,message
for j in d['journeys']:
 gear='helmet' if j['helmet'] else 'bare';plan=j['arrivalPlan'];seen=set();records=j['records'];arrival=next(i for i,r in enumerate(records) if r['stage']=='workshop_unload');foot=records[arrival]['foot'];observed=0
 check(Image.open(O/records[arrival-1]['source']).tobytes()==Image.open(O/records[arrival]['source']).tobytes(),'Exact prior source at actual arrival')
 check(abs(plan['until']-plan['unload_started']-2)<1e-8,'Original2s budget')
 for r in records:
  if r['stage']=='workshop_unload':check(r['foot']==foot,'Physical root remains planted after arrival')
  slot=r.get('stowRow',-1)
  if slot<0:continue
  row=plan['rows'][slot];path=R/catalog[gear][row['key']][row['index']].removeprefix('res://');source=Image.open(path).convert('RGBA');actual=Image.open(O/r['source']).convert('RGBA');check(np.array_equal(np.array(source),np.array(actual)),'Actual submitted program source exactly equals latest bound source');seen.add(slot);observed+=1;inputs[path.relative_to(R).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
 check(len(seen)==len(plan['rows']),'Every program row submitted')
 check({c['stowRow'] for c in j['captures'] if c.get('stowRow',-1)>=0}==seen,'Every program row has native/source capture')
 complete=next(r['time'] for r in records[arrival:] if r['stage']!='workshop_unload');duration=complete-records[arrival]['time'];expected=plan['until']-plan['started'];check(abs(duration-expected)<1/30,'Native timer agrees within60Hz boundary')
 proof.append({'gear':gear,'programRows':len(seen),'exactRecordedSourceSelections':observed,'settleAndYawSeconds':plan['unload_started']-plan['started'],'unloadBudgetSeconds':2,'observedStageSeconds':duration,'targetFoot':foot,'all14RiseRows':j['unloadSlots']})
(P/'validation.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'Actual recorded source agreement, native program-row coverage, physical root and stage timer; not anatomical stance-lock, interruptions or save admission','journeys':proof,'sourceHashes':inputs},indent=2)+'\n');print('CARDINAL NATURAL STOW:',checks,'independent source/root/clock checks pass')
