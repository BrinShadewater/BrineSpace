from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent
source=P/'sources/first-step-v1.png';raw=np.array(Image.open(source).convert('RGBA'))
labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
ids=sorted(np.argsort(counts)[-3:],key=lambda k:np.where(labs==k)[1].mean());parts=[]
for k in ids:
 y,x=np.where(labs==k);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
 assert box[0]>0 and box[1]>0 and box[2]<raw.shape[1] and box[3]<raw.shape[0]
 a=raw.copy();a[~(binary_dilation(labs==k,iterations=1)&(raw[:,:,3]>80))]=0
 parts.append((a,box))
# One fixed common-thigh-to-sole ruler; no independent pose-height fitting.
scale=61/(parts[0][1][3]-parts[0][1][1]);ground=parts[0][1][3]-1
Y,X=np.indices((256,256));masters={g:np.array(Image.open(R/f'character/bill-cargo-west-master-head-v1/frames/{g}/pickup-west/011.png').convert('RGBA')) for g in ['bare','helmet']}
mask=(masters['bare'][:,:,3]>180)&(Y>=155)&(Y<164);hip=float((np.where(mask)[1].min()+np.where(mask)[1].max())/2)
native=[];records=[]
for a,box in parts:
 yy,xx=np.where((a[:,:,3]>180)&(np.indices(a.shape[:2])[0]<box[1]+8));axis=float((xx.min()+xx.max())/2)
 im=Image.fromarray(a).crop(tuple(box));im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
 pos=[round(hip-(axis-box[0])*scale),round(224-(ground-box[1])*scale)]
 out=Image.new('RGBA',(256,256));out.alpha_composite(im,tuple(pos));native.append(np.array(out));records.append({'box':box,'scale':scale,'position':pos,'axis':axis})
def neutral(a):return (a[:,:,3]>180)&(Y>=164)&(Y<220)&(np.ptp(a[:,:,:3],axis=2)<25)&(a[:,:,:3].mean(2)>15)
pool=np.concatenate([a[:,:,:3][neutral(a)] for a in native]);target=masters['bare'];gain=np.median(target[:,:,:3][neutral(target)],axis=0)/np.median(pool,axis=0)
inputs={};files={g:[] for g in masters};durations=[40,50,55,65,65,45]
for gear,master in masters.items():
 for i in range(6):
  f=P/f'frames/{gear}/carry-start-west/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True)
  if i==0 or i>=4:
   src=R/(f'character/bill-cargo-west-master-head-v1/frames/{gear}/pickup-west/011.png' if i==0 else f'character/bill-carry-west-gait-v1/frames/{gear}/carry-west/000.png');shutil.copy2(src,f);inputs[src.relative_to(R).as_posix()]=hashlib.sha256(src.read_bytes()).hexdigest()
  else:
   a=native[i-1].copy();m=neutral(a);rgb=a[m,:3].astype(float)*gain;lum=rgb.mean(1);matte=lum-np.maximum(lum-100,0)*.18;a[m,:3]=np.clip(rgb*(matte/np.maximum(lum,1))[:,None],0,255).astype('uint8');a[Y<164]=master[Y<164];Image.fromarray(a).save(f)
  files[gear].append('res://'+f.relative_to(R).as_posix())
 m={'name':'Bill West held-to-first-step candidate','status':'staged_visual_review','frameWidth':256,'frameHeight':256,'standingHeight':148,'pivot':[128,224],'precomposed':True,'states':[{'id':'carry-start-west','frameFiles':files[gear],'frameDurationsMs':durations,'loop':False,'facings':['west']*6,'waterPoses':[False]*6}]};(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
inputs[source.relative_to(R).as_posix()]=hashlib.sha256(source.read_bytes()).hexdigest()
reg={'sourceSha256':inputs,'scale':scale,'sourceGround':ground,'hipX':hip,'frames':records,'neutralGainPooled':gain.tolist(),'sharedHighlightCurve':[100,.82],'resumeGaitPhaseSeconds':.139,'scope':'Three authored lower-body interiors; exact held0 and gait0 final two byte copies, exact upper RGBA in all rows. One source ruler, pooled grade, no per-pose rescale/exposure.'};(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
board=Image.new('RGBA',(1536,600),(34,52,62,255));d=ImageDraw.Draw(board)
for row,gear in enumerate(files):
 for i,f in enumerate(files[gear]):board.alpha_composite(Image.open(R/f.removeprefix('res://')),(i*256,row*300));d.text((i*256+8,row*300+265),gear+' '+str(i),fill='white')
board.convert('RGB').save(P/'candidate-review.png');print('West first-step paired bridge; source ruler',scale,'pooled grade',gain.tolist())
