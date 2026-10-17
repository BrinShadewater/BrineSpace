from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json

p = Path(__file__).resolve().parent
root = p.parents[1]
sheet = Image.open(p / 'reference-sheet.png').convert('RGB')
board = Image.new('RGB', (650, 245), '#27333b')
d = ImageDraw.Draw(board)
d.text((14, 10), 'BRINE reference candidate / 148px body-height comparison', fill='white')
# Fixed source windows, one shared scale; grey remains visible: these are sheet crops, not sprites.
windows = [(65, 30, 395, 722), (432, 30, 619, 722), (630, 30, 942, 722), (991, 30, 1166, 722)]
scale = 148 / 682
for i, (label, box) in enumerate(zip(['Front', 'Left', 'Rear', 'Right'], windows)):
    crop = sheet.crop(box)
    small = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS)
    x = 30 + i * 112
    board.paste(small, (x + (85 - small.width) // 2, 47))
    d.text((x, 205), label, fill='white')
bill_path = root / 'character/major-bill-v3/frames/bare/idle-south/000.png'
bill = Image.open(bill_path).convert('RGBA')
board.paste(bill, (455, 24), bill)
d.text((487, 205), 'Bill selected', fill='white')
board.save(p / 'scale-review.png')
refs = ['character/brine-comms-v14/portrait.png', 'character/brine-face-v7-2026-09-26/clean-master.png', 'character/major-bill-v3/frames/bare/idle-south/000.png']
manifest = {'status': 'reference candidate; owner acceptance pending; not installed', 'references': {v: hashlib.sha256((root/v).read_bytes()).hexdigest() for v in refs}, 'outputs': {v: hashlib.sha256((p/v).read_bytes()).hexdigest() for v in ['source-v1.png', 'reference-sheet.png', 'scale-review.png', 'prompt.txt', 'revision-prompt.txt']}, 'review': 'Offline fixed-window crops, shared scale; opaque grey sheet background retained. 148px comparison is not engine-scale or room proof.', 'generation_sources': ['exec-de4a014d-9688-46f4-b6d8-bc610d8d1c73.png', 'exec-715aef4c-8672-4005-a082-ffaab662947c.png']}
(p / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
print('Saved reference candidate, scale comparison and reference/output hashes.')
