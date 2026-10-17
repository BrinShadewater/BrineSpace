from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
note='''## Bill new East land/water articulated source study — October 2, 2026

Two built-in imagegen attempts retain exact prompts/raw sources/execution IDs.
V1four articulated pitch interiors rejected for oversized heads/bright face drift.
V2targeted compact-head/material edit improves original-master relative identity;
first candidate and all its packaged sources retained separately. Both transparent
atlases contain four connected whole figures. Component extraction with3px fringe
omits low-alpha atmospheric halo, fixed.27anatomical scale for all interiors; one
atlas-wide neutral curve against selected idle, no per-pose exposure/stature fitting.
Warm skin/hair/burgundy not normalized. Generated material/proportions remain reviewable.

Bare East study packages four interiors between byte-exact padded selected idle0
and swim0 at common320canvas/pivot160,224/H148. Both originals bind to normal-loaded
RGBA metadata inventory.500ms entrance; exit is derived reverse, not separate authored
motion. Two APNGs decode all six poses exactly and preserve500ms; endpoint crop RGBA
checks pass. Full source board, direct original high-density side-master comparison
and82/54/27px density board viewed. Compact head/collar/suit detail retained in static
review; head lowers through articulated torso/hips/limbs rather than rigid rotation.

Not final source/owner/native acceptance: last interior extends legs farther than
the selected compact swim endpoint, so final leg-phase join needs refinement.
Prescribed crown trajectory into existing shoulder-pivot swim endpoint does not prove
water/floor support. Neutral idle entrance is not exact live walking-phase entrance.
Helmet counterpart, collision envelope, moving-gait dispatch, reverse exit motion,
water tint, priorities/Continue and cardinal expansion still pending. No production
loader/controller/renderer or original art changes. Full Bill goal active/incomplete.

Lesson: use original high-density design and exact selected endpoint pixels together;
uniform body registration cannot repair an enlarged head. Preserve rejected attempts,
generate articulated interiors and retain original endpoints; review final limb phase
and world support separately from static head/material fit. Next refine compact leg
join/trajectory, fit shared helmet, stage clock/geometry-aware admission and revisit
actual native land/water boundary before normal selection/full-library polish.
Review:character/bill-land-water-east-v2/index.html. No commit/export.

'''
for file in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 f=R/file;s=f.read_text(encoding='utf-8')
 if note.splitlines()[0] not in s:f.write_text(note+s,encoding='utf-8')
for f in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 s=f.read_text(encoding='utf-8')
 if note.splitlines()[0] not in s:f.write_text(s+'\n'+note,encoding='utf-8')
e=json.loads((P/'source-evidence.json').read_text());e['visualReview']={'sourceAndMasterAndDensityBoardsViewed':True,'decision':'Staged only; compact-head revision improved. Final extended-leg-to-compact-swim join, skin/material continuity and world support still need motion review.','helmetAvailable':False,'liveWalkingEntranceExact':False,'normalSelected':False}
e['inputsSHA256']={str(f.relative_to(R)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [P/'sources/interiors-v2.png',R/'character/bill-land-water-east-v1/sources/interiors-v1.png',R/'character/crew-side-masters-v1/bill-side-master-01.png',R/'character/crew-runtime-matte-v1/bill/frames/idle-east-breathing-v1/000.png',R/'character/bill-swim-east-coherent-v1/frames/swim-east/000.png']}
(P/'source-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill land/water source bridge

## Objective and acceptance
Full Bill set matching original masters/style/perspective/stature/proportions/matte
grade, then cross-library consistency/motion polish. Active/incomplete.

## Accepted decisions and constraints
Original selected idle/swim endpoints unchanged. Four articulated generated interior
poses, fixed anatomical scale/material curve; no rigid figure rotation or crossfade.

## Current state
bill-land-water-east-v1 initial atlas/build/prompts retained; v2compact-head revision,
source-only6pose enter/derived reverse exit manifests, review and evidence. Bare only,
unselected. Pipeline/bible/both skills updated. No production controller/renderer edits.

## Verification
Exact selected endpoint RGBA; both6frame APNG decodes and500ms timelines pass.
Source/master/82/54/27px boards viewed. V2head fit improved; final extended-leg to
compact-swim join remains unaccepted. No live animation, collision/support or save claim.

## Next action
Refine last interior leg phase/trajectory and master-relative grade; shared helmet
fit; moving-gait/geometry/clock-aware staged dispatch and actual native boundary
review. Continue/priority, other directions and normal water material selection,
cargo lifecycle/older-bank Continue and full Bill master/library polish remain.
''',encoding='utf-8')
print('Source milestone, original/rejected provenance and open motion requirements recorded.')
