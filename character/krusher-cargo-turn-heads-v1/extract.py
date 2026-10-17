from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw
P=Path(__file__).resolve().parent;raw=Image.open(P/'generated-strip.png').convert('RGBA');a=np.array(raw);columns=(a[:,:,3]>128).sum(axis=0)>0;starts=np.flatnonzero(columns&~np.r_[False,columns[:-1]]);ends=np.flatnonzero(columns&~np.r_[columns[1:],False])+1;groups=[(int(x0),int(x1)) for x0,x1 in zip(starts,ends) if x1-x0>100];assert len(groups)==4
boxes=[]
for x0,x1 in groups:
 y,x=np.where(a[:,x0:x1,3]>128);boxes.append([x0,int(y.min()),x1,int(y.max()+1)])
scale=23/max(b[2]-b[0] for b in boxes);records=[]
board=Image.new('RGB',(900,260),'#242c31');d=ImageDraw.Draw(board)
for i,b in enumerate(boxes):
 im=raw.crop(b);native=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS);path=P/f'head-{i}.png';native.save(path);tile=native.resize((native.width*5,native.height*5),Image.Resampling.NEAREST);board.paste(tile,(i*210+25,35),tile);d.text((i*210+15,200),f'Turn view {i} / {native.width}x{native.height}',fill='white');records.append({'sourceBox':b,'file':path.name,'size':native.size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
board.save(P/'native-head-review.png');data={'rawSha256':hashlib.sha256((P/'generated-strip.png').read_bytes()).hexdigest(),'commonScale':scale,'referenceWidth':23,'records':records,'scope':'Authored front-right/front-left/rear-right/rear-left yaw heads. One common extraction ruler, no per-head normalization. Prompt degrees are requests, not measured camera angles; pose0 includes slight yaw. Fitted to cargo-family-v1.'};(P/'extraction.json').write_text(json.dumps(data,indent=2));print(json.dumps({'heads':4,'sizes':[r['size'] for r in records],'scale':scale}))
