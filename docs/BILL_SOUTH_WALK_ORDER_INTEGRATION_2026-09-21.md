# Bill south walk order integration

Updated September 21, 2026. BrineSpace. Broad objective remains unfinished.

## Objective and decisions
Repair premature support-leg swapping by ordering complete original poses into
alternating half-steps. No new drawing, limb separation, generation or Higgsfield.
Preserve all owner rooms and other animation states.

## Current state
Canonical rebuild now calls tools/build_bill_south_walk_order.py after composing
body and equipment. Selected order: [0,4,5,3,1,2]. Both contact slots 0/3 stay fixed;
eight PNGs change across bare/helmet. All 4452 other inventoried runtime art,
metadata and import files remain byte-identical. Canvas, pivot, timing, stride,
clearance and gameplay unchanged. Original poses and frozen decoded hashes live
in character/major-bill-v3/sources/south-walk-order-2026-09-21/.
The helper rejects changed inputs instead of silently permuting unreviewed art.
Arm/leg pairing, source-scale sequence and loop seam inspected in both variants.
This selects the order-only study from BILL_FOUR_DIRECTION_GAIT_AUDIT_2026-09-21.md.

## Verification
Evidence: output/bill-south-walk-order-2026-09-21/.
- Full canonical rebuild completed. Exactly eight PNG changes verified.
- Five walk surface tests pass; south output pixels exactly equal their original
  source poses in the selected permutation, including both equipment states.
- Full art validation: 2214 frames, no errors or border touches; 780 original
  frames and 113 original manifests unchanged.
- Production loader: 11773 checks, zero failures.
- Installed paid station: exit0, 480 samples, 270 unpaused south walks; costs
  and failures enabled. Actual getter verified with no candidate overrides.
  Controlled opening/manual30Hz stepping is not a full expedition playtest.
- Separate native production-player capture: 27 frames for bare/helmet at source
  and game scale; zero missing textures. Native image and station context inspected.
  Initial log caption says East from its parent fixture; loaded key, image labels
  and both manifests establish south. Fixture caption corrected for future use.
- installed-south-walk.gif crops the installed native render; static ground ticks.
  It does not demonstrate anatomical world-space foot locking.
- Pipeline reference updated and installed copy synchronized.

## Next action
Review north's limited within-half-step motion and anatomical stance sliding across
all directions. Owner visual acceptance remains open. Current Windows/Mac test
packages predate east, west and south walk integrations; refresh at the next
release checkpoint. Continue natural room furnishing/polish with protected owner
layouts unchanged.
