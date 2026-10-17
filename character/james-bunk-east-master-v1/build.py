"""Fixed anatomical scale for the active seven-pose bunk choreography."""
from pathlib import Path
import json,copy,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
def extract(path):
 raw=Image.open(path).convert('RGBA');a=np.array(raw);labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=sorted(np.argsort(counts)[-7:],key=lambda k:np.where(labs==k)[0].mean());ordered=[]
 for subset in [ids[:4],ids[4:]]:ordered+=sorted(subset,key=lambda k:np.where(labs==k)[1].mean())
 cells=[];boxes=[]
 for k in ordered:
  y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4];x0,y0,x1,y1=box;cell=a[y0:y1,x0:x1].copy();cell[~binary_dilation(labs[y0:y1,x0:x1]==k,iterations=2)]=0;cells.append(Image.fromarray(cell));boxes.append(box)
 return cells,boxes
def ground(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>180);floor=int(y.max());yy=np.indices(a.shape[:2])[0];y,x=np.where((a[:,:,3]>180)&(yy>=floor-4));return np.array([x.mean(),floor])
def main():
 cells,boxes=extract(HERE/'source.png');master_folder=ROOT/'character/crew-runtime-matte-v1/branforth';m=json.loads((master_folder/'manifest.json').read_text());s=next(s for s in m['states'] if s['id']=='idle-east');master=Image.open(master_folder/s['frameFiles'][0]).convert('RGBA');ma=np.array(master);y,x=np.where(ma[:,:,3]>180);height=int(y.max()-y.min()+1);a=np.array(cells[0]);y,x=np.where(a[:,:,3]>180);scale=height/(y.max()-y.min()+1);target=ground(master)+[36,52];rows=[];tracking=[]
 for i,cell in enumerate(cells):
  anchor=ground(cell);at=np.rint(target-anchor*scale).astype(int);im=Image.new('RGBA',(256,256));im.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),tuple(at));rows.append(im);tracking.append(dict(sourceBox=boxes[i],translation=at.tolist()))
  dest=HERE/'registered-ungraded'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest)
  dest=HERE/'source-cells'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);cell.save(dest)
 # Explicit head ownership prevents horizontal resting faces from receiving cloth grade.
 head_boxes=[[104,70,141,104],[108,95,144,129],[70,103,107,138],[120,136,159,173],[39,153,76,190],[38,175,78,209],[52,189,95,225]]
 # Head boxes are reviewed against the registered ungraded contact before selection.
 rgb=np.array(rows[0])[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(rgb.shape[:2]);gold=(r-b>35)&(g-b>20)&(yy>110)&(yy<164)
 r,g,b=ma[:,:,:3].astype(float).transpose(2,0,1);my=np.indices(ma.shape[:2])[0];mg=(r-b>35)&(g-b>20)&(my>54)&(my<110);gain=np.median(ma[:,:,:3][mg],axis=0)/np.median(rgb[gold],axis=0)
 for i,im in enumerate(rows):
  a=np.array(im);rgb=a[:,:,:3].astype(float);r,g,b=rgb.transpose(2,0,1);yy,xx=np.indices(a.shape[:2]);x0,y0,x1,y1=head_boxes[i];head=(xx>=x0)&(xx<x1)&(yy>=y0)&(yy<y1);gold=(a[:,:,3]>0)&(r-b>35)&(g-b>20)&~head;body=(a[:,:,3]>0)&~head&~gold;lum=rgb.mean(2);mapped=np.interp(lum,[0,50,70,90,120,160,200,255],[0,50,68,80,99,126,149,170]);factor=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);rgb[body]*=factor[body,None];rgb[gold]*=gain;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');rows[i]=Image.fromarray(a);tracking[i]['protectedHeadBox']=head_boxes[i]
 fullmaster=Image.new('RGBA',(256,256));fullmaster.alpha_composite(master,(36,52));rows[0]=fullmaster
 retained=json.loads((ROOT/'character/chief-engineer-branforth-v2/supplemental/bunk-east/bare/manifest.json').read_text());pack=dict(name='James master-matched east bunk',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_bunk_master_revision',states=[]);hashes={}
 for action,indices in [('bunk-enter',list(range(7))),('bunk-exit',list(reversed(range(7)))),('bunk-sleep',[6])]:
  old=next(s for s in retained['states'] if s['id']==action+'-east');state=copy.deepcopy(old);files=[]
  for j,i in enumerate(indices):
   p=HERE/'frames/bare'/action/f'{j:03d}.png';p.parent.mkdir(parents=True,exist_ok=True);rows[i].save(p);files.append(p.relative_to(HERE).as_posix());hashes[files[-1]]=hashlib.sha256(p.read_bytes()).hexdigest()
  state.update(frameFiles=files,frameCount=len(files),facings=['east']*len(files),waterKinds=['sleep' if i==6 else 'idle' if i==0 else 'lie' for i in indices],waterPoses=[False]*len(files),provenance=dict(source='source.png',prompt='prompt.txt',fixedScale=float(scale),sourcePoses=indices,derivation='Independent seven-pose complete bodies; selected standing master; native choreography metadata, exact reversed exit and shared sleep'))
  pack['states'].append(state)
 (HERE/'bare-manifest.json').write_text(json.dumps(pack,indent=2)+'\n');(HERE/'registration.json').write_text(json.dumps(dict(fixedScale=float(scale),masterHeight=height,targetAnchor=target.tolist(),goldGain=gain.tolist(),tracking=tracking,sourceSha256=hashlib.sha256((HERE/'source.png').read_bytes()).hexdigest()),indent=2)+'\n');(HERE/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 contact=Image.new('RGB',(1792,640),'#303b40');draw=ImageDraw.Draw(contact)
 for i,im in enumerate(rows):contact.paste(im,(i*256,50),im);draw.text((i*256+8,8),str(i)+' registered',fill='white');un=Image.open(HERE/'registered-ungraded'/f'{i:03d}.png');contact.paste(un,(i*256,370),un);draw.text((i*256+8,328),str(i)+' before grade',fill='white')
 contact.save(HERE/'contact.png');print('15 bare references at fixed scale',scale,'gold gain',gain.tolist())
if __name__=='__main__':main()
