from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-north-v2';D=P/'browser-review'
e=json.loads((P/'entry-review.json').read_text());browser=json.loads((D/'review.json').read_text())
assert len(browser['cases'])==4 and all(x['terminalPose']==8 for x in browser['cases'])
exact=[]
for gear in ['bare','helmet']:
    m=json.loads((P/gear/'manifest.json').read_text());old_m=json.loads((OLD/gear/'manifest.json').read_text())
    for key in ['frameWidth','frameHeight','pivot','standingHeight']:assert m[key]==old_m[key]
    assert m['states'][0]['frameDurationsMs']==old_m['states'][0]['frameDurationsMs']
    m['states'][0]['provenance']='Eight NorthV2 frames exact. New bent-elbow push4 from targeted atlas edit, original shared density .25/head anchor160145. Torso below arms/belt/lower body from nativeY180 exact toV2. Source-only; native/master/full-motion acceptance pending.'
    (P/gear/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    for i in range(9):
        a=Image.open(P/f'{gear}/frames/land-swim-north/{i:03}.png').convert('RGBA');b=Image.open(OLD/f'{gear}/frames/land-swim-north/{i:03}.png').convert('RGBA')
        if i==4:
            assert a.tobytes()!=b.tobytes();assert np.array_equal(np.array(a)[180:],np.array(b)[180:])
        else:assert a.tobytes()==b.tobytes();exact.append(f'{gear}/{i}')
assert len(exact)==16 and e['decodedPairedAPNGFramesExact']==18
paths=['res://character/bill-land-water-north-v1/sources/crouch-canvas-v2.png',
       'res://character/bill-land-water-north-v1/sources/entry-atlas-v1.png',
       'res://character/bill-land-water-north-v1/sources/entry-atlas-v1.png',
       'res://character/bill-land-water-north-v3/sources/reach-atlas-v3.png',
       'res://character/bill-land-water-north-v2/sources/lift-atlas-v2.png',
       'res://character/bill-land-water-north-v1/sources/entry-atlas-v1.png',
       'res://character/bill-land-water-north-v1/sources/entry-atlas-v1.png']
for rec,path in zip(e['registrations'],paths):rec['source']=path
e['inheritedSourceHashes']=e.pop('sourceHashes',{})
e['sourceHashes']={path:hashlib.sha256((R/path.removeprefix('res://')).read_bytes()).hexdigest() for path in set(paths)}
e['otherEightFramesPerGearExact']=exact
e['protectedPose4BodyFromY']=180
e['visualReview']='Before/after reach plus deep-crouch/corrected-lift/master ruler inspected; new bent elbows bring glove tips nearer rear crown. Seven close neck fittings inspected. Four real browser playback cases reach8,82screen captures retained; sampled progressing board shows reduced hand-position overshoot through3→4. Colour/master/native-contact/full-speed temporal acceptance remains open.'
e['browserMotionReview']={'review':'browser-review/index.html','cases':browser['cases'],'screenshots':82,'scope':browser['captureScope'],'acceptance':'Sampled chronological hand reach improvement; not native contact, exact phase screenshot binding or complete temporal/master acceptance.'}
browser['visualReview']='Fixed-crop sampled advancing bare/helmet board inspected after corrected reach. Hands in4 now closer to crown and preceding crouch3 than former overhead stretch; shoulder/collar shell joins readable. Body build/matte palette broadly coherent in captured poses, endpoint grade/physical motion/full-speed temporal acceptance pending.'
(D/'review.json').write_text(json.dumps(browser,indent=2)+'\n')
(P/'entry-review.json').write_text(json.dumps(e,indent=2)+'\n')
note='''## Bill North intermediate reach repair and sampled replay — October 2, 2026

New sibling bill-land-water-north-v3 changes push-off4 only, bare/helmet, preserving
NorthV2 corrected axial lift. Targeted upper-right atlas edit exec-19342959-9ddd-
4f29-9e5c-d05e0d355ed0 saved with exact prompt. Bent elbows/glove tips nearer rear
crown bridge deep crouch to lift instead of full overhead stretch. Fixed source
density.25, actual crown1247/79 registered160/145. Original source torso below
articulated arms/belt/hips/legs/boots from nativeY180 copied exactly; no body scale,
per-pose width/height normalization or exposure compensation.

All16 unaffected bare/helmet frames byte-exact toV2; two changed push frames both
retain all pixels fromY180 down. Canvas320x352/p160224/H148,500ms and all holds
unchanged;18decoded APNG frames/durations exact. Original static endpoints exact.
Source provenance now names actual V1/V2/V3 raw paths rather than inherited local
filenames implying absent raw files. Before/after reach beside neighbours/master
ruler and complete neck fitting board inspected; connected helmet/collar fit.

Actual browser controls exercise both gears at normal/quarter speed; four cases
reach8.80advancing screens plus2paused idle captures retained; quarter AX labels
1..8both gears, sparse normal bare4/5/7/8 and helmet4/5/6/7/8. Fixed-crop progressing
board reviewed: hand-position overshoot reduced in captured3→4, original lower-body
motion retained. AX label precedes screenshot and can cross a hold boundary; no
exact source-phase pixel binding. Elapsed clock starts after click returns; no
browser-duration/native/all-frame temporal claim. No Godot/profile access.

Lesson: a chronological defect may need intermediate joint articulation rather
than slower timing or a whole-figure transform. Re-author only affected source
phase, protect established lower-body/context pixels, prove all unaffected exports
exact, then repeat the affected moving review. Material/detail continuity still
needs master/native evidence independent of playback functionality.

Next actual North entry/native contact/clearance/guards/checkpoint/Continue and
independently authored North exit. Full master/normal-endpoint grade remains open,
as do South bridges, West fidelity/endpoint polish, normal admission/cargo lifecycle
and full-set cross-family consistency. Goal active/incomplete; no commit/export.
Review:character/bill-land-water-north-v3/entry.html?v=reach-v3.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    f=R/rel;t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(note+t,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · Project: BrineSpace · Task: Bill North intermediate reach

## Objective and acceptance
Full original-master-consistent Bill set then cross-family polish. Incomplete.

## Accepted decisions and constraints
Fixed source density and anatomy, exact protected lower body/other poses, canonical
rear helmet. Static endpoint and browser evidence separate from native admission.

## Current state
Targeted reach raw/prompt, prepare/build/helmet/review/record scripts;18frames/
two manifests/APNGs, source and neck comparisons, finite player, entry-review.json.
82browser screens/playback/board/review, six guidance files updated. V1/V2 retained.

## Verification
16other frames exact toV2;2changed frames retain originalY180+pixels.
18decoded APNG frames/holds exact, unchanged500ms/profile. Neighbour/master-ruler
and neck boards reviewed. Four actual UI playback cases final8; quarter1..8
labels observed; normal samples sparse; advancing board inspected. No native proof.

## Next action
Actual North entry native/contact/clearance/cancel/save/Continue and independent
exit. Master/endpoint grade/full temporal acceptance, South bridges, West polish,
normal/cargo admission and full-family consistency remain. Goal active.
Preview tab5 deliverable. No running process, commit or export.
''',encoding='utf-8')
print(json.dumps({'changedFrames':2,'otherFramesExact':16,'protectedBodyFromY':180,'browserCases':4,'guidanceFiles':6}))
