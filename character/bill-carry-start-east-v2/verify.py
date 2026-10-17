from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parent.parent;b=json.loads((P/'bindings.json').read_text(encoding='utf-8'));checks=0
def check(ok,message):
 global checks
 checks+=1
 assert ok,message
for file,digest in b['sourceSha256'].items():check(hashlib.sha256((R/file).read_bytes()).hexdigest()==digest,'Bound exact input')
Y,X=np.indices((256,256));mask=(Y<164)|((X>=135)&(Y<170));rows={}
for g in ['bare','helmet']:
 m=json.loads((P/f'{g}-manifest.json').read_text(encoding='utf-8'));s=m['states'][0];master=np.array(Image.open(R/f'character/bill-cargo-east-master-head-v1/frames/{g}/pickup-east/010.png'))
 check(m['status']=='staged_visual_review' and m['standingHeight']==148 and m['pivot']==[128,224],'Staged canonical registration')
 check(not s['loop'] and len(s['frameFiles'])==6 and sum(s['frameDurationsMs'])==320,'Original bridge clock')
 rows[g]=[]
 for i,file in enumerate(s['frameFiles']):
  p=R/file.removeprefix('res://');a=np.array(Image.open(p));rows[g].append(a);check(np.array_equal(a[mask],master[mask]),'Exact steady master protected pixels')
  y,x=np.where(a[:,:,3]>180);check(y.max()<=225 and x.min()>0 and x.max()<255,'Complete fitted body')
  if i==0:check(p.read_bytes()==(R/f'character/bill-cargo-east-master-head-v1/frames/{g}/pickup-east/010.png').read_bytes(),'Held join byte exact')
  if i>=4:check(p.read_bytes()==(R/f'character/bill-carry-east-gait-v1/frames/{g}/carry-east/001.png').read_bytes(),'Gait1 join byte exact')
for a,h in zip(rows['bare'],rows['helmet']):check(np.array_equal(a[140:],h[140:]),'Paired lowerbody')
check(b['resumeFrame']==1 and b['resumeGaitPhaseSeconds']==.105,'Resume exact gait phase')
(P/'validation.json').write_text(json.dumps({'checks':checks,'passed':True,'scope':'Package/source/steady protected body/endpoints only; not motion/contact or native acceptance'},indent=2)+'\n',encoding='utf-8');print(f'BILL EAST FIRST STEP V2: {checks} checks pass')
