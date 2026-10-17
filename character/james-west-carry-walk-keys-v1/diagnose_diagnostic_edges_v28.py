from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
p=Path(__file__).resolve().parent;r=p.parents[1];out=r/'character/james-full-set-review-2026-10-02/diagnostics-v28'
inventory=r/'character/james-full-set-review-2026-10-02/current-selection-v27/source-inventory.json';d=json.loads(inventory.read_bytes());rows=[];sources={}
for direction in ['south','north','west']:
 for mode in ['bare','helmet']:
  state=d['states'][mode]['inspect-'+direction]
  for i,rel in enumerate(state['frameFiles']):
   f=r/rel;sources[rel]=hashlib.sha256(f.read_bytes()).hexdigest();a=np.array(Image.open(f).convert('RGBA'));rgb=a[:,:,:3].astype(int);red,green,blue=rgb.transpose(2,0,1)
   alpha=a[:,:,3];solid=alpha>0;fully_inside=solid.copy()
   for dy in [-1,0,1]:
    for dx in [-1,0,1]:
     if dx==dy==0:continue
     shift=np.zeros_like(solid);y0=max(0,dy);y1=min(solid.shape[0],solid.shape[0]+dy);x0=max(0,dx);x1=min(solid.shape[1],solid.shape[1]+dx)
     shift[y0:y1,x0:x1]=solid[y0-dy:y1-dy,x0-dx:x1-dx];fully_inside &= shift
   edge=solid&~fully_inside;gmask=solid&(10*green>13*red)&(10*green>13*blue)&(green>20)
   high=gmask&(green>70)
   rows.append(dict(direction=direction,mode=mode,slot=i,strongGreenPixels=int(gmask.sum()),strongGreenEdgePixels=int((gmask&edge).sum()),
       strongGreenLowAlphaPixels=int((gmask&(alpha<128)).sum()),oldHighThresholdPixels=int(high.sum())))
summary=[]
for direction in ['south','north','west']:
 for mode in ['bare','helmet']:
  bank=[x for x in rows if x['direction']==direction and x['mode']==mode]
  summary.append(dict(direction=direction,mode=mode,frames=len(bank),framesWithStrongGreen=sum(x['strongGreenPixels']>0 for x in bank),
      totalStrongGreen=sum(x['strongGreenPixels'] for x in bank),totalEdgeGreen=sum(x['strongGreenEdgePixels'] for x in bank),
      totalLowAlphaGreen=sum(x['strongGreenLowAlphaPixels'] for x in bank),totalOldHighThreshold=sum(x['oldHighThresholdPixels'] for x in bank),
      peak=max(bank,key=lambda x:x['strongGreenPixels'])))
(out/'edge-diagnostic.json').write_text(json.dumps(dict(sourceSha256=sources,records=rows,summary=summary,normalChanged=False,
    scope='Read-only chroma/alpha neighbourhood diagnostic, not semantic classification or proof that every flagged green pixel is contamination.8-neighbour edge means adjacent alpha0; old70 threshold compared with dark20 threshold.'),indent=2)+'\n')
print(json.dumps(summary))
