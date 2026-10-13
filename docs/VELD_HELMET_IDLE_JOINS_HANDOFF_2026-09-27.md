# Veld helmet idle and join handoff

Updated: September 27, 2026 - BrineSpace

## Objective and acceptance
Owner authorized matching helmet idles, idle/walk join checks and fitting/removal review. Four idle candidates and eight-state staging pack now ready. No new owner motion acceptance or runtime installation claimed.

## Accepted decisions and constraints
Same four helmet references and input framing as selected walks. Four Hailuo2.3Fast six-second768p jobs, estimated16 credits total; optimizer false confirmed. No additional paid retries. Preserve white lamp, equipment sides, palettes and poses. Keep the installed bare pack intact.

## Current state
`character/veld-helmet-idles-v1/` holds generation metadata and all four source videos, build.py, build_joins.py, idle manifest, checks, previews, fitting/joins images, and `joined-pack/manifest.json`.

Idle sources: south52-123, east51-98, north50-97, west64-114. Original forward sequences did not loop cleanly. Final idles traverse these actual breathing poses forward then reverse, excluding duplicated endpoints; no morphing, blending or invented frames. 430 playback frames (219 unique source frames), durations south5917ms/east3917ms/north3917ms/west4167ms. Fixed body scale/pivot as matching walk; no per-frame normalization.

Staged pack: 594 frame slots (430 idle+164 walk). Walk rows cyclically rotated only to closest idle pose: south25, east24, north34, west39. Every copied walk PNG remains identical to its selected source; timing rotated with poses. SourceFrameOrder/sourceFrames and sourceVideo record derivation. Preview idle-walk-idle-review.gif includes 1s idle, 2.2s walk, 1s idle (mid-stride stop).

## Verification
Manifest validation clean, including staged pack. All idle sources/exports uncut. Sole Y constant within each clip:172 for east/north/west,173 for south; source height varies at most1px. Revised loop seam difference does not exceed internal maximum in any direction. Agent reviewed source/joins contact sheets; owner temporal review remains pending. Four-idle GIF plays native cadence; transition GIF plays30fps sample sequence.

Fitting-joins.png shows old east equip/remove endpoints have visibly smaller helmet/head and softer/darker body than current bare/helmet idles. Existing equip/remove source has8 poses; no changes made to those actions or runtime. No Godot/save access in this candidate-only pass.

## Next action
Rebuild east helmet fitting/removal using current bare and helmet masters, retaining actual empty-helmet pickup/return and one visible head. Preserve action durations2.14s/2.24s unless consumer contract is intentionally changed. Check joins visually, then install the complete helmet profile and perform isolated native equipment/movement/save tests. Do not install old fitting artwork alongside the new idles as if consistent.
