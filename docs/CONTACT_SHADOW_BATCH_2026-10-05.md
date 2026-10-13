# Contact-shadow batching accepted in source

Updated: October 5, 2026 · BrineSpace · Release gates remain open

## Objective and acceptance

Implement R1 with unchanged shadow pixels/order, bounded caches, safe fallbacks
and matched station measurements. Source acceptance is separate from packaged
Windows/Mac performance and visual certification.

## Accepted decisions and constraints

Batch the three contact bands per footprint into one ordered triangle submission.
Keep projected shadows, room perimeter, prop/foot ordering and original StyleBox
colour selection unchanged. Tiny/adapted geometry, scale-dependent item
oversampling and unknown inheritance retain the original StyleBox path.
`--reference-contact-shadows` disables the batch for diagnosis.

Separate shape geometry from light colour: changing light must not regenerate
vertices. Caches are bounded to 256 geometries and 64 palettes; they retain no
textures or scene nodes. No art, layout, simulation, needs or save changes.

## Current state

- `scripts/contact_shadow_batch.gd` and paired UID: restricted geometry,
  conservative fallback, precision and oversampling handling, separate caches.
- `rooms/whole-room/room_lighting.gd`: per-foot integration, enabled by default.
- `tests/test_contact_shadow_batch.gd` and paired UID; `tests/index.json`: native
  pixel regression and lane registration. Set `BRINESPACE_TEST_USER_DIR` to the
  resolved scratch profile, or supply `--profile=...`, after isolating APPDATA.
- Evidence/runners: `output/shadow-room-integration-2026-10-05/`; initial authored
  comparisons in `output/shadow-authored-rooms-2026-10-05/`; final runtime room
  comparisons in `output/shadow-runtime-rooms-2026-10-05/`.

Geometry follows the pinned Godot implementation's float precision and AA shape;
the helper retains MIT attribution/license. Viewport oversampling is read through
the actual bound getter, with conservative fallback for item-scale inheritance.
[Pinned CanvasItem source](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/scene/main/canvas_item.cpp)
and [StyleBox source](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/scene/resources/style_box_flat.cpp).

## Verification

Final maintained native regression: **128/128 byte-exact images**, covering hull
clipping, corner arms, tiny feet, hidden/owned shadows, overlapping transparency,
moved props, fractional positions/zoom, nearby light colours and viewport
oversampling 0.8333/1/1.5/2, including item-scale reference fallback. It passed again
after enabling the default. An early diagnostic used an unavailable parent getter;
that attempt was invalid and corrected before acceptance.

Actual runtime helper: **192/192 byte-exact floor/shadow images** across Brine Core,
life support, tidal condenser and crew habitation, four rotations, three light
levels, two zooms and two oversampling levels. Each saves ten draw calls in that
floor pass. Representative floor output visually inspected. These are authored
layouts, not every owner layout or complete moving crew/prop composition. An
initial generated runner parse error was fixed before the successful run.

The existing 40-room benchmark ran at 1080p, 60 samples per phase, idle/zoom/lighting
at 1x/2x/4x. Three reference, three initial candidate and three revised candidate
processes ran sequentially, never alongside another native test. Active crew,
production and drones use the maintained fixture. All accepted runs have zero
engine errors and missing-image failures; all owner audits show **2,936 unchanged**
non-log files. Nine benchmark logs/JSONs retain individual phases and stalls.

| Aggregate across nine phases, median of three runs per phase | Reference | Initial colour-keyed cache | Accepted geometry/palette caches |
|---|---:|---:|---:|
| Mean of phase mean-frame-time medians | 43.344 ms | 43.969 ms | 39.883 ms |
| Mean of phase draw-call medians | 5,427.1 | 5,004.9 | 5,005.4 |
| Lighting shadow CPU, 1x / 2x / 4x | 1.304 / 1.306 / 1.332 ms | 9.049 / 7.605 / 5.340 ms | 1.085 / 1.046 / 1.047 ms |

The initial cache coupled colour to geometry and is rejected. Revised runs retain
only 73 geometries, with 7,156–7,976 hits and 10–12 palettes. The accepted candidate
reduces this aggregate frame-time measure about 8% and draw calls about 7.8%.
These are editor diagnostics on the owner's RTX 4070 Ti using the existing fixed
simulation-step harness, not a packaged real-time 60 FPS certification. Long stalls
persist, frame-time gates fail, and native Mac/Retina remains unverified. No claim
of a texture-memory reduction, clean endurance test or complete original-bug closure.

## Next action

Implement R2's zero-alpha mineral draw skip, retain its excavation/visual checks,
then measure the combined candidate. Keep this shadow reference switch for future
regressions. Full packaged 12/40-room workloads, 1440p/minimum PC hardware, native
Mac, long-stall attribution, memory budgets and original-report acceptance remain.
No release export or itch.io change was made.
