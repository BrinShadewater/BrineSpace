"""Retain four complete rear figures; support claims require visual review."""
from pathlib import Path
import hashlib, json, shutil
import numpy as np
from PIL import Image, ImageDraw
from rebuild_bill_art import binary

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'character/marsh-north-run-material-v1'
S = BASE / 'sources'
generation = 'exec-ef4d6379-f06c-4cdf-9858-33a62c898ded'
original = Path('C:/Users/Alex/.codex/generated_images/01a0fbf5-ac74-7c72-98e7-34736a220c96') / (generation + '.png')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

rp = S / 'contacts-02.request.json'
req = json.loads(rp.read_text())
assert sha(S / 'contacts-02.prompt.txt') == req['promptSha256']
for r in req['orderedReferences'] + req['sourceFrames']:
    assert sha(ROOT / r['path']) == r['sha256']
rawpath = S / 'contacts-02.raw.png'
shutil.copy2(original, rawpath)
req.update(status='Retained unselected: opposite contact arrangements, wrong passing support', generationId=generation, originalGeneratedPath=str(original), rawSha256=sha(rawpath))
rp.write_text(json.dumps(req, indent=2) + '\n')
raw = Image.open(rawpath).convert('RGBA')
a = np.array(raw)
xs = np.flatnonzero(np.sum(a[:, :, 3] >= 128, axis=0) >= 2)
groups = np.split(xs, np.flatnonzero(np.diff(xs) > 8) + 1)
assert len(groups) == 4, len(groups)
edges = [0] + [round((groups[i].max() + groups[i+1].min()) / 2) for i in range(3)] + [raw.width]
cuts = [(edges[i], 0, edges[i+1], raw.height) for i in range(4)]
cells = [binary(raw.crop(c)) for c in cuts]
nb = cells[-1].getbbox()
scale = 146 / (nb[3] - nb[1])
out = BASE / 'contacts-02-unselected'
out.mkdir(exist_ok=True)
names = ['left-contact.png', 'right-contact.png', 'wrong-left-support-passing.png', 'ruler.png']
records, frames = [], []
for i, c in enumerate(cells):
    dense = binary(c.resize((round(c.width * scale), round(c.height * scale)), Image.Resampling.BOX))
    b = dense.getbbox()
    offset = (92 - round((b[0] + b[2]) / 2), 172 - b[3])
    f = Image.new('RGBA', (184, 184))
    f.alpha_composite(dense, offset)
    assert np.count_nonzero(np.array(f)[:, :, 3]) == np.count_nonzero(np.array(dense)[:, :, 3])
    f.save(out / names[i])
    fb = f.getbbox()
    records.append({'file': names[i], 'sourceCell': cuts[i], 'wholeTranslation': offset, 'bounds': fb, 'size': [fb[2]-fb[0], fb[3]-fb[1]], 'sha256': sha(out/names[i])})
    frames.append(f)
recipe = {'normalAdmission': False, 'fullGoalComplete': False, 'commonNeutralScale': scale, 'neutralOccupiedTargetHeight': 146, 'rawSha256': sha(rawpath), 'records': records, 'operations': 'Four complete alpha128 cells, one neutral BOX scale, whole translation to bbox bottom172, no clipping, mirroring, patches, recolour or pose-specific fitting.', 'visualReview': 'Raw inspected: contact figures show opposite support arrangements. Figure3 is LEFT support / raised RIGHT sole, contradicting requested RIGHT passing. Figure1 raised sole extends below flat support boot; bbox alignment cannot certify contact. Packed comparison requires further review; no cycle admission.'}
(out / 'recipe.json').write_text(json.dumps(recipe, indent=2) + '\n')
guide = json.loads((S / 'guide-provenance.json').read_text())
idle = Image.open(ROOT / guide['primarySourceFrames'][0]['path']).convert('RGBA')
board = Image.new('RGB', (5*368, 440), '#293b40')
draw = ImageDraw.Draw(board)
for i, f in enumerate([idle] + frames):
    large = f.resize((368,368), Image.Resampling.NEAREST)
    board.paste(large, (i*368,50), large)
    draw.text((i*368+4,5), (['Selected North idle'] + names)[i], fill='white')
board.save(out / 'comparison.png')
print(json.dumps({'generationId': generation, 'scale': scale, 'sizes': [r['size'] for r in records], 'normalAdmission': False}))
