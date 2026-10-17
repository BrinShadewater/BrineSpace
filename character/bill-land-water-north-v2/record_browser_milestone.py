from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent;D=P/'browser-review'
e=json.loads((D/'review.json').read_text());pause=json.loads((D/'pause.json').read_text())
assert len(e['cases'])==4 and all(x['terminalPose']==8 for x in e['cases'])
assert pause['unchanged'] and pause['pausedPose']==pause['heldPose']==1
e['pause']=pause
e['visualReview']='Fixed-crop advancing board viewed for bare/helmet paused idle and sampled quarter-speed labels1..8. Whole figure fits responsive viewport; rear equipment and corrected shell/collar remain readable in sampled frames. Deep-crouch3 to raised-arm push4 produces a visible hand-position jump warranting an intermediate reach revision. Endpoints/material/detail/physical-motion full acceptance remains pending. Sparse normal-speed snapshots are not all-frame temporal evidence.'
(D/'review.json').write_text(json.dumps(e,indent=2)+'\n')
source=json.loads((P/'entry-review.json').read_text())
source['browserMotionReview']={'review':'browser-review/index.html','cases':4,'advancingScreenshots':80,'pausedIdleScreenshots':2,'normalAndQuarterBothGearReachedFinal':True,'pauseHeld':True,'scope':e['captureScope'],'remaining':'Hand-position transition3→4 revision; full-speed temporal quality, master/endpoint grade and native contact/integration remain.'}
(P/'entry-review.json').write_text(json.dumps(source,indent=2)+'\n')
note='''## Bill North sampled browser playback and reach diagnosis — October 2, 2026

Actual NorthV2 source player exercised through controls in in-app browser, bare and
helmet at normal and quarter speed. Four cases advance to final8. Eighty advancing
screenshots plus two scrubbed paused idle views saved. Quarter-speed AX labels1..8
observed in both profiles; sparse normal captures observe bare4/5/6/8 and helmet
4/5/6/7/8. Initial0 captured separately paused, not claimed as an advancing capture.
Pause held1 across review work; scrubber Home returns0. UI selected speed/gear
verified. Browser screenshots use1265x712 viewport; generated caption fixed.

Responsive preview now displays complete canvas within viewport at fixed aspect
ratio, preventing trailing-boot clipping. Correct UTF-8 reads when copying builder
source remove garbled title punctuation. Artwork/holds/pivots/scales unchanged;
16 unaffected pose images still exact toV1 and18decoded APNG frames/holds exact.
No Godot run or owner profile access. Browser playback is separate from native proof.

Sampled progressing board inspected with same screen crop for every pose; canonical
helmet/collar readable and figure complete. Deep-crouch3→raised-arm push4 visibly
jumps hand position, so refine an intermediate reach before motion acceptance.
Master/endpoint hair/metal/material grade and native contact still pending. AX pose
label recorded immediately before screenshot may cross a hold boundary; no exact
source-phase screenshot binding claimed. Timings measured after click return,
not dispatch; no browser duration claim. Observing final8 alone does not establish
all-frame temporal quality, particularly at normal speed.

Lesson: fit review canvas to display without cropping limbs or distorting aspect;
keep display scaling distinct from physical source density. Exercise real controls,
save advancing evidence and report sampled phase coverage. A working finite player,
exact APNG and static pose board do not establish smooth chronological articulation.

Next author smoother hand reach for phase3→4 with existing master build/grade,
repeat the affected moving review, then North native entry/contact/clearance/guards/
save/Continue and independent exit. South bridges, West fidelity/endpoint polish,
normal admission/cargo lifecycle/full-family consistency remain. Full goal active.
Review:character/bill-land-water-north-v2/browser-review/index.html.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    f=R/rel;t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(note+t,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(t+'\n'+note,encoding='utf-8')
(D/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · Project: BrineSpace · Task: Bill North browser motion diagnosis

## Objective and acceptance
Full original-master-matched Bill set followed by cross-family polish. Incomplete.

## Accepted decisions and constraints
Source/native evidence separate. Preserve source pixels, anatomy, density, holds
and owner data. Fixed-aspect viewport fit is display only; no pose scale normalization.

## Current state
UTF-8 builder copy and responsive canvas correction;82browser screenshots,
playback.json/pause.json, build_browser_review.py/record_browser_milestone.py,
fixed-crop moving board/review.json/index.html. Six guidance files updated.

## Verification
Four actual UI playback cases final8; both quarter-speed cases observe1..8,
normal-speed samples partial. Scrubbed idle0 both gears; pause1held.16unaffected
source frames exact;18APNGdecoded frames/holds exact. Advancing board inspected.
No exact AX-label-to-screenshot phase binding or duration/native motion proof.

## Next action
Repair hand-position jump3→4, repeat affected moving source review, then North
native contact/clearance/guards/checkpoints/Continue and independent exit.
South bridges/cargo/admission/full-set master-grade-proportion polish remain.
Preview tab5 marked deliverable. No running process, commit or export. Goal active.
''',encoding='utf-8')
print(json.dumps({'playbackCases':4,'screenshots':82,'pauseHeld':True,'remainingRepair':'reach3-to4','guidanceFiles':6}))
