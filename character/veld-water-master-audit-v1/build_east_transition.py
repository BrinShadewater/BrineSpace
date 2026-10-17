"""Rebuild four authored east launch interiors at one anatomy scale; exact joins."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];cov=json.loads((ROOT/'character/veld-consistency-audit-v2/coverage.json').read_text());source=Image.open(HERE/'east-transition-source-v1.png').convert('RGBA');a=np.array(source);labels,n=label(a[:,:,3]>160);counts=np.bincount(labels.ravel());ids=sorted(range(1,n+1),key=lambda k:counts[k],reverse=True)[:4];ids.sort(key=lambda k:np.where(labels==k)[1].mean());SCALE=.26
# One atlas-wide neutral material curve against selected accepted idle; not per-pose.
ref=np.array(Image.open(ROOT/'character/crew-runtime-matte-v1/veld/frames/idle-east-breathing-v1/000.png'));r=ref[:,:,:3].astype(float);rm=(ref[:,:,3]>200)&(np.ptp(r,axis=2)<22)&(r.mean(2)>20)&(r.mean(2)<130);rm[:59]=False
rgb=a[:,:,:3].astype(float);sm=(a[:,:,3]>200)&(np.ptp(rgb,axis=2)<22)&(rgb.mean(2)>20)&(rgb.mean(2)<130);knots=np.percentile(rgb[sm].mean(1),[0,15,35,55,75,90,100]);targets=np.percentile(r[rm],[0,15,35,55,75,90,100],axis=0)
for c in range(3):a[sm,c]=np.interp(rgb[sm].mean(1),knots,targets[:,c]).clip(0,255).astype('uint8')
skin=(a[:,:,3]>200)&(rgb[:,:,0]>110)&(rgb[:,:,0]>rgb[:,:,1]*1.17)&(rgb[:,:,1]>rgb[:,:,2]*1.12);a[skin,:3]=np.rint(rgb[skin]*[.9,.93,.94]).clip(0,255).astype('uint8')
source=Image.fromarray(a);body=[];helm=[];records=[];checks=0
for variant,rows in [('bare',body),('helmet',helm)]:
 path=ROOT/cov['selected']['bare']['tread-east']['files'][0] if variant=='bare' else HERE/'frames/helmet/tread-east/000.png';im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(path).convert('RGBA'),(36,58));rows.append(im)
master=Image.open(ROOT/'character/veld-helmet-fitting-east-v2/frames/equipped-idle-east/000.png').convert('RGBA').crop((82,17,116,55));o=np.array(master);oh,ow=o.shape[:2];pivot=np.array([ow*.5,oh*.85]);edge=np.array([30,21])
for j,k in enumerate(ids):
 keep=binary_dilation(labels==k,iterations=2);cut=np.array(source);cut[~keep]=0;yy,xx=np.where(labels==k);box=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];raw=Image.fromarray(cut).crop(box);ar=np.array(raw);y,x=np.where((ar[:,:,3]>160)&(np.indices(ar.shape[:2])[0]<30));center=(x.min()+x.max())/2
 pose=raw.resize((round(raw.width*SCALE),round(raw.height*SCALE)),Image.Resampling.LANCZOS);top=[90,94,98,101][j];pos=(round(136-center*SCALE),top);bare=Image.new('RGBA',(256,256));bare.alpha_composite(pose,pos);b=np.array(bare);rgb=b[:,:,:3].astype(int);Y,X=np.indices(b.shape[:2]);warm=(b[:,:,3]>200)&(rgb[:,:,0]>rgb[:,:,1]+15)&(rgb[:,:,0]>rgb[:,:,2]+25)&(Y>=top)&(Y<top+28);y,x=np.where(warm);faceX=int(x.max());near=warm&(X>=faceX-1);ny,nx=np.where(near);target=np.array([faceX,float(np.median(ny))]);theta=np.deg2rad(4*(j+1));c,s=np.cos(theta),np.sin(theta);rotate=lambda v:np.array([v[0]*c-v[1]*s,v[0]*s+v[1]*c]);offset=target-rotate(edge-pivot)-pivot;ctr=offset+pivot;dx,dy=X+.5-ctr[0],Y+.5-ctr[1];sx=dx*c+dy*s+pivot[0];sy=-dx*s+dy*c+pivot[1];ix=np.floor(sx).astype(int);iy=np.floor(sy).astype(int);inside=(ix>=0)&(iy>=0)&(ix<ow)&(iy<oh);pixels=o[np.clip(iy,0,oh-1),np.clip(ix,0,ow-1)];graft=inside&(pixels[:,:,3]>0)
 clear=(X>=pos[0]+int(center*SCALE)-19)&(X<faceX+3)&(Y>=top-1)&(Y<top+25);h=b.copy();h[clear]=0;h[graft]=pixels[graft];helmet=Image.fromarray(h);assert np.array_equal(b[~(graft|clear)],h[~(graft|clear)]);checks+=1
 for im in [bare,helmet]:
  ar=np.array(im);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1
 body.append(bare);helm.append(helmet);records.append({'cell':j,'component':k,'sourceBox':box,'scale':SCALE,'headAnchor':[136,top],'position':pos,'helmetFaceEdge':target.tolist(),'helmetOffset':offset.tolist(),'helmetTilt':4*(j+1)})
for variant,rows in [('bare',body),('helmet',helm)]:
 path=ROOT/cov['selected']['bare']['swim-east']['files'][0] if variant=='bare' else HERE/'frames/helmet/swim-east/000.png';im=Image.new('RGBA',(256,256));im.alpha_composite(Image.open(path).convert('RGBA'),(6,40));rows.append(im)
 sourceManifest=json.loads((ROOT/cov['selected']['bare']['swim-start-east']['manifest']).read_text());states=[]
 for action,order in [('swim-start-east',list(range(6))),('swim-stop-east',list(range(5,-1,-1)))]:
  state=next(s for s in sourceManifest['states'] if s['id']==action).copy();files=[]
  for i,index in enumerate(order):
   file=f'frames/{variant}/{action}/{i:03}.png';(HERE/file).parent.mkdir(parents=True,exist_ok=True);rows[index].save(HERE/file);files.append(file)
  state['frameFiles']=files;states.append(state)
 manifest={**sourceManifest,'name':'Veld coherent east swim transitions '+variant,'states':states,'status':'staged_master_transition_pending_visual_review'}
 (HERE/f'east-transition-{variant}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
contact=Image.new('RGBA',(1536,560),'#202a30');draw=ImageDraw.Draw(contact)
for row,rows in enumerate([body,helm]):
 for i,im in enumerate(rows):contact.alpha_composite(im,(i*256,row*280+24));draw.text((i*256+4,row*280+4),('bare' if row==0 else 'helmet')+' / '+str(i),fill='white')
contact.save(HERE/'east-transition-master-v1.png');(HERE/'east-transition-fit-checks.json').write_text(json.dumps({'checks':checks,'failures':0,'sourceSha256':hashlib.sha256((HERE/'east-transition-source-v1.png').read_bytes()).hexdigest(),'fixedAnatomicalScale':SCALE,'neutralCurveKnots':knots.tolist(),'neutralCurveTargets':targets.tolist(),'records':records,'installed':False},indent=2)+'\n',encoding='utf-8');print(f'{checks} transition body/clipping checks pass.')
