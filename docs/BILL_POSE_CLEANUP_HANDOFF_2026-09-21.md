# Project handoff

Updated: September 21, 2026 · Project: BrineSpace · Task: Bill pose cleanup

## Objective and acceptance
Continue Bill's pixel-layer walk repair alongside room furnishing, other animation
repairs and game polish. This milestone repairs one visible artifact, not the gait.

## Accepted decisions and constraints
Use existing pixels and targeted edits. Preserve identity, timing, planted feet and
owner room layouts. No Higgsfield. Broad joint masks and layer-order studies did
not produce acceptable replacements and remain uninstalled.

## Current state
`tools/repair_bill_walk.py` now applies a source-guarded west phase-0 ankle cleanup.
Thirty pixels change in each `character/major-bill-v3/frames/{bare,helmet}/walk-west/000.png`:
remove the bright cutout spur above the boot and continue its existing dark edge.
Toe, sole, upper body, other phases, stride and timing are unchanged.

Exact pixel deltas, before images, installation hashes, enlarged comparison and
native captures: `output/bill-pose-cleanup-2026-09-21/`.
CURRENT_STATUS.md records the installed change.

## Verification
Three focused Python surface tests pass, including exact canonical review/export
parity for all 24 side frames. Complete pack: 11,773 checks, zero failures.
Native runtime/reference check: 240 distance-driven comparisons, zero failures.
Inspected enlarged before/after and native contact pose. These establish the local
artifact repair and reproduction, not owner acceptance of natural gait.

## Next action
Continue individual knee contour/shading repair; avoid repeating rejected broad
mask, layer-order, generic kneepad and increased-height studies. Review room pilots
at gameplay zoom and reconcile saved/default layouts before refreshing releases.

## East phase-4 knee edge follow-through
Installed a guarded seven-pixel contour repair in both bare/helmet east walk frame
004. Two outward teeth are trimmed using the existing dark edge pixels. Other
frames, upper body, soles, stride and durations remain unchanged. Canonical
repair_knee_contour reproduces the edit and checks source row bounds before repair.
Evidence/backups: output/bill-knee-contours-2026-09-21/. Enlarged before/after and
native phase sample 024 inspected. Three focused Python surface/command tests pass;
240 native runtime/rebuilt-reference comparisons pass. No complete-pack rerun was
needed for this local pixel-only change; previous pack coverage is historical.
This improves one edge, not the underlying bulky-knee gait or cargo-art mismatch.
Next: broader pose/anatomy work remains, with owner comparison response pending.
