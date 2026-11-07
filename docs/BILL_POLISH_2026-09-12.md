# Bill polish handoff

Updated: September 12, 2026 · Project: BrineSpace

## Objective and acceptance
One additional visual polish pass preserving Bill's detailed source art and colours.

## Accepted decisions and constraints
Continue local repairs from original artwork. Preserve animation coverage, body pixels, timing, density and pivots. Do not alter concurrent room work.

## Current state
`tools/rebuild_bill_art.py` now fits tread helmets to Bill's head instead of doubled legacy pilot bounds. All four directions have corrected visor/collar placement. Rebuilt `character/major-bill-v3/`: 24 equipped tread frames plus eight shared swim start/stop endpoints changed. All other PNG hashes, including every bare frame, are unchanged. Pipeline reference and installed skill synchronized; visual bible updated.

Review evidence: `output/bill-polish-2026-09-12/`, including before hashes, changed-frame list, original tread frames and all-pose comparison.

## Verification
- Original 780 frames and 113 manifests unchanged; 175 bare/168 equipped states, 2,214 references validated; zero errors or border touches.
- Complete-pack test passes: `output/test-runs/20260912-031103-headless`.
- Native all-state render passes, 96 sheets: `output/test-runs/20260912-031040-native`.
- Visually inspected all 24 corrected tread poses and native page 06 with tread/swim/action states. These are sampled visual checks, not owner acceptance of continuous motion.

## Next action
Polish implemented in the source checkout. No executable rebuilt. Broader original choreography remains as documented in the full-replacement handoff.
