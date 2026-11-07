"""Publish current selected-source native rest contact/save evidence, bounded scope."""
from pathlib import Path
import hashlib
import json
import re
import shutil
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'output/marsh-animation-audit/rest-contact-2026-10-03'
O = ROOT / 'character/marsh-rest-contact-review-2026-10-03'
O.mkdir(exist_ok=True)
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
owner = read(A / 'owner-before.json')
inputs = read(A / 'inputs-before.json')
inventory = read(ROOT / 'character/marsh-full-family-audit-2026-10-03/inventory.json')
results = {}
for kind, stamps, crop in [('bunk', [0, 200, 550, 800, 1100, 1400, 1700], (310, 390, 490, 570)),
                           ('berth', [0, 200, 550, 850, 1150, 1400], (450, 250, 630, 430))]:
    assert owner == read(A / f'owner-after-{kind}.json')
    assert inputs == read(A / f'inputs-after-{kind}.json')
    assert (A / f'{kind}-exit.txt').read_text().strip() == '0'
    log = (A / f'{kind}.log').read_text()
    assert 'ERROR:' not in log and 'WARNING:' not in log and '0 failures' in log
    checks = int(re.search(r'CONTACT CHECKS:\s+(\d+)', log)[1])
    frames = inventory['states']['bunk-enter-east' if kind == 'bunk' else 'berth-lie-east']['frames']
    captures = []
    for slot, stamp in enumerate(stamps):
        name = f'restore-bare-{stamp:04}.png' if kind == 'bunk' else f'restore-{stamp:04}.png'
        p = A / kind / name
        im = Image.open(p).convert('RGB')
        assert im.size == (1600, 900)
        assert sha(ROOT / frames[slot]['path']) == frames[slot]['sha256']
        target = O / f'{kind}-{name}'
        shutil.copy2(p, target)
        captures.append({'slot': slot, 'elapsedMs': stamp, 'fullNativeCapture': target.relative_to(ROOT).as_posix(),
                         'fullNativeSha256': sha(target), 'selectedSource': frames[slot]})
    boards = []
    for page, start in enumerate(range(0, len(stamps), 4)):
        group = captures[start:start + 4]
        board = Image.new('RGB', (360 * len(group), 390), '#293b40')
        draw = ImageDraw.Draw(board)
        for col, cap in enumerate(group):
            native = Image.open(ROOT / cap['fullNativeCapture']).convert('RGB')
            board.paste(native.crop(crop).resize((360, 360), Image.Resampling.NEAREST), (col * 360, 30))
            draw.text((col * 360 + 4, 5), f'{kind} / slot{cap["slot"]} / {cap["elapsedMs"]}ms / restored', fill='white')
        p = O / f'{kind}-contact-{page:02}.png'
        board.save(p)
        boards.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'crop': crop,
                       'operations': 'Whole room contact crop enlarged uniformly2x nearest; original full native capture retained.',
                       'actuallyInspected': False})
    results[kind] = {'checks': checks, 'failures': 0, 'exitCode': 0, 'errors': 0, 'warnings': 0,
                     'captures': captures, 'boards': boards, 'diskRestores': len(captures),
                     'scope': 'Normal chooser/path arrival at authored currentq3 bunk, seven disk restores/pause/reverse interruption/completion/powerloss/lowbattery/invalid snapshots.' if kind == 'bunk' else 'Isolated legacyq0 berth compatibility arrival, six disk restores/pause/reverse interruption/completion/powerloss/lowbattery/invalid snapshots; no normal berth admission.'}
report = {'results': results, 'stableBoundedInputs': len(inputs), 'unchangedOwnerNonLogFiles': len(owner),
          'inventorySha256': sha(ROOT / 'character/marsh-full-family-audit-2026-10-03/inventory.json'),
          'restSourceVisualReview': 'character/marsh-full-family-audit-2026-10-03/rest-family-static-review-2026-10-03.json',
          'limits': 'Thirteen actual restored native contact poses and full disk saves for the specified profiles. No continuously watched entry/exit, title Continue, all rotations, owner layouts or full set acceptance.',
          'normalAdmissionChanged': False, 'fullGoalComplete': False}
(O / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'bunkChecks': results['bunk']['checks'], 'berthChecks': results['berth']['checks'],
                  'diskRestores': 13, 'stableBoundedInputs': len(inputs), 'unchangedOwnerNonLogFiles': len(owner)}))
