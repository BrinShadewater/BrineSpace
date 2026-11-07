# Bill north action integration

Updated: September 21, 2026 · Project: BrineSpace

## Objective and acceptance
Remove the north kneel/work/rise height pop and old suit-style mismatch. Installed
for playtesting after bounded native review. Owner motion acceptance remains open.

## Accepted decisions and constraints
No Higgsfield. Independent north sources, exact prompts and registrations preserved.
Original source contracts, other directions and owner room layouts remain unchanged.

## Current state
`tools/build_bill_north_actions.py` reads selected sheets under
`character/major-bill-v3/sources/north-actions-2026-09-21/`, using the shared source
extraction helper. Canonical rebuild selects its kneel/repair/stand bare/helmet clips.
Work endpoints equal settled kneel; stand reverses kneel. The left boot correction
retains the folded right leg in front at shared silhouette edges. Bottom-band boot
centroids range 110.47-111.18 pixels, versus the prior 103.47-113.18 range. This is a
registration measure, not a whole-anatomy acceptance certificate. Helmets reuse the
existing north overlay with per-frame head anchors.

## Verification
Maintained helper reproduces all 36 reviewed candidate frames exactly. Refined native
fixture captured 198 frames per equipment state, zero failures/no logged errors.
Direction and helmet selection are forced to isolate rendering; not autonomous
facing or donning evidence. Agent endpoint-board review confirms height consistency
and helmet fit. Evidence: output/bill-north-refined-native-2026-09-21.

Full canonical rebuild completed, 504 original source crops reproduced. Full library
validation passes: 2,214 frames, zero errors/border touches, 780 source frames and 113
source manifests preserved. Exactly 36 intended PNGs changed; all other generated
assets and metadata match the pre-integration snapshot. Evidence:
output/bill-north-action-integration-2026-09-21, including rollback frame copies.

Installed-loader confirmation completed: 198 frames per equipment state, zero
failures/no logged errors. Agent inspected the installed equipped repair capture.
Evidence and paired GIF: output/bill-north-installed-native-2026-09-21.

## Next action
West remains the next documented directional
action repair. Existing Windows/Mac packages predate both north and south action fixes.
