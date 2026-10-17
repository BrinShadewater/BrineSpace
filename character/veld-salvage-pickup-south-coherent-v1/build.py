"""Authored work/pickup, frozen cargo ruler/material curves and exact paired joins."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
H=Path(__file__).resolve().parent;R=H.parents[1];C=R/'character/veld-swim-carry-south-coherent-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def box(m):
 y,x=np.where(m);return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
def face(a):
 v=a[:,:,:3].astype(float);m=(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>1.25*v[:,:,1])&(v[:,:,1]>1.12*v[:,:,2]);l,n=label(m);assert n;z=np.bincount(l.ravel());return l==1+np.argmax(z[1:])
def masks(a):
 v=a[:,:,:3].astype(float);fb=box(face(a));y,x=np.indices(a.shape[:2]);h=fb[3]-fb[1]
 head=(y>fb[1]-h*2.5)&(y<fb[3])&(x>(fb[0]+fb[2])*.5-h*1.5)&(x<(fb[0]+fb[2])*.5+h*1.5);body=(~head)&(y<fb[3])&(a[:,:,3]>200)
 return dict(skin=face(a),cloth=body&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),patch=body&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35))
fit=json.loads((C/'fit-checks.json').read_text());scale=fit['fixedAtlasScale'];curves=fit['curves'];records=[];images={g:{} for g in ['bare','helmet']};checks=0
masterpath=R/'character/veld-water-master-audit-v1/fitted-swim-south-head.png';head=Image.open(masterpath).convert('RGBA');ha=np.array(head);v=ha[:,:,:3].astype(float);skin=(ha[:,:,3]>150)&(v[:,:,0]>90)&(v[:,:,0]>v[:,:,1]*1.18)&(v[:,:,1]>v[:,:,2]*1.1);hl,hn=label(skin);hz=np.bincount(hl.ravel());hfb=box(hl==1+np.argmax(hz[1:]));hp=(111,156-(hfb[3]-1));clear=(113,hp[1]-3,143,158)
for role in ['work','pickup']:
 p=H/f'{role}-source-v1.png';raw=np.array(Image.open(p).convert('RGBA'));lab,n=label(raw[:,:,3]>160);z=np.bincount(lab.ravel());ids=sorted(range(1,n+1),key=lambda k:z[k],reverse=True)[:6];assert len(ids)==6
 ids.sort(key=lambda k:(int(np.where(lab==k)[0].mean()//(raw.shape[0]/2)),np.where(lab==k)[1].mean()))
 for g in images:images[g][role]=[]
 for i,k in enumerate(ids):
  b=box(lab==k);b=[b[0]-2,b[1]-2,b[2]+2,b[3]+2];assert min(b[:2])>=0 and b[2]<=raw.shape[1] and b[3]<=raw.shape[0]
  cut=raw.copy();cut[~binary_dilation(lab==k,iterations=2)]=0;im=Image.fromarray(cut).crop(b);a=np.array(im);v=a[:,:,:3].astype(float);fb=box(face(a))
  for key,mask in masks(a).items():
   for c in range(3):a[mask,c]=np.interp(v[mask].mean(1),curves[key]['knots'],np.array(curves[key]['targets'])[:,c]).clip(0,255).astype('uint8')
  pose=Image.fromarray(a).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);pos=(round(128-(fb[0]+fb[2])*.5*scale),round(156-fb[3]*scale));bare=Image.new('RGBA',(256,256));bare.alpha_composite(pose,pos)
  helmet=bare.copy();helmet.paste((0,0,0,0),clear);helmet.alpha_composite(head,hp)
  before=np.array(bare);after=np.array(helmet);y,x=np.indices((256,256));v=before[:,:,:3].astype(float);foreground=(before[:,:,3]>200)&(np.ptp(v,axis=2)<25)&(y>=154)&(y<166)&(x>=111)&(x<146);after[foreground]=before[foreground];helmet=Image.fromarray(after)
  mask=np.ones((256,256),bool);mask[clear[1]:clear[3],clear[0]:clear[2]]=False;mask[hp[1]:hp[1]+head.height,hp[0]:hp[0]+head.width]=False
  assert np.array_equal(np.array(bare)[mask],np.array(helmet)[mask]);checks+=1
  records.append(dict(role=role,sourceCell=i,sourceBox=b,sourceFaceBox=fb,fixedScale=scale,position=pos,helmetPosition=hp,selected=role=='work' or i in [1,2,3,4]))
  for g,im in [('bare',bare),('helmet',helmet)]:
   a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1;images[g][role].append(im)
board=Image.new('RGBA',(1536,1150),'#202a30');d=ImageDraw.Draw(board);hashes={};endpoints={}
for gi,g in enumerate(images):
 images[g]['pickup'][0]=images[g]['work'][0].copy();cargo=C/f'frames/{g}/swim-carry-south/000.png';images[g]['pickup'][5]=Image.open(cargo).convert('RGBA');endpoints[g]=dict(cargo=cargo.relative_to(R).as_posix(),cargoSha256=sha(cargo))
 old=json.loads((R/f'character/dr-veld-v2/packs/{g}-256x256-p128.0-128.0/manifest.json').read_text());states=[]
 for ri,(role,key) in enumerate([('work','salvage-south'),('pickup','swim-pickup-south')]):
  state=next(s for s in old['states'] if s['id']==key).copy();files=[]
  for i,im in enumerate(images[g][role]):
   out=H/f'frames/{g}/{key}/{i:03}.png';out.parent.mkdir(parents=True,exist_ok=True);im.save(out);f=out.relative_to(H).as_posix();files.append(f);hashes[f]=sha(out)
   row=gi*2+ri;board.alpha_composite(im,(i*256,row*280+15));d.text((i*256+4,row*280+4),f'{g} {role} {i}',fill='white')
  state['frameFiles']=files;states.append(state)
 manifest=dict(name='Veld coherent south underwater work/pickup '+g,frameWidth=256,frameHeight=256,pivot=[128,128],standingHeight=148,textureFilter='linear',precomposed=True,status='staged_pending_controller_and_world_joins',states=states)
 (H/f'{g}-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
board.save(H/'paired-contact-v1.png')
(H/'fit-checks.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,frozenCargoFitSha256=sha(C/'fit-checks.json'),scale=scale,curves=curves,records=records,headMasterSha256=sha(masterpath),endpoints=endpoints,sourceHashes={p.name:sha(p) for p in [H/'work-source-v1.png',H/'pickup-source-v1.png']},frameHashes=hashes,scope='Authored extraction, unchanged frozen cargo ruler/grade, protected body, canvas clipping and exact endpoints; motion/controller/world separate'),indent=2)+'\n')
print(f'{checks} fit checks PASS;24paired work/pickup refs, exact joins and frozen cargo ruler {scale:.5f}.')
