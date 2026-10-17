"""Bounded authored empty-hand patches; retain reviewed body and equipment."""
from pathlib import Path
import hashlib,json,math
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def regions(a,head):
    v=a[:,:,:3].astype(float);solid=a[:,:,3]>200;luma=v.mean(2)
    warm=(v[:,:,0]>v[:,:,1]*1.12)&(v[:,:,1]>v[:,:,2]*1.20)
    skin=solid&head&warm&(luma>=80)
    hair=solid&head&~skin&((warm&(luma<80))|(luma>115))
    blue=solid&~head&(v[:,:,2]>v[:,:,0]*1.30)&(v[:,:,2]>v[:,:,1]*1.10)
    return {'skin':skin,'hair':hair,'science':blue,'neutral':solid&~head&~blue&(np.ptp(v,axis=2)<45)}
editpath=P/'sources/neutral-branch/edit-v2.png'
raw=np.array(Image.open(editpath).convert('RGBA'));assert raw.shape==(1024,1536,4)
reg=json.loads((P/'registration.json').read_text());scale=reg['fixedRuler']
grade=json.loads((P/'material-grade.json').read_text());heads=[(306,122),(765,184),(1238,223),(255,680),(637,756),(1090,875)]
yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool)
for hx,hy in heads:head|=((xx-hx)/49)**2+((yy-hy)/49)**2<1
graded=raw.copy();curves={}
# One pooled edit-source grade, same retained master targets. No pose-specific LUT.
for name,mask in regions(raw,head).items():
    intensity=raw[:,:,:3][mask].mean(1);knots=np.percentile(intensity,[0,15,35,55,75,90,100]);target=np.array(grade[name]['targets'])
    for c in range(3):graded[mask,c]=np.interp(intensity,knots,target[:,c]).clip(0,255).astype('uint8')
    curves[name]={'knots':knots.tolist(),'targets':target.tolist(),'sourcePixels':int(mask.sum())}
labs,n=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.where(labs==k)[0].mean()//512,np.where(labs==k)[1].mean()))
assert min(sizes[ids])>40000
windows={2:[1160,307,1316,388],3:[195,751,391,855]}
bindings={editpath.relative_to(R).as_posix():sha(editpath)};checks=0;records=[];output={}
for gear in ['bare','helmet']:
    entry=R/f'character/veld-read-seated-south-coherent-v1/frames/{gear}/read-seated-south/000.png'
    first=Image.new('RGBA',(256,272));first.alpha_composite(Image.open(entry).convert('RGBA'))
    bindings[entry.relative_to(R).as_posix()]=sha(entry);frames=[first];files=[]
    for slot,i in [(1,2),(2,3)]:
        record=next(r for r in reg['poses'] if r['gear']==gear and r['sourcePose']==i)
        box=record['box'];size=record['size'];position=record['position'];w=windows[i]
        keep=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0)
        a=graded.copy();a[~keep]=0
        cut=Image.fromarray(a).crop(box).resize(size,Image.Resampling.LANCZOS)
        edited=Image.new('RGBA',(256,272));edited.alpha_composite(cut,position)
        originalpath=P/f'frames/{gear}/death-sofa-read-south/{slot:03}.png'
        original=np.array(Image.open(originalpath).convert('RGBA'));b=np.array(edited)
        # Lanczos support stays within a recorded native rectangle. Feather only
        # its internal two-pixel boundary; no drawn replacement anatomy.
        x0=math.floor(position[0]+(w[0]-box[0])*scale)-1;y0=math.floor(position[1]+(w[1]-box[1])*scale)-1
        x1=math.ceil(position[0]+(w[2]-box[0])*scale)+1;y1=math.ceil(position[1]+(w[3]-box[1])*scale)+1
        cy,cx=np.indices(original.shape[:2]);distance=np.minimum.reduce([cx-x0,cy-y0,x1-1-cx,y1-1-cy]);weight=np.clip(distance/2,0,1)
        patched=np.rint(original*(1-weight[:,:,None])+b*weight[:,:,None]).astype('uint8');patched[patched[:,:,3]<8]=0
        protected=weight==0;assert np.array_equal(patched[protected],original[protected]);checks+=1
        bindings[originalpath.relative_to(R).as_posix()]=sha(originalpath)
        frames.append(Image.fromarray(patched));records.append({'gear':gear,'sourcePose':i,'sourceWindow':w,'nativeWindow':[x0,y0,x1,y1],'protectedPixels':int(protected.sum()),'grade':'one pooled edit-source curve / original master targets','internalEdgeFeatherPixels':2})
    for slot in range(3):
        path=P/f'frames/{gear}/death-sofa-neutral-south/{slot:03}.png';path.parent.mkdir(parents=True,exist_ok=True);frames[slot].save(path);files.append('res://'+path.relative_to(R).as_posix())
        box=frames[slot].getbbox();assert box[0]>0 and box[1]>0 and box[2]<256 and box[3]<272;checks+=1
    for slot in [3,4,5]:
        path=P/f'frames/{gear}/death-sofa-read-south/{slot:03}.png';files.append('res://'+path.relative_to(R).as_posix());frames.append(Image.open(path).convert('RGBA'));bindings[path.relative_to(R).as_posix()]=sha(path)
    assert frames[0].crop((0,0,256,256)).tobytes()==Image.open(entry).convert('RGBA').tobytes();checks+=1
    manifest=json.loads((P/f'{gear}-manifest.json').read_text());manifest['name']='Veld South sofa empty-handed supported floor fall '+gear
    state=dict(manifest['states'][0]);state['id']='death-sofa-neutral-south';state['frameFiles']=files;manifest['states']=[state]
    (P/f'{gear}-neutral-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8');output[gear]=frames
board=Image.new('RGB',(1536,588),'#202a30');d=ImageDraw.Draw(board)
for row,gear in enumerate(['bare','helmet']):
    for slot,frame in enumerate(output[gear]):board.paste(frame,(slot*256,row*294+20),frame);d.text((slot*256+5,row*294+3),gear+' empty hand '+str(slot),fill='white')
board.save(P/'neutral-source-review.png')
(P/'neutral-registration.json').write_text(json.dumps({'checks':checks,'fixedRuler':scale,'bindings':bindings,'patches':records,'materialGrade':curves,'aliases':'slots3,4,5 retain exact reviewed brace and floor files','scope':'bounded authored patches, source review pending; unselected, no controller/world evidence'},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'checks':checks,'failures':0,'newFrames':6,'exactSharedAliases':6,'normalSelection':False}))
