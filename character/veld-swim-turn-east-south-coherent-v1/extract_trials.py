"""Extract independent yaw poses and compare uniform physical rulers; no selection."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
source=H/'bare-source-v1.png';a=np.array(Image.open(source).convert('RGBA'));lab,n=label(a[:,:,3]>160);counts=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:counts[k],reverse=True)[:4];assert len(ids)==4
ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/2)),np.where(lab==k)[1].mean()))
records=[];checks=0;crops=[]
for i,k in enumerate(ids):
 y,x=np.where(lab==k);box=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3];assert box[0]>=0 and box[1]>=0 and box[2]<=a.shape[1] and box[3]<=a.shape[0];checks+=1
 cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;im=Image.fromarray(cut).crop(box);ar=np.array(im);v=ar[:,:,:3].astype(float)
 sm=(ar[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12);fl,fn=label(sm);fc=np.bincount(fl.ravel());assert fn>0;face=fl==(1+np.argmax(fc[1:]));fy,fx=np.where(face);fb=[int(fx.min()),int(fy.min()),int(fx.max()+1),int(fy.max()+1)];checks+=1
 (H/'source-crops').mkdir(exist_ok=True);im.save(H/f'source-crops/{i:03}.png');crops.append((im,fb));records.append({'slot':i,'sourceBox':box,'faceBox':fb,'requestedYaw':18+18*i})
board=Image.new('RGBA',(1536,840),'#202a30');draw=ImageDraw.Draw(board)
e=Image.open(R/'character/veld-water-east-coherent-v1/frames/bare/swim-east/000.png').convert('RGBA');s=Image.open(R/'character/veld-water-south-coherent-v1/frames/bare/swim-south/000.png').convert('RGBA')
for row,scale in enumerate([.24,.26,.28]):
 board.alpha_composite(e,(0,row*280+24));board.alpha_composite(s,(1280,row*280+24));draw.text((4,row*280+4),f'selected east / uniform scale {scale}',fill='white')
 for i,(im,fb) in enumerate(crops):
  t=(i+1)/5;target=np.array([153,121])*(1-t)+np.array([128,150])*t;face=np.array([(fb[0]+fb[2])/2,fb[3]]);pos=np.rint(target-face*scale).astype(int)
  pose=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(256,256));out.alpha_composite(pose,tuple(pos));ar=np.array(out);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
  path=H/f'body-trials/scale-{scale}/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);out.save(path);board.alpha_composite(out,((i+1)*256,row*280+24));draw.text(((i+1)*256+4,row*280+4),f'source slot{i}; fixed {scale}',fill='white')
board.save(H/'physical-ruler-trials-v1.png')
(H/'source-fit-v1.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceSize':list(a.shape[1::-1]),'records':records,'status':'ungraded source and uniform ruler trials; no selected manifest or runtime changes','yawCaveat':'Generated last pose approaches south early; angular pacing and helmet fit need review'},indent=2)+'\n')
print(f'{checks} extraction/face/border checks PASS; four sources and12 uniform-scale trials saved; not selected')
