from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];B=P.parent/'bill-rest-north-coherent-v1'
m=json.loads((P/'manifest.json').read_text());bm=json.loads((B/'manifest.json').read_text());r=json.loads((P/'helmet-registration.json').read_text());checks=[]
def check(v,label):assert v,label;checks.append(label)
check(np.array_equal(np.array(Image.open(R/m['states'][0]['frameFiles'][0][6:])),np.array(Image.open(R/r['endpoint']))),'exact equipped idle')
yy,xx=np.indices((256,256))
for row in r['frames']:
    i=row['frame'];bare=np.array(Image.open(R/bm['states'][0]['frameFiles'][i][6:]));gear=np.array(Image.open(R/m['states'][0]['frameFiles'][i][6:]))
    cx,cy=row['eraseEllipse']['center'];rx,ry=row['eraseEllipse']['radii'];region=((xx-cx)/rx)**2+((yy-cy)/ry)**2<1
    px,py=row['position'];w,h=row['componentSize'];region|=(xx>=px)&(xx<px+w)&(yy>=py)&(yy<py+h)
    check(np.array_equal(bare[~region],gear[~region]),f'body exact outside fitted helmet {i}')
    check(not np.any(gear[[0,-1],:,3]) and not np.any(gear[:,[0,-1],3]),f'unclipped equipment {i}')
    check(row['nativeScale']==1,f'component ruler {i}')
for gs,bs in zip(m['states'],bm['states']):check(gs['frameDurationsMs']==bs['frameDurationsMs'] and gs['loop']==bs['loop'],gs['id']+' paired timing')
check(r['frames'][-1]['componentPose']==r['frames'][-2]['componentPose']==4,'same authored sleep helmet component')
check(r['frames'][-1]['position']==r['frames'][-2]['position'],'sleep helmet position held')
check(m['states'][-1]['restHeadOffset']==bm['states'][-1]['restHeadOffset'],'paired resting head reference')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'manifestSha256':sha(P/'manifest.json'),'scope':'component/body/paired timeline and stable helmet package invariants; furniture and visual acceptance separate'},indent=2)+'\n')
print(f'{len(checks)} equipment package checks pass')
