from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
e=json.loads((P/'review.json').read_text());assert e['translatedOpaquePixelsAndRGBAExact'] and e['APNGDecodedFramesExact']==12 and e['floorContactY']==224
e['visualReview']='Four before/after source pairs inspected in contact board; complete bare/helmet six-pose rows compared at original common148 ruler against original master. Early front soles now meet idle contact line224 without changing painted anatomy/material/helmet. Crouch-to-buoyant pitch spacing remains visibly large; not final continuous motion or physical world support acceptance.'
(P/'review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note='''## Bill East early grounded contact registration trial — October 2, 2026

Source/master common-ruler review identified early lean/crouch front boot sole
contacts below canonical idle line224 before lift. New unselected V4 bare+helmet
entry packages shift two complete original poses upward6/27pixels using explicit
semantic front-boot regions/alpha>180. Original canvas320/p160,224/H148, scale1;
no body-height fitting, body/head/helmet repaint, colour grade or resampling.
Helmet moves together with complete original figure, preserving its neck/arm fit.

Eight other poses RGBA exact; four shifted poses retain all original painted
pixels/alpha support without clipping. Two six-frame APNGs,12decoded frames exact,
both original500ms timelines. All four before/after pairs and complete bare/helmet
master rows visually reviewed. Early soles now reach same source contact line;
actual floor/support/buoyancy/collision and continuous native motion not proven.
Existing runtime and source selections/saves unchanged. No Godot run needed for
this deterministic source registration; no owner files or production changes.
Earlier all-wet placeholder pose flags omitted, runtime material classification
pending. Separate exit and all older source/proof packages preserved.

Correction exposes66px crown gap from registered crouch to first buoyant pose.
Need new articulated push/lift intermediate at common anatomical scale, then
paired helmet fitting, pose-aware material/head registration and moving native
contact/collision/interruption/Continue review on explicitly versioned new bank.
Do not interpolate scale or rigidly rotate limbs to hide this missing pose.
Other cardinal water bridges, cargo lifecycle and full Bill master/style/grade/
proportion/cross-family polish remain. Full goal active/incomplete.
Lesson: distinguish dry semantic boot contact from swimming root/head registration.
Correct whole-figure placement while preserving anatomy/material before judging
motion; preserved pixels and matching contact row do not prove continuous support.
Review:character/bill-land-water-east-v4/index.html. No commit/export.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/rel;text=f.read_text(encoding='utf-8')
 if heading not in text:f.write_text(note+text,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 text=f.read_text(encoding='utf-8')
 if heading not in text:f.write_text(text+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Bill early entry contact

## Objective and acceptance
Full master-consistent Bill animation set then cross-family consistency/polish.
Source registration trial only; whole goal and native support acceptance open.

## Accepted decisions and constraints
Common148 standing ruler/320canvas/p160,224. Preserve anatomy/paint/material/
helmet as complete figure; no per-pose stature fit. Early grounded versus later
buoyant contacts require explicit motion/support interpretation, not alpha flags.

## Current state
build.py, bare/helmet manifests/frames/500ms source APNGs, source/master/contact
boards, review.json. Two Y translations(-6,-27), four exact poses per gear.
Pipeline, bible, status and maintained/installed skill lessons updated.

## Verification
Eight original full poses exact; four shifted all painted pixels preserved,
no clipping/resampling/regrade.12APNG decoded frames exact. Four before/after
pairs and both six-pose master rows inspected. Boot sole semantic rows match224.
No native motion/contact/collision/master acceptance or normal/staged bank switch.

## Next action
Author missing push/lift intermediate for66px crouch-to-buoyant crown gap at
same anatomical scale/detail/matte palette. Pair helmet, update material/head
registration, then moving native support/collision and Continue on new bank.
Other directions/cargo lifecycle/full-set/master/cross-family polish remain.
Goal active; no live processes/commit/export.
''',encoding='utf-8')
print('Recorded early contact source trial and missing authored lift pose; goal active.')
