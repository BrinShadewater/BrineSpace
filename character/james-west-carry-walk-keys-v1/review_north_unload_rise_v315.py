from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'north-unload-rise-source-v315';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();d=json.loads((o/'inputs.json').read_bytes());assert all(sha(r/f)==h for f,h in d['references'].items());assert sha(o/'prompt.txt')==d['promptSha256']
Image.open(o/'raw.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST).save(o/'fixed-canvas-source.png');files=[p/'north-unload-low-source-v314/fixed-canvas-source.png',o/'fixed-canvas-source.png',r/d['originalTarget']];board=Image.new('RGB',(1152,440),(47,58,62));draw=ImageDraw.Draw(board);metrics=[]
for i,(f,label) in enumerate(zip(files,['preceding low pose314','new rise315','old rise4'])):
 im=Image.open(f).convert('RGBA');ys,xs=np.where(np.asarray(im)[:,:,3]>=128);b=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),boundsAlpha128=b));scaled=im.resize((384,384),Image.Resampling.NEAREST);board.paste(scaled,(i*384,40),scaled);draw.text((i*384+8,8),label,fill='white');draw.text((i*384+8,420),str(b),fill='white')
board.save(o/'source-neighbor-review.png');(o/'source-measurements.json').write_text(json.dumps(metrics,indent=2)+'\n',encoding='utf-8');(o/'generation.json').write_text(json.dumps(dict(tool='built-in imagegen',generationId='04b8208d-93e2-44b4-bc99-dc7620bfd37c',rawSha256=sha(o/'raw.png')),indent=2)+'\n',encoding='utf-8');print(json.dumps(metrics))
