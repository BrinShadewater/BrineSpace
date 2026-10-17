"""Independent lying sources: fixed anatomical scale and reviewed head ownership."""
from pathlib import Path
import json,copy,os,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
retained_root=ROOT/'character/chief-engineer-branforth-v2/packs/bare-256x256-p128.0-224.0'
retained=json.loads((retained_root/'manifest.json').read_text())
def extract(path):
 raw=Image.open(path).convert('RGBA');a=np.array(raw);labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=sorted(np.argsort(counts)[-12:],key=lambda k:np.where(labs==k)[0].mean());out=[]
 for row in range(2):
  for k in sorted(ids[row*6:row*6+6],key=lambda k:np.where(labs==k)[1].mean()):
   y,x=np.where(labs==k);box=[int(x.min())-3,int(y.min())-3,int(x.max())+4,int(y.max())+4];x0,y0,x1,y1=box;assert min(x0,y0)>=0 and x1<=a.shape[1] and y1<=a.shape[0],'source clipping';cell=a[y0:y1,x0:x1].copy();cell[~binary_dilation(labs[y0:y1,x0:x1]==k,iterations=2)]=0;out.append((Image.fromarray(cell),box))
 return out
def foot(im):
 a=np.array(im);y,x=np.where(a[:,:,3]>180);bottom=int(y.max());yy=np.indices(a.shape[:2])[0];y,x=np.where((a[:,:,3]>180)&(yy>=bottom-4));return np.array([x.mean(),bottom])
def head(im,d,i):
 a=np.array(im);mask=a[:,:,3]>180;y,x=np.where(mask);xx=np.indices(mask.shape)[1]
 if d in ['east','west'] and i>=3:mask&=(xx<x.min()+37 if d=='east' else xx>x.max()-37)
 y,x=np.where(mask);top=int(y.min());yy=np.indices(mask.shape)[0];y,x=np.where(mask&(yy<top+5));cx=float(x.mean());box=[round(cx-20),top-2,round(cx+20),top+33];return np.array([cx,top+14]),box
def gold(a,exclude=None):
 r,g,b=a[:,:,:3].astype(float).transpose(2,0,1);mask=(a[:,:,3]>0)&(r-b>35)&(g-b>20)
 if exclude:mask[exclude[1]:exclude[3],exclude[0]:exclude[2]]=False
 return mask
def build(d):
 p=ROOT/'character'/('james-lying-'+d+'-v1');cells=extract(p/'source.png');mf=ROOT/'character/crew-runtime-matte-v1/branforth';m=json.loads((mf/'manifest.json').read_text());st=next(s for s in m['states'] if s['id']=='idle-'+d);master=Image.open(mf/st['frameFiles'][0]).convert('RGBA');ma=np.array(master);y,x=np.where(ma[:,:,3]>180);height=int(y.max()-y.min()+1);a=np.array(cells[0][0]);y,x=np.where(a[:,:,3]>180);scale=height/(y.max()-y.min()+1);target=foot(master)+[36,52];rows=[];tracking=[]
 for i,(cell,box) in enumerate(cells):
  at=np.rint(target-foot(cell)*scale).astype(int);im=Image.new('RGBA',(256,256));im.alpha_composite(cell.resize((round(cell.width*scale),round(cell.height*scale)),Image.Resampling.LANCZOS),tuple(at));point,hb=head(im,d,i)
  if i>=6:
   delta=np.rint(np.array(tracking[5]['headAnchor'])-point).astype(int);translated=Image.new('RGBA',(256,256));translated.alpha_composite(im,tuple(delta));im=translated;point,hb=head(im,d,i);at+=delta
  rows.append(im);tracking.append(dict(sourceBox=box,translation=at.tolist(),headAnchor=point.tolist(),protectedHeadBox=hb))
  dest=p/'registered-ungraded'/f'{i:03d}.png';dest.parent.mkdir(exist_ok=True);im.save(dest)
 full=Image.new('RGBA',(256,256));full.alpha_composite(master,(36,52));fa=np.array(full);_,master_box=head(full,d,0);a=np.array(rows[0]);gain=np.median(fa[:,:,:3][gold(fa,master_box)],axis=0)/np.median(a[:,:,:3][gold(a,tracking[0]['protectedHeadBox'])],axis=0)
 for i,im in enumerate(rows):
  a=np.array(im);rgb=a[:,:,:3].astype(float);x0,y0,x1,y1=tracking[i]['protectedHeadBox'];protect=np.zeros(a.shape[:2],bool);protect[y0:y1,x0:x1]=True;gm=gold(a,tracking[i]['protectedHeadBox']);body=(a[:,:,3]>0)&~protect&~gm;lum=rgb.mean(2);mapped=np.interp(lum,[0,50,70,90,120,160,200,255],[0,50,68,80,99,126,149,170]);factor=np.divide(mapped,lum,out=np.ones_like(lum),where=lum>0);rgb[body]*=factor[body,None];rgb[gm]*=gain;a[:,:,:3]=np.rint(rgb).clip(0,255).astype('uint8');rows[i]=Image.fromarray(a)
 rows[0]=full;rows[6]=rows[5].copy();rows[11]=rows[5].copy();tracking[6]=copy.deepcopy(tracking[5]);tracking[11]=copy.deepcopy(tracking[5]);indices={'lie-down':list(range(6)),'sleep':[5,7,8,9,10,5],'get-up':list(reversed(range(6)))}
 if d=='north':
  indices['sleep']=[5]*6 # Source breathing stretches calves; retain authored quiet neutral pending a coherent breathing source.
  for i in range(7,11):rows[i]=rows[5].copy();tracking[i]=copy.deepcopy(tracking[5])
 pack=dict(name='James '+d+' lying candidate',frameWidth=256,frameHeight=256,pivot=[128,224],standingHeight=148,precomposed=True,textureFilter='linear',status='staged_lying_master_revision',states=[]);hashes={}
 for action,poses in indices.items():
  old=next(s for s in retained['states'] if s['id']==action+'-'+d);state=copy.deepcopy(old);files=[]
  for j,i in enumerate(poses):
   f=p/'frames'/action/f'{j:03d}.png';f.parent.mkdir(parents=True,exist_ok=True);rows[i].save(f);rel=f.relative_to(p).as_posix();files.append(rel);hashes[rel]=hashlib.sha256(f.read_bytes()).hexdigest()
  state.update(frameFiles=files,frameCount=6,provenance=dict(source='source.png',prompt='prompt.txt',fixedScale=float(scale),sourcePoses=poses,derivation='Independent cardinal source, fixed anatomical scale, exact selected standing arrival, shared sleep neutral and exact reverse'))
  if d=='north' and action in ['lie-down','get-up']:
   depths=[0,19,58,58,77,96];state['depthOffsets']=depths if action=='lie-down' else list(reversed(depths));state['provenance']['depthCorrection']='North midpoint source38 ->58 to retain visibility above retained bedside cabinet; reversed on rise'
  if action=='sleep':state['restHeadOffset']=((np.array(tracking[5]['headAnchor'])-[128,224])*65.28/148).tolist()
  pack['states'].append(state)
 (p/'bare-manifest.json').write_text(json.dumps(pack,indent=2)+'\n');(p/'frame-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n');(p/'registration.json').write_text(json.dumps(dict(fixedScale=float(scale),masterHeight=height,goldGain=gain.tolist(),tracking=tracking,sourceSha256=hashlib.sha256((p/'source.png').read_bytes()).hexdigest()),indent=2)+'\n')
 board=Image.new('RGB',(1792,640),'#303b40');maskboard=board.copy();draw=ImageDraw.Draw(board);md=ImageDraw.Draw(maskboard)
 for i,im in enumerate(rows):
  at=(i%6*256,50+i//6*320);board.paste(im,at,im);maskboard.paste(im,at,im);draw.text((at[0]+8,at[1]-42),d+' '+str(i),fill='white');x0,y0,x1,y1=tracking[i]['protectedHeadBox'];md.rectangle((x0+at[0],y0+at[1],x1+at[0],y1+at[1]),outline='#7dd5db')
 board.paste(full,(1536,50),full);draw.text((1544,8),'selected master',fill='white');board.save(p/'contact.png');maskboard.save(p/'head-ownership.png');print(d,'18 refs,scale',round(scale,5),'headOffset',next(s for s in pack['states'] if s['id'].startswith('sleep'))['restHeadOffset']);return pack,p
if __name__=='__main__':
 import sys
 combined=None
 for d in (sys.argv[1:] or ['east','south','west','north']):
  m,p=build(d)
  if combined is None:combined={k:copy.deepcopy(v) for k,v in m.items() if k!='states'};combined.update(name='James directional lying family staged',states=[])
  for st in m['states']:
   st=copy.deepcopy(st);st['frameFiles']=[Path(os.path.relpath(p/f,HERE)).as_posix() for f in st['frameFiles']];combined['states'].append(st)
 (HERE/'bare-manifest.json').write_text(json.dumps(combined,indent=2)+'\n')
