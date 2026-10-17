from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,sys
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/sys.argv[1];d=json.loads((o/'inputs.json').read_bytes());raw=Image.open(o/'raw.png').convert('RGBA');im=raw.resize((256,256),Image.Resampling.LANCZOS);im.save(o/'fixed-canvas-source.png');base=Image.open(r/d['sourceFile']).convert('RGBA');b=Image.new('RGBA',(768,280),(47,59,63,255));dr=ImageDraw.Draw(b);rows=[]
for i,(src,label) in enumerate([(base,'Original'),(im,'Candidate'),(Image.open(p/'arrival-turn-refine-v290/fixed-canvas-source.png').convert('RGBA'),'Midway reference')]):
 a=np.asarray(src);ys,xs=np.where(a[:,:,3]>=128);rows.append(dict(label=label,bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)],height=int(ys.max()-ys.min()+1)));b.alpha_composite(src,(i*256,24));dr.text((i*256+3,4),label,fill='white');dr.line((i*256,100,i*256+256,100),fill=(100,130,130,255));dr.line((i*256,248,i*256+256,248),fill=(100,130,130,255))
b.save(o/'source-review.png');(o/'registration-diagnostic.json').write_text(json.dumps(dict(rawSize=raw.size,rows=rows,bodyFitApplied=False,normalChanged=False),indent=2)+'\n');print(json.dumps(rows))
