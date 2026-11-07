# Tidal Condenser owner repair — native review complete

Final checkpoint: overhead wall family, matching architectural palette and independent
pump/monitor are integrated. Static all-direction, operating samples, direct/retained
parity and actual station pause checks are recorded below. This is agent review of
the source workspace; no export or owner acceptance is claimed.

`tools/verify_tidal_station_pause.gd` uses isolated saves and the real main-scene
process with a powered Tidal room. After dismissing fixture comms and disabling
its automatic polling, all four rotations advance the station clock by at least
0.35 seconds, then freeze both renderer clock and native room pixels when paused.
`output/tidal-owner-repair-2026-09-12/station-pause/result.json` records zero failures.
The initial comms-held result is preserved separately. No script/runtime errors;
environment raw-image export warnings remain outside this asset change. q0 full
station capture visually confirms an unobstructed visible room. Latest bounds
check `20260912-202834-headless` passes 176 furnished orientations.

Latest checkpoint: source-v2 fixes cartridge access and replaces the baked exterior
with a clean magenta key. `tools/build_tidal_owner_directions.py` registers all four
exact turns. Native q0–q3 in `output/tidal-owner-repair-2026-09-12/wall-native` reviewed:
inventory and inward access remain consistent, all banks mount on their selected
walls, no background rectangles. Stderr empty. Run `20260912-201204-headless` passes
176 layouts, 20 side variants and 47 cards. q0 card refreshed.

Riser mismatch traced to `rooms/whole-room/riser_catalog.gd`: no Tidal-specific
entry, so it falls back to `assets/riser-departments-v1/engineering/source.png`.
A Tidal-only override is now installed in `assets/room-risers-v3/registrations.json`,
using `assets/tidal-owner-v2/riser.png` and the original face/cap geometry (face
2,201,2002,312.8125; cap 2,171,2002,30). Grey-blue panels and dull-brass pipes match
the machinery. Native q0–q3 in `output/tidal-owner-repair-2026-09-12/riser-native`
were visually reviewed for palette, cap seams and doorway joins; stderr is empty.
Card check `20260912-201533-headless` passes all 47 identities; the selected card
is refreshed from reviewed q0. Source/card hashes are in `riser-review.json`.
Independent pump/monitor camera and effects remain open. Earlier candidate
findings below are historical, not live selection.

## Objective

Preserve the owner's strong machinery identity while making all equipment overhead
and inward-facing, and matching the background wall colors to the machinery.
Gameplay and character animation remain outside this task.

## Evidence and current state

Fresh q0–q3 baseline: `output/tidal-owner-repair-2026-09-12/before`.
North selects `assets/material-polish-v1/tidal-north.png`; sides select
`assets/tidal-directional-v1/tidal-sides.png`; south selects
`assets/room-facing-repair-v1/tidal-south-topdown-v3.png`.
North contains three coil returns, two vessels, three cartridges and a console.
South has only two returns and lacks the console. Side banks retain tall cylinder
and cabinet faces. The rear wall uses orange engineering panels against the
grey-blue/brass machinery. Independent pump and monitor also need camera review.

## Candidate review

`assets/tidal-owner-v2/source-v1.png` preserves the full inventory but is NOT live.
It fails inward access: the three horizontal cartridge releases point left rather
than toward the bottom operator edge. Its RGB background contains a baked
checkerboard, not transparency. Console top-plane clarity also needs review.
Do not register or propagate this candidate unchanged. Exact prompt is preserved.

## Next action

Independent-equipment checkpoint: `equipment-source-v1.png` is rejected for
retaining the tall filter elevation and rear cartridge releases. Its prompt and
review are preserved. `equipment-source-v2.png` uses explicit plan geometry without
the elevation reference: circular filter lid, flat dial/screen/keypad and cartridge
releases toward the operator. `tools/build_tidal_equipment.py` keys the magenta
exterior and pull-tab apertures, removes magenta fringe, crops each component and
prepares exact four-facing PNGs. `equipment-build.json` records dimensions and
hashes. These are selected in `tidal_condenser_view.gd`. Native q0–q3 in
`output/tidal-owner-repair-2026-09-12/equipment-native` were reviewed for camera,
inward access and room fit. Stderr empty. Run `20260912-202340-headless` passes
176 layouts, 20 side variants and 47 cards. Gauge interior covers the baked needle;
the replacement needle and screen traces use artwork's quarter-turn transform.
Direct operating samples are now visually reviewed in
`output/tidal-owner-repair-2026-09-12/equipment-states/states.png`, produced by
`tools/capture_tidal_equipment_states.gd`: four facings, paired pump/monitor,
offline and operating clocks 0 and 1. Screen traces stay within the source display,
offline screens are blank, and gauges remain aligned. Stderr empty. This fixture
uses fixed clocks; actual station pause remains open. The fixture now also captures
`retained.png` through production `room_content_canvas.gd`; RGB pixel comparison
against the direct sheet is identical across all 24 prop/state/facing samples.
Native process completed with empty stderr. The independent prop visual bounds
now follow the new oriented texture rather than the old atlas outline. The older
tidal playtest checks legacy `effect_marks`
coordinates, so its screen assertion cannot establish the new overlay's alignment.

Continue the owner asset queue with Command Center's matching wall and overhead
equipment review. Tidal's requested art changes have passed the recorded native
checks; keep owner acceptance distinct from this verification.
Wall-family and riser reviews are agent verification, not owner acceptance.
