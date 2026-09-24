# Bill standing work endpoint handoff

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Reduce Bill north/west idle-to-work identity jumps while preserving connected
lowering/tool poses. This is one concrete repair within the remaining work-body
consistency task; moving suit/backpack identity differences are not solved.

## Accepted decisions and constraints
Use exact canonical idle art at kneel frame 0 and stand frame 5, aligned by profile
pivots. Apply equally to bare and smaller-helmet variants. Preserve all other art,
timing, stride, metadata and clearance. No generation, Higgsfield, room edits,
publication or commits. Ordinary expedition and owner visual acceptance remain open.

## Current state
Final selection in tools/rebuild_bill_art.py applies the endpoint transfer after
historical source recipes and the smaller-helmet pass. Exactly eight PNGs change;
4451 other inventoried runtime files are unchanged. Offset is (36,52), derived
from the current profile pivots rather than canvas edges. Source selection/hashes:
character/major-bill-v3/sources/work-endpoints-2026-09-21/selection.json.
The prior helmet-size hash freeze remains its historical checkpoint; four helmet
hashes are superseded here. No standing-height, controller or registration changes.

## Verification
Evidence: output/bill-work-endpoints-2026-09-21/.
Canonical rebuild passes. Three work/helmet tests and four north/south-west endpoint
and continuity tests pass (the continuity suite itself covers south/west; the new
endpoint test covers north/west). Full validator: 2214 frames, zero errors/border
touches; 780 original frames and 113 original manifests unchanged. Consumer:
11773 checks, zero failures. Native production-player installed sequence: 171
samples, eight variants, zero missing textures, pixel-exact match to the staged
candidate at every sample. Onset stills and sequence reviewed.
West canonical standing toe begins two source pixels behind, and its bottom one
pixel above, the old generated standing pose. The remaining planted lowering
frames retain x106/bottom224; idle-aligned endpoint is x108/bottom223. The original
fixed-bound test failed on this deliberate replacement, then was updated alongside
an independent exact-pivot pixel test. Do not claim perfect foot locking.

## Next action
Refine the moving north/west suit/backpack identity with canonical references;
endpoint replacement alone does not harmonize those independently authored poses.
Keep connected body construction and avoid per-joint shifts. The f2ec1eb651c14137
Windows/Mac candidates remain their validated checkpoint and predate these eight
endpoint images; do not imply the packages include them. Continue room and gameplay
polish; native Apple Silicon testing and owner feedback remain open.
