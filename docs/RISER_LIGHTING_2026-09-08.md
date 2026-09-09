# Project handoff

Updated: September 8, 2026 · Project: Brine Space · Task: Riser lights and outward exterior illumination

## Objective and acceptance

Owner requested removal of north low-wall decorations and lights, dressing on
the riser, visible lights with the riser hidden, and brighter outward exterior light.

## Accepted decisions and constraints

The low north pressure-hull strip is bare; dedicated riser dressing remains.
Riser visibility is a cutaway display choice and no longer relocates fixtures.
Existing raised overrides take precedence; legacy low offsets translate to riser
height with brightness/color/hidden settings preserved. No economy changes.

## Current state

Changed `rooms/whole-room/decoration_props.gd`, `room_lighting.gd`,
`scripts/room_layout_editor.gd`, `scripts/grid_canvas.gd`, and
`scripts/station_hardware.gd`. Studio framing fits the riser-mounted lights even
when wall geometry is hidden. Exterior cones start outside the crown/foundation,
point away in all four directions, skip occupied neighboring edges and respect
master-power/exterior switches. Added `tests/test_riser_lighting.gd` and UID;
updated old low-mount test expectations in existing fixtures and the studio guide.

## Verification

Godot 4.6.1 passes: `test_riser_lighting.gd`, `test_simple_room_studio.gd`,
`test_room_layout_editor.gd`, and `test_station_hardware.gd`. The dedicated test
covers canonical mounts, legacy studio migration, unchanged anchors across wall
visibility and adjacency, outward beam geometry, and station light/power gates.

Visually reviewed `output/layout-editor/riser-fixtures-on.png`,
`riser-fixtures-hidden.png`, and `exterior-outward.png`. Off and power-off captures
also exist. Test logs: `output/riser-light-test.log`, `riser-studio-simple.log`,
`riser-studio-regression.log`, `riser-hardware.log`. No script errors; existing
raw-image export warnings remain. Test layouts are isolated from owner saves.

## Next action

Owner visual review in Studio and a live station. Static room-card images were
not rebaked in this runtime lighting change. No commit or deployment requested.
