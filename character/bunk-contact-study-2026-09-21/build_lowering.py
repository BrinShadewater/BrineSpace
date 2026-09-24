"""Staged Veld lowering clip, hip-registered; not bound to runtime catalog."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
source = Image.open(ROOT / 'veld-lowering-source.png').convert('RGBA')
canonical = Image.open(PROJECT / 'character/dr-veld-v2/frames/bare/sleep-east/000.png').convert('RGBA')
palette = canonical.convert('RGB').quantize(colors=256)
boxes = [(151,257,642,562),(798,333,1379,561),(1490,373,2080,564)]
hips = [(371,542),(1118,541),(1820,546)]
scale = 0.22
target = (122,219)
out = ROOT / 'veld-lowering'
out.mkdir(exist_ok=True)
for i,(box,hip) in enumerate(zip(boxes,hips)):
    crop = source.crop(box)
    small = crop.resize(tuple(round(v*scale) for v in crop.size),Image.Resampling.NEAREST)
    alpha = small.getchannel('A').point(lambda v:255 if v>=128 else 0)
    small = small.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
    small.putalpha(alpha)
    paste = tuple(round(target[j]-(hip[j]-box[j])*scale) for j in range(2))
    frame = Image.new('RGBA',(256,256))
    frame.alpha_composite(small,paste)
    frame.save(out/f'{i:03d}.png')
states=[]
for name,indices,durations,loop in [('bunk-lower-east',[0,1,2],[300,300,300],False),('bunk-rise-east',[2,1,0],[300,300,300],False),('bunk-sleep-east',[2],[1000],True)]:
    states.append({'id':name,'frameFiles':[f'{i:03d}.png' for i in indices],
        'furniture':'bunk','frameDurationsMs':durations,'loop':loop,'depthOffsets':[100]*len(indices)})
(out/'manifest.json').write_text(json.dumps({'canvas':[256,256],'pivot':[128,224],
    'standingHeight':148,'states':states},indent=2)+'\n')
(out/'recipe.json').write_text(json.dumps({'source_sha256':hashlib.sha256((ROOT/'veld-lowering-source.png').read_bytes()).hexdigest(),
    'boxes':boxes,'hips':hips,'scale':scale,'target_hip':target,
    'derivations':'rise reverses lowering; sleep reuses final sheet pose',
    'scope':'staged torso lowering only; no floor arrival or controller integration'},indent=2)+'\n')
