"""Deterministic candidate extraction; no runtime selection or new painted anatomy."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
IDLE=P.parent/'bill-seated-south-coherent-v1/frames/sit-down-south/000.png'
ref=np.array(Image.open(IDLE).convert('RGBA'));rr=ref[:,:,:3].astype(float);ry,rx=np.indices(ref.shape[:2])
rn=(ref[:,:,3]>200)&(ry>102)&(np.ptp(rr,axis=2)<45)&(rr[:,:,0]<1.4*rr[:,:,1])&(rr[:,:,0]<1.4*rr[:,:,2])
q=[0,.05,.15,.35,.5,.7,.85,.95,.98,1];dst=np.quantile(rr.mean(2)[rn],q)
authorities={'face':(ref[:,:,3]>180)&(ry>=85)&(ry<102)&(rx>=112)&(rx<144)&(rr.mean(2)>65)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]),'hair':(ref[:,:,3]>180)&(ry>=76)&(ry<85)&(rr[:,:,0]>1.12*rr[:,:,1])&(rr[:,:,1]>1.25*rr[:,:,2]),'burgundy':(ref[:,:,3]>180)&(ry>100)&(ry<128)&(rr[:,:,0]>70)&(rr[:,:,0]>1.4*rr[:,:,1])&(rr[:,:,0]>1.4*rr[:,:,2])}
specs=[{'file':'walk-v6.png','count':6,'cells':[0,1,2,3,4,5],'ruler':148/490,'axes':[291,790,1270,285,788,1280],'baselines':[510,510,510,1010,1010,1010]}]
files=[];records=[]
for spec in specs:
 a=np.array(Image.open(P/'sources'/spec['file']).convert('RGBA'));rgb=a[:,:,:3].astype(float);yy,xx=np.indices(a.shape[:2]);head=((yy>=15)&(yy<125))|((yy>=520)&(yy<635))
 n=(a[:,:,3]>200)&~head&(np.ptp(rgb,axis=2)<45)&(rgb[:,:,0]<1.4*rgb[:,:,1])&(rgb[:,:,0]<1.4*rgb[:,:,2])
 src=np.quantile(rgb.mean(2)[n],q);warm=(rgb[:,:,0]>1.12*rgb[:,:,1])&(rgb[:,:,1]>1.25*rgb[:,:,2])&(a[:,:,3]>200)
 masks={'face':head&warm&(rgb.mean(2)>=80),'hair':head&warm&(rgb.mean(2)<80),'burgundy':~head&(a[:,:,3]>200)&(rgb[:,:,0]>70)&(rgb[:,:,0]>1.4*rgb[:,:,1])&(rgb[:,:,0]>1.4*rgb[:,:,2])}
 gains={k:np.median(rr[authorities[k]],axis=0)/np.maximum(np.median(rgb[mask],axis=0),1) for k,mask in masks.items()}
 out=a.copy();lum=rgb.mean(2);out[n,:3]=np.clip(rgb[n]*np.interp(lum[n],src,dst)[:,None]/np.maximum(lum[n,None],1),0,255).astype('uint8')
 for k,mask in masks.items():out[mask,:3]=np.clip(rgb[mask]*gains[k],0,255).astype('uint8')
 labs,_=label(a[:,:,3]>180);sizes=np.bincount(labs.ravel());sizes[0]=0;ids=sorted(np.argsort(sizes)[-spec['count']:],key=lambda k:(np.median(np.where(labs==k)[0])//512,np.where(labs==k)[1].min()))
 for j,cell in enumerate(spec['cells']):
  ident=ids[cell];y,x=np.where(labs==ident);box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)];mask=binary_dilation(labs==ident,iterations=3)&(a[:,:,3]>0);clean=out.copy();clean[~mask]=0
  im=Image.fromarray(clean).crop(box);s=spec['ruler'];im=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.LANCZOS);pos=[round(128-(spec['axes'][j]-box[0])*s),round(224-(spec['baselines'][j]-box[1])*s)]
  plane=Image.new('RGBA',(256,256));plane.alpha_composite(im,pos);f=P/f'frames/walk-south-east/{len(files):03}.png';f.parent.mkdir(parents=True,exist_ok=True);plane.save(f);files.append('res://'+f.relative_to(R).as_posix())
  records.append({'frame':len(files)-1,'source':'sources/'+spec['file'],'sourceCell':cell,'box':box,'scale':[s,s],'pelvisAxisX':spec['axes'][j],'sourceBaseline':spec['baselines'][j],'position':pos,'neutralCurve':{'source':src.tolist(),'master':dst.tolist()},'semanticGains':{k:v.tolist() for k,v in gains.items()}})
m={'name':'Bill southeast walk review candidate','status':'review_candidate','frameWidth':256,'frameHeight':256,'pivot':[128,224],'standingHeight':148,'textureFilter':'linear','precomposed':True,'strideDistanceCells':{'walk-south-east':.12},'states':[{'id':'walk-south-east','frameFiles':files,'frameDurationsMs':[120]*6,'loop':True}]}
(P/'manifest.json').write_text(json.dumps(m,indent=2)+'\n');(P/'registration.json').write_text(json.dumps({'frames':records,'scope':'One fixed148/490 ruler across v6 atlas, one shared material grade; no per-pose fitting. Candidate gait/identity review pending.'},indent=2)+'\n')
masters=[P.parent/'bill-seated-east-coherent-v1/frames/sit-down-east/000.png',IDLE]
board=Image.new('RGB',(2048,512),(34,52,62));d=ImageDraw.Draw(board)
for i,f in enumerate(masters+[R/f[6:] for f in files]):
 im=Image.open(f).convert('RGBA');board.paste(im,(i*256,0),im);small=im.resize((142,142),Image.Resampling.LANCZOS);board.paste(small,(i*256+57,320),small);d.text((i*256+16,265),['East master','South master'][i] if i<2 else 'Walk '+str(i-2),fill='white')
board.save(P/'master-review.png');print('Built six review poses; runtime remains unchanged')
