"""Reproducible, staged Branforth bunk poses; does not edit runtime catalogs."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent.parent
source = Image.open(ROOT / 'branforth-entry-source.png').convert('RGBA')
canonical = PROJECT / 'character/chief-engineer-branforth-v2/frames/bare'
palette = Image.open(canonical / 'sleep-east/000.png').convert('RGB').quantize(colors=256)
out = ROOT / 'branforth-entry'
out.mkdir(exist_ok=True)
idle = Image.open(canonical / 'idle-east/000.png').convert('RGBA')
frame = Image.new('RGBA', (256, 256))
frame.alpha_composite(idle, (36, 52))
frame.save(out / '000.png')
boxes = [(0, 0, 512, 540), (512, 0, 1024, 540), (1024, 0, 1536, 540),
         (0, 540, 512, 1024), (512, 540, 1024, 1024), (1024, 540, 1536, 1024)]
anchors = [(257, 498), (826, 503), (1201, 383), (239, 867), (761, 882), (1296, 895)]
targets = [(128, 224), (128, 224)] + [(122, 219)] * 4
scale = 0.30
for i, (box, anchor, target) in enumerate(zip(boxes, anchors, targets), 1):
    crop = source.crop(box)
    small = crop.resize(tuple(round(v * scale) for v in crop.size), Image.Resampling.NEAREST)
    alpha = small.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
    small = small.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
    small.putalpha(alpha)
    frame = Image.new('RGBA', (256, 256))
    frame.alpha_composite(small, tuple(round(target[j] - (anchor[j] - box[j]) * scale) for j in range(2)))
    frame.save(out / f'{i:03d}.png')
durations = [120, 240, 300, 300, 300, 300, 280]
states = []
for name, indices in [('bunk-enter-east', list(range(7))), ('bunk-exit-east', list(reversed(range(7))))]:
    states.append({'id': name, 'frameFiles': [f'{i:03d}.png' for i in indices],
                   'frameDurationsMs': [durations[i] for i in indices], 'loop': False,
                   'furnitureFrames': ['bunk' if i >= 4 else '' for i in indices],
                   'depthOffsets': [100 if i >= 4 else 96 for i in indices]})
states.append({'id': 'bunk-sleep-east', 'frameFiles': ['006.png'], 'frameDurationsMs': [1000],
               'loop': True, 'furnitureFrames': ['bunk'], 'depthOffsets': [100]})
(out / 'manifest.json').write_text(json.dumps({'canvas': [256, 256], 'pivot': [128, 224],
                                               'standingHeight': 148, 'states': states}, indent=2) + '\n')
(out / 'recipe.json').write_text(json.dumps({'source_sha256': hashlib.sha256((ROOT / 'branforth-entry-source.png').read_bytes()).hexdigest(),
    'boxes': boxes, 'anchors': anchors, 'targets': targets, 'scale': scale,
    'alpha': 'threshold 128', 'palette': 'canonical sleep-east 256 colors',
    'scope': 'staged contact study; equipment/controller not installed'}, indent=2) + '\n')
