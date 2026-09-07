"""Arrange native Godot depth crops without scaling or altering their pixels."""
import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument('source', type=Path)
parser.add_argument('--quarter', type=int, choices=range(4), required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
target = args.output.resolve()
if not target.is_relative_to(root / 'output') or target.exists():
    raise SystemExit('Use a new PNG within output/')
manifest = json.loads((args.source / 'depth-review.json').read_text())
records = [p for p in manifest['poses'] if p['quarter'] == args.quarter]
ids = sorted({p['index'] for p in records})
if not ids or len(records) != len(ids) * 2:
    raise SystemExit('Expected front and behind for every registered prop')
images = {p['detail']: Image.open(args.source / p['detail']).convert('RGB') for p in records}
width = max(i.width for i in images.values()) + 16
height = max(i.height for i in images.values()) + 34
sheet = Image.new('RGB', (width * len(ids), height * 2), '#142029')
draw = ImageDraw.Draw(sheet)
for p in records:
    x = ids.index(p['index']) * width + 8
    y = (0 if p['pose'] == 'behind' else 1) * height + 26
    sheet.paste(images[p['detail']], (x, y))
    draw.text((x, y - 20), f"q{args.quarter} {p['prop']} / {p['pose']}", fill='#e4e9eb')
sheet.save(target)
