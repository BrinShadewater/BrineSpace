from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
evidence=json.loads((P/'flood-motion-evidence.json').read_text());assert evidence['validation']['passed']
note='''## Bill cardinal water readability and depth seam study — October 2, 2026

Staged flood_readability_v2 replaces previous .85 hard cutoff with continuous body
tint blending from original RGB(.37,.71,.74)/depth alpha toward(.72,.86,.86,.90)
over .55–.95. Existing head highlight/wake fade over .70–.95; bubbles enter over
.75–.95. Original head-mask geometry, wake geometry, bubble locations, source
textures/pivots/H148, physical root and retained room drawing order preserved.
Only swimming textures in the staged workshop view; dry and other actors untouched.

Prescribed source playback in actual selected-main retained room renderer: all96
loaded swim/tread holds, four directions/both gears, normal versus candidate; plus
14fixed-source depths per gear including .849/.85/.851.248native presentations,
124exact decoded source pairs,1506checks0fail/95.99s/engine0/cleanlog.2931owner
non-log files unchanged/scratch APPDATA. Four full pose boards and two cutoff seam
boards viewed: readable silhouette, face/helmet and suit throughout source holds;
old .85 head visibility drop removed in captured seam. Source proportions untouched.

Review contains32native authored-hold APNGs,16unchanged-source APNGs and four depth
sweeps, all frames decode exactly to captured pixels. These reconstruct authored
holds; no actual continuous60fps, natural route/safety/physical swim or outside-room
fallback acceptance. Static board review does not certify playback motion quality,
underlying water-to-dry source joins, original-master identity or full source set.
Normal production flood renderer remains unchanged; candidate unselected.

Initial native loads failed due to copied wake tabs mixed with spaces; terminal
logs/reports archived and old source retained in flood-motion-first-interval.
PowerShell GUI check-only launch initially appeared successful before process output;
blocking captured Python subprocess identified real parse failure. Indentation fix
only; final native run clean. Source hashes are post-run, not prelaunch world freeze.

Lesson: preserve effect geometry and source art while blending runtime material and
head/wake/bubble visibility through the same depth interval. Verify exact cutoff
neighbors in native room pixels; reconstructed timelines prove packaging/timing,
not continuous gameplay. Next actual advancing flood routes/native motion, dry/water
joins, outside fallback and guarded normal selection; cargo floor lifetime/priority
disposition/idle joins/older-bank Continue and full Bill master/library polish open.
Goal active/incomplete. No commit/export. Review:
character/bill-floor-case-north-v1/flood-motion-review.html.

'''
for file in ['docs/CURRENT_STATUS.md','docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 target=R/file;old=target.read_text(encoding='utf-8')
 if note.splitlines()[0] not in old:target.write_text(note+old,encoding='utf-8')
for target in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 old=target.read_text(encoding='utf-8')
 if note.splitlines()[0] not in old:target.write_text(old+'\n'+note,encoding='utf-8')
(P/'FLOOD_MOTION_HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill water continuity

## Objective and acceptance
Complete full Bill set matching masters/style/perspective/stature/proportions/matte
grade, then cross-family consistency and motion polish. Active/incomplete.

## Accepted decisions and constraints
Same source, pivot, root and room depth. Staged material continuity replaces hard
water cutoff; source geometry and original water effect geometry preserved.

## Current state
New flood_readability_v2/UID, fixture-only flood_motion_player/UID, full cardinal
hold/depth fixture+runner and rebuildable original-capture/APNG review. Normal
production renderer unchanged. Updated pipeline/bible and both skill references.

## Verification
1506native checks0fail/95.99s/engine0/cleanlog.248native presentations/124paired
exact sources; all96loaded swim/tread holds plus14depths per gear. Six boards viewed.
52APNGs decode exactly to native/source pixels.2931owner files unchanged/scratch.
Initial parse failure retained; final indentation correction clean. Hashes post-run.
Review timelines reconstructed from authored holds, not continuously captured motion.

## Next action
Actual advancing flood routes/native motion and dry/water joins, global fallback
outside removed room and guarded normal material admission. Cargo idle join, early
held-case priority disposition/shared-room lifetime, older-bank Continue, remaining
full Bill families and direct master/cross-family grade/proportion polish remain.
''')
evidence['visualReview']={'allSixBoardsViewed':True,'findings':'All loaded cardinal swim/tread holds readable; original source proportions/detail preserved. .849/.85/.851 seam retains head detail. No continuous playback/natural-route/master acceptance.'}
(P/'flood-motion-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Scoped native review, handoff and pipeline/bible/skill lessons recorded.')
