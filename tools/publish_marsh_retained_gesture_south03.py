"""Freeze completed native player evidence without implying normal admission."""
from pathlib import Path
import hashlib
import json
import shutil
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
A = ROOT / 'output/marsh-animation-audit/retained-gesture-south03-2026-10-03'
O = ROOT / 'character/marsh-retained-gesture-material-v1/south03-unselected'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
owner = read(A / 'owner-before.json')
inputs = read(A / 'inputs-before.json')
assert owner == read(A / 'owner-after.json') and inputs == read(A / 'inputs-after.json')
assert (A / 'native-exit.txt').read_text().strip() == '0'
log = (A / 'native.log').read_text()
assert 'ERROR:' not in log and 'WARNING:' not in log and '0failures' in log
native = read(A / 'report.json')
assert native['checks'] == 190 and native['failures'] == 0 and native['playerRestores'] == 6
assert len(native['captures']) == 6 and len(native['samples']) == 52
for cap in native['captures']:
    path = A / cap['file']
    shutil.copy2(path, O / cap['file'])
    cap['sha256'] = sha(path)
boards = []
for page in range(2):
    board = Image.new('RGB', (2016, 490))
    for col, cap in enumerate(native['captures'][page*3:page*3+3]):
        im = Image.open(O / cap['file']).convert('RGB')
        assert im.size == (672, 490)
        board.paste(im, (672 * col, 0))
    path = O / f'native-contact-{page:02}.png'
    board.save(path)
    boards.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha(path), 'actuallyInspected': False,
                   'operations': 'Three full native captures side by side, no resize or crop.'})
native.update({'boards': boards, 'stableBoundedInputs': len(inputs), 'unchangedOwnerNonLogFiles': len(owner),
               'nativeScriptSha256': sha(ROOT / 'tools/review_marsh_retained_gesture_south03.gd'),
               'continuousMotionReviewed': False, 'normalAdmission': False})
report = read(O / 'verification.json')
report['nativeEvidence'] = native
(O / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'checks': native['checks'], 'failures': 0, 'samples': 52, 'playerRestores': 6, 'stableInputs': len(inputs), 'unchangedOwnerFiles': len(owner)}))
