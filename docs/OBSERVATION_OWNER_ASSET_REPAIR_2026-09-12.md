# Observation owner repair — in progress

Current owner direction supersedes the older fixed-north installation decision:
movable equipment must work top-down/inward through rotation, and portholes belong
to background architecture. Preserve warm reading-room identity and desk/chair.

Diagnosis: `observation_room_view.gd` explicitly calls its parent with rotation0,
constructs fixed rotation0 layout, and draws `observation_north` (including large
porthole) as a furniture prop at ART_ORIGIN(-180,-258). `north_wall.gd` skips this
room entirely. Existing architectural source `assets/room-risers-v2/observation_room.png`
is registered but therefore not drawn. Side shelves use library companions;
desk/chair and reading set are separate fixed-facing sprites.

Fresh baseline: `output/observation-owner-repair-2026-09-12/before`, native capture
completed with empty stderr. Its q0–q3 are not evidence of four furnishing rotations,
because the renderer deliberately pins that state.

`assets/observation-owner-v2/riser.png` is a new architectural palette candidate:
walnut panels, brass fittings, left round porthole and right wide ocean window,
central doorway bay clear. Exact prompt preserved. It is not selected yet.

Next: create overhead window-free north shelving matching side inventory, restore
architectural wall drawing while removing the window-bearing furniture prop, then
rotate furniture and office set with actual room direction. Verify all doorway
orientations, shelf/desk/chair scale, retained rendering and card selection.
No gameplay or character animation changes. No new acceptance/export.

Separation checkpoint: architectural wall drawing restored for Observation and
the existing v2 registration now selects the walnut/brass wall. Porthole-bearing
`observation_north` artwork is replaced by the new overhead cabinet (books, plants,
globe, helmet, fossil and fish illustration). Raw source, alpha processing and four
turns preserved by `build_observation_shelves.py`. Native q0 in
`output/observation-owner-repair-2026-09-12/separated-native` reviewed: windows live
above furniture, display shelf is window-free and wall joins are intact. Stderr
empty; `20260912-210208-headless` passes176 layouts. Rotation is STILL pinned,
and existing desk/chair remain frontal; this checkpoint does not complete those
owner requests. Next: overhead office set and true rotated furnishing geometry.

Office source checkpoint: `office-raw.png` and prompt preserve an overhead walnut
desktop with book/blotter/green reading lamp, and a separate brown leather chair
with its narrow backrest at the bottom and seat toward the desk. Native alpha is
present; `build_observation_office.py` removes haze below16 and prepares exact q0–q3
turns. Desk crop1115×580; chair427×402. Sources inspected for overhead camera and
relative orientation. Not selected yet; room-scale fit, reading-set state treatment
and actual rotated geometry remain to be integrated and verified.

Rotation integration: Observation now uses the requested quarter in layout and
embedded configuration. Overhead desk/chair and north cabinet rotate with their
rectangles; existing side shelf inventories use registered-alpha exact turns from
`build_observation_side_turns.py`. Architectural windows stay on the background wall.
Initial native `rotated-native` and layout test exposed old default overrides that
reapplied identical desk/chair positions in every rotation, blocking the south
door and overlapping shelves. `update_observation_rotated_layout.py` removes only
those four office position/size fields per Observation layout, with backups.
The corrected176-layout check passes in `20260912-210905-headless`. Native corrected
capture is `rotated-layout-native`; all four views visually reviewed with consistent
desk/chair relationship, inward shelves, clear entrance and fixed architectural
windows. Stderr empty. Reading-lamp state, retained rendering and cards remain open.

Reading-state checkpoint: `draw_reading_light` adds a steady powered warm area
on the desktop using the same quarter-turn transform as the art. Native fixture
`capture_observation_furnishing_states.gd` renders four rotations × offline/two
powered clocks. Visual review confirms contained light; direct/retained RGB are
identical, powered clock samples identical, off/on differ. Evidence at
`output/observation-owner-repair-2026-09-12/furnishing-states`; stderr empty.
Selected q0 card refreshed. Actual station and existing-cache power transition
remain to verify; fresh retained canvases alone cannot prove invalidation.


Final native state checkpoint: existing retained canvases were reused through
off/on transitions. All six transition rows match the corresponding direct
reference, and initial direct/retained pixels match. Actual station fixture
`verify_observation_station_pause.gd` resolves the view through `rare_room_views`;
four rotations pass with powered state, advancing running clock, frozen paused
clock and identical paused native pixels. Evidence: `station-pause/result.json`
and paired captures under `output/observation-owner-repair-2026-09-12`.
Native q0 station image reviewed for architecture, overhead furnishings and entry.
The run includes existing environment image-load/export warnings; no export was
tested. Earlier 176-layout, 20-side and 47-card checks remain scoped evidence.
Owner acceptance remains separate. Next room in the asset queue: Salvage Workshop.
