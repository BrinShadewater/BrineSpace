from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent.parent
note='''## Bill West master fabric and badge source corrections — October 2, 2026

New unselected bill-land-water-west-v3 repairs crouch/push materials against the
original master RIGHT left-facing figure. Built-in imagegen edits retained at
V1sources/crouch-canvas-v4.png and push-canvas-v3.png with exact prompts/hashes;
generations exec-2c5760c3-9a86-44e2-83f3-ca31153cd4ed and
exec-23fd84d8-f757-4075-8d82-f3f87cd535f2. Less blue-green graphite, more quilted
fabric/worn metal detail; gear emblem replaced by master square/ring shoulder
badge. Requested colour-only edits also regenerated face/hair/silhouette pixels.
Do not claim exact anatomical preservation from edit wording.

Actual1254square→320wholecanvas scale; crouch sole239 wholeposeY-15→224, push0.
Painted support preserved, no per-pose height fit. Alpha180 old/new silhouette
IoU0.968831crouch and0.940906push are diagnostics, not anatomy acceptance. Common
master148 board/V2-V3 and native4x detail/neck crops reviewed: compact two-hand
poses retained, fabric/badge closer to master. Metals brighter and subtle face/
hair changes remain. Other three intermediate poses and normal walking/equipped
endpoint material/detail differences still need comparative polish.

Seven bare/helmet poses500ms per gear; fourteen decoded APNG frames/holds exact.
Canonical40x40West shell native scale1/rotation0, five protected body/foreground
fits. New crouch/push crown anchors148114/140117 account for source movement.
Ten other paired V2frames remain RGBA exact. All16V2 bank inputs from completed
native proof still match; original staged runtime and2987-check evidence unchanged.
That proof covers V2, not changed V3. New source bank native/motion/Continue pending.
Seven alpha160 figures have one substantial component; does not prove anatomy.
No new Godot or owner profile writes, normal source selection or gameplay changes.

Reproducible prepare/build/material-review/helmet/finalize/review-page scripts,
source manifests/frames/APNGs, provenance/diagnostics and comparison boards saved.
Review:character/bill-land-water-west-v3/index.html. Full goal active/incomplete.
Lesson: neutral palette alone does not restore quilted material or the right
insignia. Cross-reference original suit construction, inspect at shared native
density, track generated silhouette/face changes and re-register canonical helmet.
Next arm-ready/lift/near-prone material/detail, actual continuous motion/new-bank
native bridge proof, independent West exit/checkpoint/Continue, remaining cardinal
bridges/cargo lifecycle and full Bill master/style/perspective/size/height/
proportion/colour cross-family polish.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 p=R/rel;t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(note+t,encoding='utf-8')
for p in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 t=p.read_text(encoding='utf-8')
 if heading not in t:p.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · BrineSpace · Bill West master material/detail candidate

## Objective and acceptance
Complete full master-consistent Bill animation set, then cross-family polish.
V3 two-pose detail repair leaves complete objective active/incomplete.

## Accepted decisions and constraints
Original West is right master figure facing left. Shared148 anatomy ruler,
320/p160224; wholecanvas scaling/semantic dry contact, native canonical helmet.
Preserve V2 source and native evidence; changed banks need fresh runtime proof.

## Current state
New V3 bare/helmet seven-pose500ms source trial. Raw crouch-v4/push-v3 edits and
prompts under V1sources. Build/material/helmet/review scripts, provenance/IoU,
master and texture comparisons, interactive paired page. Six guidance files updated.

## Verification
14decoded APNG frames/holds exact, ten V2paired poses exact; all16frozen V2source
inputs stable. Wholecanvas scale, no clipping; five head-fit body protections and
seven connected silhouettes. Original/master/common ruler/material/neck boards
reviewed. Neutral quilting/badges improved, brighter metal and generated face
differences remain. No new native/Godot/profile writes or normal admission.

## Next action
Finish other three intermediate material/detail corrections; review actual motion
and new-source native bridge. Independent West exit/checkpoint/Continue, remaining
cardinal transitions/cargo lifecycle and full Bill fidelity/polish remain.
''',encoding='utf-8')
print('Recorded two master material/detail corrections and remaining family scope; six guidance files updated.')
