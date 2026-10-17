from pathlib import Path
from PIL import Image, ImageDraw
import hashlib,json
import numpy as np

p=Path(__file__).resolve().parent
r=p.parents[1]
o=p/'arrival-turn-chronology-v295'
o.mkdir(exist_ok=True)
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
old=r/'character/james-cargo-turn-north-west-v1/frames/bare/carry-turn-west-north'
files=[old/'000.png',p/'arrival-turn-pose1-v292/fixed-canvas-source.png',p/'arrival-turn-pose2-v293/fixed-canvas-source.png',p/'arrival-turn-refine-v290/fixed-canvas-source.png',p/'arrival-turn-pose4-v294/fixed-canvas-source.png',old/'005.png']
endpoints=[p/'thigh-construction-phase0-v244/bare-head-protected.png',r/'character/james-cargo-material-joined-v1/frames/bare/unload-north/000.png']
labels=['Latest carry0','Old turn0','New turn1','New turn2','New turn3','New turn4','Old turn5','North unload0']
sequence=[endpoints[0]]+files+[endpoints[1]]
board=Image.new('RGBA',(2048,560),(47,59,63,255));d=ImageDraw.Draw(board)
rows=[]
for i,(f,label) in enumerate(zip(sequence,labels)):
 im=Image.open(f).convert('RGBA');board.alpha_composite(im,(i*256,24));d.text((i*256+3,4),label,fill='white')
 original=(old/f'{i-1:03}.png') if 1<=i<=6 else f
 board.alpha_composite(Image.open(original).convert('RGBA'),(i*256,304));d.text((i*256+3,284),'Original turn' if 1<=i<=6 else label,fill='white')
 for y in (100,248,380,528):d.line((i*256,y,i*256+255,y),fill=(100,130,130,255))
 a=np.asarray(im);ys,xs=np.where(a[:,:,3]>=128)
 rows.append(dict(label=label,file=f.relative_to(r).as_posix(),sha256=sha(f),bounds128=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]))
board.save(o/'chronology-review.png')
# Crops are diagnostic only; all source registration above remains unmodified.
detail=Image.new('RGBA',(1536,608),(47,59,63,255));dd=ImageDraw.Draw(detail)
for i,f in enumerate(files):
 im=Image.open(f).convert('RGBA');dd.text((i*256+3,4),f'Turn {i}',fill='white')
 detail.alpha_composite(im.crop((85,70,170,120)).resize((255,150),Image.Resampling.NEAREST),(i*256,24))
 detail.alpha_composite(im.crop((85,115,170,175)).resize((255,180),Image.Resampling.NEAREST),(i*256,204))
 detail.alpha_composite(im.crop((85,175,170,225)).resize((255,150),Image.Resampling.NEAREST),(i*256,414))
detail.save(o/'equipment-head-feet-review.png')
frames=[Image.open(f).convert('RGBA') for f in files]
clocks=[100,140,160,160,140,100]
frames[0].save(o/'bare-turn-study.apng',save_all=True,append_images=frames[1:],duration=clocks,loop=0,disposal=0,blend=0)
decoded=Image.open(o/'bare-turn-study.apng')
for i,src in enumerate(frames):
 decoded.seek(i);assert np.array_equal(np.asarray(decoded.convert('RGBA')),np.asarray(src))
(o/'inputs.json').write_text(json.dumps(dict(sources=rows,clockMs=clocks,decodedFramesExact=6,normalChanged=False,sourceAcceptance=False,scope='Bare provisional source chronology; unchanged old turn endpoints are deliberately visible, not exact new walk/unload joins.'),indent=2)+'\n')
print(json.dumps(dict(rows=rows,decodedExact=6,output=str(o))))
