from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;B=P.parent/'bill-seated-south-coherent-v1';H=P.parent/'bill-seated-helmet-south-coherent-v1'
IDLE=P.parent/'crew-runtime-matte-v1/bill/frames/idle-south-matte-v2/000.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(source,heads,density):
 raw=np.array(Image.open(source).convert('RGBA'));rgb=raw[:,:,:3].astype(float);yy,xx=np.indices(raw.shape[:2]);labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=sorted(np.argsort(counts)[-6:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
 ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2]);q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22);rn=(ref[:,:,3]>200)&(ry>50)&(np.ptp(rr,axis=2)<22);src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(rr.mean(2)[rn],q);mapped=np.interp(rgb.mean(2),src,dst);w=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0);grade=raw.copy();grade[:,:,:3]=np.clip(rgb*(1-w[:,:,None])+mapped[:,:,None]*w[:,:,None],0,255).astype('uint8')
 hair=np.zeros(raw.shape[:2],bool);face=hair.copy();patch=hair.copy()
 for hx,hy in heads:
  hair|=(abs(xx-hx)<43*density)&(yy>=hy)&(yy<hy+40*density)
  face|=(abs(xx-hx)<38*density)&(yy>=hy+23*density)&(yy<hy+75*density)
  patch|=(abs(xx-hx)<115*density)&(yy>hy+65*density)&(yy<hy+160*density)
 warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(raw[:,:,3]>200);hair&=warm;face&=warm&(rgb.mean(2)>65);patch&=(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])&(raw[:,:,3]>200)
 rh=(ref[:,:,3]>180)&(ry>=24)&(ry<33)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]);rf=(ref[:,:,3]>180)&(abs(rx-92)<12)&(ry>=33)&(ry<50)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2])&(rr.mean(2)>65);rp=(ref[:,:,3]>180)&(ry>50)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2]);gains={}
 for name,mask,authority in [('hair',hair,rh),('face',face,rf),('burgundy',patch,rp)]:
  gain=np.median(rr[authority],axis=0)/np.median(rgb[mask],axis=0);gains[name]=gain.tolist();grade[mask,:3]=np.clip(rgb[mask]*gain,0,255).astype('uint8')
 return raw,labs,ids,grade,{'neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'gains':gains}
def main():
 endpoint=Image.open(B/'frames/sit-down-south/005.png').convert('RGBA');helmet_endpoint=Image.open(H/'frames/sit-down-south/005.png').convert('RGBA');ar=np.array(endpoint);y,x=np.where(ar[:,:,3]>180);ground=int(y.max());boot=float(np.median(x[(y>=ground-4)&(x>np.median(x))]));head=Image.open(H/'sources/canonical-head.png').convert('RGBA');yy,xx=np.indices((256,256));packs={'bare':[],'helmet':[]};hashes={};records={};grades={};reviews=[]
 specs=[('sit-idle','breathing-v1.png',[(266,17),(768,18),(1270,12),(266,520),(768,521),(1270,521)],.22,.25,1.3,[1,2,3,4]),('read-seated','reading-v1.png',[(263,8),(768,8),(1278,8),(263,522),(772,522),(1280,522)],.207,.2445,1.35,list(range(6)))]
 for action,name,heads,sx,sy,density,poses in specs:
  raw,labs,ids,grade,curve=prepare(P/'sources'/name,heads,density);bare=[endpoint] if action=='sit-idle' else [];helmet=[helmet_endpoint] if action=='sit-idle' else [];rows=[]
  for i in poses:
   mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(labs==ids[i]);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];a=grade.copy();a[~mask]=0;im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*sx),round(im.height*sy)),Image.Resampling.LANCZOS)
   # Register the opaque boot after the single fixed resize. Theoretical source
   # coordinates can miss the resampled alpha contact by one or two pixels.
   by,bx=np.where(np.array(im)[:,:,3]>180);sole=int(by.max());front=float(np.median(bx[(by>=sole-4)&(bx>np.median(bx))]));pos=(round(boot-front),ground-sole);plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);hx,hy=heads[i];hx=round(pos[0]+(hx-box[0])*sx);hy=round(pos[1]+(hy-box[1])*sy);bare.append(plane)
   a=np.array(plane);rgb=a[:,:,:3].astype(float);erase=(xx>=hx-14)&(xx<=hx+16)&(yy>=hy-2)&(yy<hy+35)&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.14*rgb[:,:,2]);out=a.copy();out[erase]=0;helmet_im=Image.fromarray(out);helmet_im.alpha_composite(head,(hx-18,hy-8));out=np.array(helmet_im);out[hy+35:]=a[hy+35:];helmet.append(Image.fromarray(out));rows.append({'frame':len(bare)-1,'sourcePose':i,'sourceBox':box,'position':pos,'headAxis':[hx,hy],'protectedBodyFromY':hy+35,'scaleX':sx,'scaleY':sy})
  if action=='sit-idle':bare.append(endpoint.copy());helmet.append(helmet_endpoint.copy())
  for gear,images in [('bare',bare),('helmet',helmet)]:
   files=[]
   for i,im in enumerate(images):
    f=P/f'frames/{gear}/{action}-south/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);im.save(f);file=f.relative_to(P).as_posix();files.append(file);hashes[file]=sha(f)
   packs[gear].append({'id':action+'-south','frameFiles':files,'frameDurationsMs':[160]*6,'loop':True,'facings':['south']*6,'waterPoses':[False]*6,'waterKinds':[action]*6,'depthOffsets':[40]*6})
  records[action]={'source':name,'sourceSha256':sha(P/'sources'/name),'fixedRuler':[sx,sy],'density':density,'frames':rows};grades[action]=curve;reviews.extend([bare,helmet])
 for gear,states in packs.items():
  m={'name':'Bill south seated loops '+gear,'frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'precomposed':True,'textureFilter':'linear','status':'staged_candidate','states':states}
  if gear=='helmet':m['equipment']='diving-helmet'
  (P/(gear+'-manifest.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,1024),(34,52,62))
 for j,images in enumerate(reviews):
  for i,im in enumerate(images):board.paste(im,(i*256,j*256),im)
 board.save(P/'contact-sheet.png')
 for name,data in [('registration.json',records),('material-grade.json',grades),('frame-hashes.json',hashes)]: (P/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 print('Built south seated breathing/reading:4gear states/24refs;shared master grade/native helmet')
if __name__=='__main__':main()
