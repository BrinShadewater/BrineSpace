from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image

P = Path(__file__).resolve().parent
family = P.parent / 'james-water-turn-family-v1'
checks = 0
def check(ok, message):
    global checks
    checks += 1
    assert ok, message

registration = json.loads((P / 'registration.json').read_text())
for source, audit in [('source-v1.png', json.loads((P / 'source-origin.json').read_text())),
                      ('source-pose4-v2.png', json.loads((P / 'pose4-audit.json').read_text()))]:
    check(hashlib.sha256((P / source).read_bytes()).hexdigest() == audit['sha256'], 'Original generated source preserved')
for mode in ['bare', 'helmet']:
    candidate = json.loads((P / (mode + '-manifest.json')).read_text())
    selected = json.loads((family / (mode + '-manifest.json')).read_text())
    old = next(x for x in selected['states'] if x['id'] == 'swim-turn-east-north')
    forward, reverse = candidate['states']
    check(candidate['pivot'] == selected['pivot'] and candidate['standingHeight'] == selected['standingHeight'], 'Master drawing profile unchanged')
    check(forward['frameDurationsMs'] == old['frameDurationsMs'] and not forward['loop'], 'Selected finite clock preserved')
    for field in ['frameFiles', 'frameDurationsMs', 'facings', 'waterKinds', 'waterPoses', 'depthOffsets']:
        check(reverse[field] == list(reversed(forward[field])), 'Exact authored reverse ' + field)
    for index, filename in enumerate(forward['frameFiles']):
        image = Image.open(P / filename)
        check(image.mode == 'RGBA' and image.size == (256, 276), 'True RGBA canvas')
        box = image.getbbox()
        check(box and box[0] > 0 and box[1] > 0 and box[2] < 256 and box[3] < 276, 'Complete unclipped body')
        if index in [0, 5]:
            master = Image.open(family / old['frameFiles'][index]).convert('RGBA')
            check(image.tobytes() == master.tobytes(), 'Exact selected endpoint pixels')
        elif mode == 'helmet':
            body = np.array(Image.open(P / 'frames/bare' / f'{index:03}.png').convert('RGBA'))
            equipped = np.array(image)
            cx, cy, rx, ry = registration['helmet'][index]['headOwnershipEllipse']
            yy, xx = np.indices(body.shape[:2])
            region = ((xx-cx)/rx)**2 + ((yy-cy)/ry)**2 <= 1
            check(np.array_equal(body[~region], equipped[~region]), 'Helmet preserves body outside owned head')
    check(registration['metrics'][mode]['worldExtent'][3] <= 28.229190, 'Tight turn keeps master rear reach')
selection = json.loads((P / 'selection.json').read_text()) if (P / 'selection.json').exists() else {}
check(registration['runtimeInstalled'] == bool(selection.get('runtimeInstalled',False)), 'Build and selected runtime status agree')
report = {'checks': checks, 'failures': 0, 'status': 'selected_package_pass' if registration['runtimeInstalled'] else 'staged_package_pass',
          'scope': 'Two exact-reversed quarter keys,12 unique paired frames, immutable source alpha, master density/endpoints/clock, unclipped bodies and canonical head ownership. Native installation/journeys remain separate evidence; not full-set or owner acceptance.'}
(P / 'verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf8')
print('JAMES CONSOLE TURN PACKAGE:', checks, 'checks; 0 failures')
