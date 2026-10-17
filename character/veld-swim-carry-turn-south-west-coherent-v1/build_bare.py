"""Authored cargo yaw, shared material grade and exact master endpoints."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import label,binary_dilation
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def box(m):
 y,x=np.where(m);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def masks(a):
 v=a[:,:,:3].astype(float);sm=(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12);l,n=label(sm);z=np.bincount(l.ravel());assert n;skin=l==1+np.argmax(z[1:]);fb=box(skin);w=fb[2]-fb[0];y,x=np.indices(a.shape[:2]);head=(x>fb[0]-w*.65)&(x<fb[2]+w*.5)&(y>fb[1]-w*2)&(y<fb[3]+2)
 # Hands/case ahead of the face stay ungraded. Cloth/patch authority is body.
 body=(~head)&(y<fb[3])&(a[:,:,3]>200)
 return dict(skin=skin,cloth=body&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),patch=body&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)),fb,head
source=H/'body-source-v1.png';a=np.array(Image.open(source).convert('RGBA'));l,n=label(a[:,:,3]>160);z=np.bincount(l.ravel());ids=sorted(range(1,n+1),key=lambda k:z[k],reverse=True)[:4];ids.sort(key=lambda k:(int(np.where(l==k)[0].mean()//(a.shape[0]/2)),np.where(l==k)[1].mean()))
crops=[];records=[];checks=0
for i,k in enumerate(ids):
 local=a;ll=l;sourceFile=source.name
 b=box(ll==k);b=[b[0]-2,b[1]-2,b[2]+2,b[3]+2];assert min(b[:2])>=0 and b[2]<=local.shape[1] and b[3]<=local.shape[0];checks+=1
 cut=local.copy();cut[~binary_dilation(ll==k,iterations=2)]=0;im=Image.fromarray(cut).crop(b);crops.append(im);records.append(dict(slot=i+1,sourceFile=sourceFile,sourceSha256=sha(H/sourceFile),sourceBox=b));(H/'source-crops').mkdir(exist_ok=True);im.save(H/f'source-crops/{i:03}.png')
refs=[R/f'character/veld-swim-carry-{d}-coherent-v1/frames/bare/swim-carry-{d}/000.png' for d in ['south','west']]
values={k:[] for k in ['skin','cloth','patch']};targets={k:[] for k in values}
for im,dest in [(im,values) for im in crops]+[(Image.open(p).convert('RGBA'),targets) for p in refs]:
 ar=np.array(im);mm,_,_=masks(ar)
 for key in dest:dest[key].extend(ar[:,:,:3][mm[key]])
q=[0,15,35,55,75,90,100];curves={k:dict(knots=np.percentile(np.mean(values[k],axis=1),q).tolist(),targets=np.percentile(targets[k],q,axis=0).tolist()) for k in values}
anchors=[]
for p in refs:
 _,fb,_=masks(np.array(Image.open(p).convert('RGBA')));anchors.append([(fb[0]+fb[2])*.5,fb[3]])
scale=.21;frames=[Image.open(refs[0]).convert('RGBA')]
for i,im in enumerate(crops):
 ar=np.array(im);before=ar.copy();v=ar[:,:,:3].astype(float);mm,fb,head=masks(ar)
 for key,m in mm.items():
  for c in range(3):ar[m,c]=np.interp(v[m].mean(1),curves[key]['knots'],np.array(curves[key]['targets'])[:,c]).clip(0,255).astype('uint8')
 union=mm['skin']|mm['cloth']|mm['patch'];assert np.array_equal(before[~union],ar[~union]);assert np.array_equal(before[:,:,3],ar[:,:,3]);checks+=2
 t=(i+1)/5;target=np.array(anchors[0])*(1-t)+np.array(anchors[1])*t;pos=np.rint(target-np.array([(fb[0]+fb[2])*.5,fb[3]])*scale).astype(int);pose=Image.fromarray(ar).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(256,256));out.alpha_composite(pose,tuple(pos));frames.append(out);records[i].update(faceBox=fb,position=pos.tolist(),scale=scale)
frames.append(Image.open(refs[1]).convert('RGBA'));old=json.loads((R/'character/dr-veld-v2/packs/bare-256x256-p128.0-128.0/manifest.json').read_text());states=[];hashes={}
for direction,row in [('south-west',frames),('west-south',list(reversed(frames)))]:
 state=next(s for s in old['states'] if s['id']=='swim-carry-turn-'+direction).copy();assert len(state['frameDurationsMs'])==6;files=[]
 for i,im in enumerate(row):
  ar=np.array(im);assert not np.any(np.concatenate([ar[0,:,3],ar[-1,:,3],ar[:,0,3],ar[:,-1,3]])>20);checks+=1;p=H/f'frames/bare/{state["id"]}/{i:03}.png';p.parent.mkdir(parents=True,exist_ok=True);im.save(p);f=p.relative_to(H).as_posix();files.append(f);hashes[f]=sha(p)
 state['frameFiles']=files;states.append(state)
m=dict(name='Veld cargo south/west turns bare',frameWidth=256,frameHeight=256,pivot=[128,128],standingHeight=148,textureFilter='linear',precomposed=True,status='staged_pending_helmet_native_motion_world_review',states=states)
(H/'bare-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');board=Image.new('RGBA',(1536,580),'#202a30');d=ImageDraw.Draw(board)
for i,im in enumerate(frames):
 board.alpha_composite(im,(i*256,20));board.alpha_composite(im.resize((142,142),Image.Resampling.BILINEAR),(i*256+57,320));d.text((i*256+4,4),str(i)+(' exact cargo master' if i in [0,5] else ' authored yaw'),fill='white')
board.save(H/'bare-contact-v1.png');(H/'bare-fit-v1.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,scale=scale,records=records,curves=curves,sourceSha256=sha(source),frameHashes=hashes,endpointHashes={str(p.relative_to(R)):sha(p) for p in refs},scope='Authored extraction/shared material ownership/clipping/exact cargo endpoints; anatomical scale and angular pacing require visual review'),indent=2)+'\n',encoding='utf-8');print(f'{checks} bare fit checks PASS;12refs staged')
