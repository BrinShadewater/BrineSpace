"""Native master-head consistency layer over independently authored run bodies."""
from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import binary_fill_holes,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1];states=[];equipment=[];records=[];strides={}
for direction in ['east','west','south','north']:
 B=P.parent/f'bill-run-{direction}-coherent-v1';master=P.parent/f'bill-seated-{direction}-coherent-v1/frames/sit-down-{direction}/000.png';ref=np.array(Image.open(master).convert('RGBA'));rgb=ref[:,:,:3].astype(int);y,x=np.indices(ref.shape[:2]);reg=json.loads((B/'helmet-registration.json').read_text());top=int(reg['idleAxis'][1]);warm=(ref[:,:,3]>0)&(y>=top-3)&(y<top+28)&(x>=100)&(x<166)&(rgb[:,:,0]>1.10*rgb[:,:,1])&(rgb[:,:,1]>1.10*rgb[:,:,2])&(np.ptp(rgb,axis=2)>7);mask=np.zeros(ref.shape[:2],bool)
 crown=(ref[:,:,3]>180)&(y>=top)&(y<top+14)&(x>=100)&(x<166);cy,cx=np.where(crown);left=int(cx.min())-(4 if direction=='west' else 2);right=int(cx.max())+(5 if direction=='east' else 3);warm&=(x>=left)&(x<right)
 for yy in range(top-3,top+28):
  xx=np.where(warm[yy])[0]
  if len(xx):mask[yy,max(0,int(xx.min())-1):min(256,int(xx.max())+2)]=True
 mask=binary_dilation(binary_fill_holes(mask),iterations=2)&(ref[:,:,3]>0)&(y>=top-3)&(y<top+25)&(x>=left)&(x<right);a=ref.copy();a[~mask]=0;yy,xx=np.where(mask);box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];head=Image.fromarray(a).crop(box);(P/'sources').mkdir(exist_ok=True);head_path=P/f'sources/{direction}-master-head.png';head.save(head_path)
 m=json.loads((B/'manifest.json').read_text());state=copy.deepcopy(m['states'][0]);files=[];frames=[];strides.update(m['strideDistanceCells'])
 for i,f in enumerate(state['frameFiles']):
  im=Image.open(R/f[6:]).convert('RGBA');a=np.array(im);anchor=reg['frames'][i]['headAxis'];dx=round(anchor[0]-reg['idleAxis'][0]);dy=anchor[1]-reg['idleAxis'][1];pos=[box[0]+dx,box[1]+dy];hmask=(a[:,:,3]>180)&(x>=100)&(x<166)&(y>=anchor[1])&(y<anchor[1]+14);yy,xx=np.where(hmask);x0=int(xx.min())-6;x1=int(xx.max())+7;y0=anchor[1];y1=y0+27;rgb=a[:,:,:3].astype(int);oldwarm=(a[:,:,3]>0)&(x>=x0)&(x<x1)&(y>=y0)&(y<y1)&(rgb[:,:,0]>1.10*rgb[:,:,1])&(rgb[:,:,1]>1.10*rgb[:,:,2])&(np.ptp(rgb,axis=2)>7);oldmask=np.zeros(a.shape[:2],bool)
  for yy in range(y0,y1):
   xx=np.where(oldwarm[yy])[0]
   if len(xx):oldmask[yy,int(xx.min()):int(xx.max())+1]=True
  oldmask=(binary_dilation(binary_fill_holes(oldmask),iterations=2)|((y>=y0-3)&(y<y0+15)))&(a[:,:,3]>0)&(y>=y0-3)&(y<y1)&(x>=x0)&(x<x1);a[oldmask]=0;opaque_y=np.where(np.array(head)[:,:,3]>160)[0];pos[1]=y1-1-int(opaque_y.max());out=Image.fromarray(a);out.alpha_composite(head,pos);dest=P/f'frames/run-{direction}/{i:03}.png';dest.parent.mkdir(parents=True,exist_ok=True);out.save(dest);files.append('res://'+dest.relative_to(R).as_posix());maskfile=P/f'sources/erase-{direction}-{i:03}.png';Image.fromarray(oldmask.astype('uint8')*255).save(maskfile);frames.append({'frame':i,'originalFile':f,'originalSha256':hashlib.sha256((R/f[6:]).read_bytes()).hexdigest(),'headPosition':pos,'collarBaselineY':y1,'eraseRect':[x0,y0-3,x1,y1],'eraseMask':maskfile.relative_to(P).as_posix(),'componentSize':list(head.size),'nativeScale':1})
 state['frameFiles']=files;states.append(state);equipment.append(copy.deepcopy(json.loads((B/'helmet-manifest.json').read_text())['states'][0]));records.append({'direction':direction,'master':master.relative_to(R).as_posix(),'masterSha256':hashlib.sha256(master.read_bytes()).hexdigest(),'sourceBox':box,'componentFile':head_path.relative_to(P).as_posix(),'nativeScale':1,'frames':frames})
 board=Image.new('RGB',(1792,1024),(34,52,62));draw=ImageDraw.Draw(board)
 for row,paths in enumerate([[master]+[R/f[6:] for f in m['states'][0]['frameFiles']],[master]+[R/f[6:] for f in files]]):
  for col,f in enumerate(paths):
   im=Image.open(f).convert('RGBA');board.paste(im,(col*256,row*512),im);crop=im.crop((100,65,166,115)).resize((198,150),Image.Resampling.NEAREST);board.paste(crop,(col*256+29,row*512+310),crop)
  draw.text((12,row*512+270),'Original selected' if row==0 else 'Native master head selected',fill='white')
 board.save(P/f'{direction}-head-review.png')
m={'name':'Bill native master-head cardinal run consistency layer','status':'selected_runtime','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'strideDistanceCells':strides,'states':states};(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');m=copy.deepcopy(m);m.update(name='Bill unchanged native shared-helmet cardinal runs',equipment='diving-helmet');m['states']=equipment;(P/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n');(P/'head-registration.json').write_text(json.dumps({'directions':records,'scope':'Native accepted head pixels segmented by warm per-row silhouette, source body/gray collar protected, no resampling; all directional collar/shoulder joins require visual review'},indent=2)+'\n');print('24 native master-head candidates;24 original equipped frames referenced unchanged; normal paired override selected')


