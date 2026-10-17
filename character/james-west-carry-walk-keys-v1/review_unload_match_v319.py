from pathlib import Path
from PIL import Image, ImageDraw
import json, hashlib
import numpy as np
p=Path(__file__).resolve().parent; r=p.parents[1]; o=p/'north-unload-return-match-v319'
sha=lambda f: hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((o/'inputs.json').read_bytes())
assert all(sha(r/f)==h for f,h in d['references'].items())
assert sha(o/'prompt.txt')==d['promptSha256']
raw=Image.open(o/'raw.png').convert('RGBA')
raw.resize((256,256),Image.Resampling.NEAREST).save(o/'fixed-canvas-source.png')
files=[p/'north-unload-low-source-v314/fixed-canvas-source.png',p/'north-unload-return-source-v316/fixed-canvas-source.png',o/'fixed-canvas-source.png',p/'north-unload-rise-between-v317/fixed-canvas-source.png',r/'character/james-cargo-material-joined-v1/frames/bare/unload-north/004.png']
labels=['previous bend314','current return316','trial319','next rise317','original return4']
board=Image.new('RGB',(1280,440),(47,58,62)); draw=ImageDraw.Draw(board); metrics=[]
for i,(f,label) in enumerate(zip(files,labels)):
 im=Image.open(f).convert('RGBA'); ys,xs=np.where(np.asarray(im)[:,:,3]>=128)
 b=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),boundsAlpha128=b))
 board.paste(im,(i*256,100),im); draw.text((i*256+8,10),label,fill='white'); draw.text((i*256+8,380),str(b),fill='white')
board.save(o/'source-neighbor-review.png')
(o/'source-measurements.json').write_text(json.dumps(dict(rawSize=raw.size,wholeCanvasNearestOnly=True,sources=metrics),indent=2)+'\n',encoding='utf-8')
(o/'generation.json').write_text(json.dumps(dict(tool='built-in imagegen',generationId='032152a1-c5ae-4e3d-96b2-37ca142ce3e2',rawSha256=sha(o/'raw.png')),indent=2)+'\n',encoding='utf-8')
print(json.dumps(metrics))
