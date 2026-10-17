from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json
import numpy as np

p=Path(__file__).resolve().parent
r=p.parents[1]
o=p/'north-unload-start-source-v309'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((o/'inputs.json').read_bytes())
assert all(sha(r/f)==h for f,h in inputs['referenceSha256'].items())
assert sha(o/'prompt.txt')==inputs['promptSha256']
raw=Image.open(o/'raw.png').convert('RGBA')
raw.resize((256,256),Image.Resampling.NEAREST).save(o/'fixed-canvas-source.png')
files=[r/inputs['sourceFile'],o/'fixed-canvas-source.png',r/inputs['destinationOriginalFile'],r/'character/james-cargo-material-joined-v1/frames/bare/unload-north/002.png']
labels=['exact turn end / unload0','new early bend309','old unload1','old unload2']
board=Image.new('RGB',(1536,460),(47,58,62));draw=ImageDraw.Draw(board)
metrics=[]
for i,(f,label) in enumerate(zip(files,labels)):
 im=Image.open(f).convert('RGBA');a=np.asarray(im)[:,:,3]
 ys,xs=np.where(a>=128);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
 metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),boundsAlpha128=bounds,heightAlpha128=bounds[3]-bounds[1]))
 board.paste(im.resize((384,384),Image.Resampling.NEAREST),(i*384,40),im.resize((384,384),Image.Resampling.NEAREST))
 draw.text((i*384+8,8),label,fill='white');draw.text((i*384+8,430),str(bounds),fill='white')
board.save(o/'source-neighbor-review.png')
(o/'source-measurements.json').write_text(json.dumps(dict(rawSize=raw.size,method='Whole raw canvas nearest resize once to256; no body fitting, translation or regrade.',sources=metrics),indent=2)+'\n',encoding='utf-8')
(o/'generation.json').write_text(json.dumps(dict(tool='built-in imagegen',generationId='a097fb4e-241f-4b81-a7a5-d9433d3fad02',originalFile='C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-a097fb4e-241f-4b81-a7a5-d9433d3fad02.png',rawSha256=sha(o/'raw.png'),promptSha256=sha(o/'prompt.txt')),indent=2)+'\n',encoding='utf-8')
print(json.dumps(metrics))
