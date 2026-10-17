from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label, binary_dilation

P=Path(__file__).resolve().parent
R=P.parents[1]
SOURCE=P/'sources/rest-v2.png'
IDLE=P.parent/'bill-seated-east-coherent-v1/frames/sit-down-east/000.png'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
raw=np.array(Image.open(SOURCE).convert('RGBA'))
rgb=raw[:,:,:3].astype(float)
yy,xx=np.indices(raw.shape[:2])
labs,_=label(raw[:,:,3]>180)
sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(int(np.median(np.where(labs==k)[0]))//650,int(np.where(labs==k)[1].min())))
heads=[(211,139),(674,285),(1151,322),(90,749),(572,843),(1086,841)]
head=np.zeros(raw.shape[:2],bool)
for hx,hy in heads: head|=(xx-hx)**2+(yy-hy)**2<58**2
ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
neutral=(raw[:,:,3]>200)&~head&(np.ptp(rgb,axis=2)<45)&(rgb[:,:,0]<1.4*rgb[:,:,1])&(rgb[:,:,0]<1.4*rgb[:,:,2])
rn=(ref[:,:,3]>200)&(ry>100)&(np.ptp(rr,axis=2)<45)&(rr[:,:,0]<1.4*rr[:,:,1])&(rr[:,:,0]<1.4*rr[:,:,2])
q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1]
src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[rn],q)
graded=raw.copy();mapped=np.interp(rgb.mean(2)[neutral],src,dst)
graded[neutral,:3]=np.clip(rgb[neutral]*mapped[:,None]/np.maximum(rgb.mean(2)[neutral,None],1),0,255).astype('uint8')
warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])
rh=(ref[:,:,3]>180)&(ry>=76)&(ry<85)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])
rf=(ref[:,:,3]>180)&(ry>=85)&(ry<102)&(rx>115)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])&(rr.mean(2)>65)
rp=(ref[:,:,3]>180)&(ry>100)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])
masks={'hair':head&warm&(raw[:,:,3]>200)&(rgb.mean(2)<90),'face':head&warm&(raw[:,:,3]>200)&(rgb.mean(2)>=90),'burgundy':~head&(raw[:,:,3]>200)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])}
gains={}
for name,authority in [('hair',rh),('face',rf),('burgundy',rp)]:
    mask=masks[name];gain=np.median(rr[authority],axis=0)/np.median(rgb[mask],axis=0)
    graded[mask,:3]=np.clip(rgb[mask]*gain,0,255).astype('uint8');gains[name]=gain.tolist()
# One ruler across poses. Never normalize a reclining bounding box to standing height.
sx,sy=.28,148/466
contacts=[None,(854,569),(1419,567),(440,917),(967,911),(1479,911)]
targets=[None,(190,223),(190,223),(190,223),(195,223),(195,223)]
frames=[Image.open(IDLE).convert('RGBA')];records=[]
for i in range(1,6):
    mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0)
    y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
    a=graded.copy();a[~mask]=0
    im=Image.fromarray(a).crop(box)
    im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS)
    anchor=contacts[i];target=targets[i]
    pos=[round(target[0]-(anchor[0]-box[0])*sx),round(target[1]-(anchor[1]-box[1])*sy)]
    plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane)
    records.append({'pose':i,'box':box,'position':pos,'sourceSupport':anchor,'targetSupport':target,'scale':[sx,sy],'headCenter':[round(pos[0]+(heads[i][0]-box[0])*sx),round(pos[1]+(heads[i][1]-box[1])*sy)]})
lower_path=P/'sources/lowering-v3.png'
lower=np.array(Image.open(lower_path).convert('RGBA'));lr=lower[:,:,:3].astype(float)
ly,lx=np.indices(lower.shape[:2]);ll,_=label(lower[:,:,3]>180);ss=np.bincount(ll.ravel());ss[0]=0
li=sorted(np.argsort(ss)[-2:],key=lambda k:np.where(ll==k)[1].min())
lh=((lx-477)**2+(ly-184)**2<95**2)|((lx-1247)**2+(ly-341)**2<95**2)
ln=(lower[:,:,3]>200)&~lh&(np.ptp(lr,axis=2)<45)&(lr[:,:,0]<1.4*lr[:,:,1])&(lr[:,:,0]<1.4*lr[:,:,2])
lc=np.quantile(lr.mean(2)[ln],q);lg=lower.copy();lm=np.interp(lr.mean(2)[ln],lc,dst)
lg[ln,:3]=np.clip(lr[ln]*lm[:,None]/np.maximum(lr.mean(2)[ln,None],1),0,255).astype('uint8')
lw=(lr[:,:,0]>1.12*lr[:,:,1])&(lr[:,:,1]>1.25*lr[:,:,2])
lower_gains={}
for name,mask,authority in [('hair',lh&lw&(lower[:,:,3]>200)&(lr.mean(2)<90),rh),('face',lh&lw&(lower[:,:,3]>200)&(lr.mean(2)>=90),rf),('burgundy',~lh&(lower[:,:,3]>200)&(lr[:,:,0]>1.4*lr[:,:,1])&(lr[:,:,0]>1.4*lr[:,:,2]),rp)]:
    gain=np.median(rr[authority],axis=0)/np.median(lr[mask],axis=0)
    lg[mask,:3]=np.clip(lr[mask]*gain,0,255).astype('uint8');lower_gains[name]=gain.tolist()
interiors=[];lower_records=[]
for i in range(2):
    mask=binary_dilation(ll==li[i],iterations=3)&(lower[:,:,3]>0);y,x=np.where(ll==li[i])
    box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];a=lg.copy();a[~mask]=0
    im=Image.fromarray(a).crop(box);ruler=[.16,.192];im=im.resize((round(im.width*ruler[0]),round(im.height*ruler[1])),Image.Resampling.LANCZOS)
    contact=[(593,789),(1489,783)][i];target=[(162,223),(190,223)][i]
    pos=[round(target[0]-(contact[0]-box[0])*ruler[0]),round(target[1]-(contact[1]-box[1])*ruler[1])]
    plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);interiors.append(plane)
    lower_records.append({'source':'sources/lowering-v3.png','pose':i,'box':box,'scale':ruler,'position':pos,'sourceSupport':contact,'targetSupport':target})
frames=[frames[0]]+interiors+frames[1:]
files=[];hashes={}
for i,im in enumerate(frames):
    f=P/f'frames/lie-down-east/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f)
    files.append('res://'+f.relative_to(R).as_posix());hashes[files[-1]]=sha(f)
def state(name,sequence,durations,loop=False):
    return {'id':name+'-east','frameFiles':[files[i] for i in sequence],'frameDurationsMs':durations,'loop':loop,'facings':['east']*len(sequence),'waterPoses':[False]*len(sequence),'depthOffsets':[0]*len(sequence)}
durations=[65,85,100,110,120,130,110,80]
states=[state('lie-down',range(8),durations),state('get-up',range(7,-1,-1),durations[::-1]),state('sleep',[7,6],[600,600],True)]
states[0]['terminalFrame']=7;states[1]['terminalFrame']=7;states[1]['derived']='exact reverse of authored lie-down'
# Sleep joins use precisely the finite entry endpoint. Actual furniture proof pending.
headcenter=records[-1]['headCenter']
states[2]['restHeadOffset']=[round((headcenter[0]-128)*65.28/148,4),round((headcenter[1]-224)*65.28/148,4)]
manifest={'name':'Bill east generic rest candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
data={'generation':'exec-7fe0a5e8-739d-4f29-b80a-0e30f113f55a','loweringGeneration':'exec-be41fd9f-87f5-4fc8-8f54-9f210c2b116a','rejectedChoreography':'exec-59db2955-ab5c-46ac-84cf-51c8eb471fe0','sourceSha256':sha(SOURCE),'loweringSourceSha256':sha(lower_path),'idleSha256':sha(IDLE),'fixedRuler':[sx,sy],'frames':records,'loweringFrames':lower_records,'scope':'bare east candidate; one fixed ruler per independent source; no runtime/furniture/helmet or owner acceptance; breathing cadence and registration need native review'}
for name,obj in [('manifest.json',manifest),('registration.json',data),('frame-hashes.json',hashes),('material-grade.json',{'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'gains':gains,'authority':str(IDLE.relative_to(R))})]:
    (P/name).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
(P/'lowering-material-grade.json').write_text(json.dumps({'neutralInput':lc.tolist(),'neutralOutput':dst.tolist(),'gains':lower_gains},indent=2)+'\n')
board=Image.new('RGB',(2048,512),(34,52,62))
for i,im in enumerate(frames):board.paste(im,(256*i,0),im);board.paste(frames[0],(256*i,256),frames[0])
board.save(P/'contact-sheet.png')
native=Image.new('RGB',(8*148,2*148),(34,52,62))
for i,im in enumerate(frames):
    small=im.resize((148,148),Image.Resampling.LANCZOS);base=frames[0].resize((148,148),Image.Resampling.LANCZOS)
    native.paste(small,(i*148,0),small);native.paste(base,(i*148,148),base)
native.save(P/'density-review.png')
checks={'exactIdle':np.array_equal(np.array(frames[0]),ref),'entryExitReverse':states[1]['frameFiles']==states[0]['frameFiles'][::-1],'lieSeconds':sum(states[0]['frameDurationsMs'])==800,'riseSeconds':sum(states[1]['frameDurationsMs'])==800,'sleepJoin':states[2]['frameFiles'][0]==states[0]['frameFiles'][-1],'wakeJoin':states[1]['frameFiles'][0]==states[2]['frameFiles'][0],'literalPaths':all(f.startswith('res://') for f in files),'unclipped':all(not np.any(np.array(im)[[0,-1],:,3]) and not np.any(np.array(im)[:,[0,-1],3]) for im in frames),'fixedRuler':all(v['scale']==[sx,sy] for v in records)}
assert all(checks.values()),checks
(P/'verification.json').write_text(json.dumps({'passed':True,'checks':checks,'scope':'package endpoints/timing/bounds only; visual/native/runtime acceptance separate'},indent=2)+'\n')
print('Built bare east rest3 states,8 authored slots;9 package invariants pass; runtime/furniture unproven')
