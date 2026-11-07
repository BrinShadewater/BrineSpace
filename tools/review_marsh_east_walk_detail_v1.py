"""Fixed whole-canvas candidate review with complete walking neighborhood."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/marsh-east-walk-detail-v1'
INV = ROOT / 'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json'
d = json.loads(INV.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
walk = d['states']['walk-east']
idle = d['states']['idle-east']['frames'][0]
target = walk['frames'][3]
references = [idle, *walk['frames']]
for entry in references:
    assert sha(ROOT / entry['path']) == entry['sha256'], entry['path']
old = Image.open(ROOT / target['path']).convert('RGBA')
mask = lambda im: np.asarray(im)[:, :, 3] >= 128
bounds = lambda im: Image.fromarray(mask(im).astype('uint8') * 255).getbbox()
ob = bounds(old)
candidates = []
records = []
for number in ['01', '02']:
    rawpath = OUT / f'candidate-{number}.raw.png'
    if not rawpath.exists():
        continue
    raw = Image.open(rawpath).convert('RGBA')
    assert raw.width == raw.height
    frame = raw.resize((184, 184), Image.Resampling.LANCZOS)
    path = OUT / f'candidate-{number}-frame.png'
    frame.save(path)
    bb = bounds(frame)
    a, b = mask(old), mask(frame)
    records.append({'candidate': number, 'rawPath': rawpath.relative_to(ROOT).as_posix(),
        'rawSha256': sha(rawpath), 'rawCanvas': list(raw.size), 'framePath': path.relative_to(ROOT).as_posix(),
        'frameSha256': sha(path), 'fixedWholeCanvasFactor': 184 / raw.width,
        'opaqueBounds': bb, 'originalOpaqueBounds': ob,
        'heightRatio': (bb[3] - bb[1]) / (ob[3] - ob[1]), 'crownDisplacement': bb[1] - ob[1],
        'soleDisplacement': bb[3] - ob[3], 'opaqueIoU': int((a & b).sum()) / int((a | b).sum()),
        'normalAdmission': False, 'reviewed': False})
    candidates.append((number, frame))
board = Image.new('RGB', (8 * 184, 3 * 214), '#293b40')
draw = ImageDraw.Draw(board)
def place(im, col, row, label):
    board.paste(im, (col * 184, row * 214 + 25), im)
    draw.text((col * 184 + 3, row * 214 + 3), label, fill='white')
masterpath = ROOT / 'character/marsh-motion-polish-v1/sources/east-standing-identity-01.png'
master = Image.open(masterpath).convert('RGBA')
factor = 147 / 1232
master = master.resize((round(master.width * factor), round(master.height * factor)), Image.Resampling.LANCZOS)
board.paste(master, (31, 25 + round(172 - 1393 * factor)), master)
draw.text((3, 3), 'original material master', fill='white')
place(Image.open(ROOT / idle['path']).convert('RGBA'), 1, 0, 'current own idle')
place(old, 2, 0, 'selected walking /3')
for col, (number, frame) in enumerate(candidates, 3):
    place(frame, col, 0, 'candidate' + number)
for slot, entry in enumerate(walk['frames']):
    im = Image.open(ROOT / entry['path']).convert('RGBA')
    place(im, slot, 1, f'current walk /{slot}')
    revised = candidates[-1][1] if slot == 3 else im
    place(revised, slot, 2, f'provisional walk /{slot}')
board.save(OUT / 'whole-neighborhood.png')
board.resize((2944, 1284), Image.Resampling.NEAREST).save(OUT / 'whole-neighborhood-2x.png')
report = {'scope': 'Whole-pose and all six walking neighbors at fixed native density; no native/motion acceptance.',
    'references': references, 'masterPath': masterpath.relative_to(ROOT).as_posix(), 'masterSha256': sha(masterpath),
    'masterDisplayScale': factor, 'candidates': records, 'normalArtChanged': False, 'fullGoalComplete': False}
(OUT / 'comparison.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps([{k: r[k] for k in ['candidate', 'opaqueBounds', 'heightRatio', 'crownDisplacement', 'soleDisplacement', 'opaqueIoU']} for r in records]))
