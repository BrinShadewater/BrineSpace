from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label
P=Path(__file__).resolve().parent;R=P.parents[1];reg=json.loads((P/'head-registration.json').read_text());checks=[]
def check(ok,name):
    assert ok,name
    checks.append(name)
components={}
for gear,box in [('bare',reg['bareSourceBox']),('helmet',reg['gearSourceBox'])]:
    h=Image.open(P/f'sources/{gear}-master-head.png').convert('RGBA');plane=Image.new('RGBA',(256,256));plane.alpha_composite(h,tuple(box[:2]));components[gear]=plane
    master=Image.open(R/f'character/bill-seated-{"helmet-" if gear=="helmet" else ""}north-coherent-v1/frames/sit-down-north/000.png').convert('RGBA');a=np.array(h);old=np.array(master.crop(tuple(box)));mask=a[:,:,3]>0
    check(np.array_equal(a[mask],old[mask]),'Exact native master component '+gear)
for gear,name in [('bare','manifest.json'),('helmet','helmet-manifest.json')]:
    m=json.loads((P/name).read_text());inventory=json.loads((R/reg['sourceInventory']).read_text())
    for state in m['states']:
        ref=inventory['selectedStateSources'][gear][state['id']];oldm=json.loads((R/ref['manifest']).read_text());old=next(s for s in oldm['states'] if s['id']==state['id'])
        check(state['frameDurationsMs']==old['frameDurationsMs'] and state['loop']==old['loop'],'Original source clock and loop')
        check(m['strideDistanceCells']==oldm['strideDistanceCells'],'Original cargo stride')
    check(m['pivot']==[128,224] and m['standingHeight']==148,'Native foot origin and density')
for row in reg['frames']:
    old=np.array(Image.open(R/row['bareFile'][6:]).convert('RGBA'));a=np.array(Image.open(R/row['output'][6:]).convert('RGBA'))
    check(hashlib.sha256((R/row['bareFile'][6:]).read_bytes()).hexdigest()==row['bareSha256'],'Bare sources immutable')
    check(hashlib.sha256((R/row['originalFile'][6:]).read_bytes()).hexdigest()==row['originalSha256'],'Original paired sources immutable')
    if row['endpointExact']:
        check(np.array_equal(a,np.array(Image.open(R/row['originalFile'][6:]).convert('RGBA'))),'Exact accepted empty endpoint');continue
    component=components[row['gear']];angle=row['angle']
    if angle:component=component.rotate(angle,resample=Image.Resampling.BICUBIC,center=(128,100))
    translated=Image.new('RGBA',(256,256));translated.alpha_composite(component,tuple(row['translation']));h=np.array(translated)
    erase=np.array(Image.open(P/row['eraseMask']))>0;region=erase|(h[:,:,3]>0)
    check(np.array_equal(a[~region],old[~region]),'All protected anatomy/case/detail pixels exact')
    base=old.copy();base[erase]=0;expected=Image.fromarray(base);expected.alpha_composite(component,tuple(row['translation']))
    check(np.array_equal(a,np.array(expected)),'Native component/neck rotation exact; no scale or grade')
    labels,n=label(a[:,:,3]>160);sizes=np.bincount(labels.ravel());body=int(sizes[1:].argmax()+1);headmask=h[:,:,3]>200
    check(float((labels[headmask]==body).mean())>.98,'Head shares main body silhouette')
    rgb=old[:,:,:3].astype(float);yy,xx=np.indices((256,256));neutral=(rgb.max(2)-rgb.min(2)<12)&(yy>=row['sourceTop']+12)&(old[:,:,3]>0)
    check(not erase[neutral].any(),'Neutral collar/backpack excluded from head erasure')
for gear,name in [('bare','manifest.json'),('helmet','helmet-manifest.json')]:
    m=json.loads((P/name).read_text());states={s['id']:s for s in m['states']}
    check((R/states['pickup-north']['frameFiles'][-1][6:]).read_bytes()==(R/states['unload-north']['frameFiles'][0][6:]).read_bytes(),'Exact static held pickup/unload endpoint')
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':len(checks),'labels':checks,'scope':'Native master pixels/rotation, protected cargo anatomy, source clocks/stride/endpoints and connected neck; visual/runtime separate'},indent=2)+'\n');print(str(len(checks))+' package checks pass')
