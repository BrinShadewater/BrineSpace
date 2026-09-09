# Corridor floor variation, default doors and water review

Updated: September 8, 2026 · BrineSpace

## Objective and acceptance

Reduce obvious floor repetition, give corridor/corner/T entryways gray metal doors by default, and verify water effects across the variants. [Dry and flooded review](../output/corridor-polish-v3/index.html). Owner acceptance pending.

## Accepted decisions and constraints

Retain aligned pipe lanes, solid borders, short T returns and centered riser windows. Reuse existing source art through registered selections; preserve saved floor and layout edits. No loose clutter added. Water simulation rules remain unchanged.

## Current state

`modular_floor.gd` adds curated border substitutions and occasional alternative observation grating, preserving pipe alignment and nine shape/variant arrangements. `door_finish.gd` adds the cooler metal finish; `department_door.gd` assigns it to corridor shapes and connected pairs touching a corridor. `corridor_wall_art.gd` uses it for raised entry doors.

`corridor_dressing.gd` draws closed gray doors at exposed low entries. `grid_canvas.gd` replaces old plain cap defaults, preserves shared live doors on connected entries, and supplies closed low doors when a neighbor exists without a valid connection. `room_layout_editor.gd` shows default doors with risers disabled as well. Nine native cards and both consumers are refreshed under `assets/corridor-polish-v3`.

## Verification

- 72 native dry raised/low shape/variant/rotation captures pass. Clean corner with gray entry doors visually inspected.
- `test_corridor_water_variations.gd`: all nine variants exercised in a live station with a BRINE neighbor at 0.8/0.2 water levels. Actual door aperture changes produce closing state; native pause holds pixels; all 36 rotated hallway water polygons match their footprints. Thirty-six closing captures are in the gallery. T-junction flooded capture visually inspected.
- `test_room_flooding.gd`: zero failures. No water simulation fixes were required by these checks.
- Focused floor/finish tests and all 47 card identities pass. Gallery JavaScript syntax checked.

Logs: `output/corridor-polish-v3/{native,water,physics,floors,cards}.log`. Water fixture isolates saves/settings/layouts; its script has a paired UID. Existing raw-image export warnings remain. This is bounded native verification, not exported-build or complete gameplay acceptance.

## Next action

Owner reviews floor variation, gray door color and wet closing captures, then supplies visual corrections.
