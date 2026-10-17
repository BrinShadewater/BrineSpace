"""Extract bounded authored legs at one source ruler; retain exact selected upper-body pixels."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent;b=json.loads((P/'bindings.json').read_text(encoding='utf-8'))
for file,digest in b['sourceSha256'].items():assert hashlib.sha256((R/file).read_bytes()).hexdigest()==digest,'Frozen canonical source changed: '+file
a=np.array(Image.open(P/'sources/first-step-v2.png').convert('RGBA'));labs,_=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
ids=np.argsort(counts)[-4:];ids=sorted(ids,key=lambda k:np.where(labs==k)[1].mean());components=[]
for k in ids:
 y,x=np.where(labs==k);box=[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)];assert box[0]>0 and box[1]>0 and box[2]<a.shape[1] and box[3]<a.shape[0]
 mask=binary_dilation(labs==k,iterations=1)&(a[:,:,3]>80);part=a.copy();part[~mask]=0;components.append((part,box))
height=components[0][1][3]-components[0][1][1];scale=148/height;ground=components[0][1][3]-1
# Only third lower-body pixels adopt the targeted pose repair. Keep its v2 fit
# coordinates and the v2 first-body ruler; regenerated protected anatomy is excluded.
v3=np.array(Image.open(P/'sources/first-step-v3.png').convert('RGBA'));v3labs,_=label(v3[:,:,3]>180);v3counts=np.bincount(v3labs.ravel());v3counts[0]=0;v3ids=sorted(np.argsort(v3counts)[-4:],key=lambda k:np.where(v3labs==k)[1].mean())
third=v3.copy();third[~(binary_dilation(v3labs==v3ids[2],iterations=1)&(v3[:,:,3]>80))]=0
components[2]=(third,components[2][1])
held={g:Image.open(R/(b['held'] if g=='bare' else 'character/bill-cargo-east-master-head-v1/frames/helmet/pickup-east/010.png')).convert('RGBA') for g in ['bare','helmet']}
def crown(im):
 t=np.array(im);ys,xs=np.where(t[:,:,3]>180);top=ys.min();y,x=np.where((t[:,:,3]>180)&(np.indices(t.shape[:2])[0]<top+8));return float((x.min()+x.max())/2),int(top)
axis,top=crown(held['bare']);native=[];records=[]
for n,(part,box) in enumerate(components):
 y,x=np.where(part[:,:,3]>180);sy,sx=np.where((part[:,:,3]>180)&(np.indices(part.shape[:2])[0]<box[1]+8));source_axis=float((sx.min()+sx.max())/2)
 cut=Image.fromarray(part).crop(tuple(box));cut=cut.resize((round(cut.width*scale),round(cut.height*scale)),Image.Resampling.LANCZOS)
 pos=[round(axis-(source_axis-box[0])*scale),round(224-(ground-box[1])*scale)]
 canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(cut,tuple(pos));native.append(canvas)
 dy=round((box[1]-components[0][1][1])*scale);records.append({'source':'sources/first-step-v3.png' if n==2 else 'sources/first-step-v2.png','sourceBox':box,'scale':scale,'position':pos,'upperTranslation':[0,dy],'seam':164+dy})
# One shared pooled neutral-leg gain from this generated family, not per-frame exposure.
def neutral(t):
 y=np.indices(t.shape[:2])[0];return (t[:,:,3]>180)&(y>=164)&(y<220)&(t[:,:,:3].max(2)-t[:,:,:3].min(2)<25)&(t[:,:,:3].mean(2)>15)
pool=np.concatenate([np.array(im)[:,:,:3][neutral(np.array(im))] for im in native]);target=np.array(held['bare']);gain=np.median(target[:,:,:3][neutral(target)],axis=0)/np.median(pool,axis=0)
for n,im in enumerate(native):
 t=np.array(im);mask=neutral(t);t[mask,:3]=np.clip(t[mask,:3]*gain,0,255).astype('uint8');native[n]=Image.fromarray(t)
files={g:[] for g in held}
for g in held:
 for i in range(6):
  path=P/f'frames/{g}/carry-start-east/{i:03}.png';path.parent.mkdir(parents=True,exist_ok=True)
  if i==0:shutil.copy2(R/(b['held'] if g=='bare' else 'character/bill-cargo-east-master-head-v1/frames/helmet/pickup-east/010.png'),path)
  elif i==5:shutil.copy2(R/(b['carry'] if g=='bare' else b['helmetCarry'])['sourceFiles'][0].removeprefix('res://'),path)
  else:
   rec=records[i-1];dy=rec['upperTranslation'][1];upper=Image.new('RGBA',(256,256));upper.alpha_composite(held[g],(0,dy));t=np.array(upper);Y,X=np.indices(t.shape[:2]);protect=(Y<rec['seam'])|((X>=135)&(Y<170+dy));t[~protect]=0
   legs=np.array(native[i-1]);legs[protect]=t[protect];Image.fromarray(legs).save(path)
  files[g].append('res://'+path.relative_to(R).as_posix())
 durations=[40,50,55,65,65,45]
 manifest={'name':'Bill authored East first-step bridge preview','status':'staged_visual_review','frameWidth':256,'frameHeight':256,'standingHeight':148,'pivot':[128,224],'precomposed':True,'states':[{'id':'carry-start-east','frameFiles':files[g],'frameDurationsMs':durations,'loop':False,'facings':['east']*6,'waterPoses':[False]*6}]}
 (P/f'{g}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(P/'registration.json').write_text(json.dumps({'calibration':{'source':'sources/first-step-v2.png','firstCompleteHeight':height,'scale':scale,'targetStandingHeight':148,'sourceGround':ground},'fixedNeutralLegGain':gain.tolist(),'scope':'Bounded authored lower body only; exact master upper pixels translated by measured source crown drop; endpoint byte copies. No per-pose resizing.','frames':records},indent=2)+'\n',encoding='utf-8')
board=Image.new('RGBA',(1536,620),(34,52,62,255));draw=ImageDraw.Draw(board)
for row,g in enumerate(files):
 for i,file in enumerate(files[g]):board.alpha_composite(Image.open(R/file.removeprefix('res://')).convert('RGBA'),(i*256,row*310));draw.text((i*256+8,row*310+275),g+' '+str(i),fill='white')
board.convert('RGB').save(P/'candidate-review.png');print('Staged East bridge: shared ruler',scale,'leg gain',gain.tolist())
