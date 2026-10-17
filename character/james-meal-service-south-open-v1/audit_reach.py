"""Measure source planting and matte palette; never infer anatomy from clocks."""
from pathlib import Path
import json
from PIL import Image
import numpy as np
P=Path(__file__).resolve().parent
m=json.loads((P/'reach-manifest.json').read_text());state=m['states'][0];rows=[];base=None
for i,path in enumerate(state['frameFiles']):
 a=np.array(Image.open(P/path).convert('RGBA'));centers=[]
 for x0,x1 in [(80,116),(140,176)]:
  yy,xx=np.where(a[220:225,x0:x1,3]>180);centers.append(round(float(xx.mean()+x0),3) if len(xx) else None)
 if base is None:base=centers
 rgb=a[:,:,:3].astype(float);bright=rgb.mean(2);spread=rgb.max(2)-rgb.min(2)
 neutral=(a[:,:,3]>180)&(spread<25)&(bright>25)&(bright<190)
 low=(a[:,:,3]>180)&(bright<30)
 rows.append({'frame':i,'soleBandCenters':centers,'displacementFromMaster':[round(centers[j]-base[j],3) if centers[j] is not None else None for j in range(2)],'neutralMedianRGB':np.median(rgb[neutral],axis=0).round(2).tolist(),'veryDarkFraction':round(float(low.sum()/(a[:,:,3]>180).sum()),4)})
result={'scope':'Opaque sole-band centers at fixed pivot and broad palette distribution; not complete anatomical, identity or material proof','rows':rows,'maxAbsSoleShift':max(abs(v) for r in rows for v in r['displacementFromMaster'] if v is not None)}
(P/'reach-foot-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
