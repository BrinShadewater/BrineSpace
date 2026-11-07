"""Package six coherent whole-pose edits, preserving native contract and alpha."""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/marsh-north-walk-family-detail-v1'
INV = ROOT / 'character/marsh-selected-normal-audit-2026-10-03-post-west-walk/inventory.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
d = json.loads(INV.read_text())
frozen = json.loads((OUT / 'references.json').read_text())
assert sha(INV) == frozen['inventory']['sha256']
for entry in [d['catalog'], *d['orderedBodyManifests']]:
    assert sha(ROOT / entry['path']) == entry['sha256']
originals, revised, records = [], [], []
for slot, entry in enumerate(d['states']['walk-north']['frames']):
    source = ROOT / entry['path']
    assert sha(source) == entry['sha256']
    old = Image.open(source).convert('RGBA')
    rawpath = OUT / f'phase-{slot:03}.raw.png'
    raw = Image.open(rawpath).convert('RGBA')
    assert raw.width == raw.height
    frame = raw.resize((184, 184), Image.Resampling.LANCZOS)
    path = OUT / f'{slot:03}.png'
    frame.save(path)
    a, b = np.asarray(old)[:, :, 3] >= 128, np.asarray(frame)[:, :, 3] >= 128
    bounds = lambda m: Image.fromarray(m.astype('uint8') * 255).getbbox()
    ob, bb = bounds(a), bounds(b)
    records.append({'slot': slot, 'original': entry, 'rawPath': rawpath.relative_to(ROOT).as_posix(),
        'rawSha256': sha(rawpath), 'rawCanvas': list(raw.size), 'frameSha256': sha(path),
        'framePath': path.relative_to(ROOT).as_posix(), 'originalOpaqueBounds': ob, 'opaqueBounds': bb,
        'heightRatio': (bb[3]-bb[1])/(ob[3]-ob[1]), 'crownDisplacement': bb[1]-ob[1],
        'soleDisplacement': bb[3]-ob[3], 'opaqueIoU': int((a & b).sum())/int((a | b).sum()),
        'method': 'Single whole-canvas184/raw-width resampling; original alpha preserved, no pose fit/pivot move/anatomy splice/recolour.',
        'reviewed': False, 'normalAdmission': False})
    originals.append(old)
    revised.append(frame)
board = Image.new('RGB', (6*184, 6*214), '#293b40')
draw = ImageDraw.Draw(board)
def place(im, col, row, label, pivot=(92, 172)):
    dx, dy = round(92-pivot[0]), round(172-pivot[1])
    board.paste(im, (col*184+dx, row*214+25+dy), im)
    draw.text((col*184+3, row*214+3), label, fill='white')
master = Image.open(ROOT / frozen['master']['path']).convert('RGBA')
master_rgb=np.asarray(master)[:,:,:3]
non_matte=~((master_rgb[:,:,0]>200)&(master_rgb[:,:,2]>200)&(master_rgb[:,:,1]<100))
master_bounds=Image.fromarray(non_matte.astype('uint8')*255).getbbox()
factor = 147/(master_bounds[3]-master_bounds[1])
master = master.resize((round(master.width*factor), round(master.height*factor)), Image.Resampling.LANCZOS)
board.paste(master, (31, 25+round(172-(master_bounds[3]-1)*factor)), master)
draw.text((3, 3), 'original master', fill='white')
idle = d['states']['idle-north']
place(Image.open(ROOT/idle['frames'][0]['path']).convert('RGBA'), 1, 0, 'own idle')
place(Image.open(ROOT/'character/marsh-v2/supplemental/east-walk-polish-v1/000.png').convert('RGBA'), 2, 0, 'selected East walk0')
for slot in range(6):
    place(originals[slot], slot, 1, f'current walk /{slot}')
    place(revised[slot], slot, 2, f'family revision /{slot}')
for row, key in enumerate(['walk-start-north', 'idle-north', 'run-north'], 3):
    state = d['states'][key]
    for slot, entry in enumerate(state['frames']):
        assert sha(ROOT/entry['path']) == entry['sha256']
        place(Image.open(ROOT/entry['path']).convert('RGBA'), slot, row, f'{key} /{slot}', state['pivot'])
board.save(OUT/'family-joins-native.png')
# Exact head neighborhoods for diagnosis only; never used as replacement art.
head = Image.new('RGB', (6*170, 3*110), '#293b40')
hd = ImageDraw.Draw(head)
for row, images in enumerate([originals, revised, [Image.open(ROOT/idle['frames'][0]['path']).convert('RGBA')]*6]):
    for slot, im in enumerate(images):
        crop = im.crop((50, 12, 135, 57)).resize((170, 90), Image.Resampling.NEAREST)
        head.paste(crop, (170*slot, 110*row+20), crop)
        hd.text((170*slot+3, 110*row+3), ['current', 'revision', 'ownidle'][row]+f' /{slot}', fill='white')
head.save(OUT/'heads-2x.png')
durations = d['states']['walk-north']['state']['frameDurationsMs']
# APNG review media with exact authored durations and no frame-bound fitting.
rgb = []
for im in revised:
    bg = Image.new('RGBA', (184,184), '#293b40');bg.alpha_composite(im);rgb.append(bg)
rgb[0].save(OUT/'walk-review.png', save_all=True, append_images=rgb[1:], duration=durations, loop=0, disposal=0, blend=0)
state = dict(d['states']['walk-north']['state'])
state['frameFiles'] = ['res://' + (OUT / f'{i:03}.png').relative_to(ROOT).as_posix() for i in range(6)]
(OUT/'manifest.json').write_text(json.dumps({'pivot':[92,172], 'standingHeight':148, 'states':[state]}, indent=2)+'\n')
(OUT/'review.json').write_text(json.dumps({'scope':'Six-phase whole-pose family study; normal selection unchanged; held/native-density/head review and APNG media do not establish native/cadence acceptance.',
    'records': records, 'durationsMs': durations, 'masterDisplayScale':factor,'masterForegroundDisplayBounds':master_bounds,'masterDisplayMethod':'Fixed147/sourceMasterForegroundHeight display ruler; magenta retained in unpainted reference, no candidate pose fitting.', 'normalAdmission':False,
    'boards':[{'path':p.relative_to(ROOT).as_posix(), 'sha256':sha(p), 'reviewed':False} for p in [OUT/'family-joins-native.png', OUT/'heads-2x.png']],
    'fullGoalComplete':False}, indent=2)+'\n')
print(json.dumps([{k:r[k] for k in ['slot','opaqueBounds','heightRatio','crownDisplacement','soleDisplacement','opaqueIoU']} for r in records]))
