# Zoom, restore and large-station follow-up

Native Godot 4.6.1 Compatibility, 1600×900, VSync disabled, RTX 4070 Ti.
These are local fixture measurements, not performance guarantees.

## Changes

- Department door parts now retain canonical geometry by frame, orientation,
  department, corridor shape and prototype variant. Light, crew depth and zoom
  remain live. The cache is capped at 256 entries and stores no raster images.
  `--rebuild-door-parts` restores the direct geometry path.
- Room content slots keep their bounds and classification when only zoom changes.
  Native drawing commands still refresh with the original draw transform, retaining
  pixel precision; this does not claim complete command reuse at arbitrary zoom.
- Fit supplies the station center to the zoom operation immediately, including
  its deferred layout correction, instead of first centering on the previous view.
- Navigation inside one ordinary authored room uses clear endpoints plus the
  existing exact blocker sweep. The cell and closed-door restrictions are convex;
  intermediate samples repeat work without adding clearance information there.
  Corridors, legacy rooms and every cross-cell segment keep sampled checks and
  the exact sweep. `--sample-all-navigation-segments` selects the old path.
  Active saved routes are still validated; no navigation is deserialized.
- The large-station fixture now separates simulation, script drawing stages,
  and (when available) engine viewport CPU/GPU render timings.

## Paired local measurements

Baseline: `output/hitch-baseline.log`. Updated:
`output/hitch-final-profile_large_station.log`.
Structured comparison: `output/hitch-comparison.json`.
Both runs use the same earlier floor, prop and BRINE retention features.

| View | Before mean ms | After mean ms | Change |
|---|---:|---:|---:|
| 50-room Fit | 41.18 | 37.78 | 8.2% lower |
| 50-room close | 16.95 | 16.22 | 4.3% lower |
| 101-room Fit | 76.03 | 75.49 | 0.7% lower; effectively unchanged |
| 101-room close | 20.70 | 19.42 | 6.2% lower |

Construction completes during the 100-room fixture, so it has 101 rooms when
sampled. These changes preserve the GPU draw-call count. The 101-room Fit view
still runs around 13 FPS; reduced script work has not solved that view.

| Interaction | Before affected frame ms | After affected frame ms |
|---|---:|---:|
| Construction completes | 30.80 | 27.85 |
| Menu opens | 38.62 | 36.91 |
| Menu closes | 27.70 | 27.18 |
| Fit | 235.57 | 204.00 |
| Normal view | 51.50 | 44.14 |
| Save | 10.28 | 9.77 |
| Restore | 594.93 | 461.72 |

Fit improved 13.4%, normal-view transition 14.3%, restoration 22.4%.
Interactions are single cold transitions with twelve following frames, not
repeated-trial percentiles. Restore includes reading the saved state into an
already loaded game with fresh NPC instances; it is not full title-screen
Continue or cold art loading. Restore CPU itself was 565.01 → 433.77 ms.
Other concurrent desktop activity can affect these timings.

## Verification

- `tests/test_hitch_parity.gd` / `tests/check_hitch_parity.py`: 33 native
  pixel-identical RGBA pairs, including all four rotations, power fades,
  door motion, placement/removal, culling/panning/zoom and busy crew/drone frames.
  Static counters stay retained while live animation advances. Current fixture
  includes 42 rooms and 37 room views, including concurrent catalog additions.
- `tests/test_navigation_segment_parity.gd`: 26,624 comparisons against the old
  sampler, covering every open-side mask, random segments, stationary points,
  exact blocker edges and cell crossings; zero differences.
- Existing near-tangent clearance, movement trace, save, menu recovery, shared
  menu, UI workspace and architect recovery checks pass with no script errors.
- Native close view inspected. Existing raw-image loader warnings remain.

## Remaining limits

The Fit hitch is reduced, not eliminated. Static floor/wall/prop commands still
rebuild for a new scale. Further retention must preserve original transform
precision, depth ordering, visibility and light-fade invalidation. Active graph
construction still blocks restoration. A future staged loader must avoid exposing
partially restored state or advancing crew before route validation finishes.

Detailed script stage timings overlap: `live_rooms` includes room setup and
content preparation; `room_contents` includes front doors and lighting. Do not
sum them together with their child timings. The interaction stage snapshots in
older logs are the last observed redraw, not a breakdown of the whole transition;
the current fixture omits those snapshots to avoid presenting stale values.

## Renderer diagnosis

Additional timed-viewport run: `output/hitch-gpu-profile.log`. At 101-room Fit:

- Simulation: 2.90 ms/frame.
- Room/rear-door preparation: 25.04 ms/frame, including 6.16 ms content preparation.
- Front doors and lighting: 9.51 ms/frame.
- Retained content draw callbacks: 2.48 ms/frame.
- Engine viewport rendering: 25.77 ms CPU and 21.93 ms GPU.
- Total observed frame: 73.74 ms; 11,687 draw calls.

CPU and GPU timelines overlap, and viewport timing is a separate diagnostic run;
these values must not be added as a serial frame budget or substituted into the
paired comparison. Both drawing preparation/submission and GPU cost are material;
simulation is a small share. The next experiment should target retained door/light
commands and measure both CPU submission and GPU time, with the same exact-image
checks. Reducing simulation update frequency would address little of this cost.

The production route sweep also passed: 6,400 room pairs, 2,916 compatible pairs,
67,068 graph segments, zero failures. Its first attempt overlapped another task's
write to `main.gd` and saw a transient UTF-8 load failure; the completed rerun is
recorded in `output/hitch-retry-test_production_ten_walker_paths.log`.

Final completed checks: `output/hitch-verified-results.json`. The workspace test
also verifies Fit settles within two pixels of the station center.
