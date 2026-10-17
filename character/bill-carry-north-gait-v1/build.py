from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent
Y,X=np.indices((256,256));protected=Y<164
masters={g:np.array(Image.open(R/f'character/bill-cargo-north-master-head-v1/frames/{g}/pickup-north/011.png').convert('RGBA')) for g in ['bare','helmet']}
parts=[];cal=[]
for src,count in [('first-half-v2.png',4),('opposite-half-v3.png',4)]:
 a=np.array(Image.open(P/'sources'/src).convert('RGBA'));labs,_=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0;ids=sorted(np.argsort(sizes)[-count:],key=lambda k:np.where(labs==k)[1].mean())
 y,x=np.where(labs==ids[-1]);height=int(y.max()-y.min()+1);scale=148/height;ground=int(y.max());cal.append({'source':src,'standingSample':count-1,'standingHeight':height,'scale':scale,'sourceGround':ground})
 for i,k in enumerate(ids[:3]):
  t=a.copy();t[~(binary_dilation(labs==k,iterations=1)&(a[:,:,3]>80))]=0
  yy,xx=np.indices(t.shape[:2]);band=(t[:,:,3]>180)&(yy>=ground-55/scale)&(yy<ground-49/scale);axis=float((np.where(band)[1].min()+np.where(band)[1].max())/2)
  ys,xs=np.where(t[:,:,3]>180);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
  im=Image.fromarray(t).crop(box);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);position=[round(128-(axis-box[0])*scale),round(223-(ground-box[1])*scale)]
  out=Image.new('RGBA',(256,256));out.alpha_composite(im,position);part=np.array(out);part[protected]=0;parts.append((part,{'source':src,'sample':i,'box':box,'scale':scale,'hipAxis':axis,'position':position}))
def neutral(a):return (a[:,:,3]>180)&(Y>=164)&(Y<220)&(a[:,:,:3].max(2)-a[:,:,:3].min(2)<25)&(a[:,:,:3].mean(2)>15)
pool=np.concatenate([a[:,:,:3][neutral(a)] for a,_ in parts]);gain=np.median(masters['bare'][:,:,:3][neutral(masters['bare'])],axis=0)/np.median(pool,axis=0)
files={}
for gear,master in masters.items():
 files[gear]=[]
 for i,(part,rec) in enumerate(parts):
  a=part.copy();mask=neutral(a);rgb=a[mask,:3].astype(float)*gain;lum=rgb.mean(1);matte=lum-np.maximum(lum-100,0)*.18;a[mask,:3]=np.clip(rgb*(matte/np.maximum(lum,1))[:,None],0,255).astype('uint8');a[protected]=master[protected]
  f=P/f'frames/{gear}/carry-north/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(f);files[gear].append('res://'+f.relative_to(R).as_posix())
 m={'name':'Bill North master upper alternating carry gait candidate','status':'staged_visual_review','frameWidth':256,'frameHeight':256,'standingHeight':148,'pivot':[128,224],'textureFilter':'linear','precomposed':True,'strideDistanceCells':{'carry':.12},'states':[{'id':'carry-north','frameFiles':files[gear],'frameDurationsMs':[140]*6,'loop':True,'facings':['north']*6,'waterPoses':[False]*6}]};(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
reg={'calibration':cal,'protectedUpper':'Exact canonical RGBA above y164; generated pixels cleared first','neutralGainPooled':gain.tolist(),'sharedMatteCurve':{'threshold':100,'slope':.82},'frames':[v for _,v in parts],'masterSha256':{f'character/bill-cargo-north-master-head-v1/frames/{g}/pickup-north/011.png':hashlib.sha256((R/f'character/bill-cargo-north-master-head-v1/frames/{g}/pickup-north/011.png').read_bytes()).hexdigest() for g in masters}}
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
b=Image.new('RGB',(1792,600),'#22343e');d=ImageDraw.Draw(b)
for row,g in enumerate(files):
 for i,f in enumerate([f'res://character/bill-cargo-north-master-head-v1/frames/{g}/pickup-north/011.png']+files[g]):
  a=Image.open(R/f.removeprefix('res://')).convert('RGBA');b.paste(a,(i*256,row*300),a);d.text((i*256+8,row*300+265),g+(' master' if i==0 else ' phase'+str(i-1)),fill='white')
b.save(P/'candidate-review.png');print('Six paired North poses; one full-standing ruler per source family; gain',gain.tolist())
