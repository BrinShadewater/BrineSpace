# Bill passing-pose source candidate

Updated: 2026-09-21 - BrineSpace

## Objective and constraints
Repair coherent knee/shin silhouette before expanding walk clips. No Higgsfield;
preserve owner rooms and selected production animation until candidate validation.

## Current state
One built-in image_gen edit of current bare east phase 002 produced a separate
source. Exact prompt and raw source are preserved under
output/bill-passing-pose-2026-09-21/. The generator altered detail outside the
requested area and emitted 1254-square soft-alpha art, not a drop-in sprite.
register_candidate.py deterministically resamples to 184 square, maps the original
palette and replaces only rows119:153. Original upper body and boots are byte-exact;
1,038 pixels change inside the repair band. Same repair band applied to a separate
helmet candidate. Six-frame diagnostic manifests use the unchanged other poses.

## Verification and review
Source alpha/dimension inspection saved. Inspected source, registered comparison
and native frame013 at runtime scale: knee silhouette is more continuous and
compact; no whole-animation acceptance. Native diagnostic produced60captures
without logged engine errors. Its printed capture count is not a regression suite.
One repaired frame introduces a style/shape discontinuity with adjacent original
frames; do not install a mixed clip on the strength of its still improvement.
Production files, room layouts, gameplay and release candidates unchanged.

## Next action
Use this source as the representative knee/shin treatment for neighboring poses,
while preserving each phase's near/far leg order, support and equipment details.
Review all changed clips temporally and at normal gameplay scale, then integrate
through the canonical rebuild with bare/helmet parity. Current candidate alone
is not an accepted repair.
