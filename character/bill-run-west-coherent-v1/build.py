from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
IDLE=P.parent/'bill-seated-west-coherent-v1/frames/sit-down-west/000.png'
ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
rn=(ref[:,:,3]>200)&(ry>102)&(np.ptp(rr,axis=2)<45)&(rr[:,:,0]<1.4*rr[:,:,1])&(rr[:,:,0]<1.4*rr[:,:,2])
q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];dst=np.quantile(rr.mean(2)[rn],q)
authorities={'face':(ref[:,:,3]>180)&(ry>=85)&(ry<102)&(rx<130)&(rr.mean(2)>65)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]),'hair':(ref[:,:,3]>180)&(ry>=76)&(ry<85)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]),'burgundy':(ref[:,:,3]>180)&(ry>100)&(ry<128)&(rr[:,:,0]>70)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])}
sources=['run-v1.png'];arrays=[np.array(Image.open(P/'sources'/f).convert('RGBA')) for f in sources]
neutral=[];headmasks=[]
for a in arrays:
 rgb=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2]);head=((yy>=50)&(yy<156))|((yy>=546)&(yy<650))
 headmasks.append(head);neutral.append((a[:,:,3]>200)&~head&(np.ptp(rgb,axis=2)<45)&(rgb[:,:,0]<1.4*rgb[:,:,1])&(rgb[:,:,0]<1.4*rgb[:,:,2]))
src=np.quantile(np.concatenate([a[:,:,:3].mean(2)[n] for a,n in zip(arrays,neutral)]),q)
gains={};masks=[]
for a,head in zip(arrays,headmasks):
 rgb=a[:,:,:3].astype(float);warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(a[:,:,3]>200)
 masks.append({'face':head&warm&(rgb.mean(2)>=80),'hair':head&warm&(rgb.mean(2)<80),'burgundy':~head&(a[:,:,3]>200)&(rgb[:,:,0]>70)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])})
for name,authority in authorities.items():
 vals=np.concatenate([a[:,:,:3][m[name]] for a,m in zip(arrays,masks)])
 gains[name]=np.median(rr[authority],axis=0)/np.maximum(np.median(vals,axis=0),1)
files=[];records=[];ruler=148/430
for k,(a,n,mm) in enumerate(zip(arrays,neutral,masks)):
 rgb=a[:,:,:3].astype(float);out=a.copy();lum=rgb.mean(2)
 out[n,:3]=np.clip(rgb[n]*np.interp(lum[n],src,dst)[:,None]/np.maximum(lum[n,None],1),0,255).astype('uint8')
 for name,mask in mm.items():out[mask,:3]=np.clip(rgb[mask]*gains[name],0,255).astype('uint8')
 lab,_=label(a[:,:,3]>180);sizes=np.bincount(lab.ravel());sizes[0]=0;ids=sorted(np.argsort(sizes)[-6:],key=lambda z:(int(np.median(np.where(lab==z)[0]))//512,int(np.where(lab==z)[1].min())))
 for i,lid in enumerate(ids):
  y,x=np.where(lab==lid);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];mask=binary_dilation(lab==lid,iterations=3)&(a[:,:,3]>0);clean=out.copy();clean[~mask]=0
  im=Image.fromarray(clean).crop(box);im=im.resize((round(im.width*ruler),round(im.height*ruler)),Image.Resampling.LANCZOS)
  root=[284,762,1260,267,744,1250][i];baseline=[489,489,489,961,961,961][i];pos=[round(128-(root-box[0])*ruler),round(224-(baseline-box[1])*ruler)]
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);f=P/f'frames/run-west/{len(files):03}.png';f.parent.mkdir(parents=True,exist_ok=True);plane.save(f);files.append('res://'+f.relative_to(R).as_posix())
  records.append({'frame':len(files)-1,'source':'sources/'+sources[k],'box':box,'scale':[ruler,ruler],'pelvisAxisX':root,'sourceBaseline':baseline,'position':pos})
m={'name':'Bill west authored run candidate','status':'selected_runtime','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'strideDistanceCells':{'run-west':.168},'states':[{'id':'run-west','frameFiles':files,'frameDurationsMs':[90,80,100,90,80,100],'loop':True}]}
(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');(P/'registration.json').write_text(json.dumps({'frames':records,'neutralCurve':{'source':src.tolist(),'master':dst.tolist()},'semanticGains':{k:v.tolist() for k,v in gains.items()},'scope':'fixed anatomical ruler across independently authored6pose atlas, shared pooled grade; no per-pose scale or equalized crouch height'},indent=2)+'\n')
board=Image.new('RGB',(1792,512),(34,52,62));draw=ImageDraw.Draw(board)
for i,f in enumerate([IDLE]+[R/f[6:] for f in files]):
 im=Image.open(f).convert('RGBA');board.paste(im,(i*256,0),im);small=im.resize((142,142),Image.Resampling.LANCZOS);board.paste(small,(i*256+57,320),small);draw.text((i*256+20,260),'Master' if i==0 else 'Run '+str(i-1),fill='white')
board.save(P/'master-review.png');print('Built6 distinct west run candidates with pooled master grade/fixed148 anatomy')
