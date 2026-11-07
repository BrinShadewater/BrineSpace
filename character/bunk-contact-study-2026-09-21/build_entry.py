"""Staged Veld floor-to-bunk sequence, preserving exact idle/sleep endpoints."""
from pathlib import Path
import json
import hashlib
from PIL import Image

ROOT=Path(__file__).resolve().parent
PROJECT=ROOT.parent.parent
source=Image.open(ROOT/'veld-entry-source.png').convert('RGBA')
palette=Image.open(PROJECT/'character/dr-veld-v2/frames/bare/sleep-east/000.png').convert('RGB').quantize(colors=256)
out=ROOT/'veld-entry';out.mkdir(exist_ok=True)
idle=Image.open(PROJECT/'character/dr-veld-v2/frames/bare/idle-east/000.png').convert('RGBA')
canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(idle,(36,52));canvas.save(out/'000.png')
boxes=[(49,98,322,677),(610,182,932,676),(1105,221,1528,669)]
anchors=[(248,675),(865,670),(1265,510)]
targets=[(128,224),(128,224),(122,219)]
for i,(box,anchor,target) in enumerate(zip(boxes,anchors,targets),1):
    crop=source.crop(box)
    small=crop.resize(tuple(round(v*0.22) for v in crop.size),Image.Resampling.NEAREST)
    alpha=small.getchannel('A').point(lambda v:255 if v>=128 else 0)
    small=small.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');small.putalpha(alpha)
    frame=Image.new('RGBA',(256,256));frame.alpha_composite(small,tuple(round(target[j]-(anchor[j]-box[j])*0.22) for j in range(2)))
    frame.save(out/f'{i:03d}.png')
for i in range(3):(out/f'{i+4:03d}.png').write_bytes((ROOT/'veld-lowering'/f'{i:03d}.png').read_bytes())
durations=[120,240,300,300,300,300,280]
states=[]
for name,indices,holds in [('bunk-enter-east',list(range(7)),durations),('bunk-exit-east',list(reversed(range(7))),list(reversed(durations)))]:
    # Floor-supported entry poses draw in front; mattress-supported poses between layers.
    states.append({'id':name,'frameFiles':[f'{i:03d}.png' for i in indices],
        'furnitureFrames':['bunk' if i>=4 else '' for i in indices],
        'frameDurationsMs':holds,'loop':False,'depthOffsets':[96 if i<4 else 100 for i in indices]})
states.append({'id':'bunk-sleep-east','frameFiles':['006.png'],'frameDurationsMs':[1000],'loop':True,'furnitureFrames':['bunk'],'depthOffsets':[100]})
(out/'manifest.json').write_text(json.dumps({'canvas':[256,256],'pivot':[128,224],'standingHeight':148,'states':states},indent=2)+'\n')
(out/'recipe.json').write_text(json.dumps({'source_sha256':hashlib.sha256((ROOT/'veld-entry-source.png').read_bytes()).hexdigest(),
    'boxes':boxes,'anchors':anchors,'targets':targets,'scale':0.22,
    'reused':'exact canonical idle padded (36,52); three existing lowering frames',
    'omitted':'generated fourth entry pose replaced with selected lowering start',
    'scope':'staged 1.84-second entry/reversed exit; no runtime binding'},indent=2)+'\n')
