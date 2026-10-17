from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];live=R/'character/chief-engineer-branforth-v2/clearance.json';baseline=P/'retained-clearance.json'
if not baseline.exists():baseline.write_bytes(live.read_bytes())
old=json.loads(baseline.read_bytes());out=copy.deepcopy(old);evidence=dict(worldStandingHeight=65.28,scope='New selected turn alpha union added to existing conservative transition profiles only',baselineSha256=hashlib.sha256(baseline.read_bytes()).hexdigest(),turns={})
def union(boxes):return [float(min(b[0] for b in boxes)),float(min(b[1] for b in boxes)),float(max(b[2] for b in boxes)),float(max(b[3] for b in boxes))]
for mode in ['bare','helmet']:
 m=json.loads((P/(mode+'-manifest.json')).read_bytes());sc=65.28/m['standingHeight'];pivot=m['pivot'];bounds={}
 for s in m['states']:
  boxes=[]
  for rel in s['frameFiles']:
   a=np.array(Image.open(P/rel).convert('RGBA'));y,x=np.where(a[:,:,3]>0);boxes.append([(x.min()-pivot[0])*sc,(y.min()-pivot[1])*sc,(x.max()+1-pivot[0])*sc,(y.max()+1-pivot[1])*sc])
  bounds[s['id']]=union(boxes)
 evidence['turns'][mode]=bounds
 for d in ['east','south','west','north']:
  out['actions'][mode]['transition-'+d]=union([old['actions'][mode]['transition-'+d]]+[box for key,box in bounds.items() if d in key.split('-')[2:]])
(P/'clearance.json').write_text(json.dumps(out,indent=2)+'\n');(P/'clearance-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Selected turn alpha union preserves swim/tread and unrelated action profiles')
