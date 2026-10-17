"""Authored basic water yaw, frozen atlas scale and exact registered endpoints."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'sources/pickup-v1.png'
HEADS=[(276,266),(752,266),(1262,266),(277,766),(752,766),(1262,766)]
SCALE=.25
ENDPOINTS=[('bill-salvage-south-coherent-v1/frames/salvage-south/000.png',(0,0)),('bill-swim-carry-south-coherent-v1/frames/swim-carry-south/000.png',(24,-24))]
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));rgb=raw[:,:,:3].astype(float);sy,sx=np.indices(raw.shape[:2])
 labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.median(np.where(labs==k)[0]))//512,int(np.where(labs==k)[1].min())))
 authority=[];red_authority=[];hair_authority=[]
 for direction in ['south']:
  a=np.array(Image.open(HERE.parent/f'crew-runtime-matte-v1/bill/frames/idle-{direction}-breathing-v1/000.png').convert('RGBA'));ar=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2])
  authority.extend(ar.mean(2)[(a[:,:,3]>200)&(yy>53)&(np.ptp(ar,axis=2)<22)].tolist())
  red_authority.extend(ar[(a[:,:,3]>200)&(yy>53)&(ar[:,:,0]>1.4*ar[:,:,1])&(ar[:,:,0]>1.4*ar[:,:,2])].tolist())
  hair_authority.extend(ar[(a[:,:,3]>180)&(yy>=25)&(yy<32)&(ar[:,:,0]>1.12*ar[:,:,1])&(ar[:,:,1]>1.25*ar[:,:,2])].tolist())
 q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];neutral=(raw[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)
 src=np.quantile(rgb.mean(2)[neutral],q);dst=np.quantile(authority,q);mapped=np.interp(rgb.mean(2),src,dst)
 weight=np.clip((22-np.ptp(rgb,axis=2))/14,0,1)*(raw[:,:,3]>0)
 graded=raw.copy();graded[:,:,:3]=np.clip(rgb*(1-weight[:,:,None])+mapped[:,:,None]*weight[:,:,None],0,255).astype('uint8')
 heads=np.zeros(raw.shape[:2],bool);crowns=heads.copy()
 for hx,hy in HEADS:
  heads|=(abs(sx-hx)<65)&(sy>=hy-5)&(sy<hy+85)
  crowns|=(abs(sx-hx)<48)&(sy>=hy)&(sy<hy+30)
 patch_region=np.zeros(raw.shape[:2],bool)
 for px,py in [(190,302),(365,302),(665,307),(849,291),(1180,302),(1361,302),(179,813),(377,813),(668,813),(848,813),(1170,813),(1358,813)]:patch_region|=((sx-px)**2+(sy-py)**2<32**2)
 patch=patch_region&(raw[:,:,3]>200)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])
 hair=(raw[:,:,3]>180)&crowns&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])
 hair_authority=[]
 for path,center in [(ENDPOINTS[0][0],(128,110)),(ENDPOINTS[1][0],(104,134))]:
  a=np.array(Image.open(HERE.parent/path).convert('RGBA'));hx,hy=center;c=a[hy:hy+9,hx-12:hx+13];cr=c[:,:,:3].astype(float);cm=(c[:,:,3]>180)&(cr[:,:,0]>1.12*cr[:,:,1])&(cr[:,:,1]>1.25*cr[:,:,2]);hair_authority.extend(cr[cm].tolist())
 patch_gain=np.median(red_authority,axis=0)/np.median(rgb[patch],axis=0);hair_gain=np.median(hair_authority,axis=0)/np.median(rgb[hair],axis=0)
 graded[patch,:3]=np.clip(rgb[patch]*patch_gain,0,255).astype('uint8');graded[hair,:3]=np.clip(rgb[hair]*hair_gain,0,255).astype('uint8')
 cyan=(raw[:,:,3]>180)&(rgb[:,:,1]>1.4*rgb[:,:,0])&(rgb[:,:,2]>1.4*rgb[:,:,0])&(rgb[:,:,1]>60)
 cyan_reference=[]
 for path,pad in ENDPOINTS:
  a=np.array(Image.open(HERE.parent/path).convert('RGBA'));ar=a[:,:,:3].astype(float);cm=(a[:,:,3]>180)&(ar[:,:,1]>1.4*ar[:,:,0])&(ar[:,:,2]>1.4*ar[:,:,0])&(ar[:,:,1]>60);cyan_reference.extend(ar[cm].tolist())
 cyan_gain=np.median(cyan_reference,axis=0)/np.median(rgb[cyan],axis=0);graded[cyan,:3]=np.clip(rgb[cyan]*cyan_gain,0,255).astype('uint8')
 face_region=np.zeros(raw.shape[:2],bool)
 for hx,hy in HEADS:face_region|=(abs(sx-hx)<=40)&(sy>=hy+65)&(sy<hy+118)
 face=face_region&(raw[:,:,3]>180)&(rgb[:,:,0]>1.3*rgb[:,:,1])&(rgb[:,:,1]>1.1*rgb[:,:,2])&(rgb.mean(2)>45)
 reference=np.array(Image.open(HERE.parent/'bill-swim-south-coherent-v1/frames/swim-south/000.png').convert('RGBA'))[152:167,92:117];rr=reference[:,:,:3].astype(float)
 skin=(reference[:,:,3]>180)&(rr[:,:,0]>1.3*rr[:,:,1])&(rr[:,:,1]>1.1*rr[:,:,2])&(rr.mean(2)>45)
 face_gain=np.median(rr[skin],axis=0)/np.median(rgb[face],axis=0);graded[face,:3]=np.clip(rgb[face]*face_gain,0,255).astype('uint8')
 frames=[];records=[]
 for path,pad in ENDPOINTS:
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(HERE.parent/path).convert('RGBA'),pad);frames.append(plane)
 start,end=frames;frames=[start]
 for i in [1,2,3,4]:
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  isolated=graded.copy();isolated[~mask]=0;im=Image.fromarray(isolated).crop(box);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS)
  target=(128,110);hx,hy=HEADS[i];pos=(round(target[0]-(hx-box[0])*SCALE),round(target[1]-(hy-box[1])*SCALE))
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane);records.append({'sourcePose':i,'alphaComponent':int(ids[i]),'sourceBox':box,'sourceCrownAxis':HEADS[i],'targetCrownAxis':target,'position':pos,'scale':SCALE})
 frames.append(end);times=[70,80,90,100,100,80];states=[];hashes={}
 for key,poses,durations,facings in [('swim-pickup-south',frames,times,['south']*6)]:
  files=[]
  for i,im in enumerate(poses):
   p=HERE/'frames'/key/f'{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);rel=p.relative_to(HERE).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
  states.append({'id':key,'frameFiles':files,'frameDurationsMs':durations,'loop':False,'facings':facings,'waterKinds':['salvage']+['swim']*5,'waterPoses':[True]*6,'depthOffsets':[0]*6,'provenance':'four authored pickup interiors;exact staged work and selected cargo endpoints'})
 manifest={'name':'Bill south underwater pickup candidate','frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'staged_candidate','states':states}
 registration={'source':'sources/pickup-v1.png','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'generation':'exec-59a6d403-305b-43a9-8df9-10b023fe19e1','scale':SCALE,'endpointAuthorities':[{'path':path,'padding':pad,'sha256':hashlib.sha256((HERE.parent/path).read_bytes()).hexdigest()} for path,pad in ENDPOINTS],'unusedSourcePoses':[0,5],'frames':records}
 grade={'authority':'south idle neutral/shoulder samples;current swimming crown samples','neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'burgundyGain':patch_gain.tolist(),'crownGain':hair_gain.tolist(),'cyanGain':cyan_gain.tolist(),'scope':'one frozen atlas curve/gain, bounded crown excludes face;no per-pose exposure or scale'}
 grade['faceGain']=face_gain.tolist();grade['faceScope']='one atlas-wide bounded skin gain against selected south swim;hair/suit excluded'
 for file,data in [('manifest.json',manifest),('registration.json',registration),('material-grade.json',grade),('frame-hashes.json',hashes)]: (HERE/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,256),(29,43,51));d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):board.paste(im,(i*256,0),im);d.text((i*256+5,5),str(i),fill='white')
 board.save(HERE/'contact-sheet.png');print('Built south pickup;exact work/cargo endpoints;four authored interiors')
if __name__=='__main__':main()
