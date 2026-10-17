"""One physical ruler/material curve; explicit rear head and case ownership."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rect(shape,b):
 m=np.zeros(shape,bool);x,y,X,Y=b;m[max(y,0):Y,max(x,0):X]=True;return m
def masks(a,hb,cb):
 v=a[:,:,:3].astype(float);head=rect(a.shape[:2],hb);case=rect(a.shape[:2],cb);body=~(head|case)&(a[:,:,3]>200)
 return dict(skin=head&~case&(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12),cloth=body&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),patch=body&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)),head,case
sem=json.loads((H/'semantic-landmarks.json').read_text(encoding='utf-8'));crops=[Image.open(H/f'source-crops/{i:03}.png').convert('RGBA') for i in range(4)]
ends={d:Image.open(R/f'character/veld-swim-carry-{d}-coherent-v1/frames/bare/swim-carry-{d}/000.png').convert('RGBA') for d in ['north','east']}
values={k:[] for k in ['skin','cloth','patch']};targets={k:[] for k in values}
for im,b,dest in [(im,b,values) for im,b in zip(crops,sem['raw'])]+[(ends[d],sem['endpoints'][d],targets) for d in ends]:
 a=np.array(im);mm,_,_=masks(a,b['head'],b['case'])
 for k in dest:dest[k].extend(a[:,:,:3][mm[k]])
q=[0,15,35,55,75,90,100];curves={k:dict(knots=np.percentile(np.mean(values[k],axis=1),q).tolist(),targets=np.percentile(targets[k],q,axis=0).tolist()) for k in values}
anchors={d:np.array([(b['head'][0]+b['head'][2])/2,(b['head'][1]+b['head'][3])/2]) for d,b in sem['endpoints'].items()};scale=sem['scale'];records=[];checks=0;frames=[ends['north']]
crop_records=json.loads((H/'crop-records.json').read_text())
for i,(im,b) in enumerate(zip(crops,sem['raw'])):
 a=np.array(im);before=a.copy();v=a[:,:,:3].astype(float);mm,head,case=masks(a,b['head'],b['case'])
 for k,mask in mm.items():
  for c in range(3):a[mask,c]=np.interp(v[mask].mean(1),curves[k]['knots'],np.array(curves[k]['targets'])[:,c]).clip(0,255).astype('uint8')
 union=mm['skin']|mm['cloth']|mm['patch'];assert np.array_equal(before[~union],a[~union]);assert np.array_equal(before[:,:,3],a[:,:,3]);assert np.array_equal(before[head&~mm['skin']],a[head&~mm['skin']]);assert np.array_equal(before[case],a[case]);checks+=4
 t=(i+1)/5;target=anchors['north']*(1-t)+anchors['east']*t;hb=b['head'];center=np.array([(hb[0]+hb[2])/2,(hb[1]+hb[3])/2])*scale;pos=np.rint(target-center).astype(int);pose=Image.fromarray(a).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);out=Image.new('RGBA',(256,256));out.alpha_composite(pose,tuple(pos));frames.append(out)
 records.append(dict(**crop_records[i],rawHeadBox=hb,rawCaseBox=b['case'],placement=pos.tolist(),headTarget=target.tolist(),scale=scale,nativePoseSize=list(pose.size)))
frames.append(ends['east']);old=json.loads((R/'character/dr-veld-v2/packs/bare-256x256-p128.0-128.0/manifest.json').read_text());states=[];hashes={}
for direction,row in [('north-east',frames),('east-north',list(reversed(frames)))]:
 state=next(s for s in old['states'] if s['id']=='swim-carry-turn-'+direction).copy();files=[]
 for i,im in enumerate(row):
  a=np.array(im);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1;f=f'frames/bare/{state["id"]}/{i:03}.png';(H/f).parent.mkdir(parents=True,exist_ok=True);im.save(H/f);files.append(f);hashes[f]=sha(H/f)
 state['frameFiles']=files;states.append(state)
m=dict(name='Veld cargo north/east turns bare',frameWidth=256,frameHeight=256,pivot=[128,128],standingHeight=148,textureFilter='linear',precomposed=True,status='staged_pending_native_motion_world_review',states=states)
(H/'bare-manifest.json').write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8');board=Image.new('RGBA',(1536,580),'#202a30');d=ImageDraw.Draw(board)
for i,im in enumerate(frames):
 board.alpha_composite(im,(i*256,20));board.alpha_composite(im.resize((142,142),Image.Resampling.BILINEAR),(i*256+57,320));d.text((i*256+4,4),str(i)+(' exact cargo master' if i in [0,5] else ' authored yaw'),fill='white')
board.save(H/'bare-contact-v1.png');(H/'bare-fit-v1.json').write_text(json.dumps(dict(checks=checks,failures=0,installed=False,scale=scale,records=records,curves=curves,frameHashes=hashes,sourceSha256=sha(H/sem['source']),endpointHashes={d:sha(R/f'character/veld-swim-carry-{d}-coherent-v1/frames/bare/swim-carry-{d}/000.png') for d in ends},scope='Explicit full-head/case ownership; uniform atlas ruler and grade; exact cargo endpoints; visual anatomy/yaw review separate'),indent=2)+'\n',encoding='utf-8');print(f'{checks} bodyfit checks PASS;12 bare refs staged')
