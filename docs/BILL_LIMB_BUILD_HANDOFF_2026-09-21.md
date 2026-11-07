# Bill limb build handoff

Updated: September21,2026. Project: BrineSpace.

## Objective and acceptance
Repair Bill's walk surfaces and leg continuity without changing identity, boots or movement. The broader goal remains unfinished. Candidate reproduction is verified; full motion/style acceptance and production integration remain open.

## Accepted decisions and constraints
No Higgsfield. Independent east/west sources, no mirroring. Preserve owner rooms. Keep generated sources and exact prompts, and distinguish unselected candidate from production.

## Current state
Added tools/build_bill_limb_candidate.py and character/major-bill-v3/sources/limb-study-2026-09-21/{east,west} raw images, prompts and registrations. README marks these unselected. The command only writes beneath output/, validates source hashes and builds from original authored sources; no dependency on temporary output images or current live walk PNGs. Production repair_bill_walk/rebuild_bill_art bindings are unchanged.

## Verification
Ran candidate builder into output/bill-bidirectional-limbs-2026-09-21/rebuilt. All24bare/helmet east/west PNGs match prior candidate pixels exactly; rebuild-parity.json records each. Existing candidate24frame invariants and60native captures cover generation/loading and pixel preservation, not whole-motion acceptance. No new generation in this build step. No export or commit.

## Next action
Review complete motion/crossing/wrap and cross-direction pad consistency, then either refine source registration or connect the accepted candidate to the canonical production rebuild. Only then rerun production-art, unaffected-clip and runtime integration checks. Keep source study independent until that decision.
