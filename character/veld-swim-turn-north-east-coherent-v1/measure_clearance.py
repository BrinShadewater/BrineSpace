"""Measure staged ordinary swim turns; do not mutate selected safety bounds."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
H=Path(__file__).resolve().parent;R=H.parents[1]
path=R/'character/dr-veld-v2/clearance.json';bounds=json.loads(path.read_text());records=[]
for folder in ['veld-swim-turn-east-south-coherent-v1','veld-swim-turn-south-west-coherent-v1','veld-swim-turn-west-north-coherent-v1','veld-swim-turn-north-east-coherent-v1']:
 for variant in ['bare','helmet']:
  p=R/'character'/folder/f'{variant}-manifest.json';m=json.loads(p.read_text());scale=384*.17/m['standingHeight'];pivot=np.tile(m['pivot'],2)
  for state in m['states']:
   dest=state['id'].split('-')[-1];action=bounds['actions'][variant]['transition-'+dest];swim=bounds['swim'][variant][dest]
   effective=[min(action[i],swim[i]) if i<2 else max(action[i],swim[i]) for i in range(4)];boxes=[]
   for file in state['frameFiles']:
    a=np.array(Image.open(p.parent/file).convert('RGBA'));y,x=np.where(a[:,:,3]>20);boxes.append((np.array([x.min(),y.min(),x.max()+1,y.max()+1])-pivot)*scale)
   b=np.array(boxes);extent=[float(b[:,0].min()),float(b[:,1].min()),float(b[:,2].max()),float(b[:,3].max())]
   covered=all(effective[i]<=extent[i] if i<2 else effective[i]>=extent[i] for i in range(4))
   required=[min(action[i],extent[i]) if i<2 else max(action[i],extent[i]) for i in range(4)]
   records.append(dict(folder=folder,variant=variant,state=state['id'],scale=scale,alphaThreshold=20,nativeUnion=extent,selectedEffectiveBounds=effective,coveredBySelected=covered,proposedConservativeActionBounds=required))
report=dict(scope='Staged candidate alpha envelopes only; no furnished/exterior/traffic route or installation claim',selectedClearanceSha256=hashlib.sha256(path.read_bytes()).hexdigest(),installed=False,records=records,undercovered=sum(not r['coveredBySelected'] for r in records))
(H/'candidate-clearance-v1.json').write_text(json.dumps(report,indent=2)+'\n');print(f"{len(records)} staged turn envelopes measured; {report['undercovered']} need conservative expansion before installation")
