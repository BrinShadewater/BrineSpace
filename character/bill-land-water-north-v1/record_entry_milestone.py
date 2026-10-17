from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
e=json.loads((P/'entry-review.json').read_text())
assert e['pairedFrames']==18 and e['decodedPairedAPNGFramesExact']==18
assert e['endpointExactToSelectedSources'] and e['timelineMs']==500
assert all(r['bodyOutsideHeadExact'] and r['foregroundExact'] for r in e['helmetFittings'])
note='''## Bill North paired articulated water-entry source candidate — October 2, 2026

New bare/helmet source banks provide nine poses each,500ms,320x352/p160224/H148.
Exact padded selected idle and North swim contexts, original-master crouchv2,
then six new independently articulated source-atlas poses: crouch/deep crouch/
push/lift/near-prone/extend. This replaces earlier rejected launch studies only
as a new provisional source candidate; normal source selection remains unchanged.
Independent North exit not yet authored; no reverse-entry substitute admitted.

New near-prone reference exec-03f2b8d7-7eb4-4ce6-a2c3-12927d641de4 and six-pose
atlas exec-cc306187-9f78-4e39-ad55-67b08baf571e saved with exact prompts immediately.
High-resolution current North swim atlas made the compact bent-leg rear projection
visible, avoiding upright arms-overhead drift. Six atlas cells share one anatomical
drawing density .25 against native rear head/equipment ruler; crouch retains its
master-defined148/976 density. Whole-figure translations only, no per-pose box
height/width fitting, rigid limb rotation or per-pose exposure compensation.
Head anchors103/118/131/145/169/184/198; first three source crouches share224sole.
Those source anchors are not proof of physical native floor/water contact.

Existing canonical rear40x34 swim shell used at scale1/rotation0 for seven new
interiors, original body outside bounded head region/foreground/from crown+25
exact. Both equipped endpoint pixels preserved. All18 APNG frames and authored
durations decode exact; both profiles share500ms holds40/50/55/55/60/60/60/60/60;
no clipping. Complete bare/paired source boards and seven close neck fitting pairs
visually inspected. Collar joins coherent in inspected poses, master rear equipment
and matte quilting retained. Lift pose5 still has slight lateral twist; hair/metal/
normal-endpoint grade and temporal/native/master acceptance remain pending.
Finite normal/quarter-speed paired source player generated, not browser-motion
verified. No game save/profile access, native test, production installation or export.

Lesson: source CANVAS size does not establish anatomical drawing density. Use one
documented physical component ruler and fixed source-atlas scale, preserving all
relative body dimensions; then inspect full anatomy and projection. A single
standing-derived draft can preserve hardware sizes yet lose foreshortening. Use
high-resolution current pose sources for the action camera. Shared density and
exact shell/protected-body pixels still do not certify coherent full-speed motion,
shoulder occlusion, master grade or controller contact. Retain rejected studies.

Next repair lift twist and review source motion/master/endpoint grade, then real
North native transition/contact/clearance/guards/save/Continue. Independently
authored North exit, South bridges, West endpoint/master polish, guarded normal
admission, cargo lifecycle and full-family consistency remain. Goal active/incomplete.
Review:character/bill-land-water-north-v1/entry.html?v=paired-source-v1.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    f=R/rel;t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(note+t,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · Project: BrineSpace · Task: Bill North paired entry source

## Objective and acceptance
Complete Bill's full original-master-matched set then full cross-family polish. Open.

## Accepted decisions and constraints
Independent axial rear poses, canonical rear helmet, exact static selected endpoint
contexts. Fixed physical source density and whole-figure registration; no per-pose
stature/width normalization. Normal actor/game sources and owner data untouched.

## Current state
New near-prone reference and six-pose entry atlas/raw prompts; build.py,
build_helmet.py, build_review.py, record_entry_milestone.py;18PNGs/two manifests/
twoAPNGs; bare/paired contact/neck boards, finite paired player and entry-review.json.
Earlier rejected studies/audit retained. Six guidance files updated.

## Verification
All18 APNG decoded frames/durations exact;500ms both profiles; endpoint pixels exact,
no clipping. Seven canonical scale1/rotation0 shell fittings retain protected source
body/foreground pixels. Complete bare/paired boards and neck details inspected.
No browser continuous-motion review, native integration or production selection.

## Next action
Repair pose5 lift twist; motion and master/normal-endpoint grade review. North entry
native contact/clearance/cancel/save/Continue; independent exit and South bridges.
West fidelity/endpoint polish, normal admission, cargo lifecycle and full-set polish remain.
No running process, commit or export. Goal active/incomplete.
''',encoding='utf-8')
print(json.dumps({'pairedSourceFrames':18,'timelineMs':500,'guidanceFiles':6,'nativeAdmission':False}))
