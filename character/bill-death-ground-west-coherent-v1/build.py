from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;ROOT=P.parent.parent
SOURCE=P/'sources/death-v1.png';IDLE=P.parent/'bill-seated-west-coherent-v1/frames/sit-down-west/000.png'
cfg={'generation':'exec-a45dae4c-2fe1-4d6e-bb05-083b69932de1','fixedRuler':[.28,.3065],'heads':[[255,143],[701,205],[1189,297],[133,791],[601,884],[1115,884]],'sourceContacts':[[220,578],[736,578],[1250,575],[315,928],[926,928],[1446,928]],'targetContacts':[[114,223],[114,223],[124,223],[130,223],[160,223],[160,223]],'sequence':[1,2,3,4,5],'durations':[250,300,350,400,400,300]}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
raw=np.array(Image.open(SOURCE).convert('RGBA'));rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2]);labs,_=label(raw[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0
ids=sorted(np.argsort(sizes)[-6:],key=lambda k:(np.median(np.where(labs==k)[0])//650,np.where(labs==k)[1].min()))
ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
head=np.zeros(raw.shape[:2],bool)
for hx,hy in cfg['heads']:head|=(xx-hx)**2+(yy-hy)**2<53**2
warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])
neutral=(raw[:,:,3]>200)&~head&(np.ptp(rgb,axis=2)<45)&(rgb[:,:,0]<1.4*rgb[:,:,1])&(rgb[:,:,0]<1.4*rgb[:,:,2])
rn=(ref[:,:,3]>200)&(ry>100)&(np.ptp(rr,axis=2)<45)&(rr[:,:,0]<1.4*rr[:,:,1])&(rr[:,:,0]<1.4*rr[:,:,2])
q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[rn],q)
graded=raw.copy();mapped=np.interp(rgb.mean(2)[neutral],src,dst);graded[neutral,:3]=np.clip(rgb[neutral]*mapped[:,None]/np.maximum(rgb.mean(2)[neutral,None],1),0,255).astype('uint8')
rh=(ref[:,:,3]>180)&(ry>=76)&(ry<85)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])
rf=(ref[:,:,3]>180)&(ry>=85)&(ry<102)&(rx<140)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])&(rr.mean(2)>65)
rp=(ref[:,:,3]>180)&(ry>100)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])
masks={'hair':head&warm&(raw[:,:,3]>200)&(rgb.mean(2)<90),'face':head&warm&(raw[:,:,3]>200)&(rgb.mean(2)>=90),'burgundy':~head&(raw[:,:,3]>200)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])}
gains={}
for name,authority in [('hair',rh),('face',rf),('burgundy',rp)]:
 mask=masks[name];gain=np.median(rr[authority],axis=0)/np.median(rgb[mask],axis=0);graded[mask,:3]=np.clip(rgb[mask]*gain,0,255).astype('uint8');gains[name]=gain.tolist()
frames=[Image.open(IDLE).convert('RGBA')];records=[]
for i in cfg['sequence']:
 mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
 a=graded.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);sx,sy=cfg['fixedRuler'];im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS)
 anchor=cfg['sourceContacts'][i];anchor[1]=int(y.max());target=cfg['targetContacts'][i];pos=[round(target[0]-(anchor[0]-box[0])*sx),round(target[1]-(anchor[1]-box[1])*sy)]
 plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane);records.append({'pose':i,'box':box,'position':pos,'contact':anchor,'target':target,'size':list(im.size),'scope':'source knee/forearm/boot floor contacts; natural local collapse, not planted standing registration'})
files=[];hashes={}
for i,im in enumerate(frames):
 f=P/f'frames/death-ground-west/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);files.append(f.relative_to(P).as_posix());hashes[files[-1]]=sha(f)
state={'id':'death-ground-west','frameFiles':files,'frameDurationsMs':cfg['durations'],'loop':False,'terminalFrame':5,'facings':['west']*6,'waterPoses':[False]*6,'waterKinds':['death-ground']*6,'depthOffsets':[0]*6}
manifest={'name':'Bill west dry ground collapse candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':[state]}
registration={**cfg,'frames':records,'sourceSha256':sha(SOURCE),'idleSha256':sha(IDLE),'scope':'exact selected idle entry; authored lowering and limp terminal; no normal selection/actual mortality proof'}
for name,data in [('manifest.json',manifest),('registration.json',registration),('frame-hashes.json',hashes),('material-grade.json',{'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'gains':gains,'headRegions':cfg['heads'],'authority':IDLE.relative_to(ROOT).as_posix(),'scope':'one global atlas grade; rotated head-local circular palette masks'})]:(P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,512),(34,52,62))
for i,im in enumerate(frames):board.paste(im,(i*256,0),im);board.paste(frames[0],(i*256,256),frames[0])
board.save(P/'contact-sheet.png');print('Built west ground collapse candidate; fixed ruler/natural lowering/exact idle')
