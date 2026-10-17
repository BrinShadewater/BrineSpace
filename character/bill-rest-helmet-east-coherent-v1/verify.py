from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];B=P.parent/'bill-rest-east-coherent-v1'
m=json.loads((P/'manifest.json').read_text());bm=json.loads((B/'manifest.json').read_text());r=json.loads((P/'helmet-registration.json').read_text());checks=[]
def check(v,label):assert v,label;checks.append(label)
canonical=np.array(Image.open(P/'sources/canonical-head.png'));closed=np.array(Image.open(P/'sources/canonical-closed-eye.png'));mask=np.zeros(canonical.shape[:2],bool);mask[16:19,26:29]=True
check(np.array_equal(canonical[:,:,3],closed[:,:,3]),'closed eyelid alpha exact')
check(np.array_equal(canonical[~mask],closed[~mask]),'closed eyelid hardware/face outline exact')
check(np.any(canonical[mask]!=closed[mask]),'authored eyelid applied')
check(np.array_equal(np.array(Image.open(R/m['states'][0]['frameFiles'][0][6:])),np.array(Image.open(R/r['endpoint']))),'exact equipped idle')
yy,xx=np.indices((256,256))
for row in r['frames']:
    i=row['frame'];bare=np.array(Image.open(R/bm['states'][0]['frameFiles'][i][6:]));gear=np.array(Image.open(R/m['states'][0]['frameFiles'][i][6:]))
    cx,cy=row['eraseEllipse']['center'];rx,ry=row['eraseEllipse']['radii'];region=((xx-cx)/rx)**2+((yy-cy)/ry)**2<1
    px,py=row['position'];w,h=row['componentSize'];region|=(xx>=px)&(xx<px+w)&(yy>=py)&(yy<py+h)
    check(np.array_equal(bare[~region],gear[~region]),f'body exact outside fitted helmet {i}')
    check(not np.any(gear[[0,-1],:,3]) and not np.any(gear[:,[0,-1],3]),f'unclipped equipment {i}')
    check(row['nativeScale']==1,f'canonical ruler {i}')
for gs,bs in zip(m['states'],bm['states']):check(gs['frameDurationsMs']==bs['frameDurationsMs'] and gs['loop']==bs['loop'],gs['id']+' paired timing')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'manifestSha256':sha(P/'manifest.json'),'scope':'component/body/paired timeline package invariants; station and visual acceptance separate'},indent=2)+'\n')
print(f'{len(checks)} equipment package checks pass')
