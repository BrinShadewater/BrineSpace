from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parent.parent;reg=json.loads((P/'registration.json').read_text(encoding='utf-8'));checks=0
def check(ok,message):
 global checks
 checks+=1
 assert ok,message
Y,X=np.indices((256,256));protected=Y<164;rows={}
for file,digest in reg['masterSha256'].items():check(hashlib.sha256((R/file).read_bytes()).hexdigest()==digest,'Canonical input bytes')
for g in ['bare','helmet']:
 m=json.loads((P/f'{g}-manifest.json').read_text(encoding='utf-8'));s=m['states'][0];master=np.array(Image.open(R/f'character/bill-cargo-west-master-head-v1/frames/{g}/pickup-west/011.png'))
 check(m['status']=='staged_visual_review' and m['standingHeight']==148 and m['pivot']==[128,224],'Unselected canonical registration')
 check(s['loop'] and len(s['frameFiles'])==6 and sum(s['frameDurationsMs'])==840 and m['strideDistanceCells']['carry']==.12,'Original cycle/stride with6source slots')
 rows[g]=[]
 for i,file in enumerate(s['frameFiles']):
  a=np.array(Image.open(R/file.removeprefix('res://')));rows[g].append(a);check(np.array_equal(a[protected],master[protected]),'Exact steady head/helmet/suit/hands/case RGBA')
  y,x=np.where(a[:,:,3]>180);check(y.min()==np.where(master[:,:,3]>180)[0].min() and y.max()==224,'Constant crown and grounded sole')
  check(x.min()>0 and x.max()<255,'Complete anatomy')
  check(reg['frames'][i]['scale']==next(c['scale'] for c in reg['calibration'] if reg['frames'][i]['source'].endswith(c['source'].split('/')[-1])),'One component ruler')
  labs,_=label(a[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0;check(n.max()/n.sum()>.98,'Connected fitted body')
for a,h in zip(rows['bare'],rows['helmet']):check(np.array_equal(a[164:],h[164:]),'Exact paired lowerbody')
(P/'validation.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'Package/steady protected body/shared ruler/paired lowerbody only; not gait/contact/smoothness certificate'},indent=2)+'\n',encoding='utf-8');print(f'BILL WEST GAIT: {checks} checks pass')
