"""Deterministically reuse native accepted head pixels; preserve source gait/body."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_fill_holes,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1];D='east';B=P.parent/'bill-run-east-coherent-v1';master=P.parent/'bill-seated-east-coherent-v1/frames/sit-down-east/000.png'
ref=np.array(Image.open(master).convert('RGBA'));rgb=ref[:,:,:3].astype(int);y,x=np.indices(ref.shape[:2]);reg=json.loads((B/'helmet-registration.json').read_text());top=int(reg['idleAxis'][1]);warm=(ref[:,:,3]>0)&(y>=top-3)&(y<top+28)&(x>=100)&(x<166)&(rgb[:,:,0]>rgb[:,:,1]+2)&(rgb[:,:,1]>rgb[:,:,2]+2)
mask=np.zeros(ref.shape[:2],bool)
for yy in range(top-3,top+28):
 xx=np.where(warm[yy])[0]
 if len(xx):mask[yy,max(0,int(xx.min())-1):min(256,int(xx.max())+2)]=True
mask=binary_dilation(binary_fill_holes(mask),iterations=2)&(ref[:,:,3]>0)&(y>=top-3)&(y<top+27);a=ref.copy();a[~mask]=0;yy,xx=np.where(mask);box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];head=Image.fromarray(a).crop(box);(P/'sources').mkdir(exist_ok=True);head.save(P/'sources/east-master-head.png')
m=json.loads((B/'manifest.json').read_text());files=[];records=[]
for i,f in enumerate(m['states'][0]['frameFiles']):
 im=Image.open(R/f[6:]).convert('RGBA');a=np.array(im);anchor=reg['frames'][i]['headAxis'];dx=round(anchor[0]-reg['idleAxis'][0]);dy=anchor[1]-reg['idleAxis'][1];pos=[box[0]+dx,box[1]+dy];hmask=(a[:,:,3]>180)&(x>=100)&(x<166)&(y>=anchor[1])&(y<anchor[1]+14);yy,xx=np.where(hmask);erase=[int(xx.min())-3,anchor[1],int(xx.max())+4,anchor[1]+27];x0,y0,x1,y1=erase;rgb=a[:,:,:3].astype(int);oldwarm=(a[:,:,3]>0)&(x>=x0)&(x<x1)&(y>=y0)&(y<y1)&(rgb[:,:,0]>rgb[:,:,1]+2)&(rgb[:,:,1]>rgb[:,:,2]+2);oldmask=np.zeros(a.shape[:2],bool)
 for yy in range(y0,y1):
  xx=np.where(oldwarm[yy])[0]
  if len(xx):oldmask[yy,int(xx.min()):int(xx.max())+1]=True
 oldmask=(binary_dilation(binary_fill_holes(oldmask),iterations=2)|((y>=y0-3)&(y<y0+15)))&(a[:,:,3]>0)&(y>=y0-3)&(y<y1)&(x>=x0)&(x<x1);a[oldmask]=0;out=Image.fromarray(a);out.alpha_composite(head,pos);dest=P/f'frames/run-east/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append('res://'+dest.relative_to(R).as_posix());records.append({'frame':i,'originalFile':f,'headPosition':pos,'eraseRect':[x0,y0-3,x1,y1],'componentSize':list(head.size),'nativeScale':1})
m['name']='Bill east native-master-head run candidate';m['status']='review_candidate';m['states'][0]['frameFiles']=files;(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');(P/'head-registration.json').write_text(json.dumps({'master':master.relative_to(R).as_posix(),'masterSha256':hashlib.sha256(master.read_bytes()).hexdigest(),'sourceBox':box,'headSize':list(head.size),'nativeScale':1,'frames':records,'scope':'Native accepted head segmented by warm per-row silhouette, no resampling; head/collar gap and shoulders must be visually reviewed before selection'},indent=2)+'\n')
board=Image.new('RGB',(1792,1024),(34,52,62));draw=ImageDraw.Draw(board)
for row,paths in enumerate([[master]+[R/f[6:] for f in json.loads((B/'manifest.json').read_text())['states'][0]['frameFiles']],[master]+[R/f[6:] for f in files]]):
 for col,f in enumerate(paths):
  im=Image.open(f).convert('RGBA');board.paste(im,(col*256,row*512),im);crop=im.crop((100,65,166,115)).resize((198,150),Image.Resampling.NEAREST);board.paste(crop,(col*256+29,row*512+310),crop)
 draw.text((12,row*512+270),'Original selected' if row==0 else 'Native master head candidate',fill='white')
board.save(P/'east-head-review.png');print('Six native-head east candidates built; no loader change')
