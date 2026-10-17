from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
IDLE=P.parent/'crew-runtime-matte-v1/bill/frames/idle-north-transition-matte-v1/000.png'
def prepare(source,heads,count,density=1):
 raw=np.array(Image.open(source).convert('RGBA'));rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2]);labs,_=label(raw[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0
 ids=sorted(np.argsort(n)[-count:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
 ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22);rn=(ref[:,:,3]>200)&(ry>50)&(np.ptp(rr,axis=2)<22)
 src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[rn],q);mapped=np.interp(rgb.mean(2),src,dst);w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 grade=raw.copy();grade[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8')
 hair=np.zeros(raw.shape[:2],bool);face=hair.copy();patch=hair.copy()
 for hx,hy in heads:
  hair|=(abs(xx-hx)<43*density)&(yy>=hy)&(yy<hy+65*density)
  face|=(xx>hx)&(xx<hx+45)&(yy>=hy+23)&(yy<hy+75)
  patch|=(abs(xx-hx)<115*density)&(yy>hy+65*density)&(yy<hy+160*density)
 warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(raw[:,:,3]>200)
 hair&=warm&(rgb.mean(2)<110);face&=warm&(rgb.mean(2)>65);patch&=(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])&(raw[:,:,3]>200)
 rh=(ref[:,:,3]>180)&(ry>=24)&(ry<33)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]);rf=(ref[:,:,3]>180)&(rx>92)&(ry>=33)&(ry<50)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])&(rr.mean(2)>65);rp=(ref[:,:,3]>180)&(ry>50)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])
 gains={}
 for name,mask,authority in [('hair',hair,rh),('burgundy',patch,rp)]:
  gain=np.median(rr[authority],axis=0)/np.median(rgb[mask],axis=0);gains[name]=gain.tolist();grade[mask,:3]=np.clip(rgb[mask]*gain,0,255).astype('uint8')
 return raw,labs,ids,grade,{"neutralInput":src.tolist(),"neutralOutput":dst.tolist(),"gains":gains}
def main():
 primary_heads=[(305,50),(770,85),(1228,128),(303,591),(770,590),(1231,593)]
 primary=prepare(P/'sources/sit-v1.png',primary_heads,6)
 middle_heads=[(443,124),(1101,199)]
 middle=prepare(P/'sources/interiors-boots-v4.png',middle_heads,2,1.85)
 ref=Image.open(IDLE).convert('RGBA');idle=Image.new('RGBA',(256,256));idle.paste(ref,(36,52));frames=[idle];records=[]
 ar=np.array(ref);by,bx=np.where(ar[:,:,3]>180);ground=int(by.max()+52);boot=float(np.median(bx[(by>=by.max()-6)&(bx>np.median(bx))]))+36
 choices=[(primary,primary_heads,1,.305,.3267,'sources/sit-v1.png'),(middle,middle_heads,0,.165,.177,'sources/interiors-boots-v4.png'),(middle,middle_heads,1,.165,.177,'sources/interiors-boots-v4.png'),(primary,primary_heads,4,.305,.3267,'sources/sit-v1.png'),(primary,primary_heads,5,.305,.3267,'sources/sit-v1.png')]
 for frame,(data,heads,i,sx,sy,source) in enumerate(choices,1):
  raw,labs,ids,graded,curve=data;mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];sole=float(y.max());front=float(np.median(x[(y>=y.max()-10)&(x>np.median(x))]));a=graded.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS);pos=(round(boot-(front-box[0])*sx),round(ground-(sole-box[1])*sy));plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane);hx,hy=heads[i]
  records.append({'frame':frame,'source':source,'sourcePose':i,'sourceBox':box,'scaleX':sx,'scaleY':sy,'position':pos,'sourceFrontBoot':[front,sole],'targetFrontBoot':[boot,ground],'headAxis':[round(pos[0]+(hx-box[0])*sx),round(pos[1]+(hy-box[1])*sy)],'headTiltDegrees':0})
 files=[];hashes={}
 for i,im in enumerate(frames):
  f=P/'frames/sit-down-north'/f'{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);name=f.relative_to(P).as_posix();files.append(name);hashes[name]=hashlib.sha256(f.read_bytes()).hexdigest()
 states=[]
 for action,sequence,durations,depth in [('sit-down',files,[100,120,140,160,160,120],[0,8,16,24,32,40]),('sit-rise',files[::-1],[120,160,160,140,120,100],[40,32,24,16,8,0])]:
  states.append({'id':action+'-north','frameFiles':sequence,'frameDurationsMs':durations,'loop':False,'facings':['north']*6,'waterPoses':[False]*6,'waterKinds':[action]*6,'depthOffsets':depth,'provenance':'authored independent whole figures;reversed rise;exact selected standing idle;seated idle family pending'})
 m={'name':'Bill north sitting transition candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
 registration={'idleAuthority':IDLE.relative_to(P.parent).as_posix(),'idleSha256':hashlib.sha256(IDLE.read_bytes()).hexdigest(),'idlePadding':[36,52],'sources':{name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['sources/sit-v1.png','sources/interiors-boots-v4.png']},'primaryRuler':[.305,.3267],'interiorRuler':[.165,.177],'frames':records,'excludedPrimaryPoses':[0,2,3],'scope':'fixed source rulers;body lowers naturally;local boot registration;retained furniture translation reviewed separately'}
 for name,data in [('manifest.json',m),('registration.json',registration),('frame-hashes.json',hashes),('material-grade.json',{'primary':primary[-1],'interiors':middle[-1],'authority':registration['idleAuthority']})]:(P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(34,52,62));d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):board.paste(im,(i*256,0),im);board.paste(idle,(i*256,256),idle);d.text((i*256+6,6),str(i),fill='white')
 board.save(P/'contact-sheet.png');print('Built north sitting transition pair;800ms;seated idle/contact acceptance pending')
if __name__=='__main__':main()
