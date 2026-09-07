"""Arrange native diagnostic crops; never rescale or change source art."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument('source', type=Path)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
target = args.output.resolve()
if not target.is_relative_to(root / 'output') or target.exists():
    raise SystemExit('Use a new output PNG within output/')
record = json.loads((args.source / 'edge-review.json').read_text())
scale = record.get('world_scale')
if isinstance(scale, bool) or not isinstance(scale, (int, float)) or not 0 < scale < float('inf'):
    raise SystemExit('Invalid capture world scale')
if record.get('state') != 'offline':
    raise SystemExit('Expected offline diagnostic captures')
rows = record['renders']
identities = list(dict.fromkeys(r['prop'] for r in rows))
if len(rows) != 2 * len(identities) or not identities:
    raise SystemExit('Expected two backgrounds per prop')
images = {}
crop_bounds = {}
for row in rows:
    path = (args.source / row['file']).resolve()
    if not path.is_relative_to(args.source.resolve()):
        raise SystemExit('Capture path must stay within source directory')
    if hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256']:
        raise SystemExit('Capture hash mismatch')
    image = Image.open(path).convert('RGB')
    x, y, w, h = row['crop']
    if any(type(v) is not int for v in (x, y, w, h)):
        raise SystemExit('Diagnostic crop must use integer pixels')
    if min(x, y) < 0 or w <= 0 or h <= 0 or x+w > image.width or y+h > image.height:
        raise SystemExit('Invalid diagnostic crop')
    key = (row['prop'], row['background'])
    if key in images:
        raise SystemExit('Duplicate prop/background')
    images[key] = image.crop((x, y, x+w, y+h))
    crop_bounds[key] = row['crop']
for identity in identities:
    if any((identity, bg) not in images for bg in ['dark', 'light']):
        raise SystemExit('Missing contrast background')
    if crop_bounds[(identity, 'dark')] != crop_bounds[(identity, 'light')]:
        raise SystemExit('Contrast pair must use identical crop bounds')
width = max(i.width for i in images.values()) + 16
height = max(i.height for i in images.values()) + 34
sheet = Image.new('RGB', (width * len(identities), height * 2), '#142029')
draw = ImageDraw.Draw(sheet)
for col, identity in enumerate(identities):
    for row, bg in enumerate(['dark', 'light']):
        x, y = col*width+8, row*height+26
        sheet.paste(images[(identity, bg)], (x, y))
        draw.text((x, y-20), f'{identity} / {bg} / native {scale:g}x', fill='#e4e9eb')
sheet.save(target)
print(f'EDGE REVIEW SHEET: {len(images)} hash-checked native crops; {target}')
