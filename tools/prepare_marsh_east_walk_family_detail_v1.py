"""Freeze six whole-pose targets and common grade/identity/detail references."""
from pathlib import Path
import hashlib, json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'character/marsh-east-walk-family-detail-v1'
INV = ROOT / 'character/marsh-selected-normal-audit-2026-10-03-post-south-contact/inventory.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
d = json.loads(INV.read_text())
OUT.mkdir(exist_ok=True)
refs = []
targets = d['states']['walk-east']['frames']
assert len(targets) == 6
for slot, entry in enumerate(targets):
    source = ROOT / entry['path']
    assert sha(source) == entry['sha256']
    guide = OUT / f'target-{slot:03}-1024.png'
    im = Image.open(source).convert('RGBA')
    assert im.size == (184, 184)
    im.resize((1024, 1024), Image.Resampling.NEAREST).save(guide)
    refs.append({'slot': slot, 'source': entry, 'guide': guide.relative_to(ROOT).as_posix(), 'guideSha256': sha(guide)})
idle = d['states']['idle-east']['frames'][0]
source = ROOT / idle['path']
assert sha(source) == idle['sha256']
Image.open(source).convert('RGBA').resize((1024, 1024), Image.Resampling.NEAREST).save(OUT / 'own-idle-1024.png')
crop = ROOT / 'character/marsh-east-walk-detail-v1/master-collar-suit.png'
master = ROOT / 'character/marsh-motion-polish-v1/sources/east-standing-identity-01.png'
assert Image.open(master).crop((340, 375, 660, 805)).tobytes() == Image.open(crop).tobytes()
report = {'inventory': {'path': INV.relative_to(ROOT).as_posix(), 'sha256': sha(INV)}, 'targets': refs,
    'ownIdle': idle, 'idleGuideSha256': sha(OUT / 'own-idle-1024.png'),
    'master': {'path': master.relative_to(ROOT).as_posix(), 'sha256': sha(master)},
    'materialCrop': {'path': crop.relative_to(ROOT).as_posix(), 'sha256': sha(crop), 'sourceCrop': [340, 375, 660, 805]},
    'method': 'Whole184square targets/ownidle nearest-expanded to1024, no pose fitting; original unpainted material crop; current ownidle governs visible temple and shared grade.',
    'normalAdmission': False}
(OUT / 'references.json').write_text(json.dumps(report, indent=2) + '\n')
print('Six exact whole-pose targets and common master/ownidle references frozen')
