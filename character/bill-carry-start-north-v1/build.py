from pathlib import Path
import json,hashlib,shutil
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parent.parent;G=R/'character/bill-carry-north-gait-v1'
source=P/'sources/first-step-v1.png';raw=np.array(Image.open(source).convert('RGBA'));labs,_=label(raw[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0;ids=sorted(np.argsort(counts)[-4:],key=lambda k:np.where(labs==k)[1].mean())
y,x=np.where(labs==ids[3]);height=int(y.max()-y.min()+1);scale=148/height;ground=int(y.max());Y,X=np.indices((256,256));protected=Y<164
masters={g:np.array(Image.open(R/f'character/bill-cargo-north-master-head-v1/frames/{g}/pickup-north/011.png').convert('RGBA')) for g in ['bare','helmet']}
native=[];records=[]
for i,k in enumerate(ids[:3]):
 a=raw.copy();a[~(binary_dilation(labs==k,iterations=1)&(raw[:,:,3]>80))]=0;yy,xx=np.indices(a.shape[:2]);band=(a[:,:,3]>180)&(yy>=ground-55/scale)&(yy<ground-49/scale);axis=float((np.where(band)[1].min()+np.where(band)[1].max())/2);ys,xs=np.where(a[:,:,3]>180);box=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 im=Image.fromarray(a).crop(box);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);pos=[round(128-(axis-box[0])*scale),round(223-(ground-box[1])*scale)];out=Image.new('RGBA',(256,256));out.alpha_composite(im,pos);part=np.array(out);part[protected]=0;native.append(part);records.append({'sample':i,'box':box,'scale':scale,'position':pos,'hipAxis':axis})
def neutral(a):return (a[:,:,3]>180)&(Y>=164)&(Y<220)&(np.ptp(a[:,:,:3],axis=2)<25)&(a[:,:,:3].mean(2)>15)
pool=np.concatenate([a[:,:,:3][neutral(a)] for a in native]);gain=np.median(masters['bare'][:,:,:3][neutral(masters['bare'])],axis=0)/np.median(pool,axis=0)
for a in native:
 m=neutral(a);rgb=a[m,:3].astype(float)*gain;lum=rgb.mean(1);matte=lum-np.maximum(lum-100,0)*.18;a[m,:3]=np.clip(rgb*(matte/np.maximum(lum,1))[:,None],0,255).astype('uint8')
inputs={str(source.relative_to(R).as_posix()):hashlib.sha256(source.read_bytes()).hexdigest()};files={}
for gear,master in masters.items():
 gf=json.loads((G/f'{gear}-manifest.json').read_text())['states'][0]['frameFiles']
 files[gear]=[]
 for i in range(6):
  f=P/f'frames/{gear}/carry-start-north/{i:03}.png';f.parent.mkdir(parents=True,exist_ok=True)
  if i==0 or i>=4:
   src=R/(f'character/bill-cargo-north-master-head-v1/frames/{gear}/pickup-north/011.png' if i==0 else gf[0].removeprefix('res://'));shutil.copy2(src,f);inputs[src.relative_to(R).as_posix()]=hashlib.sha256(src.read_bytes()).hexdigest()
  else:
   a=native[i-1].copy();a[protected]=master[protected];Image.fromarray(a).save(f)
  files[gear].append('res://'+f.relative_to(R).as_posix())
 m={'name':'Bill North held-to-first-step candidate','status':'staged_visual_review','frameWidth':256,'frameHeight':256,'standingHeight':148,'pivot':[128,224],'precomposed':True,'textureFilter':'linear','states':[{'id':'carry-start-north','frameFiles':files[gear],'frameDurationsMs':[40,50,55,65,65,45],'loop':False,'facings':['north']*6,'waterPoses':[False]*6}]};(P/f'{gear}-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
reg={'sourceSha256':inputs,'standingSample':3,'standingSourceHeight':height,'scale':scale,'sourceGround':ground,'frames':records,'neutralGainPooled':gain.tolist(),'sharedHighlightCurve':[100,.82],'resumeGaitPhaseSeconds':.139,'scope':'Three authored first-step interiors; exact upper above164, canonical held0 and gait0 final byte copies; one standing ruler/ground, pooled grade.'};(P/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
b=Image.new('RGB',(1536,600),'#22343e');d=ImageDraw.Draw(b)
for row,gear in enumerate(files):
 for i,f in enumerate(files[gear]):
  a=Image.open(R/f.removeprefix('res://')).convert('RGBA');b.paste(a,(i*256,row*300),a);d.text((i*256+8,row*300+265),gear+' start'+str(i),fill='white')
b.save(P/'candidate-review.png');print('North paired bridge:',height,scale,gain.tolist())
