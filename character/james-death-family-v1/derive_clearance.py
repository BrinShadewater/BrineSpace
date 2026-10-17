from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];base=P/'retained-clearance.json'
if not base.exists():base.write_bytes((R/'character/chief-engineer-branforth-v2/clearance.json').read_bytes())
old=json.loads(base.read_bytes());out=copy.deepcopy(old);evidence={'baselineSha256':hashlib.sha256(base.read_bytes()).hexdigest(),'scope':'Death pose envelopes for fixture placement only; all selected clearance remains unchanged','bounds':{}}
def union(bs):return [float(min(b[0] for b in bs)),float(min(b[1] for b in bs)),float(max(b[2] for b in bs)),float(max(b[3] for b in bs))]
for mode in ['bare','helmet']:
 m=json.loads((P/(mode+'-manifest.json')).read_text());sc=65.28/m['standingHeight'];pivot=m['pivot'];bounds={}
 for s in m['states']:
  boxes=[]
  for rel in s['frameFiles']:
   a=np.array(Image.open(P/rel).convert('RGBA'));y,x=np.where(a[:,:,3]>0);boxes.append([(x.min()-pivot[0])*sc,(y.min()-pivot[1])*sc,(x.max()+1-pivot[0])*sc,(y.max()+1-pivot[1])*sc])
  bounds[s['id']]=union(boxes)
  if False:out['life'][mode][s['id']]=union([old['life'][mode][s['id']],bounds[s['id']]])
 evidence['bounds'][mode]=bounds
(P/'clearance.json').write_text(json.dumps(out,indent=2)+'\n');(P/'clearance-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');print('Derived death envelopes for fixture placement; runtime clearance unchanged')
