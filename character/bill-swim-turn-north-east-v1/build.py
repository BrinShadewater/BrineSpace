"""Authored basic water yaw, frozen atlas scale and exact registered endpoints."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent
SOURCE=HERE/'sources/turn-spacing-v2.png'
HEADS=[(236,142),(733,146),(1249,148),(329,651),(814,676),(1363,680)]
SCALE=.28
ENDPOINTS=[('bill-swim-north-coherent-v1/frames/swim-north/000.png',(24,56)),('bill-swim-east-coherent-v1/frames/swim-east/000.png',(6,40))]
def main():
 raw=np.array(Image.open(SOURCE).convert('RGBA'));rgb=raw[:,:,:3].astype(float);sy,sx=np.indices(raw.shape[:2])
 labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
 ids=sorted(np.argsort(counts)[-6:],key=lambda k:(int(np.median(np.where(labs==k)[0]))//512,int(np.where(labs==k)[1].min())))
 authority=[];red_authority=[];hair_authority=[]
 for direction in ['north','east']:
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
 for px,py in [(177,217),(299,217),(666,209),(788,230),(1289,242),(365,741),(773,761),(1319,772)]:patch_region|=((sx-px)**2+(sy-py)**2<32**2)
 patch=patch_region&(raw[:,:,3]>200)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])
 hair=(raw[:,:,3]>180)&crowns&(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])
 hair_authority=[]
 for path,center in [(ENDPOINTS[0][0],(104,48)),(ENDPOINTS[1][0],(148,64))]:
  a=np.array(Image.open(HERE.parent/path).convert('RGBA'));hx,hy=center;c=a[hy:hy+9,hx-12:hx+13];cr=c[:,:,:3].astype(float);cm=(c[:,:,3]>180)&(cr[:,:,0]>1.12*cr[:,:,1])&(cr[:,:,1]>1.25*cr[:,:,2]);hair_authority.extend(cr[cm].tolist())
 patch_gain=np.median(red_authority,axis=0)/np.median(rgb[patch],axis=0);hair_gain=np.median(hair_authority,axis=0)/np.median(rgb[hair],axis=0)
 graded[patch,:3]=np.clip(rgb[patch]*patch_gain,0,255).astype('uint8');graded[hair,:3]=np.clip(rgb[hair]*hair_gain,0,255).astype('uint8')
 cyan=(raw[:,:,3]>180)&(rgb[:,:,1]>1.4*rgb[:,:,0])&(rgb[:,:,2]>1.4*rgb[:,:,0])&(rgb[:,:,1]>60)
 cyan_reference=[]
 for path,pad in ENDPOINTS:
  a=np.array(Image.open(HERE.parent/path).convert('RGBA'));ar=a[:,:,:3].astype(float);cm=(a[:,:,3]>180)&(ar[:,:,1]>1.4*ar[:,:,0])&(ar[:,:,2]>1.4*ar[:,:,0])&(ar[:,:,1]>60);cyan_reference.extend(ar[cm].tolist())
 cyan_gain=np.median(cyan_reference,axis=0)/np.median(rgb[cyan],axis=0);graded[cyan,:3]=np.clip(rgb[cyan]*cyan_gain,0,255).astype('uint8')
 frames=[];records=[]
 for path,pad in ENDPOINTS:
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(Image.open(HERE.parent/path).convert('RGBA'),pad);frames.append(plane)
 start,end=frames;frames=[start]
 for i in [1,2,3,4]:
  mask=binary_dilation(labs==ids[i],iterations=3)&(raw[:,:,3]>0);y,x=np.where(mask);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
  isolated=graded.copy();isolated[~mask]=0;im=Image.fromarray(isolated).crop(box);im=im.resize((round(im.width*SCALE),round(im.height*SCALE)),Image.Resampling.LANCZOS)
  t=i/5;target=(128+26*t,104);hx,hy=HEADS[i];pos=(round(target[0]-(hx-box[0])*SCALE),round(target[1]-(hy-box[1])*SCALE))
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);frames.append(plane);records.append({'sourcePose':i,'sourceBox':box,'sourceCrownAxis':HEADS[i],'targetCrownAxis':target,'position':pos,'scale':SCALE})
 frames.append(end);times=[80,110,130,130,110,80];states=[];hashes={}
 for key,poses,durations,facings in [('swim-turn-north-east',frames,times,['north','north','north','east','east','east']),('swim-turn-east-north',frames[::-1],times[::-1],['east','east','east','north','north','north'])]:
  files=[]
  for i,im in enumerate(poses):
   p=HERE/'frames'/key/f'{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);rel=p.relative_to(HERE).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
  states.append({'id':key,'frameFiles':files,'frameDurationsMs':durations,'loop':False,'facings':facings,'waterKinds':['swim']*6,'waterPoses':[True]*6,'depthOffsets':[0]*6,'provenance':'four authored interior yaw poses;exact padded candidate loop endpoints;reverse derived without mirroring'})
 manifest={'name':'Bill north/east basic water turn candidate','frameWidth':256,'frameHeight':256,'pivot':[128,128],'standingHeight':148,'textureFilter':'linear','precomposed':True,'status':'installed_runtime_reviewed','states':states}
 registration={'source':'sources/turn-spacing-v2.png','sourceSha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'generation':'exec-a130826c-2cfe-42a3-b7c1-b362511b4d2c','originalGeneration':'exec-54473ea0-0cbc-42af-8a3a-38246fea8344','scale':SCALE,'endpointAuthorities':[{'path':path,'padding':pad,'sha256':hashlib.sha256((HERE.parent/path).read_bytes()).hexdigest()} for path,pad in ENDPOINTS],'unusedSourcePoses':[0,5],'frames':records}
 grade={'authority':'pooled north/east idle neutral/shoulder samples;current swimming crown samples','neutralInput':src.tolist(),'neutralOutput':dst.tolist(),'burgundyGain':patch_gain.tolist(),'crownGain':hair_gain.tolist(),'cyanGain':cyan_gain.tolist(),'scope':'one frozen atlas curve/gain, bounded crown excludes face;no per-pose exposure or scale'}
 for file,data in [('manifest.json',manifest),('registration.json',registration),('material-grade.json',grade),('frame-hashes.json',hashes)]: (HERE/file).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
 board=Image.new('RGB',(1536,256),(29,43,51));d=ImageDraw.Draw(board)
 for i,im in enumerate(frames):board.paste(im,(i*256,0),im);d.text((i*256+5,5),str(i),fill='white')
 board.save(HERE/'contact-sheet.png');print('Built two bare water-basic swim turns;exact endpoints;four authored intermediates')
if __name__=='__main__':main()
