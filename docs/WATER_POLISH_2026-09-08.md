# Water physics and graphics polish

Updated: September 8, 2026 · Project: BrineSpace

## Objective and acceptance

Owner requested another water systems, physics, shadow and graphics polish pass.
Native four-stage and doorway captures reviewed; owner art acceptance pending.

## Accepted decisions and constraints

Existing water rates, thresholds, survival durations and collision-based crew
routes remain. Water is still a per-compartment depth model, not a fluid mesh.
No unrelated artwork, personal layout or broad renderer refactoring.

## Current state

- `scripts/room_flooding.gd`: clamp local leaks/pumps before simultaneous paired
  door exchange. This prevents nearly empty pumps from sending nonexistent water
  downstream, and separates saturated overflow from door transfer. Equal-depth
  neighbors skip connectivity/door lookups. Invalid elapsed time returns safely.
- `scripts/flood_visuals.gd`: subtle directional doorway currents follow actual
  aperture and depth difference; broader, softer underwater crew shadows;
  unchanged prop uniforms skip redundant updates. Material reuse/reflooding resets
  uniform state correctly. Shared clock/transform reads reduce repeated work.
- `scripts/flood_surface.gdshader` reduces deep-water caustic glare;
  `scripts/flood_submersion.gdshader` avoids bright menisci on dark shadow pixels.
  `rooms/whole-room/nursery_whole_view.gd` uses the depth-sensitive crew shadow.
- Extended `tests/test_room_flooding.gd` and `tests/test_flood_rendering.gd`.
  `tests/playtest_room_flooding.gd` explicitly releases the selected architect
  before the saved fixture, avoiding invisible crew when startup is in cryostasis.
- Preview: `output/flood-heights-polish.png`; native doorway captures:
  `output/flood-polish-transit-360.png` and `-1200.png`.

## Verification

Physics, rendering/cache reuse, native Save/Continue and full three-crew native
transit pass. Added cases cover nearly empty pumps, saturated leaks, reverse room
iteration, half apertures, isolation, nonfinite time, dry-room skipped work and
reflooded/reused shader slots. Scoped whitespace check passes.

Same uncapped three-room fixture, 60-frame warmup / 180 measured frames:
median 10.98 ms (previous 10.50), p95 12.52 ms (previous 11.44), simulation median
0.453 ms (previous 0.457). This pass is not a measured frame-rate improvement;
added currents/shadow detail carry a small rendering cost. Full-station scaling
was not measured. Reports and logs: `output/flood-profile-polish.json` and
`output/flood-polish-*.log`; reproducer `output/profile_flood_polish.gd`.

## Next action

Owner visual review of depth/shadow strength. Larger populated-station profiling
would be the next performance investigation; no export or release was run.
