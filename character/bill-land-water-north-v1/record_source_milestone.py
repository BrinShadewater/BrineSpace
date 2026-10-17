from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parent.parent
e=json.loads((P/'source-review.json').read_text(encoding='utf-8'))
assert len(e['provenance'])==6 and len(e['registrations'])==5
e['visualReview']='Raw six candidates and five-column fixed-master-density/sole-line board inspected. Crouchv2 retains a plausibly matching small rear head, backpack, matte quilt detail and lowered body; provisional only. Pushv2 shrinks component drawing density; pushv3 restores component size but loses lowered foreshortening; pronev1 remains too upright/elongated. Other rejected candidates enlarged head/equipment or rolled camera. No later phase approved or complete bank inferred.'
(P/'source-review.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
note='''## Bill North water entry source development — October 2, 2026

Started independent rear-view entry from original bill-video-north-v5/master-source.png
and current bill-swim-north-coherent-v1. Six built-in image candidates/exact prompts
saved immediately under bill-land-water-north-v1/sources with generation IDs/hashes.
Crouchv2 provisionally retains master-sized rear head/backpack/boots, lowered knees,
matte quilt detail, twin cylinders/three cyan vents/I belt plate/ring shoulder marks.
Initial crouch inflated head/equipment; initial push rolled camera/enlarged boots.
Pushv2 instead shrank drawing density; pushv3 size correction lost lowered posture;
pronev1 remained too upright/elongated. These later poses are rejected/pending,
not packaged as a complete transition or credited as new animation coverage.

Five-column source-master-audit.png inspected at one master-defined148/976 density,
correcting only output-canvas dimensions1254/1280, with whole-figure sole translation.
No pose bounding-box fitting, per-part resampling or silhouette width normalization.
Sole line is diagnostic registration, not final water/root/contact admission.
Raw art/source/provenance retained; normal game banks and owner profile untouched.
Source-only work; no Godot test needed. No timing/helmet/native bank yet.

Lesson: detailed costume preservation and requested dimensions do not prove pose
or scale preservation. A fixed-density comparison can reveal that a correction
restored head/equipment size while losing anatomical foreshortening. Axial North
entry must visibly interpolate lowered squat to prone camera; upright arms-overhead
art is not that transition. Use high-resolution current prone source as the pose
authority; standing detail references can overpower a low-resolution pose reference.
Do not admit rejected poses simply to fill a state-count matrix.

Next refine actual forward lean/near-prone from high-resolution current North swim
source, preserve crouch provisionally, add remaining articulated entry/independent
exit/helmet phases and common-scale/full-motion/native review. West continuous
master/endpoint matching, North/South bridges, normal admission/cargo lifecycle and
entire full-family consistency/polish remain. Full Bill goal active/incomplete.
Review:character/bill-land-water-north-v1/index.html. No commit/export.

'''
heading=note.splitlines()[0]
for rel in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
    f=R/rel;t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(note+t,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    t=f.read_text(encoding='utf-8')
    if heading not in t:f.write_text(t+'\n'+note,encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October2,2026 · Project: BrineSpace · Task: Bill North water source development

## Objective and acceptance
Complete Bill's full master-matched set then cross-family consistency/polish. Open.

## Accepted decisions and constraints
Independent rear North view, original master detail/density/matte grade. No mirroring,
per-pose stature fit or rigid limb replacement. Retain rejected sources and exact prompts.

## Current state
Six raw candidates and prompts with generation/hash provenance; provisional crouchv2.
build_source_audit.py, source-review.json, common-scale board and review page;
record_source_milestone.py. Six status/pipeline/bible/skill guidance files updated.

## Verification
Six raw figures and five-column148/976 master-density board inspected. One early
pose provisional; later push/prone phases rejected/pending. No complete animation
bank, timing, helmet, native motion/save proof or production selection. No Godot/save access.

## Next action
Use high-resolution existing North prone source as pose reference for true forward
lean/foreshortening; build remaining entry and independent exit phases, equipment,
motion/master checks and native integration. Other cardinals/cargo/full-family polish remain.
No running process, commit or export; goal active/incomplete.
''',encoding='utf-8')
print(json.dumps({'sourceCandidates':6,'provisionalPoses':1,'completeAnimationBank':False,'guidanceFiles':6}))
