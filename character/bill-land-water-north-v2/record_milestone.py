from pathlib import Path
from PIL import Image
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-north-v1'
e=json.loads((P/'entry-review.json').read_text())
exact=[]
for gear in ['bare','helmet']:
    a=json.loads((P/gear/'manifest.json').read_text());b=json.loads((OLD/gear/'manifest.json').read_text())
    for field in ['frameWidth','frameHeight','pivot','standingHeight']:assert a[field]==b[field]
    assert a['states'][0]['frameDurationsMs']==b['states'][0]['frameDurationsMs']
    for i in range(9):
        current=Image.open(P/f'{gear}/frames/land-swim-north/{i:03}.png').convert('RGBA')
        previous=Image.open(OLD/f'{gear}/frames/land-swim-north/{i:03}.png').convert('RGBA')
        if i==5:assert current.tobytes()!=previous.tobytes()
        else:assert current.tobytes()==previous.tobytes();exact.append(f'{gear}/{i}')
assert len(exact)==16 and e['decodedPairedAPNGFramesExact']==18
e['otherEightFramesPerGearExact']=exact
e['visualReview']='Revised lift inspected beside old lift, preceding push, following near-prone and selected idle ruler. Axial head/backpack/hip chain and paired trailing boots straighter; original fixed source scale .25 and head anchor169 retained. Corrected neck board inspected after semantic hair-region registration. No continuous motion/native contact/full-master-grade acceptance inferred.'
e['crownCorrection']='Initial loose warm-color region selected cuff hardware309/558 rather than rear hair. Rebuilt using observed semantic hair bounds; actual source crown275/590. Earlier wrong fitting was not accepted despite protected-body assertions. Full physical source scale remains .25.'
(P/'entry-review.json').write_text(json.dumps(e,indent=2)+'\n')
note='''## Bill North axial lift source repair — October 2, 2026

New sibling bill-land-water-north-v2 changes only lift pose5, bare/helmet, of the
nine-pose500ms source candidate. Targeted atlas edit exec-923168a1-d880-4777-9f60-
5c30e92d20ad retained immediately with exact prompt. Extract only lower-left cell;
preserve all other source poses from V1, independent of generator changes elsewhere.
Fixed source-atlas density.25; whole-figure rear crown registered to160/169, no
per-pose scale/stature/width fitting or rigid rotation. Anatomically straighter
rear-head/backpack/pelvis chain and paired trailing boots inspected in before/after
neighbour/master-ruler comparison. Canonical rear helmet fitting rebuilt.

All16 other bare/equipped frame images byte-exact to V1; both changed pose5 images
different. Shared canvas320x352/p160224/H148 and all authored holds unchanged;
all18 APNG frames/durations decode exact. Seven protected-body/foreground shell
fittings retained. Close neck board inspected after crown correction: initial loose
warm-color search chose cuff highlight309/558 and visibly misplaced helmet despite
body-protection assertions. Restrict to observed semantic hair bounds; source rear
crown275/590, connected aligned helmet/collar in corrected inspected pose. No source
grade adjustment, normal-bank change, Godot/profile access, native admission or export.

Lesson: warm hardware can satisfy a hair-color predicate. Constrain registration
to the actual observed anatomical region, and inspect component fit afterward.
Protected pixels outside a head mask do not prove the mask or anchor is correct.
For a targeted atlas edit, copy only the revised cell and prove all unaffected
exported frames exact rather than trusting a preserve-other-poses prompt.

Full-speed/quarter-speed motion and normal-endpoint/master grade remain pending;
player generated, not browser-playback verified. North independent exit, real
entry contact/clearance/guards/save/Continue, South bridges, West endpoint polish,
normal admission/cargo lifecycle and entire cross-family polish remain.
Full Bill goal active/incomplete. Review:character/bill-land-water-north-v2/entry.html.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    f=R/rel;t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(note+t,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · Project: BrineSpace · Task: Bill North axial lift source repair

## Objective and acceptance
Complete original-master-consistent Bill set, then cross-family polish. Open.

## Accepted decisions and constraints
Independent rear source, fixed anatomical drawing density, canonical native helmet.
No per-pose height/width fit; unchanged source poses and original V1 preserved.

## Current state
Targeted raw atlas/prompt; build.py, helmet/review builders, record_milestone.py;
18frame exports/two manifests/two APNGs, lift before/after and neck/paired boards,
finite paired player/entry-review.json. Six guidance files updated.

## Verification
Only pose5 changes;16 other bare/helmet images exact;18decoded APNG frames/holds exact.
Canvas/pivot/height/500ms unchanged. Neighbour/master-ruler comparison and corrected
neck board reviewed. False cuff-crown corrected to observed source hair275/590.
No browser continuous motion, native contact/clearance/checkpoint or production admission.

## Next action
Moving source/master/endpoint-grade review and actual North native bridge test;
independent North exit and South transitions. Full-set/cargo/admission/polish remain.
No running process, commit or export; goal active/incomplete.
''',encoding='utf-8')
print(json.dumps({'changedFrames':2,'unchangedFramesExact':16,'decodedAPNGExact':18,'guidanceFiles':6}))
