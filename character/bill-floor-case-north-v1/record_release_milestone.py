"""Record completed release evidence without rewriting prior accepted milestones."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
unit=json.loads((R/'output/bill-floor-case-release-v1/validation.json').read_text())
world=json.loads((R/'output/bill-floor-case-release-world-v1/validation.json').read_text())
cont=json.loads((R/'output/bill-floor-case-release-continue-v1/validation.json').read_text())
assert unit['passed'] and world['passed'] and cont['passed']
rec=json.loads((R/'output/bill-floor-case-release-continue-v1/records.json').read_text())
assert rec['failures']==0 and len(rec['records'])==8
note=f'''## Bill staged source-bound cargo release — October 2, 2026

Reviewed all28 original North unload sources. Ground contact starts at source5;
source8/.36seconds starts rising after the lowest crouch and is the inferred
staged release cue. release_state.gd requires exact canonical cue RGBA, matching
active plan/gear/clock/displayed source, valid service and dry/live North unload.
release_workshop.gd separates room ownership from visibility: suppress standalone
case only while the actual source embeds it at the same stored physical anchor.
Normal actor/player/production selection, original rasters and gameplay unchanged.

130source/state guards0fail;890native checks0fail/24actual interruption cases,
engine0/{world['seconds']}s. Both gears at .32/.39/.55seconds, actual service
suspension, fire dispatch, public gear toggle and mortality;15future floor ticks.
All24before/after pairs in8boards reviewed;96original captures retained unchanged.
Post-release case persists at owned floor point; pre-release service/fire/death
still snaps pose and loses held-case presentation. Gear-bare-after native pair is
partly occluded by room effect: not material/detail acceptance. Death captures
show initial fall source, not completed fall/contact; fire is dispatch, not refuge.

{rec['checks']}native Continue checks0fail, engine0/{cont['seconds']}s:4actual
disk/fresh-main restores, both gears immediately before/after inferred release.
Exact source/root/clock/floor presence, pause and30future actor/player/source/case
ticks match. Malformed floor restore rejects before mutation. All8presentations
and2boards reviewed;16original captures retained. Explicit staged observer/guard/
renderer, not normal production or Title/new-process admission. All2931owner
non-log files unchanged in each scratch-profile interval. Hash snapshot post-run.

Lesson: distinguish visible ground contact, release ownership and embedded-case
suppression. A clock/index alone can invent release after a cancelled gear plan;
bind the actual displayed source to its live plan and canonical authored cue.
Next authored pre-release return/priority disposition, shared renderer/room removal,
normal guarded admission and continuous/full-library master/proportion/grade polish.
Full goal active/incomplete. Reviews:character/bill-floor-case-north-v1/
release-interruption-review.html and release-continue-review.html; RELEASE_HANDOFF.md.
No commit/export.

'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 old=path.read_text(encoding='utf-8');assert note.splitlines()[0] not in old
 path.write_text(note+old,encoding='utf-8')
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 with path.open('a',encoding='utf-8') as f:f.write('\n\n'+note)
files=[P/'release_state.gd',P/'release_workshop.gd',R/'tests/test_bill_floor_case_release_v1.gd',R/'tests/test_bill_floor_case_release_world_v1.gd',R/'tests/test_bill_floor_case_release_continue_v1.gd',P/'floor_checkpoint.gd',P/'floor-case-north.png']
e={'unit':unit,'interruption':world,'continue':cont,'continueChecks':rec['checks'],'releaseCue':{'index':8,'seconds':.36,'status':'inferred/staged'},'groundContactIndex':5,'visualReview':'24 interruption pairs/8boards and4Continue pairs/2boards viewed; early held return and continuous full motion unresolved; gear-bare-after pair effect occluded','postRunHashes':{p.relative_to(R).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
(P/'release-evidence.json').write_text(json.dumps(e,indent=2)+'\n')
(P/'RELEASE_HANDOFF.md').write_text(f'''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill staged cargo release

## Objective and acceptance
Full Bill set consistent with masters, perspective, stature, proportions and matte
grade, followed by cross-family polish. Goal active and incomplete.

## Accepted decisions and constraints
Preserve original actor art, normal selection and gameplay. Staged source8 release
is inferred, distinct from source5 ground contact. Reversible work authorized.

## Current state
New release_state/release_workshop, three targeted fixtures/runners and review
builders. Source-review index/board preserves28unload originals. Case ownership
persists independently; same-anchor embedded case suppresses duplicate drawing.
No normal selection, commit/export or owner motion acceptance.

## Verification
130unit,890native/24actual interruption and{rec['checks']}native/4disk-fresh-main
Continue checks pass. All2931owner non-log files unchanged per scratch interval.
24interruption pairs and4Continue pairs viewed.96+16original captures retained.
Early pre-release service/fire/death still loses held case; gear-bare-after pair
effect obscured. Dispatch/initial fall samples do not prove evacuation/full falls.

## Next action
Author source-bound pre-release return/disposition, validate release in shared-room
renderer/removal, then normal guarded admission. Continuous native master/grade/
proportion review and remaining full-set families remain necessary.
''',encoding='utf-8')
print('Release milestone, pipeline, bible and maintained/installed skill updated.')
