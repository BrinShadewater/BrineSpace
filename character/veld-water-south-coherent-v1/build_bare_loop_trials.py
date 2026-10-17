"""Physical shoulder-scale south loop trials; no selected manifests."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label
H=Path(__file__).resolve().parent;R=H.parents[1];cov=json.loads((R/'character/veld-consistency-audit-v2/coverage.json').read_text());ref=np.array(Image.open(R/cov['selected']['bare']['idle-south']['files'][0]).convert('RGBA'));rv=ref[:,:,:3].astype(float);q=[0,15,35,55,75,90,100]
def masks(a,face_count=1):
 v=a[:,:,:3].astype(float);sm=(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12);sl,sn=label(sm);sc=np.bincount(sl.ravel());ids=sorted(range(1,sn+1),key=lambda k:sc[k],reverse=True)[:face_count];face=np.isin(sl,ids);return {'cloth':(a[:,:,3]>200)&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),'patch':(a[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35),'skin':face}
rm=masks(ref);rm['cloth'][:59]=False;values={k:[] for k in rm}
for kind in ['tread','swim']:
 a=np.array(Image.open(H/f'{kind}-source-v1.png').convert('RGBA'));v=a[:,:,:3].astype(float)
 for key,m in masks(a,6).items():values[key].extend(v[m])
curves={k:{'knots':np.percentile(np.mean(values[k],axis=1),q),'targets':np.percentile(rv[rm[k]],q,axis=0)} for k in rm}
records=[];checks=0;sheet=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(sheet)
for row,kind in enumerate(['tread','swim']):
 for slot in range(6):
  im=Image.open(H/f'source-crops/{kind}/{slot:03}.png').convert('RGBA');a=np.array(im);v=a[:,:,:3].astype(float)
  skin=masks(a)['skin'];lab,n=label(skin);counts=np.bincount(lab.ravel());face=lab==(1+np.argmax(counts[1:]));y,x=np.where(face);headX=float(np.median(x));faceBottom=int(y.max())
  for key,m in masks(a).items():
   curve=curves[key]
   for c in range(3):a[m,c]=np.interp(v[m].mean(1),curve['knots'],curve['targets'][:,c]).clip(0,255).astype('uint8')
  scale=.21;pose=Image.fromarray(a).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
  pos=(round(128-headX*scale),107 if kind=='tread' else round(156-faceBottom*scale));out=Image.new('RGBA',(256,256));out.alpha_composite(pose,pos);ar=np.array(out);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
  path=f'body-trials/{kind}/{slot:03}.png';(H/path).parent.mkdir(parents=True,exist_ok=True);out.save(H/path);sheet.alpha_composite(out,(slot*256,row*280+24));draw.text((slot*256+4,row*280+4),kind+' trial / '+str(slot),fill='white');records.append({'kind':kind,'slot':slot,'scale':scale,'sourceFaceCentre':headX,'sourceFaceBottom':faceBottom,'position':list(pos),'file':path})
sheet.save(H/'bare-loop-fit-trials-v1.png');(H/'bare-loop-trial-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'selected':False,'status':'physical_ruler_and_face_anchor_trials_pending_visual_review','physicalScaleHypothesis':'upright source shoulder span about200 maps to selected front shoulder span42; .21 frozen per atlas; inspect upright/prone head/hip rulers','curves':{k:{kk:vv.tolist() for kk,vv in v.items()} for k,v in curves.items()},'records':records},indent=2)+'\n',encoding='utf-8');print(f'{checks} bare loop trial border checks PASS; no candidate selection changed.')
