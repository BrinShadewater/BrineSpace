"""Fixed source proportions, planted boot registration and exact idle endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
SOURCE=P/'sources/recovery-head-v2.png'
IDLE=P.parent/'crew-runtime-matte-v1/bill/frames/idle-west-breathing-v1/000.png'
HEADS=[(276,50),(719,69),(1198,96),(237,599),(732,545),(1240,538)]
SX=.27;SY=.3356
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2]);labs,_=label(raw[:,:,3]>180);n=np.bincount(labs.ravel());n[0]=0
 ids=sorted(np.argsort(n)[-6:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
 ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22);rn=(ref[:,:,3]>200)&(ry>50)&(np.ptp(rr,axis=2)<22)
 src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[rn],q);mapped=np.interp(rgb.mean(2),src,dst);w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 grade=raw.copy();grade[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8')
 hair=np.zeros(raw.shape[:2],bool);face=hair.copy();patch=hair.copy()
 for hx,hy in HEADS:
  hair|=(abs(xx-hx)<43)&(yy>=hy)&(yy<hy+40)
  face|=(xx<hx)&(xx>hx-45)&(yy>=hy+23)&(yy<hy+75)
  patch|=(xx>hx+5)&(xx<hx+90)&(yy>hy+65)&(yy<hy+160)
 warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(raw[:,:,3]>200)
 hair&=warm;face&=warm&(rgb.mean(2)>65);patch&=(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])&(raw[:,:,3]>200)
 rh=(ref[:,:,3]>180)&(ry>=24)&(ry<33)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]);rf=(ref[:,:,3]>180)&(rx<92)&(ry>=33)&(ry<50)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])&(rr.mean(2)>65);rp=(ref[:,:,3]>180)&(ry>50)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])
 gains={}
 for name,mask,authority in [('hair',hair,rh),('face',face,rf),('burgundy',patch,rp)]:
  gain=np.median(rr[authority],axis=0)/np.median(rgb[mask],axis=0);gains[name]=gain.tolist();grade[mask,:3]=np.clip(rgb[mask]*gain,0,255).astype('uint8')
 by,bx=np.where(ref[:,:,3]>180);ground=int(by.max()+52);boot=float(np.median(bx[(by>=by.max()-6)&(bx>np.median(bx))]))+36
 idle=Image.new('RGBA',(256,256));idle.paste(Image.fromarray(ref),(36,52));frames=[idle];records=[]
 for i in [1,2,3,4]:
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
  sole=float(y.max());front=float(np.median(x[(y>=y.max()-10)&(x>np.median(x))]));a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*SX),round(im.height*SY)),Image.Resampling.LANCZOS);pos=(round(boot-(front-box[0])*SX),round(ground-(sole-box[1])*SY));plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane)
  hx,hy=HEADS[i];records.append({'sourcePose':i,'sourceBox':box,'scaleX':SX,'scaleY':SY,'sourceFrontBoot':[front,sole],'targetFrontBoot':[boot,ground],'position':pos,'headAxis':[round(pos[0]+(hx-box[0])*SX),round(pos[1]+(hy-box[1])*SY)],'headTiltDegrees':[0,-5,-12,-15,-6,0][i]})
 frames.append(idle.copy());hashes={};files=[]
 for i,im in enumerate(frames):
  f=P/'frames/recover-air-west'/f'{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);file=f.relative_to(P).as_posix();files.append(file);hashes[file]=hashlib.sha256(f.read_bytes()).hexdigest()
 state={'id':'recover-air-west','frameFiles':files,'frameDurationsMs':[500]*6,'loop':False,'facings':['west']*6,'waterKinds':['recover']*6,'waterPoses':[False]*6,'depthOffsets':[0]*6,'provenance':'four authored standing breathing recovery interiors;exact selected idle at both ends'}
 manifest={'name':'Bill west coherent air recovery candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','states':[state]}
 registration={'source':'sources/recovery-head-v2.png','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'generation':'exec-ed3ea8a5-c87c-46b0-8cb9-b283b5622d06','scaleX':SX,'scaleY':SY,'ruler':'one frozen source correction:44px master body width and148px standing height;no per-pose height correction','unusedSourcePoses':[0,5],'idleAuthority':IDLE.relative_to(P.parent).as_posix(),'idleSha256':hashlib.sha256(IDLE.read_bytes()).hexdigest(),'idlePadding':[36,52],'frames':records}
 for file,data in [('manifest.json',manifest),('registration.json',registration),('material-grade.json',{'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'gains':gains,'authority':registration['idleAuthority'],'scope':'one atlas material grade,face/hair/shoulder separately bounded'}),('frame-hashes.json',hashes)]: (P/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51));d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):board.paste(im,(i*256,0),im);d.text((i*256+4,4),str(i),fill='white');board.paste(idle,(i*256,256),idle)
 board.save(P/'contact-sheet.png');print('Built west recovery;fixed proportions/planted boots;exact idle ends')
if __name__=='__main__':main()
