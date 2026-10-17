from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,numpy as np,sys
version=int(sys.argv[1]) if len(sys.argv)>1 else 310
generation='8e41a5fa-d055-4fa5-98ac-1f0cd00e2dbd' if version==311 else '1a038c2d-4b33-4e30-8ac2-bd089c2247c3'
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/f'north-unload-bend-source-v{version}';d=json.loads((o/'inputs.json').read_bytes());sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(r/d['editTarget'])==d['editTargetSha256'] and sha(o/'prompt.txt')==d['promptSha256']
raw=Image.open(o/'raw.png').convert('RGBA');raw.resize((256,256),Image.Resampling.NEAREST).save(o/'fixed-canvas-source.png')
files=[r/d['precedingSource'],o/'fixed-canvas-source.png',r/'character/james-cargo-material-joined-v1/frames/bare/unload-north/002.png']
board=Image.new('RGB',(1152,440),(47,58,62));draw=ImageDraw.Draw(board);metrics=[]
for i,(f,label) in enumerate(zip(files,['preceding early bend309',f'new bend{version}','old unload2'])):
 im=Image.open(f).convert('RGBA');ys,xs=np.where(np.asarray(im)[:,:,3]>=128);bounds=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];metrics.append(dict(file=f.relative_to(r).as_posix(),sha256=sha(f),boundsAlpha128=bounds,heightAlpha128=bounds[3]-bounds[1]));scaled=im.resize((384,384),Image.Resampling.NEAREST);board.paste(scaled,(i*384,40),scaled);draw.text((i*384+8,8),label,fill='white');draw.text((i*384+8,420),str(bounds),fill='white')
board.save(o/'source-neighbor-review.png');(o/'source-measurements.json').write_text(json.dumps(dict(rawSize=raw.size,wholeCanvasNearestOnly=True,sources=metrics),indent=2)+'\n',encoding='utf-8')
(o/'generation.json').write_text(json.dumps(dict(tool='built-in imagegen',generationId=generation,originalFile=f'C:/Users/Alex/.codex/generated_images/01a0ef89-fc47-7e22-953f-3c02a051b0f6/exec-{generation}.png',rawSha256=sha(o/'raw.png'),promptSha256=sha(o/'prompt.txt')),indent=2)+'\n',encoding='utf-8');print(json.dumps(metrics))
