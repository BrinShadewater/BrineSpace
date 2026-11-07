# Project handoff

Updated: 2026-09-30 · Project: BrineSpace · Task: Room and hallway conditions

## Objective and acceptance
Audit healthy, unpowered, leaking, flooded and repaired rooms/hallways. Fill actual
visual gaps while preserving overhead perspective, fixed world density, selected
painted sources and gameplay rules.

## Accepted decisions and constraints
Owner authorized the proposed condition pass. Reuse existing damage/weld artwork;
do not age or recolor clean master assets or edit owner placements. Existing power,
damage, repair, flooding and mission-chamber rules remain authoritative.

## Current state
scripts/flood_visuals.gd now shows cracks/leaks and completed weld marks on all
three hallway types. The seam anchor rotates with their geometry. Water polygons
and the front depth band cover large footprints, respecting 28-unit large-room
perimeter walls. Flood clocks (floor, prop submersion, crew water effects and
front effects) freeze under Reduced Motion. Newly created prop materials reset
their cached clock, including reflooding while paused.

rooms/large-rooms/common.gd draws peripheral flood tint above its immediate floor
art and below walls/equipment. Previously, that art hid retained water polygons.
Enclosed Moonbay/tidal mission chambers keep their independent water visuals.
Large peripheral water is a static tint; large equipment remains drawn above it,
without the per-prop waterline shader used by regular retained room contents.
scripts/room_asset_library.gd also freezes catalog effects and the older operating
screen path under Reduced Motion. Existing inactive-screen and light rules retained.
No source PNGs, actor artwork, placements, costs, water transfer or repair rules changed.

tests/test_flood_rendering.gd covers paused reflooding, Reduced Motion and large
water bounds. tests/review_condition_motion.gd (paired UID) supplies 21 rooms:
five conditions for batteries and each hallway type, plus a flooded Moonbay.
tools/verify_condition_motion.py copies owner layouts into scratch profiles and
fingerprints the real folder. tools/preview_condition_motion.py labels native
captures without physical-pixel resizing. Preview and full four-rotation/normal
captures: output/condition-motion-v1/condition-comparison-v1.png.

## Verification
Final UID, flood regression and native review PASS, zero native failures:
output/condition-motion-20260930-033659. Actual flooded interior pixels hold under
Reduced Motion; four hallway rotations match water polygons; drained surfaces hide;
large native water bounds span four cells; no failed artwork loads. Agent reviewed
native overview, normal junctions and large flooding. Whitespace checks pass.
Initial pixel comparison included moving ocean through a hull window; corrected
to sample the interior floor. No production behavior was changed to satisfy it.

Scratch APPDATA/LOCALAPPDATA used throughout. Owner comparison PASS in 033356 and
033552. Final comparison FAIL: of 2,810 files, ten probe/backup/comms/recovery files
changed (see summary.json); concurrent attribution unresolved. Main progress,
checkpoint and room_layouts.json unchanged; no owner restoration performed.

## Next action
Owner visual review. Per-prop waterline shading on large-room equipment is a
remaining renderer limitation. Release/native performance acceptance is separate;
no new performance claim, commit, push or export in this pass.
