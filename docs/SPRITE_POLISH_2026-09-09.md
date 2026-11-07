# Sprite polish handoff

Updated: September 9, 2026 · BrineSpace · Character scale and animation pass

## Objective and decisions
Owner requested sharper sprite sheets, animation improvements for newer characters/companions, and Marsh scale consistency. Preserve 92×92 frames, foot pivot (46,86), approximately 74px standing crew height, raw PNG playback, distinct companion sizes and existing gameplay. Owner authorization covers integration; this is agent-reviewed work, not new owner visual acceptance.

## Current state
Installed `character/sprite-polish-v2` through `grid_canvas.gd`, `marsh_npc.gd` and `companion_npc.gd`. Original packs remain intact. `tools/build_sprite_polish.py` is the deterministic builder; source PNGs, exact imagegen prompts, hashes, build report and review gallery are in the versioned pack. Raster LFS attributes verified.

Marsh now has a slimmer adult silhouette matching the crew, smaller head, dedicated two-frame idle in four directions, revised six-frame locomotion and stationary tool work, and matching underwater/collapse art. First locomotion candidate retained but rejected for oversized proportions. Swim sources already contained transparency; the additional keyed attempt was unnecessary and is retained unused. Native scale remains unchanged. Conservative clearance is the union of old bounds and revised art, never reduced to make navigation pass.

Marsh has 140 state/direction entries, not 140 uniquely authored actions. Secondary activities still reuse work/collapse/swim poses; running shares the walking poses. North/south final collapse turns laterally; this remains an animation limitation. Legacy helmet frames remain loaded for compatibility but Marsh's sealed-android controller never equips a helmet.

River, Josh and Margot now use one 64-color palette per identity across locomotion and personality, matching the crew's nondithered packaging. No blur/sharpen filter or mirrored poses. River/Josh gain 32 total nonloop entry/exit clips using existing idle/action endpoints (not generated in-betweens). Existing behavior durations, pause and saves remain unchanged. Margot keeps her authored sit/groom/nap/pet clips. Bill/Veld/Branforth base sprites already use 64-color packaging and were left intact.

## Verification
Builder assertions pass for all seven manifests: frame dimensions, nonempty unclipped bounds, binary alpha, durations and <=64 opaque colors. Standalone sprite-manifest validator passes for all seven packs. `tests/test_sprite_polish.gd` plus UID passes natively: production PNG player, four-direction coverage, new idle, exact robot idle endpoints. Native frame captures cover idle/walk/work/swim/collapse with enlarged and canonical-scale copies; agent inspected the lineup and sampled action frames. GIFs preserve sequences for owner motion review. Browser policy blocked opening the local gallery, so continuous browser motion review was not completed.

`tests/test_companion_personality.gd` passes natively with revised assets, including action save/restore, pause, return to idle and pet/wake behavior. `test_marsh_unlock.gd` has four peer-count failures: expects 3, observes 5 active peers. A control fixture loading old Marsh art/clearance reproduces those four failures. That control also clears old equipment when reloading the manifest, causing additional equipment assertions; those are a control-fixture limitation, not evidence of a production regression. Production revised pack passes all its pose loads and other Marsh assertions. Logs in `output/sprite-polish`. Scoped diff whitespace check passes (CRLF notices only).

No executable export or commit. Full station congestion/occlusion and all secondary animation motion are not certified by the native sprite board.

## Next action
Owner can review `character/sprite-polish-v2/review.html`. Highest-value remaining animation work: bespoke Marsh seated/rest/carry poses and true swimming/treading separation, followed by smoother authored intermediate robot turns. Separately isolate the Marsh test's extra active peers before treating its old four-person count as a regression gate.
