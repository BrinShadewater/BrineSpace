"""One material curve and fixed atlas ruler; explicit rear-head registration."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
H=Path(__file__).resolve().parent;R=H.parents[1]
HEADS=[[90,80,172,161],[283,32,402,132],[755,53,981,237],[378,2,511,103]]
selection=json.loads((H/'source-selection-v1.json').read_text())['selected']
HEADS=[s.get('headBox',b) for s,b in zip(selection,HEADS)]
END_HEADS={'north':[117,107,138,123],'east':[127,102,163,130]}
def masks(a,box):
 v=a[:,:,:3].astype(float);head=np.zeros(a.shape[:2],bool);x,y,X,Y=box;head[max(0,y):Y,max(0,x):X]=True
 skin=head&(a[:,:,3]>200)&(v[:,:,0]>130)&(v[:,:,0]>v[:,:,1]*1.25)&(v[:,:,1]>v[:,:,2]*1.12)
 return dict(skin=skin,cloth=~head&(a[:,:,3]>200)&(np.ptp(v,axis=2)<22)&(v.mean(2)>20)&(v.mean(2)<130),patch=~head&(a[:,:,3]>200)&(v[:,:,2]>v[:,:,0]*1.2)&(v[:,:,2]>v[:,:,1]*1.3)&(v[:,:,2]>35)),head
raw=[Image.open(H/f'selected-crops/{i:03}.png').convert('RGBA') for i in range(4)]
ends={d:Image.open(R/f'character/veld-water-{d}-coherent-v1/frames/bare/swim-{d}/000.png').convert('RGBA') for d in ['north','east']}
values={k:[] for k in ['skin','cloth','patch']};targets={k:[] for k in values}
for im,b in zip(raw,HEADS):
 a=np.array(im);m,_=masks(a,b)
 for k in values:values[k].extend(a[:,:,:3][m[k]])
for d,im in ends.items():
 a=np.array(im);m,_=masks(a,END_HEADS[d])
 for k in values:targets[k].extend(a[:,:,:3][m[k]])
q=[0,15,35,55,75,90,100];curves={k:dict(knots=np.percentile(np.mean(values[k],axis=1),q).tolist(),targets=np.percentile(targets[k],q,axis=0).tolist()) for k in values}
if (H/'material-curve-master-v1.json').exists():curves=json.loads((H/'material-curve-master-v1.json').read_text())['curves']
graded=[];checks=0
for im,b in zip(raw,HEADS):
 a=np.array(im);before=a.copy();v=a[:,:,:3].astype(float);m,head=masks(a,b)
 for k,mask in m.items():
  for c in range(3):a[mask,c]=np.interp(v[mask].mean(1),curves[k]['knots'],np.array(curves[k]['targets'])[:,c]).clip(0,255).astype('uint8')
 union=m['skin']|m['cloth']|m['patch'];assert np.array_equal(before[~union],a[~union]);assert np.array_equal(before[:,:,3],a[:,:,3]);assert np.array_equal(before[head&~m['skin']],a[head&~m['skin']]);checks+=3;graded.append(Image.fromarray(a))
anchors={d:np.array([(b[0]+b[2])/2,(b[1]+b[3])/2]) for d,b in END_HEADS.items()}
board=Image.new('RGBA',(1536,4*280),'#202a30');draw=ImageDraw.Draw(board);records=[]
for row,scale in enumerate([.21,.22,.23,.24]):
 images=[ends['north']]
 for i,(im,b) in enumerate(zip(graded,HEADS)):
  pose_scale=scale*selection[i].get('fixedScale',.23)/.23;pose=im.resize((round(im.width*pose_scale),round(im.height*pose_scale)),Image.Resampling.LANCZOS);t=(i+1)/5;target=anchors['north']*(1-t)+anchors['east']*t
  center=np.array([(b[0]+b[2])/2,(b[1]+b[3])/2])*pose_scale;pos=np.rint(target-center).astype(int);out=Image.new('RGBA',(256,256));out.alpha_composite(pose,tuple(pos));images.append(out)
  if scale==.23:
   (H/'graded-trials').mkdir(exist_ok=True);out.save(H/f'graded-trials/{i:03}.png');records.append(dict(slot=i,scale=pose_scale,rawHeadBox=b,placement=pos.tolist(),headTarget=target.tolist(),nativePoseSize=list(pose.size)))
 images.append(ends['east'])
 for col,im in enumerate(images):board.alpha_composite(im,(col*256,row*280+24))
 draw.text((4,row*280+4),f'Fixed ruler {scale} — selected endpoints at left/right',fill='white')
board.save(H/'physical-grade-trials-v1.png')
(H/'material-fit-v1.json').write_text(json.dumps(dict(checks=checks,failures=0,curves=curves,records=records,rawHeadBoxes=HEADS,endpointHeadBoxes=END_HEADS,selectedScale=.23,scaleRule='Explicit per-source fixed rulers from selection (.23 atlas/.115 yaw54/.095 repaired near-east); skull/shoulder calibration, no silhouette-height normalization',registration='Explicit full head centers, because rear-facing skin may be absent; skin target from visible east master only',installed=False),indent=2)+'\n')
print(f'{checks} protected material/alpha checks PASS;4 fixed-ruler trials generated')
