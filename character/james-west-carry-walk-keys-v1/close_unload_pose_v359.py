import json
import subprocess
from pathlib import Path

from milestone_notes import record_guides

root = Path.cwd()
bank = root / 'character/james-west-carry-walk-keys-v1'
review = bank / 'north-unload-pose-v359'
inspection = json.loads((review / 'alpha-inspection.json').read_text())
source = json.loads((review / 'source-request.json').read_text())
old, new = inspection[0], inspection[2]
ratio = old['size'][0] / new['size'][0]
width_old = old['opaqueBounds'][2] - old['opaqueBounds'][0]
width_new = (new['opaqueBounds'][2] - new['opaqueBounds'][0]) * ratio
translation = old['opaqueBounds'][3] - new['opaqueBounds'][3] * ratio
height_delta = (new['opaqueBounds'][1] * ratio + translation) - old['opaqueBounds'][1]
rasters = [p.relative_to(root).as_posix() for p in review.glob('*.png')]
assert len(rasters) == 3
attrs = subprocess.run(['git', 'check-attr', '--stdin', '-z', 'filter'], input=('\0'.join(rasters) + '\0').encode(), capture_output=True, check=True).stdout.split(b'\0')
assert all(attrs[i] == b'lfs' for i in range(2, len(attrs) - 1, 3))
report = {'version': 359, 'selected': False, 'normalChanged': False, 'packageChanged': False, 'authoredPoses': 1, 'authoringMethod': source['method'], 'sourceSha256': source['outputSha256'], 'uniformCanvasScale': ratio, 'floorTranslationAt256px': translation, 'opaqueSilhouetteNarrowingPercent': round((1 - width_new / width_old) * 100, 2), 'crownLowerByPixelsAt256px': round(height_delta, 2), 'trueTransparency': True, 'sourceRgbaUnmodified': True, 'rasterLfs': 3, 'visualReview': 'Generated source and 148/82px browser comparisons viewed. Narrower supported crouch; belt wrench retained. Head, backpack, hardware and cloth drawing differ from selected source.', 'limits': 'Still study only. Canvas-derived uniform ruler plus rigid floor alignment, not a calibrated full sequence. Surrounding action joins, helmet fit, motion, contact with cargo and exact original-master identity/material remain unproven. Low-alpha fringe pixels retained in raw source.', 'next': 'If this polish is pursued, establish a coherent unloading source with matching carry/standing endpoints before changing any selected frame. Existing Windows package remains the tested deliverable.'}
(review / 'review.json').write_text(json.dumps(report, indent=2) + '\n')
section = f'''### James north unload stance study — October 4, 2026

V359 one new rear unload crouch key from built-in image_gen, using selected middle
crouch/carry, original West master and rear idle references. Exact prompt/reference
and output hashes saved in north-unload-pose-v359/source-request.json; raw1254px
RGBA retained without repainting, warping or alpha alteration. All three new rasters
covered by Git LFS. Generated source and148/82px comparisons actually viewed.

Opaque silhouette is {report['opaqueSilhouetteNarrowingPercent']}% narrower under
one canvas-derived uniform scale; rigid {translation:.2f}px floor alignment used
only for the viewer. Crown remains {height_delta:.2f}px lower than current crouch,
so this did not establish a shallower bend. Wrench remains on belt. Suit/backpack,
hardware and head detail differ; raw low-alpha fringe retained. One still is not a
coherent animation or original-master acceptance. No helmet counterpart, native
room test, source admission, selected runtime edits, rebuild or owner-save access.

UNSELECTED polish study; tested V351/V358 package retained. A coherent unloading
sequence with matching carry/standing endpoints is required before installation;
do not insert this single drawing into current motion and claim flashes solved.
Compare: character/james-west-carry-walk-keys-v1/north-unload-pose-v359/index.html.
'''
handoff = '''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James north unload polish

## Objective and acceptance
Continue James polish after packaging. One narrower-stance still study saved;
animation coherence and original-master consistency remain unproven.

## Accepted decisions and constraints
Existing tested selection retained. Forward cargo, belt wrench, matte graphite
and original master remain authorities. No standalone-frame promotion.

## Current state
New V359 raw source, exact request/hash records, alpha/geometry inspection,
148/82px comparison screenshots and local interactive viewer. No runtime edits.

## Verification
'''+section+'''
## Next action
Establish consistent unload motion before any installation; do not call this one
pose a completed animation. Existing V358 Windows ZIP remains the playable result.
'''
(review / 'HANDOFF.md').write_text(handoff)
record_guides(root, section, '### James Windows download packaged — October 4, 2026')
with (bank / 'HANDOFF.md').open('a', encoding='utf8') as stream:
    stream.write('\n' + section)
f = bank / 'material-repair-progress.json'
old_bytes = f.read_bytes()
ledger = json.loads(old_bytes)
ledger['northUnloadStanceStudy'] = report
assert f.read_bytes() == old_bytes
f.write_text(json.dumps(ledger, indent=2) + '\n')
print(json.dumps(report))
