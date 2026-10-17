"""Fit authored prone components from one raw ruler; preserve protected body."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent;R=H.parents[1];source=H/'helmet-source-v2.png';fit=json.loads((H/'material-fit-v1.json').read_text());a=np.array(Image.open(source).convert('RGBA'));lab,n=label(a[:,:,3]>160);sizes=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:sizes[k],reverse=True)[:4];ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(a.shape[0]/2)),np.where(lab==k)[1].mean()));chosen=[]
for k in ids:
 y,x=np.where(lab==k);box=[int(x.min())-2,int(y.min())-2,int(x.max())+3,int(y.max())+3];assert min(box[:2])>=0 and box[2]<=a.shape[1] and box[3]<=a.shape[0];cut=a.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;chosen.append((Image.fromarray(cut).crop(box),box))
masters=[Image.open(R/'character/veld-shared-helmet-v1/fitted-west.png').convert('RGBA').rotate(16,resample=Image.Resampling.BICUBIC,expand=True),Image.open(R/'character/veld-water-master-audit-v1/fitted-swim-north-head.png').convert('RGBA')]
def metal(a):
 v=a[:,:,:3].astype(float);return (a[:,:,3]>200)&(v[:,:,0]<v[:,:,1]*1.3)&(v[:,:,1]<v[:,:,2]*1.3)&(v[:,:,2]<v[:,:,0]*1.2)&(v.mean(2)>20)&(v.mean(2)<230)
q=[0,15,35,55,75,90,100];src=np.concatenate([np.array(raw)[:,:,:3][metal(np.array(raw))] for raw,_ in chosen]);ref=np.concatenate([np.array(im)[:,:,:3][metal(np.array(im))] for im in masters]);knots=np.percentile(src.mean(1),q);targets=np.percentile(ref,q,axis=0)
frames=[Image.open(R/'character/veld-water-west-coherent-v1/frames/helmet/swim-west/000.png').convert('RGBA')];checks=0;records=[];board=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(board)
# Component skull centers exclude downstream collar. Explicit semantic landmarks
# remain usable for rear views, which legitimately contain no visible skin.
SKULLS=[[0,0,450,380],[0,0,430,375],[0,0,430,390],[0,0,445,403]]
for i,(raw,box) in enumerate(chosen):
 (H/'helmet-source-crops').mkdir(exist_ok=True);raw.save(H/f'helmet-source-crops/{i:03}.png');before=np.array(raw);ar=before.copy();v=ar[:,:,:3].astype(float);mm=metal(ar);skin=(ar[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12)
 for c in range(3):
  ar[mm,c]=np.interp(v[mm].mean(1),knots,targets[:,c]).clip(0,255).astype('uint8');ar[skin,c]=np.interp(v[skin].mean(1),fit['curves']['skin']['knots'],np.array(fit['curves']['skin']['targets'])[:,c]).clip(0,255).astype('uint8')
 assert np.array_equal(before[~(mm|skin)],ar[~(mm|skin)]);assert np.array_equal(before[:,:,3],ar[:,:,3]);checks+=2
 scale=.07;component=Image.fromarray(ar).resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS);target=np.array(fit['records'][i]['headTarget'])+np.array([0,-2-3*(i+1)/5]);b=SKULLS[i];center=np.array([(b[0]+b[2])/2,(b[1]+b[3])/2])*scale;pos=np.rint(target-center).astype(int)
 bare=Image.open(H/f'graded-trials/{i:03}.png').convert('RGBA');ba=np.array(bare);bv=ba[:,:,:3].astype(float);b=fit['records'][i]['rawHeadBox'];base=np.array(fit['records'][i]['placement']);hb=np.rint(np.array(b)*fit['selectedScale']+np.tile(base,2)).astype(int);head=np.zeros((256,256),bool);head[hb[1]:hb[3],hb[0]:hb[2]]=True;erase=head&(ba[:,:,3]>0)&((bv[:,:,0]>bv[:,:,1]*1.1)|(bv[:,:,1]>bv[:,:,2]*1.25));clean=ba.copy();clean[erase]=0;out=Image.fromarray(clean);out.alpha_composite(component,tuple(pos));oa=np.array(out);protected=~erase;px,py=pos;protected[max(py,0):min(py+component.height,256),max(px,0):min(px+component.width,256)]=False;assert np.array_equal(ba[protected],oa[protected]);checks+=1;assert not np.any(np.concatenate([oa[0,:,3],oa[-1,:,3],oa[:,0,3],oa[:,-1,3]])>20);checks+=1;frames.append(out)
 records.append(dict(slot=i+1,sourceBox=box,scale=scale,rawSkullBox=SKULLS[i],headTarget=target.tolist(),placement=pos.tolist(),nativeComponentSize=list(component.size),erasedWarmHeadPixels=int(erase.sum()),bodyHeadBox=hb.tolist()))
 for row,im in enumerate([bare,out]):board.alpha_composite(im.crop((81,78,169,153)).resize((264,225),Image.Resampling.NEAREST),(i*384+50,row*280+30));draw.text((i*384+4,row*280+4),f'{["bare","helmet"][row]} /slot{i+1}',fill='white')
frames.append(Image.open(R/'character/veld-water-north-coherent-v1/frames/helmet/swim-north/000.png').convert('RGBA'));m=json.loads((H/'bare-manifest.json').read_text());states=[]
for direction,row in [('west-north',frames),('north-west',list(reversed(frames)))]:
 state=next(s for s in m['states'] if s['id']=='swim-turn-'+direction).copy();files=[]
 for i,im in enumerate(row):
  file=f'frames/helmet/swim-turn-{direction}/{i:03}.png';(H/file).parent.mkdir(parents=True,exist_ok=True);im.save(H/file);files.append(file)
 state['frameFiles']=files;states.append(state)
m.update(name='Veld coherent west north ordinary swim turns helmet',states=states,status='staged_paired_pending_native_motion_world_review');(H/'helmet-manifest.json').write_text(json.dumps(m,indent=2)+'\n');board.save(H/'helmet-fit-contact-v1.png');(H/'helmet-fit-v1.json').write_text(json.dumps(dict(checks=checks,failures=0,sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),records=records,fixedAtlasScale=.07,neutralCurve=dict(knots=knots.tolist(),targets=targets.tolist()),bodyOutsideRepairExact=True,installed=False),indent=2)+'\n');print(f'{checks} protected-body/material/border checks PASS;2 helmet states12refs staged')
