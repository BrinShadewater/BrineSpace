from pathlib import Path
from PIL import Image
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
review=json.loads((P/'exit-review.json').read_text(encoding='utf-8'))
for gear in ['bare','helmet']:
 for current,previous in [(0,8),(7,0)]:
  a=Image.open(P/f'{gear}/frames/swim-land-north/{current:03}.png').convert('RGBA')
  b=Image.open(R/f'character/bill-land-water-north-v3/{gear}/frames/land-swim-north/{previous:03}.png').convert('RGBA')
  assert a.tobytes()==b.tobytes()
generations={'exit-atlas-v1.png':'exec-7f380377-ee3d-4b95-b7f3-b0883d796b75','rise-canvas-v1.png':'exec-8de45eae-e998-4cda-a88f-015f844c280b','near-stand-canvas-v1.png':'exec-7d028dcf-8961-41ab-be2a-84a14a642ffc','rise-canvas-v2.png':'exec-f34370fa-eb32-4b53-9457-01199c2adcdb','near-stand-canvas-v2.png':'exec-cfa56fce-4314-4202-b59d-8e6d11465933','near-stand-canvas-v3.png':'exec-036cf8e7-4cfa-4e2a-b301-12cea1d22970'}
for r in review['registrations']:r['generation']=generations[Path(r['source']).name]
review.update(generations=generations,sourceHashes={p.name:sha(p) for p in (P/'sources').glob('*') if p.is_file()},referenceHashes={f:sha(R/f) for f in ['character/bill-video-north-v5/master-source.png','character/bill-swim-north-coherent-v1/sources/swim-v1.png','character/bill-land-water-north-v1/sources/crouch-canvas-v2.png']},rejectedSingleSources={'rise-canvas-v1.png':'Native fixed-density body and head enlarged; replaced by crouch-only editV2.','near-stand-canvas-v1.png':'Projected stature and head enlarged despite master density; replaced.','near-stand-canvas-v2.png':'Still too tall and large-headed at retained density; replaced by master-only editV3.'},visualReview='Agent inspected full paired8pose board and all6bare/helmet neck fitting pairs. New exit arm retraction/palm support/knee planting/rise progression visible; canonical shell/collar joins connected in inspected poses. Final near-standing head component much closer to original master. Rising pose5 has slightly broader bare hair/head than final pose6; full master/body/grade continuity and chronological playback remain provisional.',browserMotionReview='Finite player generated; browser motion not exercised.',nativeAcceptance=False,normalSelected=False,endpointExactToSelectedSources=True)
(P/'exit-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
heading='Bill independently authored North water-exit source candidate — October 2, 2026'
body='''New character/bill-water-exit-north-v1 provides eight poses each bare/helmet,
500ms,320x352/p160224/H148: exact padded selected swim context, six new complete
exit articulations and exact padded selected idle. Elbow retract/palm push/knee
tuck-plant/half kneel/rising squat/near standing. Four selected atlas cells share
established North.25 anatomical density; two new single sources retain original
master148/976 density. Whole-figure crown translation for early floating poses;
opaque support224 for four planted/rising interiors is source registration only.
No reversed entry, per-pose height fitting, limb rotation or production selection.

Six generation raws/prompts retained with execution/reference/source hashes. Atlas
late rising cells rejected for shortened build at common head/equipment density.
First rise/near-standing singles enlarged head/body at fixed master density. Crouch-
only editV2 improves rising squat; near-standV2 still enlarged. Original-master-only
editV3 preserves much closer final head/build. Hair colour-component diagnostic
widths:master115,crouch126,riseV2 131,rejected nearV2 143,nearV3 117. These are
semantic-colour proxies, not complete head/torso/proportion acceptance. Pose5 bare
head remains slightly broader; continued master/grade/moving review required.

Six canonical40x34rear helmet fits scale1/rotation0 preserve body outside bounded
head mask, foreground and pixels from crown+25 exactly.16decodedAPNG frames and
all eight authored holds exact; four bare/helmet static endpoint images byte-exact
to selected NorthV3 contexts. Full paired board and all six close neck fitting
pairs inspected; collar/shell connected in inspected poses. Finite normal/quarter
source player generated, not browser-motion reviewed. No Godot/profile access in
this source turn; preceding North entry native proof does not cover this exit.

Lesson: an atlas can preserve head/hardware density while shortening near-standing
limbs. Repair through original-master pose authoring rather than fitting each body
to target bounding-box height. A pose-only reference can still influence identity;
when late rises drift, minimize references and make original master the sole edit
target. Keep rejected raws and compare registered whole bodies plus head/equipment
landmarks; colour-region measurements complement actual visual review.

Next chronological playback/master repair as needed, native North entry+exit
contact/clearance/guards/checkpoint/Continue; South bridges, normal admission/cargo
lifecycle and full-set cross-family polish remain. Full objective active/incomplete.
Review:character/bill-water-exit-north-v1/index.html.
'''
entry='## '+heading+'\n\n'+body+'\n'
for relative,prepend in [('docs/CURRENT_STATUS.md',True),('docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',True),('docs/ASSET_PIPELINE_AND_WORKFLOW.md',False),('docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',False),('skills/brinespace-character-pipeline/references/crew-consistency.md',False)]:
 f=R/relative;s=f.read_text(encoding='utf-8')
 if heading not in s:f.write_text(entry+s if prepend else s+'\n'+entry,encoding='utf-8')
f=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md');s=f.read_text(encoding='utf-8')
if heading not in s:f.write_text(s+'\n'+entry,encoding='utf-8')
(P/'HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: {R} · Task: Bill North water exit

## Objective and acceptance
Complete Bill's full set against masters, camera, proportions and matte grade;
then cross-family polish. This source candidate leaves the full goal active.

## Accepted decisions and constraints
Independently authored exit, static exact selected contexts, retained canonical
helmet. No per-pose bbox fit or mirrored/reversed entry. Native evidence separate.

## Current state
sources holds6raw generations/exact prompts; build.py, build_helmet.py,
build_review.py package8poses each gear and finite index.html. exit-review.json
tracks actual selected sources/hashes/rejections; measure_hair.py is diagnostic.

## Verification
16APNG frames/holds exact,4static endpoints exact,6protected canonical shell fits.
{review['visualReview']}
No browser-motion or native exit acceptance; no owner profile access here.

## Next action
Moving/master consistency review, then actual North entry/exit lifecycle and
checkpoint/Continue; South bridges, normal admission and complete-set polish.
''',encoding='utf-8')
print(json.dumps(dict(pairedFrames=16,exactEndpointImages=4,protectedFittings=6,guidanceFiles=6,goal='active/incomplete')))
