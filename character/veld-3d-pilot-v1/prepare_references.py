"""Extract unchanged views from the owner-selected sheet for a 3D pilot."""
from pathlib import Path
from PIL import Image
import hashlib
import json

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / 'crew-turnarounds-v4' / 'veld-turnaround-01.png'
EXPECTED = '9ab9bf1811669363cb82064abb3cfd3d9f7bbc7d0ed366f0d61cc6fb3d5de838'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
im = Image.open(SOURCE)
assert im.size == (1536, 1024)
views = [('front', 145, 360), ('right', 510, 695),
         ('rear', 830, 1035), ('left', 1180, 1370)]
records = []
for state, top, bottom in [('bare', 50, 475), ('helmet', 505, 950)]:
    for direction, left, right in views:
        box = (left, top, right, bottom)
        crop = im.crop(box)
        out = ROOT / 'references' / f'{state}-{direction}.png'
        out.parent.mkdir(exist_ok=True)
        crop.save(out)
        records.append({'path': out.relative_to(ROOT).as_posix(), 'crop': box,
                        'sha256': hashlib.sha256(out.read_bytes()).hexdigest()})
(ROOT / 'references.json').write_text(json.dumps({
    'source': SOURCE.relative_to(ROOT.parent.parent).as_posix(),
    'source_sha256': EXPECTED,
    'method': 'Unscaled rectangular crops; source background retained; no generated pixels.',
    'views': records
}, indent=2) + '\n', encoding='utf-8')
print(f'Prepared {len(records)} unscaled reference crops; selected source hash matches.')
