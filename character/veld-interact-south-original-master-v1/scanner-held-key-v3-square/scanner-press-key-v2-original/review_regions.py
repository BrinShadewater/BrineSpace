from pathlib import Path
from PIL import Image
import numpy as np,json
P=Path(__file__).resolve().parent;R=P.parents[3]
paths={'original':R/'character/veld-idle-south-original-master-v1/original-idle-master.png','held':P.parent/'native-held-key.png','press':P/'native-press-key.png'}
regions={'head':[112,76,145,101],'chest':[111,106,148,128],'legs':[99,160,160,225]}
arrays={k:np.array(Image.open(v).convert('RGBA')) for k,v in paths.items()}
rows=[]
for source in ['held','press']:
 for label,box in regions.items():
  x0,y0,x1,y1=box;a=arrays['original'][y0:y1,x0:x1];b=arrays[source][y0:y1,x0:x1]
  mask=(a[:,:,3]>200)&(b[:,:,3]>200)
  rows.append(dict(source=source,region=label,box=box,commonOpaquePixels=int(mask.sum()),commonOpaqueRGBMAE=round(float(np.abs(a[:,:,:3].astype(float)-b[:,:,:3])[mask].mean()),3),originalRGBMean=np.round(a[:,:,:3][mask].mean(axis=0),2).tolist(),candidateRGBMean=np.round(b[:,:,:3][mask].mean(axis=0),2).tolist()))
record=dict(method='Fixed original registered spatial regions, common opaque pixels only. Differences combine pose/detail/colour, not pure grading. Diagnostic does not certify visual acceptance.',rows=rows)
(P/'REGION_REVIEW.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8');print(json.dumps(record))
