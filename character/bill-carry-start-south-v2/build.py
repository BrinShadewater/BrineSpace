from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent
Y,X=np.indices((256,256));protected=Y<168
masters={g:np.array(Image.open(R/f'character/bill-cargo-south-master-head-v1/frames/{g}/pickup-south/011.png').convert('RGBA')) for g in ['bare','helmet']}
parts=[];cal=[]
for src,samples in [('first-step-v1.png',[0,1,2])]:
 count=5
 a=np.array(Image.open(P/'sources'/src).convert('RGBA'));labs,_=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0;ids=sorted(np.argsort(sizes)[-count:],key=lambda k:np.where(labs==k)[1].mean())
 y,x=np.where(labs==ids[-1]);height=int(y.max()-y.min()+1);scale=144/height;ground=int(y.max());cal.append({'source':src,'standingSample':count-1,'standingHeight':height,'scale':scale,'sourceGround':ground})
 for i in samples:
  k=ids[i]
  t=a.copy();t[~(binary_dilation(labs==k,iterations=1)&(a[:,:,3]>80))]=0
  yy,xx=np.indices(t.shape[:2]);band=(t[:,:,3]>180)&(yy>=ground-55/scale)&(yy<ground-49/scale);axis=float((np.where(band)[1].min()+np.where(band)[1].max())/2)
  ys,xs=np.where(t[:,:,3]>180);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
  im=Image.fromarray(t).crop(box);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);position=[round(128-(axis-box[0])*scale),round(223-(ground-box[1])*scale)]
  out=Image.new('RGBA',(256,256));out.alpha_composite(im,position);part=np.array(out);part[protected]=0;parts.append((part,{'source':src,'sample':i,'box':box,'scale':scale,'hipAxis':axis,'position':position}))


def neutral(a):return (a[:,:,3]>180)&(Y>=168)&(Y<220)&(a[:,:,:3].max(2)-a[:,:,:3].min(2)<25)&(a[:,:,:3].mean(2)>15)
pool=np.concatenate([a[:,:,:3][neutral(a)] for a,_ in parts]);gain=np.median(masters['bare'][:,:,:3][neutral(masters['bare'])],axis=0)/np.median(pool,axis=0)
files={}
for gear,master in masters.items():
 files[gear]=[]
 for i in range(6):
  if i in [0,4,5]:
   src=R/(f'character/bill-cargo-south-master-head-v1/frames/{gear}/pickup-south/011.png' if i==0 else f'character/bill-carry-south-gait-v3/frames/{gear}/carry-south/000.png')
   f=P/f'frames/{gear}/carry-start-south/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);import shutil;shutil.copy2(src,f);files[gear].append('res://'+f.relative_to(R).as_posix());continue
  part,rec=parts[i-1]
  a=part.copy();mask=neutral(a);rgb=a[mask,:3].astype(float)*gain;lum=rgb.mean(1);matte=lum-np.maximum(lum-100,0)*.18;a[mask,:3]=np.clip(rgb*(matte/np.maximum(lum,1))[:,None],0,255).astype('uint8');a[protected]=master[protected]
  f=P/f'frames/{gear}/carry-start-south/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(f);files[gear].append('res://'+f.relative_to(R).as_posix())
 m={'name':'Bill South articulated first-step candidate','status':'staged_visual_review','frameWidth':256,'frameHeight':256,'standingHeight':148,'pivot':[128,224],'textureFilter':'linear','precomposed':True,'strideDistanceCells':{'carry':.12},'states':[{'id':'carry-start-south','frameFiles':files[gear],'frameDurationsMs':[40,50,55,65,65,45],'loop':False,'facings':['south']*6,'waterPoses':[False]*6}]};(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
reg={'actualMasterRuler':144,'reusedAuthoringSource':'character/bill-carry-start-south-v1/sources/first-step-v1.png','calibration':cal,'protectedUpper':'Exact canonical RGBA above y168; generated pixels cleared first','neutralGainPooled':gain.tolist(),'sharedMatteCurve':{'threshold':100,'slope':.82},'frames':[v for _,v in parts],'masterSha256':{f'character/bill-cargo-south-master-head-v1/frames/{g}/pickup-south/011.png':hashlib.sha256((R/f'character/bill-cargo-south-master-head-v1/frames/{g}/pickup-south/011.png').read_bytes()).hexdigest() for g in masters}}
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
b=Image.new('RGB',(1792,600),'#22343e');d=ImageDraw.Draw(b)
for row,g in enumerate(files):
 for i,f in enumerate([f'res://character/bill-cargo-south-master-head-v1/frames/{g}/pickup-south/011.png']+files[g]):
  a=Image.open(R/f.removeprefix('res://')).convert('RGBA');b.paste(a,(i*256,row*300),a);d.text((i*256+8,row*300+265),g+(' master' if i==0 else ' phase'+str(i-1)),fill='white')
b.save(P/'candidate-review.png');print('Six paired South poses; one full-standing ruler per source family; gain',gain.tolist())
