from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;O=R/'output/bill-carry-east-start-station-v4'
d=json.loads((O/'journeys.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'));assert v['passed'] and not d['failures']
rows=[]
from PIL import Image
import numpy as np
exact=0
for j in d['journeys']:
 if not j['candidate']:continue
 gear='helmet' if j['helmet'] else 'bare'
 records=j['records'];starttime=next(r['time'] for r in records if r['starting'])
 for r in records:
  bank=None
  if r['starting']:
   clock=0
   for sl,dt in enumerate([40,50,55,65,65,45]):
    clock+=dt
    if (r['time']-starttime)*1000<clock:break
   bank=P/f'frames/{gear}/carry-start-east/{sl:03}.png'
  elif r['slot']>=0:bank=R/f'character/bill-carry-east-gait-v3/frames/{gear}/carry-east/{r["slot"]:03}.png'
  if bank is not None:
   assert np.array_equal(np.array(Image.open(bank)),np.array(Image.open(O/r['sourceCapture'])));exact+=1
 indices=[i for i in range(1,len(records)-1) if records[i-1]['starting'] and not records[i]['starting']];assert len(indices)==1
 i=indices[0];last=records[i-1];join=records[i];next_record=records[i+1]
 assert join['slot']==0 and abs(join['phase']-.104)<.00001 and next_record['slot']==1
 assert (O/last['sourceCapture']).read_bytes()==(O/join['sourceCapture']).read_bytes()
 start_index=next(n for n,r in enumerate(records) if r['starting']);assert start_index>0 and records[start_index-1]['turning']
 assert (O/records[start_index-1]['sourceCapture']).read_bytes()==(O/records[start_index]['sourceCapture']).read_bytes()
 rows.append({'exactLastTurnToFirstBridgeBytes':True,'helmet':j['helmet'],'exactLastBridgeToFirstGaitBytes':True,'resumePhase':join['phase'],'nextFrameSlot':next_record['slot'],'nextFrameSeconds':next_record['time']-join['time'],'gaitCycles':j['completeGaitCycles'],'sourceStancePixelsUnchanged':True})
e={'scope':'Actual60Hz recorded source bytes and next-frame gait progression at prescribed workshop join. Does not prove anatomical foot lock or snapshot lifecycle.','passed':True,'exactRecordedSourceSelections':exact,'joins':rows,'journeysSha256':hashlib.sha256((O/'journeys.json').read_bytes()).hexdigest()}
(P/'join-diagnostic.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8');print('Verified both exact contact joins and next16.67ms passing poses')
