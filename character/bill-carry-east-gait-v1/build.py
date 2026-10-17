"""Fit authored leg components beneath immutable canonical upper-body art."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent
held={g:R/f'character/bill-cargo-east-master-head-v1/frames/{g}/pickup-east/010.png' for g in ['bare','helmet']}
masters={g:np.array(Image.open(file).convert('RGBA')) for g,file in held.items()}
Y,X=np.indices((256,256));canonical=(masters['bare'][:,:,3]>180)&(Y>=155)&(Y<164)&(X<135);hip_x=float((np.where(canonical)[1].min()+np.where(canonical)[1].max())/2)
parts=[]
components={}
for source in ['gait-legs-v1.png','gait-legs-v2.png']:
 a=np.array(Image.open(P/'sources'/source).convert('RGBA'));labs,_=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=np.argsort(counts)[-8:]
 ids=sorted(ids,key=lambda k:(np.where(labs==k)[0].mean()>512,np.where(labs==k)[1].mean()))
 components[source]=(a,labs,ids)
for i in range(8):
 source='gait-legs-v1.png' if i<4 else 'gait-legs-v2.png';a,labs,ids=components[source];k=ids[i];t=a.copy();ys,xs=np.where(labs==k);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];assert min(box[:2])>0 and box[2]<1536 and box[3]<1024,'Complete source assembly'
 mask=binary_dilation(labs==k,iterations=1)&(t[:,:,3]>80);t[~mask]=0;parts.append((t,box,source))
first_height=parts[0][1][3]-parts[0][1][1];scale=70/first_height;records=[];legs=[]
for i,(a,box,source) in enumerate(parts):
 ys,xs=np.where((a[:,:,3]>180)&(np.indices(a.shape[:2])[0]<box[1]+8));axis=float((xs.min()+xs.max())/2)
 cut=Image.fromarray(a).crop(tuple(box));cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS);strong=np.array(cut)[:,:,3]>180;bottom=int(np.where(strong)[0].max());pos=[round(hip_x-(axis-box[0])*scale),224-bottom]
 out=Image.new('RGBA',(256,256));out.alpha_composite(cut,tuple(pos));legs.append(np.array(out));records.append({'source':'sources/'+source,'cell':i,'sourceBox':box,'sourceHeight':box[3]-box[1],'scale':scale,'position':pos,'hipAxis':axis})
def neutral(a):return (a[:,:,3]>180)&(Y>=164)&(Y<220)&(a[:,:,:3].max(2)-a[:,:,:3].min(2)<25)&(a[:,:,:3].mean(2)>15)
pool=np.concatenate([a[:,:,:3][neutral(a)] for a in legs]);target=masters['bare'];gain=np.median(target[:,:,:3][neutral(target)],axis=0)/np.median(pool,axis=0)
files={g:[] for g in masters};protected=(Y<164)|((X>=135)&(Y<170))
for g,master in masters.items():
 for i,leg in enumerate(legs):
  a=leg.copy();mask=neutral(a);a[mask,:3]=np.clip(a[mask,:3]*gain,0,255).astype('uint8');a[protected]=master[protected]
  path=P/f'frames/{g}/carry-east/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True);Image.fromarray(a).save(path);files[g].append('res://'+path.relative_to(R).as_posix())
 m={'name':'Bill steady East carrying gait preview','status':'staged_visual_review','frameWidth':256,'frameHeight':256,'standingHeight':148,'pivot':[128,224],'precomposed':True,'strideDistanceCells':{'carry':.12},'states':[{'id':'carry-east','frameFiles':files[g],'frameDurationsMs':[105]*8,'loop':True,'facings':['east']*8,'waterPoses':[False]*8}]}
 (P/f'{g}-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
reg={'calibration':{'source':'sources/gait-legs-v1.png','cell':0,'sourceHeight':first_height,'canonicalUpperThighToSoleHeight':70,'scale':scale},'fixedNeutralLegGain':gain.tolist(),'protectedUpperBody':'Exact held master RGBA, no translation/scaling in any gait slot; source leg assemblies only below fitted seam','frames':records,'masterSha256':{file.relative_to(R).as_posix():hashlib.sha256(file.read_bytes()).hexdigest() for file in held.values()}}
(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGBA',(2048,600),(34,52,62,255));draw=ImageDraw.Draw(board)
for row,g in enumerate(files):
 for i,file in enumerate(files[g]):board.alpha_composite(Image.open(R/file.removeprefix('res://')).convert('RGBA'),(i*256,row*300));draw.text((i*256+8,row*300+265),g+' gait'+str(i),fill='white')
board.convert('RGB').save(P/'candidate-review.png');print('Staged8-slot paired East gait; source ruler',scale,'neutral gain',gain.tolist())
