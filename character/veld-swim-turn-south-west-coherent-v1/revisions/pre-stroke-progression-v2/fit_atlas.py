from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from material import masks,family_curves,grade
H=Path(__file__).resolve().parent;R=H.parents[1];curves=family_curves();refs={d:Image.open(R/f'character/veld-water-{d}-coherent-v1/frames/bare/swim-{d}/000.png').convert('RGBA') for d in ['south','west']};anchors={}
for d,ref in refs.items():
 _,fb,_=masks(np.array(ref));anchors[d]=np.array([(fb[0]+fb[2])/2,fb[3]])
board=Image.new('RGBA',(1536,840),'#202a30');draw=ImageDraw.Draw(board);records=[];checks=0
for row,scale in enumerate([.20,.21,.22]):
 board.alpha_composite(refs['south'],(0,row*280+24));board.alpha_composite(refs['west'],(1280,row*280+24))
 for i in [1,2,3]:
  raw=Image.open(H/f'source-crops/{i:03}.png').convert('RGBA');mapped,fb,m=grade(raw,curves);checks+=3;pose=mapped.resize((round(raw.width*scale),round(raw.height*scale)),Image.Resampling.LANCZOS);_,pfb,_=masks(np.array(pose));t=(i+1)/5;target=anchors['south']*(1-t)+anchors['west']*t;pos=np.rint(target-np.array([(pfb[0]+pfb[2])/2,pfb[3]])).astype(int);out=Image.new('RGBA',(256,256));out.alpha_composite(pose,tuple(pos));a=np.array(out);assert not np.any(np.concatenate([a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]])>20);checks+=1
  if scale==.21:
   p=H/f'graded-trials/{i:03}.png';p.parent.mkdir(exist_ok=True);out.save(p);records.append({'slot':i+1,'sourceSlot':i,'scale':scale,'nativeFaceBox':pfb,'position':pos.tolist(),'targetFaceAnchor':target.tolist()})
  board.alpha_composite(out,((i+1)*256,row*280+24));draw.text(((i+1)*256+4,row*280+4),f'source{i}; uniform {scale}',fill='white')
board.save(H/'physical-grade-trials-v1.png');(H/'material-fit-v1.json').write_text(json.dumps({'checks':checks,'failures':0,'curves':curves,'endpointFaceAnchors':{d:v.tolist() for d,v in anchors.items()},'records':records,'scaleHypothesis':.21,'status':'3 atlas angles mapped; corrected first source/helmet/clock still needed'},indent=2)+'\n');print(f'{checks} shared material/head/alpha/border checks PASS; registered after resampling')
