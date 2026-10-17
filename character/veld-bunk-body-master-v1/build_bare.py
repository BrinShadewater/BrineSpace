"""Complete master-body bunk source, one ruler and pooled semantic material grade."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
import numpy as np
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
RAW=P/'sources/bunk-body-v1.png';IDLE=R/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'
raw=np.array(Image.open(RAW).convert('RGBA'));labs,n=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-8:],key=lambda k:(np.where(labs==k)[0].min()//500,np.where(labs==k)[1].min()))
scale=148/408;heads=[(200,119),(681,157),(1085,187),(1516,228),(127,662),(538,706),(961,781),(1405,784)]
yy,xx=np.indices(raw.shape[:2]);head=np.zeros(raw.shape[:2],bool)
for x,y in heads:head|=(xx-x)**2+(yy-y)**2<55**2
master=Image.new('RGBA',(256,272));master.alpha_composite(Image.open(IDLE).convert('RGBA'),(36,52));ref=np.array(master);ry,rx=np.indices(ref.shape[:2]);rh=(rx>=117)&(rx<155)&(ry>=74)&(ry<107)
def materials(a,head):
    r,g,b=[a[:,:,c].astype(float) for c in range(3)];solid=a[:,:,3]>200;warm=(r>g*1.12)&(g>b*1.2)
    blue=solid&(b>r*1.3)&(b>g*1.1)
    face=solid&head&warm&(r>150)&(g>90)
    hair=solid&head&warm&~face
    neutral=solid&~head&~blue&(np.ptp(a[:,:,:3],axis=2)<45)
    return {'skin':face,'hair':hair,'science':blue,'neutral':neutral}
sm=materials(raw,head);rm=materials(ref,rh);graded=raw.copy();curves={};q=[0,15,35,55,75,90,100]
for name,mask in sm.items():
    target=rm[name];assert mask.sum()>30 and target.sum()>5,(name,int(mask.sum()),int(target.sum()))
    intensity=raw[:,:,:3][mask].mean(1);knots=np.percentile(intensity,q);new=np.percentile(ref[:,:,:3][target],q,axis=0)
    for c in range(3):graded[mask,c]=np.interp(intensity,knots,new[:,c]).clip(0,255).astype('uint8')
    curves[name]={'input':knots.tolist(),'master':new.tolist(),'sourcePixels':int(mask.sum()),'masterPixels':int(target.sum())}
# Source support anchors, not bounding-box-height normalisation. Pose3 has a
# longer hanging calf than the old figure; its canvas extends below pivot224.
source_anchors=[(223,492),(680,492),(1063,384),(1514,410),(127,820),(538,820),(961,820),(1405,821)]
target_anchors=[(144,223),(144,223),(95,189),(119,223),(90,223),(67,223),(63,223),(63,223)]
frames=[master];records=[];checks=0
for i,k in enumerate(ids):
    y,x=np.where(labs==k);box=(max(0,int(x.min())-3),max(0,int(y.min())-3),min(raw.shape[1],int(x.max())+4),min(raw.shape[0],int(y.max())+4))
    keep=binary_dilation(labs==k,iterations=3)&(raw[:,:,3]>0);a=graded.copy();a[~keep]=0
    size=(round((box[2]-box[0])*scale),round((box[3]-box[1])*scale));cut=Image.fromarray(a).crop(box).resize(size,Image.Resampling.LANCZOS)
    pos=tuple(round(target_anchors[i][j]-(source_anchors[i][j]-box[j])*scale) for j in range(2))
    out=Image.new('RGBA',(256,272));out.alpha_composite(cut,pos)
    arr=np.array(out);arr[arr[:,:,3]<8]=0;out=Image.fromarray(arr)
    records.append({'pose':i,'componentId':int(k),'box':box,'size':size,'position':pos,'sourceSupport':source_anchors[i],'targetSupport':target_anchors[i],'headCenter':[pos[j]+(heads[i][j]-box[j])*scale for j in range(2)]})
    assert pos[0]>=0 and pos[1]>=0 and pos[0]+size[0]<256 and pos[1]+size[1]<272;checks+=1
    if 0<i<7:frames.append(out)
    if i==7:relaxed=out
for i,im in enumerate(frames):
    f=P/f'frames/bare/bunk-enter-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f)
assert frames[0].crop((36,52,220,236)).tobytes()==Image.open(IDLE).convert('RGBA').tobytes();checks+=1
# Keep all non-arm pixels of the newly authored lying body, including tools/head/legs.
mask=np.zeros((272,256),bool);mask[202:225,100:137]=True
a=np.array(frames[6]);# Register the authored relaxed glove to the same mattress support row.
# Translate its bounded source insert one native pixel upward; no cropping or
# rescaling of anatomy and no change to the protected head/body/legs.
b=np.zeros_like(a);b[:-1]=np.array(relaxed)[1:];end=a.copy();end[mask]=b[mask];end=Image.fromarray(end)
for i,im in enumerate([frames[6],end,end]):
    f=P/f'frames/bare/death-bunk-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f)
    assert np.array_equal(np.array(im)[~mask],a[~mask]);checks+=1
base=json.loads((R/'character/dr-veld-v2/supplemental/bunk-east/bare/manifest.json').read_text());base.update(name='Veld complete master-body bunk candidate',canvas=[256,272],frameWidth=256,frameHeight=272,pivot=[128,224],standingHeight=148,textureFilter='linear',precomposed=True,status='installed_locally_owner_motion_review_open')
for s in base['states']:s['frameFiles']=[f'res://character/veld-bunk-body-master-v1/frames/bare/bunk-enter-east/{f}' for f in s['frameFiles']]
base['states'].append({'id':'death-bunk-east','frameFiles':[f'res://character/veld-bunk-body-master-v1/frames/bare/death-bunk-east/{i:03}.png' for i in range(3)],'frameDurationsMs':[180,280,420],'loop':False,'furnitureFrames':['bunk']*3,'depthOffsets':[100]*3})
(P/'bare-manifest.json').write_text(json.dumps(base,indent=2)+'\n')
(P/'bare-registration.json').write_text(json.dumps({'source':RAW.relative_to(R).as_posix(),'sourceSha256':hashlib.sha256(RAW.read_bytes()).hexdigest(),'fixedRuler':scale,'standingSourceOpaqueHeight':408,'nativeMasterHeight':148,'canvas':[256,272],'pivot':[128,224],'frames':records,'deathInsert':[100,202,137,225],'deathInsertTranslation':[0,-1],'checks':checks,'failures':0,'idle':IDLE.relative_to(R).as_posix(),'idleSha256':hashlib.sha256(IDLE.read_bytes()).hexdigest(),'scope':'whole master-body bunk candidate; actual room/contact/lifecycle and helmet proof pending'},indent=2)+'\n')
(P/'material-grade.json').write_text(json.dumps(curves,indent=2)+'\n')
board=Image.new('RGB',(1792,850),'#202a30');d=ImageDraw.Draw(board)
for row in range(3):
    for i in range(7):
        im=frames[i] if row==0 else (master if row==1 else Image.open(R/f'character/dr-veld-v2/supplemental/bunk-east/bare/{i:03}.png').convert('RGBA'))
        board.paste(im,(i*256,row*280+18),im);d.text((i*256+6,row*280+2),['New body','Selected master','Original bunk'][row]+f' {i+1}',fill='white')
board.save(P/'bare-source-review.png')
print(f'{checks} source isolation/canvas/entry/death protection checks,0failures; fixed148/408 ruler')
