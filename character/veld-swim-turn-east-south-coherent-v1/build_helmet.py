"""Fit authored prone yaw components; exact selected equipment loop endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
from fit_material_trials import masks,curves
H=Path(__file__).resolve().parent;R=H.parents[1];source=H/'helmet-source-v1.png';a=np.array(Image.open(source).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:4];assert len(ids)==4;ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/2)),np.where(lab==k)[1].mean()))
masterE=Image.open(R/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((82,17,116,55)).rotate(-16,resample=Image.Resampling.BICUBIC,expand=True);masterS=Image.open(R/'character/veld-water-master-audit-v1/fitted-swim-south-head.png').convert('RGBA')
def metal(a):
 v=a[:,:,:3].astype(float);return (a[:,:,3]>200)&(v[:,:,0]<v[:,:,1]*1.3)&(v[:,:,1]<v[:,:,2]*1.3)&(v[:,:,2]<v[:,:,0]*1.2)&(v.mean(2)>20)&(v.mean(2)<230)
q=[0,15,35,55,75,90,100];src=a[:,:,:3][metal(a)].astype(float);ref=np.concatenate([np.array(im)[:,:,:3][metal(np.array(im))] for im in [masterE,masterS]]).astype(float);knots=np.percentile(src.mean(1),q);targets=np.percentile(ref,q,axis=0)
frames=[Image.open(R/'character/veld-water-east-coherent-v1/frames/helmet/swim-east/000.png').convert('RGBA')];records=[];checks=0;headboard=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(headboard)
for i,k in enumerate(ids):
 y,x=np.where(lab==k);box=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3];assert min(box[:2])>=0 and box[2]<=a.shape[1] and box[3]<=a.shape[0];checks+=1;cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;raw=Image.fromarray(cut).crop(box);(H/'helmet-source-crops').mkdir(exist_ok=True);raw.save(H/f'helmet-source-crops/{i:03}.png');ar=np.array(raw);v=ar[:,:,:3].astype(float);sm,fb,head=masks(ar);mm=metal(ar)
 for c in range(3):ar[mm,c]=np.interp(v[mm].mean(1),knots,targets[:,c]).clip(0,255).astype('uint8');ar[sm['skin'],c]=np.interp(v[sm['skin']].mean(1),curves['skin']['knots'],np.array(curves['skin']['targets'])[:,c]).clip(0,255).astype('uint8')
 union=mm|sm['skin'];assert np.array_equal(np.array(raw)[~union],ar[~union]);checks+=1
 scale=.083;component=Image.fromarray(ar).resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS);cm,cfb,ch=masks(np.array(component));bare=Image.open(H/f'graded-trials/{i:03}.png').convert('RGBA');ba=np.array(bare);bm,bfb,bhead=masks(ba);bc=np.array([(bfb[0]+bfb[2])/2,bfb[3]]);cc=np.array([(cfb[0]+cfb[2])/2,cfb[3]]);pos=np.rint(bc-cc).astype(int)
 # Remove only original warm head support; preserve neutral collar/sleeves beneath.
 bv=ba[:,:,:3].astype(float);erase=bhead&(ba[:,:,3]>0)&((bv[:,:,0]>bv[:,:,1]*1.1)|(bv[:,:,1]>bv[:,:,2]*1.25));clean=ba.copy();clean[erase]=0;out=Image.fromarray(clean);out.alpha_composite(component,tuple(pos));oa=np.array(out);protected=~erase;px,py=pos;protected[max(py,0):min(py+component.height,256),max(px,0):min(px+component.width,256)]=False;assert np.array_equal(ba[protected],oa[protected]);checks+=1;assert not np.any(np.concatenate([oa[0,:,3],oa[-1,:,3],oa[:,0,3],oa[:,-1,3]])>20);checks+=1
 frames.append(out);headboard.alpha_composite(bare.crop((95,85,178,166)).resize((249,243),Image.Resampling.NEAREST),(i*384+50,25));headboard.alpha_composite(out.crop((95,85,178,166)).resize((249,243),Image.Resampling.NEAREST),(i*384+50,305));draw.text((i*384+4,4),f'bare /slot{i+1}',fill='white');draw.text((i*384+4,284),f'helmet /slot{i+1}',fill='white');records.append({'slot':i+1,'sourceBox':box,'scale':scale,'nativeComponentSize':list(component.size),'bodyFaceBox':bfb,'componentFaceBox':cfb,'placement':pos.tolist(),'erasedWarmHeadPixels':int(erase.sum())})
frames.append(Image.open(R/'character/veld-water-south-coherent-v1/frames/helmet/swim-south/000.png').convert('RGBA'));manifest=json.loads((H/'bare-manifest.json').read_text());states=[]
for direction,row in [('east-south',frames),('south-east',list(reversed(frames)))]:
 state=next(s for s in manifest['states'] if s['id']=='swim-turn-'+direction).copy();files=[]
 for i,im in enumerate(row):
  file=f'frames/helmet/swim-turn-{direction}/{i:03}.png';(H/file).parent.mkdir(parents=True,exist_ok=True);im.save(H/file);files.append(file)
 state.update(frameFiles=files);states.append(state)
manifest.update(name='Veld coherent east south ordinary swim turns helmet',states=states,status='staged_paired_yaw_pending_motion_native_review');(H/'helmet-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');headboard.save(H/'helmet-fit-contact-v1.png');(H/'helmet-fit-v1.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'fixedAtlasScale':.083,'records':records,'neutralCurve':{'knots':knots.tolist(),'targets':targets.tolist()},'bodyOutsideRepairExact':True,'status':'4 component fits; visual collar/aperture/pose checks required before selecting','installed':False},indent=2)+'\n');print(f'{checks} extraction/material/protected-body/border checks PASS;2 helmet states12refs staged')
