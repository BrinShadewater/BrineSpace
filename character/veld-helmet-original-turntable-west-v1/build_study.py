from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'v3-study';D.mkdir(exist_ok=True);T=R/'character/veld-cargo-turns-master-family-v1';a=np.array(Image.open(P/'raw-v3.png').convert('RGBA'));labs,n=label(a[:,:,3]>24);counts=np.bincount(labs.ravel());ids=[int(i) for i in np.where(counts>4000)[0] if i];assert len(ids)==12
boxes=[]
for i in ids:
 y,x=np.where(labs==i);boxes.append((int(y.min()),int(x.min()),int(x.max()+1),int(y.max()+1),i))
boxes=sorted(boxes,key=lambda b:(b[0]>500,b[1]));front=boxes[-1];scale=39/(front[3]-front[0]);shells=[];records=[]
for slot,(y,x,right,bottom,i) in enumerate(boxes):
 cell=a[y:bottom,x:right].copy();mask=binary_dilation(labs[y:bottom,x:right]==i,iterations=2);cell[~mask]=0;im=Image.fromarray(cell).resize((round(cell.shape[1]*scale),round(cell.shape[0]*scale)),Image.Resampling.LANCZOS);shells.append(im);(D/'shells').mkdir(exist_ok=True);im.save(D/f'shells/{slot:03}.png')
 records.append({'slot':slot,'sourceBox':[x,y,right,bottom],'nativeSize':list(im.size)})
checks=0;bindings={};fits=[]
for folder,indices in [('north-west-candidate-v4',list(range(6))),('candidate-v7',[11,10,9,8,7,5])]:
 board=Image.new('RGB',(1536,560),'#202a30');draw=ImageDraw.Draw(board)
 for slot,sourceindex in enumerate(indices):
  barepath=T/folder/f'frames/bare/{slot:03}.png';oldpath=T/folder/f'frames/helmet/{slot:03}.png';bare=Image.open(barepath).convert('RGBA');old=Image.open(oldpath).convert('RGBA');b=np.array(bare);h=np.array(old);yy,xx=np.where(np.any(b!=h,axis=2));box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];bottom=box[3]
  _,gx=np.where(h[bottom-4:bottom,box[0]:box[2],3]>160);anchor=(gx.min()+gx.max())/2+box[0];shell=shells[sourceindex];s=np.array(shell);_,sx=np.where(s[-4:,:,3]>160);center=(sx.min()+sx.max())/2;position=(round(anchor-center),bottom-shell.height)
  result=bare.copy();result.paste((0,0,0,0),tuple(box));result.alpha_composite(shell,position)
  if slot==0:
   eastfamily='north-east-candidate-v5' if folder=='north-west-candidate-v4' else 'east-south-candidate-v3';eastslot='000' if folder=='north-west-candidate-v4' else '005';alias=R/f'character/veld-helmet-original-turntable-v1/v3-study/pilot/{eastfamily}/{eastslot}.png';original=T/eastfamily/f'frames/bare/{eastslot}.png';assert original.read_bytes()==barepath.read_bytes();result=Image.open(alias).convert('RGBA');checks+=1
  out=D/f'pilot/{folder}/{slot:03}.png';out.parent.mkdir(parents=True,exist_ok=True);result.save(out)
  ra=np.array(result);protected=np.ones((256,256),bool);protected[min(box[1],position[1]):max(box[3],position[1]+shell.height),min(box[0],position[0]):max(box[2],position[0]+shell.width)]=False;assert np.array_equal(ra[protected],b[protected]);checks+=1
  for f in [barepath,oldpath,out]:bindings[f.relative_to(R).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
  x=slot*256;board.paste(old,(x,24),old);board.paste(result,(x,290),result);draw.text((x+3,4),'old '+str(slot),fill='white');draw.text((x+3,270),'shared source '+str(sourceindex),fill='white');fits.append({'family':folder,'slot':slot,'sourceSlot':sourceindex,'clearBox':box,'wholeShellPosition':list(position)})
 board.save(D/(folder+'-pilot.png'))
(D/'study.json').write_text(json.dumps({'checks':checks,'failures':0,'scale':scale,'oneFrontMasterHeight':39,'rows':records,'fits':fits,'bindings':bindings,'visualReview':'pending','scope':'Source-only rigid shared equipment fitting on unchanged whole bodies. No colour transforms or native/normal selection acceptance.'},indent=2)+'\n')
print(str(checks)+' protected-body fitting checks;12 shells/twelve pilot poses')
