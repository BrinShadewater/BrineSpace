from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;ROOT=P.parents[1];B=P.parent/'bill-death-ground-west-coherent-v1';checks=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,name):checks.append({'passed':bool(ok),'check':name})
m=json.loads((P/'manifest.json').read_text());r=json.loads((P/'helmet-registration.json').read_text());s=m['states'][0];h=json.loads((P/'frame-hashes.json').read_text());bm=json.loads((B/'manifest.json').read_text());bs=bm['states'][0]
check(m['equipment']=='diving-helmet' and m['status']=='staged_candidate','Explicit staged gear')
check(m['pivot']==[128,224] and m['standingHeight']==148 and m['precomposed'],'Shared physical plane')
check(not s['loop'] and s['terminalFrame']==5 and sum(s['frameDurationsMs'])==2000,'Finite two-second corpse hold')
check(s['frameDurationsMs']==bs['frameDurationsMs'] and s['facings']==['west']*6 and s['waterPoses']==[False]*6 and s['depthOffsets']==[0]*6,'Paired clocks and dry direction')
check(sha(P/r['component'])==r['componentSha256']==sha(ROOT/r['donor']),'Exact accepted native dry component')
check(sha(B/'registration.json')==r['bareRegistrationSha256'],'Bound source registration')
check(Image.open(P/s['frameFiles'][0]).tobytes()==Image.open(ROOT/r['endpoint']).tobytes(),'Exact equipped idle entry')
yy,xx=np.indices((256,256));metrics=[]
for i,f in enumerate(s['frameFiles']):
 a=np.array(Image.open(P/f));y,x=np.where(a[:,:,3]>180)
 check(a.shape==(256,256,4) and x.min()>0 and x.max()<255 and y.min()>0 and y.max()<255,'Whole figure contained '+str(i))
 check(sha(P/f)==h[f],'Bound frame '+str(i))
 if i==0:continue
 row=r['frames'][i-1];b=np.array(Image.open(B/f));cx,cy=row['eraseEllipse']['center'];rx,ry=row['eraseEllipse']['radii'];px,py=row['position'];w,ht=row['componentSize']
 region=(((xx-cx)/rx)**2+((yy-cy)/ry)**2<1)|((xx>=px)&(xx<px+w)&(yy>=py)&(yy<py+ht))
 check(np.array_equal(a[~region],b[~region]),'Exact body outside declared helmet/head region '+str(i))
 check(row['nativeScale']==1 and sha(B/f)==row['bareSha256'],'Frozen equipment scale and bare binding '+str(i))
 check(px>=0 and py>=0 and px+w<=256 and py+ht<=256,'Unclipped helmet component '+str(i))
 metrics.append({'frame':i,'bounds':[int(x.min()),int(y.min()),int(x.max()),int(y.max())],'changedPixels':int(np.any(a!=b,axis=2).sum()),'scope':'shared body outside declared region only; collar/anatomy visual acceptance separate'})
result={'passed':all(c['passed'] for c in checks),'checks':len(checks),'results':checks,'metrics':metrics,'scope':'candidate paired-body/pixel/scale/finite metadata; real mortality, floor clearance, expression and final master polish pending'}
(P/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({'passed':result['passed'],'checks':len(checks)}));raise SystemExit(0 if result['passed'] else 1)
