"""Fixed source proportions, planted boot registration and exact idle endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent
SOURCE=P/'sources/recovery-v1.png'
IDLE=P.parent/'crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png'
HEADS=[(310,19),(766,55),(1226,83),(311,577),(766,532),(1226,526)]
SX=.287;SY=.3217
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
  face|=(abs(xx-hx)<38)&(yy>=hy+23)&(yy<hy+75)
  patch|=(abs(xx-hx)<115)&(yy>hy+65)&(yy<hy+160)
 warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(raw[:,:,3]>200)
 hair&=warm;face&=warm&(rgb.mean(2)>65);patch&=(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])&(raw[:,:,3]>200)
 rh=(ref[:,:,3]>180)&(ry>=24)&(ry<33)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]);rf=(ref[:,:,3]>180)&(abs(rx-92)<12)&(ry>=33)&(ry<50)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])&(rr.mean(2)>65);rp=(ref[:,:,3]>180)&(ry>50)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])
 gains={}
 for name,mask,authority in [('hair',hair,rh),('face',face,rf),('burgundy',patch,rp)]:
  gain=np.median(rr[authority],axis=0)/np.median(rgb[mask],axis=0);gains[name]=gain.tolist();grade[mask,:3]=np.clip(rgb[mask]*gain,0,255).astype('uint8')
 by,bx=np.where(ref[:,:,3]>180);ground=int(by.max()+52);boot=float(np.median(bx[(by>=by.max()-6)&(bx>np.median(bx))]))+36
 idle=Image.new('RGBA',(256,256));idle.paste(Image.fromarray(ref),(36,52));frames=[idle];records=[]
 for i in [1,2,3,4]:
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
  sole=float(y.max());front=float(np.median(x[(y>=y.max()-10)&(x>np.median(x))]));a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*SX),round(im.height*SY)),Image.Resampling.LANCZOS);pos=(round(boot-(front-box[0])*SX),round(ground-(sole-box[1])*SY));plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane)
  hx,hy=HEADS[i];records.append({'sourcePose':i,'sourceBox':box,'scaleX':SX,'scaleY':SY,'sourceFrontBoot':[front,sole],'targetFrontBoot':[boot,ground],'position':pos,'headAxis':[round(pos[0]+(hx-box[0])*SX),round(pos[1]+(hy-box[1])*SY)],'headTiltDegrees':[0,0,0,0,0,0][i]})
 frames.append(idle.copy());hashes={};files=[]
 for i,im in enumerate(frames):
  f=P/'frames/recover-air-south'/f'{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);file=f.relative_to(P).as_posix();files.append(file);hashes[file]=hashlib.sha256(f.read_bytes()).hexdigest()
 state={'id':'recover-air-south','frameFiles':files,'frameDurationsMs':[500]*6,'loop':False,'facings':['south']*6,'waterKinds':['recover']*6,'waterPoses':[False]*6,'depthOffsets':[0]*6,'provenance':'four authored standing breathing recovery interiors;exact selected idle at both ends'}
 manifest={'name':'Bill south coherent air recovery candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','states':[state]}
 registration={'source':'sources/recovery-v1.png','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'generation':'exec-ae41ea4f-3961-4ca2-aa99-e3c3dce6a845','scaleX':SX,'scaleY':SY,'ruler':'one frozen source correction:66px selected shoulder span and148px upright height against230px source width and460px height;no per-pose height correction','unusedSourcePoses':[0,5],'idleAuthority':IDLE.relative_to(P.parent).as_posix(),'idleSha256':hashlib.sha256(IDLE.read_bytes()).hexdigest(),'idlePadding':[36,52],'frames':records}
 for file,data in [('manifest.json',manifest),('registration.json',registration),('material-grade.json',{'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'gains':gains,'authority':registration['idleAuthority'],'scope':'one atlas material grade,face/hair/shoulder separately bounded'}),('frame-hashes.json',hashes)]: (P/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,512),(29,43,51));d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):board.paste(im,(i*256,0),im);d.text((i*256+4,4),str(i),fill='white');board.paste(idle,(i*256,256),idle)
 board.save(P/'contact-sheet.png');print('Built south recovery;fixed proportions/planted boots;exact idle ends')
if __name__=='__main__':main()
