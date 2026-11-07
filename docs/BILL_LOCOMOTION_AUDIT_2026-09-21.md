# Project handoff

Updated: 2026-09-21 · Project: BrineSpace · Task: Bill locomotion coverage

## Objective and acceptance
Repair Bill motion across the actual selected clips; do not equate base-walk
pixel parity with all movement being repaired.

## Accepted decisions and constraints
Preserve identity, owner rooms and existing source pixels. No Higgsfield.
Production sprites remain unchanged in this diagnostic pass.

## Current state
Inspected current repair builder and selected walk/carry frames. Bill NPC selects
carry while moving dry cargo and during workshop_carry. grid_canvas routes carry
through human_water_player, while ordinary walk uses human_animations. The selected
v3 manifest contains separate carry-east/west frames with state-wide stride 0.12;
walk-east/west use 0.10567567567567569. Different strides alone are not a defect.

The native-size contact comparison shows distinct carry art with lower visible
surface detail than the base walk; broad base-walk knee overlap remains unresolved.
This is agent still-image review, not temporal or owner acceptance.

## Verification
output/bill-locomotion-audit-2026-09-21/selected-walk-carry.png aligns every row
using its manifest pivot and standingHeight. manifest-report.json records actual
selected timing, stride and registration. An initial canvas-based sheet clipped
the carry row; it was replaced by the correctly registered comparison.

## Next action
Review carry and base-walk temporal contact sequences separately in the actual
runtime. Do not transplant the base repair or its stride into cargo clips without
checking their authored contact phases and hands/load registration. Continue
pose-specific base knee work; rejected generic joint-mask studies remain rejected.

## Native follow-through
Native Godot playback captured 60 samples at 40 ms with distance-driven movement,
east/west and bare/helmet, using the selected catalog via grid loader: 480 texture
selections, none missing. native_check.gd, native.log, native-selected/ and
runtime-walk-carry.gif are in the evidence folder. The scrolling floor reflects
actual sampled movement; the two clips intentionally retain their own strides.
Inspected sample 015 confirms the art-detail mismatch in runtime; capture success
does not establish natural gait or foot planting. Eight-connected alpha analysis
found no detached components smaller than 12 pixels in the 12 base side-walk
frames, so there is no evidence for deleting isolated lower-body fragments.
Owner clarification on ordinary versus cargo movement has been requested; no
production pixels or timing were changed by this audit.
