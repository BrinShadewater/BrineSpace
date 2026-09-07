# Reactor south-facing registration

The existing `reactor` uses `layout_reactor_cross`: four ports with perimeter
walking. The new candidate is registered in `rooms/whole-room/reactor_view.gd`,
outside normal station/card consumers. It reuses the deterministic cross shell,
with one central chamber and two south-facing support assemblies. Central ground
footprint is 104x80 world units, centered at zero; visible height is registered
separately. This leaves clearance for the existing 0.30-cell perimeter anchors.

`playtest_south_facing.gd --reactor` passes 12 front/behind comparisons and prop
routes over four layouts, 1616 perimeter-segment collision samples, fixed-facing
anchors/bounds, ports and room-level active/offline/pause checks. Initial log:
`output/whole-room-pilot-01/reactor-depth.log`. Its summary incorrectly printed
16 pairs from the old four-prop fixture; the test now reports the actual count.
Native q0 was inspected: central amber chamber stays upright, routes remain
open, no generated closed doors are used. Minor floor patch/value repetition
remains visible. This is not actual-station movement or owner art acceptance.

The candidate and exact prompt/review records are in the pilot output folder;
the runtime copy is `rooms/whole-room/reactor-candidate.png`. No reactor costs,
production, risk mechanics or player saves changed. Next: matching card and
actual-station integration, including true perimeter walker samples and seams.

The repeat `reactor-depth-counted.log` failed q1 advance-dependent checks after
an initially passing run. Inspection found live keyboard shortcuts were still
enabled in the automated fixture, allowing desktop input to change pause/state.
This is a plausible interference source, not a captured key-event diagnosis.
The harness now disables unhandled keyboard input as well as `_process`, leaving
only explicit test-driven state/motion. Normal room input is unchanged. Both
initial and repeat logs are retained; use the isolated-input rerun as current
evidence rather than silently discarding the failure.

## Station integration and actual perimeter routes

The Reactor now uses the layered grid renderer and Godot-baked
`reactor-card-v1.png`; original art remains on disk. The shared station harness
supports `--reactor`. The initial pair entry test passed, but extending coverage
to exits from all three other arrival sides exposed collisions once the real
crew foot offset was included (`reactor-perimeter-station.log`).

Main's Reactor-only perimeter path now inserts intermediate corner waypoints;
other room paths are unchanged. The first 0.22-cell corners still grazed rotated
support equipment in two samples (`reactor-perimeter-corners.log`). The revised
0.20-cell corners leave clearance between supports and chamber without changing
art or colliders. The test samples 1212 exit-route positions in addition to 404
pair-entry positions over four rotations. Costs/production/discovery are unchanged.
Five regression suites passed in `test_*-reactor.log` before the final 0.20 corner
adjustment; broader viewport and post-final-adjustment checks remain pending.
