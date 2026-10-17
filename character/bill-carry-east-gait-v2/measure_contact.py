"""Diagnostic sole projection from recorded production movement, not bone identity proof."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;source=R/'output/bill-carry-east-station-v2/journeys.json'
d=json.loads(source.read_text(encoding='utf-8'));j=next(j for j in d['journeys'] if j['candidate'] and not j['helmet']);scale=384*.17/148
rows=[];samples=[]
for slot in [0,1,2]:
 file=P/f'frames/bare/carry-east/{slot:03}.png';a=np.array(Image.open(file));xs=np.where((a[222:225,:,3]>180).any(0))[0];center=(float(xs.min())+float(xs.max()))/2
 record=next(r for r in j['records'] if r['slot']==slot);rows.append({'slot':slot,'soleBandX':[int(xs.min()),int(xs.max())],'centerX':center,'physicalFootX':record['foot'][0],'firstArrivalSoleProjectionWorldX':record['foot'][0]+(center-128)*scale,'sourceSha256':hashlib.sha256(file.read_bytes()).hexdigest()})
 for r in j['records']:
  if r['slot']==slot and r['phase']<.315:samples.append(r['foot'][0]+(center-128)*scale)
values=[r['firstArrivalSoleProjectionWorldX'] for r in rows]
e={'scope':'Visible opaque sole-envelope center across first stance slots0/1/2. Does not track anatomical foot identity or certify contact/continuous sliding. Fixed alpha180 and sourcey222..224 band, sourcepivot128/224, native renderer scale384*.17/148.','journeysSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'firstArrivals':rows,'firstArrivalRangeWorld':max(values)-min(values),'allWithinFirstStanceSampleRangeWorld':max(samples)-min(samples),'notAcceptedAsFootLockProof':True}
(P/'contact-diagnostic.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8');print('First-arrival sole range:',round(e['firstArrivalRangeWorld'],4),'world; full sampled stance envelope:',round(e['allWithinFirstStanceSampleRangeWorld'],4),'world; bone identity unmeasured')
