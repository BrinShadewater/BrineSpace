"""One standing-source ruler for independent south seated anatomy audit."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
P=Path(__file__).resolve().parent;R=P.parents[1]
source=P/'sources/seated-v1.png';a=np.array(Image.open(source).convert('RGBA'))
master_path=R/'character/crew-runtime-matte-v1/veld/frames/idle-south-breathing-v1/000.png'
master=Image.new('RGBA',(256,256));master.alpha_composite(Image.open(master_path).convert('RGBA'),(36,52))
labs,n=label(a[:,:,3]>180);counts=np.bincount(labs.ravel());counts[0]=0
parts=[]
for k in np.argsort(counts)[-6:]:
 y,x=np.where(labs==k);parts.append((int(y.mean())//512,int(x.mean())//512,int(k)))
parts.sort();assert [(r,c) for r,c,k in parts]==[(r,c) for r in range(2) for c in range(3)]
y,x=np.where(labs==parts[0][2]);standing=int(y.max()-y.min()+1);ruler=148/standing
frames=[];records=[]
for slot,(_,_,k) in enumerate(parts):
 y,x=np.where(labs==k);floor=int(y.max());foot=float(x[y>=floor-8].mean())
 box=[int(x.min()-3),int(y.min()-3),int(x.max()+4),int(y.max()+4)]
 cut=a.copy();cut[~(binary_dilation(labs==k,iterations=3)&(a[:,:,3]>0))]=0
 crop=Image.fromarray(cut).crop(box);size=[round(crop.width*ruler),round(crop.height*ruler)]
 pos=[round(128-(foot-box[0])*ruler),round(223-(floor-box[1])*ruler)]
 frame=Image.new('RGBA',(256,256));frame.alpha_composite(crop.resize(size,Image.Resampling.LANCZOS),pos)
 path=P/f'diagnostic/{slot:03}.png';path.parent.mkdir(exist_ok=True);frame.save(path);frames.append(frame)
 records.append({'slot':slot,'rawBox':box,'sourceFloorY':floor,'sourceFootCenterX':foot,'position':pos,'size':size,'rawOpaqueHeight':int(y.max()-y.min()+1),'rawOpaqueWidth':int(x.max()-x.min()+1)})
board=Image.new('RGB',(1792,540),'#202a30');d=ImageDraw.Draw(board)
for col,frame in enumerate([master]+frames):
 board.paste(frame,(col*256,20),frame);d.text((col*256+5,3),'Selected south master' if col==0 else f'Raw south sit {col-1}',fill='white')
 detail=frame.crop((90,70,168,230)).resize((117,240),Image.Resampling.NEAREST);board.paste(detail,(col*256+68,280),detail)
board.save(P/'source-review.png')
report={'status':'independently authored ungraded source; not fitted/selected','executionId':'8c1af625-5f07-46ec-9b9d-d3f850b26f95','source':'sources/seated-v1.png','sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'master':str(master_path.relative_to(R)).replace('\\','/'),'masterSha256':hashlib.sha256(master_path.read_bytes()).hexdigest(),'fixedRuler':ruler,'standingOpaqueHeight':standing,'floorTarget':223,'pivot':[128,224],'frames':records,'pending':['anatomy/thigh projection and head review','pooled master material grade','exact standing/held/reverse joins','current south native helmet fit','source/motion/player/furniture/interruptions/Continue','normal selection and full-set polish']}
(P/'source-review.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'sourcePoses':6,'standingHeight':standing,'fixedRuler':ruler,'rawHeights':[r['rawOpaqueHeight'] for r in records],'nativeSizes':[r['size'] for r in records]}))
