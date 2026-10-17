"""Fixed neutral-pose ruler diagnostic, no runtime or accepted-source writes."""
from pathlib import Path
import json, hashlib, sys
import numpy as np
from scipy.ndimage import label, binary_dilation
from PIL import Image, ImageDraw
P=Path(__file__).resolve().parent
R=P.parents[1]
version=sys.argv[1] if len(sys.argv)>1 else 'v1'
source=P/f'sources/breathing-{version}.png'
reference=R/'character/veld-seated-north-coherent-v1/frames/bare/sit-down-north/005.png'
a=np.array(Image.open(source).convert('RGBA'))
ref=Image.open(reference).convert('RGBA'); ra=np.array(ref)
labs,n=label(a[:,:,3]>180); sizes=np.bincount(labs.ravel());sizes[0]=0
parts=[]
for k in np.argsort(sizes)[-6:]:
 y,x=np.where(labs==k);parts.append((int(y.mean())//512,int(x.mean())//512,int(k)))
parts.sort()
assert [(r,c) for r,c,k in parts]==[(r,c) for r in range(2) for c in range(3)],parts
ry,rx=np.where(ra[:,:,3]>180)
y,x=np.where(labs==parts[0][2])
ruler=(ry.max()-ry.min()+1)/(y.max()-y.min()+1) if version=='v1' else json.loads((P.parent/'veld-seated-north-coherent-v1/source-scale-review.json').read_text())['fixedRuler']
floor_target=int(ry.max());foot_target=float(rx[ry>=ry.max()-2].mean())
board=Image.new('RGB',(1792,570),'#202a30');d=ImageDraw.Draw(board)
frames=[];records=[]
for slot,(_,_,k) in enumerate(parts):
 y,x=np.where(labs==k);floor=int(y.max());foot=float(x[y>=floor-8].mean())
 box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
 cut=a.copy();cut[~(binary_dilation(labs==k,iterations=3)&(a[:,:,3]>0))]=0
 crop=Image.fromarray(cut).crop(box);size=[round(crop.width*ruler),round(crop.height*ruler)]
 pos=[round(foot_target-(foot-box[0])*ruler),round(floor_target-(floor-box[1])*ruler)]
 frame=Image.new('RGBA',(256,256));frame.alpha_composite(crop.resize(size,Image.Resampling.LANCZOS),pos)
 out=P/f'diagnostic-{version}/{slot:03}.png';out.parent.mkdir(exist_ok=True);frame.save(out);frames.append(frame)
 records.append({'slot':slot,'rawBox':box,'position':pos,'size':size,'rawOpaqueHeight':int(y.max()-y.min()+1),'rawFoot':foot})
for col,frame in enumerate([ref]+frames):
 board.paste(frame,(col*256,20),frame);d.text((col*256+5,3),'Current seated' if col==0 else f'Raw breathing {col-1}',fill='white')
 crop=frame.crop((90,110,166,227)).resize((152,234),Image.Resampling.NEAREST);board.paste(crop,(col*256+50,285),crop)
board.save(P/f'source-review-{version}.png')
frames[0].save(P/f'diagnostic-{version}.gif',save_all=True,append_images=frames[1:],duration=500,loop=0,disposal=2)
report={'status':'ungraded source diagnostic; unselected','executionId':'2f93fb17-d644-4d9e-8a15-7723baa1d11c' if version=='v1' else '9677c71e-4ca4-4bb0-b8e3-1292f95709ce','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'referenceSha256':hashlib.sha256(reference.read_bytes()).hexdigest(),'fixedNeutralRuler':float(ruler),'nativeNeutralOpaqueHeight':int(ry.max()-ry.min()+1),'floorTarget':floor_target,'footTarget':foot_target,'frames':records,'limitations':['new complete figures alter protected head/equipment/lower-body pixels','not certified breathing or seamless source joins','no native/runtime selection change']}
(P/f'source-review-{version}.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'poses':6,'ruler':float(ruler),'rawHeights':[v['rawOpaqueHeight'] for v in records],'status':report['status']}))
