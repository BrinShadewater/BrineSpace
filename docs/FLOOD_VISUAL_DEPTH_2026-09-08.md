# Water depth and performance handoff

Updated: September 8, 2026 · Project: BrineSpace · Task: readable flooding and smooth transit

## Objective and acceptance

Owner requested stronger water effects, visibly distinct heights, and correction
of slow/laggy swimming playback. Native visual review remains with the owner.

## Accepted decisions and constraints

Retain continuous leaks, open-door transfer, powered pumps and the existing
low/medium/high/critical thresholds (25/55/85%). Keep survival rules and production
movement. Dedicated fixtures alone stage water and disable normal run progression.

## Current state

- `scripts/flood_visuals.gd` and paired floor/submersion shaders render retained
  animated puddles/caustics, rising equipment waterlines, submerged crew bodies,
  exposed swimming heads, critical bubbles, wakes and the front cutaway depth.
- `scripts/grid_canvas.gd` excludes changing water/cracks from structural cache
  keys. `rooms/full-wall-v1/split_wall_prop.gd` avoids repeating furniture placement
  searches for unchanged layouts while still applying live layout edits.
- `scripts/room_content_canvas.gd`, `scripts/crew_sprite_player.gd`,
  `rooms/whole-room/nursery_whole_view.gd` and `scripts/room_flooding.gd` connect
  rendering to live water and the simulation clock. New scripts/shaders have UIDs.
- `tests/test_flood_rendering.gd` guards waterline/shape behavior, cache stability,
  rotation invalidation and live edits. Transit capture now uses 60 simulation fps.
- Four native heights: `output/flood-heights-v2.png`. Initial implementation and
  prior 15-fps replay remain historical evidence in `ROOM_FLOODING_2026-09-08.md`.

## Verification

Room flooding, flood rendering, station systems, live-layout refresh, and native
four-height/Save-Continue fixtures pass. Live-layout shutdown retains its existing
resource-in-use warning; no runtime script failures in passing checks.

Native uncapped three-room profile, 60-frame warmup then 180 measured frames:
median frame time 206.6 ms before, 107.0 ms after structural caching, 9.5 ms after
placement caching, and 10.5 ms with final effects (p95 11.4 ms). Final simulation
median 0.46 ms. These are fixture measurements, not a full-station FPS guarantee.
Reports: `output/flood-profile-{before,static-fix,layout-fix,after}.json`;
reproducer: `output/profile_flood_transit.gd`. Native logs use `output/flood-v2-*`.

60-fps native replay: `output/flooded-transit-v2.mp4` (2,125 frames / 35.42 s).
All three routes pass, beginning/doorway/ending frames visually reviewed, and full
MP4 decode passes. Capture log: `output/flood-transit-v2-native.log`. Scoped
whitespace check passes.

## Next action

Review the native depth comparison and smooth transit replay for art acceptance.
Tune visual strength if requested; broader populated-station performance has not
been measured in this task. No release/export or unrelated asset batches run.
