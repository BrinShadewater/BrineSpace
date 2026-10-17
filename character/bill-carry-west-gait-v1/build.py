from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent
held={g:R/f'character/bill-cargo-west-master-head-v1/frames/{g}/pickup-west/011.png' for g in ['bare','helmet']}
masters={g:np.array(Image.open(f).convert('RGBA')) for g,f in held.items()};Y,X=np.indices((256,256))
hipmask=(masters['bare'][:,:,3]>180)&(Y>=155)&(Y<164);hipx=float((np.where(hipmask)[1].min()+np.where(hipmask)[1].max())/2)
# Anatomical upper-thigh cuts exclude generated waist/belt. One ruler per raw
# family, never an independent pose bounding-height adjustment.
families=[('first-legs-v4.png',2,330),('opposite-legs-v3.png',4,380)];parts=[];cal=[]
for source,count,cuty in families:
 a=np.array(Image.open(P/'sources'/source).convert('RGBA'));labs,_=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0;ids=sorted(np.argsort(sizes)[-count:],key=lambda k:np.where(labs==k)[1].mean())
 records=[]
 for cell,k in enumerate(ids):
  t=a.copy();mask=binary_dilation(labs==k,iterations=1)&(a[:,:,3]>80);t[~mask]=0;t[:cuty]=0
  ys,xs=np.where(t[:,:,3]>180);box=[int(xs.min()),cuty,int(xs.max()+1),int(ys.max()+1)];assert box[0]>0 and box[2]<a.shape[1] and box[3]<a.shape[0]
  records.append((t,box,cell))
 scale=70/(records[0][1][3]-cuty);cal.append({'source':'sources/'+source,'cutY':cuty,'sourceHeight':records[0][1][3]-cuty,'canonicalThighToSole':70,'scale':scale})
 for t,box,cell in records:
  ys,xs=np.where((t[:,:,3]>180)&(np.indices(t.shape[:2])[0]<cuty+8));axis=float((xs.min()+xs.max())/2)
  im=Image.fromarray(t).crop(tuple(box));im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);strong=np.array(im)[:,:,3]>180;bottom=int(np.where(strong)[0].max());pos=[round(hipx-(axis-box[0])*scale),224-bottom]
  out=Image.new('RGBA',(256,256));out.alpha_composite(im,tuple(pos));parts.append((np.array(out),{'source':'sources/'+source,'cell':cell,'sourceBox':box,'scale':scale,'hipAxis':axis,'position':pos}))
def neutral(a):return (a[:,:,3]>180)&(Y>=164)&(Y<220)&(a[:,:,:3].max(2)-a[:,:,:3].min(2)<25)&(a[:,:,:3].mean(2)>15)
pool=np.concatenate([a[:,:,:3][neutral(a)] for a,_ in parts]);target=masters['bare'];gain=np.median(target[:,:,:3][neutral(target)],axis=0)/np.median(pool,axis=0);protected=Y<164
files={g:[] for g in masters}
for gear,master in masters.items():
 for i,(part,record) in enumerate(parts):
  a=part.copy();mask=neutral(a);rgb=a[mask,:3].astype(float)*gain
  # Whole-leg medians already agree. Compress only the bright neutral hardware
  # with one fixed curve across both source families and every paired pose.
  lum=rgb.mean(1);matte=lum-np.maximum(lum-100,0)*.18
  a[mask,:3]=np.clip(rgb*(matte/np.maximum(lum,1))[:,None],0,255).astype('uint8');a[protected]=master[protected]
  f=P/f'frames/{gear}/carry-west/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(f);files[gear].append('res://'+f.relative_to(R).as_posix())
 m={'name':'Bill West alternating carry gait candidate','status':'staged_visual_review','frameWidth':256,'frameHeight':256,'standingHeight':148,'pivot':[128,224],'precomposed':True,'strideDistanceCells':{'carry':.12},'states':[{'id':'carry-west','frameFiles':files[gear],'frameDurationsMs':[140]*6,'loop':True,'facings':['west']*6,'waterPoses':[False]*6}]}
 (P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
reg={'calibration':cal,'hipX':hipx,'protectedUpper':'Exact accepted West held master RGBA above y164 in all6phases; no reflection, translation or resize','neutralGainPooled':gain.tolist(),'sharedMatteCurve':{'neutralThreshold':100,'highlightSlope':.82,'scope':'neutral opaque lower legs only, all six poses and both gears'},'frames':[v for _,v in parts],'masterSha256':{str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in held.values()}}
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1536,600),'#22343e');draw=ImageDraw.Draw(board)
for row,gear in enumerate(files):
 for i,f in enumerate(files[gear]):
  a=Image.open(R/f.removeprefix('res://')).convert('RGBA');board.paste(a,(i*256,row*300),a);draw.text((i*256+8,row*300+265),gear+' phase'+str(i),fill='white')
board.save(P/'candidate-review.png');print('Staged6paired full support-cycle phases; family rulers',cal,'gain',gain.tolist())
