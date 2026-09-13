# Derelict condition handoff

## Lights and completed repair — owner clarification

Owner confirmed lights start OFF in derelicts. Completed repair removes debris
and weathering; normal lighting becomes available with power and the interior
switch. Repaired rooms awaiting their first power allocation remain unlit.

`grid_canvas.gd` now rejects unrepaired light targets and stale cached levels,
omits companion preview light pools and selects lights-off ambient shading through
`derelict_material.gdshader`. Normal repaired rendering retains its own lighting.
North-wall drawing configures the selected shared recovery view before accessing
geometry, resolving the earlier empty-layout failure with multiple restored wards.

Native `test_derelict_lights.gd` (with UID) passes all six rooms: actual 8-Metal
repair charge, partial and completed 18-second repair, stale light rejection,
waiting for power, powered-on and interior switch states. The fixture supplies
power-map states explicitly after the real repair; it does not claim economy
balance validation. Eighteen native captures: `output/derelict-lights/`; cryo
unrepaired, repaired/off and repaired/on views reviewed. All six repaired rooms
coexist in the fixture. Test report: `output/test-runs/20260912-140959-native/`.
Extended material test confirms unlit alpha preservation and passes:
`output/test-runs/20260912-141117-native/`. Relevant diff check passes.

Current outcome: source implementation and native verification complete; owner
review next. No EXE rebuilt. Previous lit derelict captures below are superseded.

## Surface weathering revision — owner correction

The owner requested weathering on the floors, walls and props themselves. The
first debris-only pass below is superseded by a condition-only canvas material:
mottled grime, pitting and patches of exposed oxide now affect source surfaces.
Wear follows each texture through pan/zoom, preserves alpha and dark recesses,
and disappears completely when the room is repaired. No raster source was edited.

Added `scripts/derelict_material.gdshader` and UID; `grid_canvas.gd` isolates
derelicts between the existing wrecks and exterior actors so active station art,
ocean and UI do not receive the material. Retained and diagnostic environment
paths keep this order. `tests/test_derelict_material.gd` and UID plus its native
lane in `tests/index.json` cover actual shader pixels.

Native material check passes: 48,992 changed equipment pixels, zero changed alpha
pixels, exact frame repeat and source-attached translation, exact return to the
original when the material is removed. All six restored-room interior comparison
regions are RGB-identical to the prior pass (494x456 screen pixels per room).
All six derelict views captured; medical, workshop, storage and pet surfaces
reviewed. Evidence: `output/derelict-material-v2/`, including original debris-only
captures, `first.log`, `material-test.log`, and `restored-parity.txt`.
Current native views: `output/derelict-material-v2/verified/`.
Environment cache test passes, and all seven cached/direct screenshot pairs are
RGB-identical (baseline, placement, removal, wall toggle, pan and zoom). Evidence:
`output/test-runs/20260912-034754-native/` and
`output/derelict-material-v2/environment-parity.txt`. Relevant diff check passes.
No executable rebuilt; owner visual review remains the next step.

Updated: September 12, 2026 · Project: BrineSpace · Task: visibly derelict rooms

## Objective and acceptance

Recoverable rooms should read as abandoned underwater compartments while rescue
subjects, department identity and door approaches remain readable.

## Accepted decisions and constraints

Visual condition only; repair, recovery, saves and geometry remain authoritative.
Decay disappears on repair. Cards depict restored rooms. Preserve original art
and unrelated working changes. Source checkout only; no executable rebuilt.

## Current state

Both human cryo wards, Marsh's charging chamber, River's workshop, Josh's storage
and Margot's pet ward now use painted sediment, biofouling, broken deck pieces,
cables and rusty grates beneath furniture, plus localized wall corrosion.

Changed: `rooms/derelict-condition-v1/` (unchanged imagegen source, exact prompt,
manifest and README), `scripts/derelict_condition.gd` and UID, selection in
`scripts/grid_canvas.gd`, floor hook in `nursery_whole_view.gd`, wall hook in
`nursery_south_facing.gd`, removed thin floor marks in
`rooms/underwater/batch-two/cryo_chamber_view.gd`, native fixture and UID,
CURRENT_STATUS and maintained material-review workflow.

## Verification

All six found compartments reviewed natively at 0.55 zoom; twelve found/restored
captures in `output/derelict-condition/after/`. Final fixture passes without
SCRIPT ERROR/ERROR entries: `output/derelict-condition-acceptance.log`.
Existing raw PNG import warnings remain. Restored screenshots use explicit visual
fixture setup, not a claim of manual paid gameplay testing.

`test_cryo_recovery`, `test_architect_recovery`, `test_companions`: all pass,
including paid recovery, pause and persistence. Evidence:
`output/test-runs/20260912-033250-headless/`. Relevant diff whitespace check passes.
Generated source: 1254-square RGBA, 863,922 fully transparent pixels, transparent
center, hash recorded, LFS filter verified. No pixel editing or recoloring.

Rejected procedural floor candidate looked like flat markers. An intermediate
fixture incorrectly marked companion rooms as human recovery rooms; corrected.
Accumulating several restored fixture wards also exposed an empty shared layout
in `north_wall.gd:56`. Final visual comparisons isolate one restoration at a time;
mixed restored-room riser behavior remains an unresolved separate follow-up, not
a proven regression from the visual condition layer.

## Next action

Owner visual review. No release or multi-resolution acceptance claimed. If the
mixed-ward riser issue is pursued, reproduce with several recovered wards and
inspect room-view recovery/cache changes before north-wall drawing.
