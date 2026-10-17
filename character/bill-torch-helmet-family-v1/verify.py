from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
P=Path(__file__).resolve().parent;R=P.parents[1];m=json.loads((P/'manifest.json').read_text());r=json.loads((P/'helmet-registration.json').read_text());bm=json.loads((P.parent/'bill-torch-actions-v1/manifest.json').read_text());checks=[]
def check(ok,label):assert ok,label;checks.append(label)
yy,xx=np.indices((256,256))
for row in r['frames']:
    state=next(s for s in m['states'] if s['id']==row['state']);f=R/state['frameFiles'][row['frame']][6:];gear=np.array(Image.open(f).convert('RGBA'));body=np.array(Image.open(R/row['bareFile'][6:]).convert('RGBA'))
    check(gear.shape==(256,256,4) and not gear[[0,-1],:,3].any() and not gear[:,[0,-1],3].any(),row['state']+str(row['frame'])+' plane/bounds')
    check(row['nativeScale']==1,'native shared helmet scale')
    if row['endpointExactSelected']:
        d=state['id'].split('-')[-1];idle=np.array(Image.open(P.parent/f'bill-seated-helmet-{d}-coherent-v1/frames/sit-down-{d}/000.png').convert('RGBA'));check(np.array_equal(idle,gear),'exact selected equipped idle')
    else:
        x0,y0,x1,y1=row['eraseRect'];px,py=row['position'];w,h=row['componentSize'];region=((xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1))|((xx>=px)&(xx<px+w)&(yy>=py)&(yy<py+h))
        check(np.array_equal(body[~region],gear[~region]),'approved body/tool/flame exact outside head region')
for s,b in zip(m['states'],bm['states']):check(s['frameDurationsMs']==b['frameDurationsMs'] and s['loop']==b['loop'],'paired clock '+s['id'])
for d in ['east','west','south','north']:
    s={a['id']:a for a in m['states']};pixels=lambda key,i:Image.open(R/s[key]['frameFiles'][i][6:]).tobytes()
    check(pixels('torch-draw-'+d,5)==pixels('weld-'+d,0),'exact entry/work '+d);check(pixels('weld-'+d,5)==pixels('torch-stow-'+d,0),'exact work/exit '+d)
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'scope':'paired source/body/hardware/clock/endpoints; equipped construction excluded by gameplay, visual motion acceptance separate'},indent=2)+'\n',encoding='utf-8')
print(str(len(checks))+' equipment package checks pass')
