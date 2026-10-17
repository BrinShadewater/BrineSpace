"""One source-family material curve, protected head support and .24 atlas ruler."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1];q=[0,15,35,55,75,90,100]
def masks(a):
 v=a[:,:,:3].astype(float);sm=(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12);lab,n=label(sm);c=np.bincount(lab.ravel());assert n>0;skin=lab==(1+np.argmax(c[1:]));y,x=np.where(skin);fb=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];w=fb[2]-fb[0];Y,X=np.indices(a.shape[:2]);head=(X>fb[0]-w*.45)&(X<fb[2]+w*.45)&(Y>fb[1]-w*1.8)&(Y<fb[3]+2)
 return {'skin':skin,'cloth':~head&(a[:,:,3]>200)&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),'patch':~head&(a[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)},fb,head
refs=[R/'character/veld-water-east-coherent-v1/frames/bare/swim-east/000.png',R/'character/veld-water-south-coherent-v1/frames/bare/swim-south/000.png'];images=[np.array(Image.open(H/f'source-crops/{i:03}.png').convert('RGBA')) for i in range(3)];values={k:[] for k in ['cloth','skin','patch']};targets={k:[] for k in values}
for a in images:
 m,fb,head=masks(a)
 for k in values:values[k].extend(a[:,:,:3][m[k]])
for p in refs:
 a=np.array(Image.open(p).convert('RGBA'));m,fb,head=masks(a)
 for k in values:targets[k].extend(a[:,:,:3][m[k]])
curves={k:{'knots':np.percentile(np.mean(values[k],axis=1),q).tolist(),'targets':np.percentile(targets[k],q,axis=0).tolist()} for k in values}
board=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(board);records=[];checks=0
for row in range(2):
 board.alpha_composite(Image.open(refs[0]).convert('RGBA'),(0,row*280+24));board.alpha_composite(Image.open(refs[1]).convert('RGBA'),(1280,row*280+24))
for i,raw in enumerate(images):
 a=raw.copy();v=a[:,:,:3].astype(float);m,fb,head=masks(a)
 for k,mask in m.items():
  for c in range(3):a[mask,c]=np.interp(v[mask].mean(1),curves[k]['knots'],np.array(curves[k]['targets'])[:,c]).clip(0,255).astype('uint8')
 union=m['skin']|m['cloth']|m['patch'];assert np.array_equal(raw[~union],a[~union]);checks+=1;assert np.array_equal(raw[:,:,3],a[:,:,3]);checks+=1;assert np.array_equal(raw[head&~m['skin']],a[head&~m['skin']]);checks+=1
 scale=.24;t=(i+1)/5;target=np.array([153,121])*(1-t)+np.array([128,150])*t;face=np.array([(fb[0]+fb[2])/2,fb[3]]);pos=np.rint(target-face*scale).astype(int)
 for row,im in enumerate([raw,a]):
  pose=Image.fromarray(im).resize((round(im.shape[1]*scale),round(im.shape[0]*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(256,256));out.alpha_composite(pose,tuple(pos));ar=np.array(out);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
  if row==1:
   path=H/f'graded-trials/{i:03}.png';path.parent.mkdir(exist_ok=True);out.save(path)
  board.alpha_composite(out,((i+1)*256,row*280+24));draw.text(((i+1)*256+4,row*280+4),('raw' if row==0 else 'shared grade')+f' slot{i}',fill='white')
 overlay=raw.copy();overlay[m['cloth'],:3]=[220,80,180];overlay[m['patch'],:3]=[40,255,50];overlay[m['skin'],:3]=[255,180,50];Image.fromarray(overlay).save(H/f'graded-trials/mask-{i:03}.png');records.append({'slot':i,'scale':scale,'position':pos.tolist(),'faceBox':fb,'materialPixels':{k:int(v.sum()) for k,v in m.items()}})
board.save(H/'material-trials-v1.png');(H/'material-fit-v1.json').write_text(json.dumps({'checks':checks,'failures':0,'curves':curves,'records':records,'headExceptSkinExact':True,'sourceAlphaExact':True,'ungradedPixelsExact':True,'status':'3 raw atlas poses graded .24 trials only; fourth source and motion/helmet gate remain','referenceHashes':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in refs}},indent=2)+'\n');print(f'{checks} material ownership/head/alpha/border checks PASS; no selected manifest')
