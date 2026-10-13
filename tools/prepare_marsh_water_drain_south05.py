"""Whole-source South rise repair with unchanged exact master/endpoints."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / 'character/marsh-water-transition-material-v1/sources'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
r = json.loads((S / 'drain-south-04.request.json').read_text())
refs = [ROOT / r['orderedReferences'][0]['path'], S / 'drain-south-04.raw.png']
prompt = '''Edit target: the second attached five-sprite transparent sheet. First attachment is PRIMARY exact current artwork authority: slim empty standing South master LEFT, loaded South swimmer CENTRE, dry carry RIGHT, enlarged together 3x without independent fitting. Preserve identity and muted matte ivory/sage/slate material from that FIRST authority. Repair the full coherent five-pose South rise sheet, with four cargo rise stages and empty standing neutral LAST. Preserve FIVE separated complete organic sprites with generous transparent gutters, no text/background/shadows/water.
Specific changes: make every upright body match the first attachment's slim shoulders, narrow hips, small adult head and slender suit limbs. The previous sheet's neutral is too broad. Do not increase the head, shoulders or thighs to a heroic stocky build. Exact neutral has width58 to height147 (ratio .395). Keep the same physical head/case size in every pose, viewerLEFT anatomicalRIGHT temple implant, sandy hair, harness/pouches, dark gloves, two ivory case FRONT latches. Keep the camera 35 degrees above the floor, with identical heading straight South and no yaw.
Pose1 LEFT: preserve the previous sheet's useful prone-to-rise pose and extended viewerLEFT leg UP above the head, viewerRIGHT folded knee; gently lift chest. Its complete height should be106 units when neutral height is147, width75. Preserve case against lowest chest and connected adult limbs.
Pose2: replace the low squashed kneel. It must be a HIGH kneeling rise, torso nearly upright, hips above knees and both adult thighs visible under the case. Chest and case have risen clear of the knees; head now higher. One shin projects toward viewer with boot under hip, the other knee contacts the floor beside it. Complete projected height115 units, not81. Keep shoulders/case/head the same physical sizes as pose1; no tiny squat. Rise via connected legs and hips, not case sliding through abdomen.
Pose3: near-standing half-kneel, torso fully upright, pelvis lifted higher than pose2, one straight supporting leg with FLAT boot at floor, other knee slightly bent with sole arriving at same floor level. Projected height135 units, not117; show full adult connected thighs/calves. Same slim body and held case.
Pose4: fully standing planted cargo hold, both flat soles same floor level, no stride or raised knee. Slim own-master torso and legs, height147, naturally wider forearms around the unchanged case at lower chest. Pose5 LAST: exact slim relaxed empty first-attachment standing master, width58 height147, both flat soles, hands relaxed at sides. Its shape is the SCALE RULER; do not reinterpret or broaden it.
One uniform physical body scale across all five drawings. Pose heights106/115/135/147/147 are projection/leg-flexion targets, never per-pose resize instructions. Improve whole poses, not isolated pasted limbs, head patches, mirroring, recolour or oversharpening. Match FIRST authority's restraint, suit construction, face and crisp small-scale sprite details. Preserve full limbs and complete alpha. No extra body parts, backpack or helmet.'''
(S / 'drain-south-05.prompt.txt').write_text(prompt, encoding='utf-8')
r.update(status='frozen before whole05 high-kneel/slim-neutral edit', promptSha256=sha(S / 'drain-south-05.prompt.txt'),
         orderedReferences=[{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
                             'role': 'primary exact current master/endpoints' if i == 0 else 'whole edit target; identity subordinate to primary'}
                            for i, p in enumerate(refs)])
for k in ['generationId', 'originalGeneratedPath', 'rawSha256']:
    r.pop(k, None)
(S / 'drain-south-05.request.json').write_text(json.dumps(r, indent=2) + '\n')
print('South05 whole-source edit prompt/reference hashes frozen.')
