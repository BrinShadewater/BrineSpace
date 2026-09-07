# Room rendering cache pass — 2026-09-06

## Changes

Registered static prop polygons reuse triangulated meshes instead of submitting
fresh polygons each frame. The shared room base owns the helper; registered prop
renderers call it while their existing animated overlays, lighting, actors and
wall ordering remain unchanged. Mesh keys contain complete vertex/UV data, so
rotations, adjusted positions and changed texture coordinates use distinct meshes.
The texture is supplied at draw time.

The per-view mesh cache stops growing at 256 entries. Further geometry uses direct
drawing. It never evicts live meshes: Godot CanvasItem commands may retain their
RIDs until a later redraw. This avoids a renderer lifetime error found and fixed
in the first test. The full-room comparison retained 1,361 meshes across 33 views.

Embedded wall-edge setup caches by layout, open-side mask and omitted-side mask,
with a 64-entry cap. Every caller receives an owned copy; mutations cannot carry
an open/omitted doorway into another room, preview or navigation snapshot. Existing
prop geometry rebuild conditions remain in force. No gameplay logic changed.

The opt-in performance fixture disables focus-based auto-pause and explicitly
sets each scenario's pause state. One earlier auto-paused run was rejected rather
than counted as a speedup.

## Controlled native timings

1600x900, 25-room fixture, VSync disabled, sequential direct/cached runs using the
same test and application settings. Both modes include the earlier light batching.
The direct comparison uses `--uncached-prop-meshes --uncached-embedded-edges`.

| Scenario | Direct | Cached | Reduction |
|---|---:|---:|---:|
| Expanded Fit mean frame | 48.07 ms | 46.59 ms | 3.1% |
| Expanded close mean frame | 30.82 ms | 28.65 ms | 7.1% |
| Fit room setup | 4.90 ms | 4.36 ms | 10.9% |
| Close room setup | 3.18 ms | 2.75 ms | 13.4% |

These are local samples, not a guarantee on other hardware. Earlier exploratory
samples showed larger gains; the final controlled numbers above are the result
being reported. This does not solve the remaining ~21 fps Fit-view limitation.
It reduces CPU preparation rather than total GPU draw submissions.

Logs: `output/render-final-direct.*`, `output/render-final-cached.*`;
machine-readable comparison: `output/render-performance-comparison.json`.

## Verification

- Native cached/direct captures: 35 rooms, 33 views, all four rotations and a
  close-up with the awakened starter. Fixed animation time and camera. Every RGBA
  channel is identical in all five pairs. Mesh cache bounds are asserted.
- `tests/check_render_cache_parity.py` independently compares image channels;
  it avoids PIL's alpha-only RGBA bounding-box trap.
- Embedded geometry: 140 room/rotation cases pass, including rebuilding and
  switching open/omitted sides.
- NPC segment clearance, actual movement trace, Architect recovery, drone fleet,
  and production-room walker-path suites pass with no script errors.
- Native placement-door previews: 140 cases, zero failures.
- Culling pixel parity still passes in both performance runs.

Native captures were visually inspected. Existing raw-image loader warnings remain;
no new imported art or source assets were created. Animated overlays continue to
execute every frame; this cache covers static registered silhouettes only.

## Remaining performance work

Fit room contents still cost about 11.8 ms; floor and wall drawing about 15.4 ms
combined. Room setup overlaps those stage totals and must not be added again.
The subsequent retained-surface pass below addresses that floor/wall cost. Room
contents and GPU submissions remain live; they are the next rendering bottleneck.


## Retained floor and wall commands (September 6 follow-up)

`grid_canvas.gd` now owns three small CanvasItem drawing passes: floors (including
per-room light pools), walls, and live contents. The environment stays on the
parent. Godot retains the floor/wall commands until their state changes; animated
doors, machinery, crew, drones, effects and placement previews continue redrawing.
This keeps the existing room renderers and their ordering without raster caches.

The structural key covers placed-room data, visible rooms, cell size, power,
current light levels, external drone apertures, raised walls, selection, cryo ward
repair/pod count, and presence of the starter pod. Its deep snapshot is replaced
only when state changes. Power fades intentionally rebuild surfaces throughout
the fade: moving light pools to a separate pass produced a one-pixel seam change,
so the original per-room floor/light order is retained. Non-layered legacy art
falls back to rebuilding with animation time. Camera movement within the same
visible room set uses the inherited transform; zoom and visibility changes rebuild.

`--redraw-static-surfaces` keeps the direct reference path available. Earlier
mesh, edge and light-pool optimizations remain enabled in both comparison modes.

| Local 25-room scenario | Direct | Retained | Frame-time reduction |
|---|---:|---:|---:|
| Expanded Fit | 52.05 ms | 31.41 ms | 39.7% |
| Expanded close | 32.40 ms | 19.80 ms | 38.9% |

Sequential native runs at 1600×900, VSync off, with the existing warmed profiler.
These measurements compare the same current checkout, not the earlier mesh-pass
baseline. They are local samples, not a cross-hardware FPS guarantee. Fit still
runs around 32 FPS and close around 51 FPS; this is not a claim of sustained 60 FPS.
Validation costs approximately 0.25 ms at Fit and 0.17 ms close. Active room
contents still cost about 14.3/9.2 ms. Retention reduces command-building CPU work;
it does not eliminate the retained commands' GPU cost.

Evidence: `output/surface-profile-{direct,retained}.*` and
`output/surface-performance-comparison.json`. Both runs pass culling pixel parity.

`tests/test_surface_cache_parity.gd` and `tests/check_surface_cache_parity.py`
compare every RGBA channel across four rotations, close view, live rotation,
power on/off, a partial light fade, raised walls, placement/removal, drone door
opening/closing, culling, pan and zoom (17 pairs). Mutations are captured in the
already-retained renderer before switching to the reference, to expose stale
cache bugs. The fixture also asserts no static rebuilds while animation time
advances. This is a dedicated free-build/disabled-failure rendering fixture;
normal run rules are unchanged.

Final verification also asserts each tested structural mutation rebuilds in the
next rendered frame. All 17 pairs pass on the completed airlock integration,
with no script errors. Shared menu, workspace, placement doors, menu recovery and
Architect selection native suites pass; geometry, NPC clearance/movement,
Architect recovery, drone fleet and production walker-path regressions pass.
The transient missing airlock animation property seen during concurrent edits
was resolved by that integration; no workaround was added to the renderer.
