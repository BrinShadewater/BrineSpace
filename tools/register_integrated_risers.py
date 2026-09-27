"""Register generated wall edits against their original opaque wall bounds."""
from pathlib import Path
import hashlib
import json
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'assets/room-risers-v4'
DEST = PACK / 'integrated-v1'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

base = json.loads((PACK / 'registrations.json').read_text())
registrations = json.loads((DEST / 'registrations.json').read_text())
subjects = json.loads((DEST / 'rollout-subjects.json').read_text())
for key, descriptions in subjects.items():
    path = DEST / 'masters' / f'{key}.png'
    im = Image.open(path)
    alpha = np.asarray(im.getchannel('A'))
    labels, _ = ndimage.label(alpha >= 128)
    counts = np.bincount(labels.ravel())
    counts[0] = 0
    ys, xs = np.where(labels == counts.argmax())
    box = [int(xs.min()), int(ys.min()), int(xs.max()+1), int(ys.max()+1)]
    old, face = base[key]['opaque_component_bounds'], base[key]['face']
    sx, sy = (box[2]-box[0])/(old[2]-old[0]), (box[3]-box[1])/(old[3]-old[1])
    mapped = [round(box[0]+(face[0]-old[0])*sx), round(box[1]+(face[1]-old[1])*sy), round(face[2]*sx), round(face[3]*sy)]
    registrations[key] = dict(source=f'res://assets/room-risers-v4/integrated-v1/masters/{key}.png', face=mapped,
        opaque_component_bounds=box, sha256=digest(path), prompt_sha256=digest(DEST/'prompts'/f'{key}.txt'),
        reference_sha256=digest(PACK/'masters'/f'{key}.png'), alpha_extrema=[int(alpha.min()),int(alpha.max())],
        native_size=list(im.size), subjects=descriptions)
overrides = DEST / 'polish-v2/registrations.json'
if overrides.exists():
    registrations.update(json.loads(overrides.read_text()))
latest = DEST / 'shape-helmet-v3/registrations.json'
if latest.exists():
    registrations.update(json.loads(latest.read_text()))
assert set(registrations) == set(base), 'Incomplete room collection'
for key, r in registrations.items():
    im = Image.open(ROOT / r['source'].removeprefix('res://'))
    x,y,w,h = r['face']
    assert 0 <= x < x+w <= im.width and 0 <= y < y+h <= im.height, key
    assert im.getchannel('A').getextrema() == (0,255), key
assert len({r['sha256'] for r in registrations.values()}) == len(base)
(DEST/'registrations.json').write_text(json.dumps(registrations, indent=2)+'\n')
(DEST/'registration-audit.json').write_text(json.dumps(dict(rooms=len(base), new_edits=len(subjects), valid_faces=True, unique_sources=True, transparent_rgba=True),indent=2)+'\n')
print(f'Registered {len(registrations)} rooms; {len(subjects)} new edits; all face bounds, alpha and source uniqueness checks passed.')
