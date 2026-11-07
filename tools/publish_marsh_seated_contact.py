"""Publish bounded staged seated contact evidence and exact renderer source parity."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'output/marsh-animation-audit/seated-contact-2026-10-03'
O = ROOT / 'character/marsh-seated-contact-review-2026-10-03'
O.mkdir(exist_ok=True)
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
owner = read(A / 'owner-before.json')
inputs = read(A / 'inputs-before.json')
assert owner == read(A / 'owner-after.json')
assert inputs == read(A / 'inputs-after.json')
assert (A / 'native-exit.txt').read_text().strip() == '0'
log = (A / 'native.log').read_text()
assert 'ERROR:' not in log and 'WARNING:' not in log and '0 failures' in log
report = read(A / 'captures/report.json')
assert report['checks'] == 276 and report['failures'] == 0
assert len(report['captures']) == 84 and report['facings'] == ['north', 'south']
invpath = ROOT / 'character/marsh-full-family-audit-2026-10-03/inventory.json'
inventory = read(invpath)
groups = {}
for cap in report['captures']:
    source = inventory['states'][cap['key']]['frames'][cap['slot']]
    original = ROOT / source['path']
    assert sha(original) == source['sha256']
    actual = A / 'captures' / cap['sourceFile']
    expected_image = Image.open(original).convert('RGBA')
    actual_image = Image.open(actual).convert('RGBA')
    assert actual_image.size == expected_image.size
    assert actual_image.tobytes() == expected_image.tobytes()
    for name in [cap['file'], cap['sourceFile']]:
        shutil.copy2(A / 'captures' / name, O / name)
    cap['nativeSha256'] = sha(O / cap['file'])
    cap['actualSourceSha256'] = sha(O / cap['sourceFile'])
    cap['selectedSource'] = source
    groups.setdefault((cap['room'], cap['rotation']), []).append(cap)
boards = []
for (room, rotation), caps in groups.items():
    # Design viewport1920x1080 is displayed at1600x900. One fixed crop per group.
    xs = [c['canvasPosition'][0] / 1.2 for c in caps]
    ys = [c['canvasPosition'][1] / 1.2 for c in caps]
    cx, cy = round((min(xs) + max(xs)) / 2), round((min(ys) + max(ys)) / 2)
    crop = (cx - 100, cy - 150, cx + 100, cy + 50)
    board = Image.new('RGB', (1200, 3 * 330), '#293b40')
    draw = ImageDraw.Draw(board)
    for i, cap in enumerate(caps):
        im = Image.open(O / cap['file']).convert('RGB')
        assert im.size == (1600, 900)
        x, y = (i % 4) * 300, (i // 4) * 330
        board.paste(im.crop(crop).resize((300, 300), Image.Resampling.NEAREST), (x, y + 30))
        draw.text((x + 4, y + 5), f"{cap['key']} / {cap['slot']}", fill='white')
    path = O / f'{room}-q{rotation}-contact.png'
    board.save(path)
    boards.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path),
                   'crop': crop, 'operations': 'Fixed native context crop per room/rotation; uniform1.5x nearest. Full native captures retained.',
                   'actuallyInspected': False})
report.update({'boards': boards, 'exactSourceMatches': 84,
               'stableBoundedInputs': len(inputs), 'unchangedOwnerNonLogFiles': len(owner),
               'inventorySha256': sha(invpath), 'fullGoalComplete': False,
               'continuousPlaybackReviewed': False, 'autonomousArrivalVerified': False})
(O / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: report[k] for k in ['checks', 'failures', 'exactSourceMatches', 'facings', 'stableBoundedInputs', 'unchangedOwnerNonLogFiles']}))
