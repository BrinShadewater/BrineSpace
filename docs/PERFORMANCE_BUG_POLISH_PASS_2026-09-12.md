# Performance, bug and polish pass

Updated September 12, 2026 · Brine Space source workspace. No export or commit.

## Objective and acceptance

Profile current gameplay, fix reproducible bugs and unnecessary rendering work,
and improve actionable feedback. Preserve the other sessions' art and animation
changes, prototype economy and saved-game behavior. Use scoped regression tests
and native visual evidence; this is not a claim that the whole game is bug-free.

## Findings and changes

- `scripts/grid_canvas.gd`: static floor/wall keys no longer include the whole
  airlock cycle, fire intensity, prepaid sprinkler seconds or electrical-repair
  progress. Those live changes previously rebuilt every visible floor and wall.
  Airlock chamber **water level remains in the key**, because its wet floor is
  painted on the static pass. Structural changes and light state still invalidate.
- `scripts/airlock_cycle.gd`: exterior clearance now respects actual blocking
  wreck state, resource deposits and queued construction. Cleared wreck records
  and depleted deposits do not block an otherwise empty approach. Bounds and
  occupied rooms still block it. Manual cycling and expedition readiness agree.
- `scripts/airlock_panel.gd`, `crew_expedition.gd`: feedback identifies the actual
  obstruction and cell instead of only saying to clear the approach.
- `scripts/room_fire.gd`: fire-alert refresh checks that its UI exists, matching
  the flood-alert helper. The gameplay-polish fixture previously printed success
  and exited zero while emitting a nil-control script error; the maintained test
  runner correctly classified it as a failure. It now runs without that error.
- New `test_live_surface_retention.gd` and `test_airlock_clearance.gd`, paired UIDs
  and render-perf/crew index entries. No animation or raster sources changed.

## Measurements and verification

`tests/profile_station.gd` completed on a real display at 1600×900. Its diagnostic
fixture measured 10.53 ms small-active, 23.27 ms with 25 rooms fit in view, 14.18 ms
close up and 3.64 ms paused. Culling pixel comparison passed. These are baseline
diagnostics, not a post-change whole-game FPS claim. Summary and log are under
`output/performance-pass-20260912/station-baseline.*`.

The focused live-state fixture demonstrated **59 floor and 59 wall rebuilds over
60 frames before the change, zero afterward**. Sampled frame time was 9.41 ms
before and approximately 6.1–6.3 ms afterward. This is a small fixed-state fixture;
concurrent sessions and changing art prevent treating it as a controlled global
speedup. The work-count reduction is the reliable result.

The first optimization attempt failed exact pixel comparison: chamber water had
been omitted from the static key. Difference bounds isolated the wet chamber.
Keeping water level in the key corrected the mismatch. Final retained pixels
match a forced floor/wall rebuild exactly, and water/rotation invalidation tests
pass. Do not suppress a failed parity check to retain a benchmark improvement.

- Before-fix evidence: `20260912-204735-headless` (polish nil-control error),
  `20260912-204925-native` (59 rebuilds), `20260912-205003-headless` (12 clearance
  failures across four directions).
- `20260912-205032-headless`: clearance, full diver-mining journey and gameplay
  polish pass. Prior focused power regression also passes.
- `20260912-205228-native`: moving exterior hatch, pause/power/Continue and
  corrected live-state retention checks pass.
- `20260912-205336-native`: final live-state parity and blocker UI checks pass;
  existing surface-cache fixture passes reuse/invalidation assertions across 47
  rooms, 44 views and four rotations. That existing fixture captures comparisons;
  its success message alone is not whole-image equivalence for every capture.
- `20260912-205346-headless`: room fire and hazard-chain checks pass. Render-bound
  fire gameplay was correctly skipped and then run in the native lane.
- `20260912-205642-native`: fire gameplay passes after correcting its isolated
  flame sample to include a real room ID. The earlier native run emitted missing-ID
  errors from exterior-light drawing despite exiting zero; no production fallback
  for malformed room dictionaries was added. This is a fixture repair, not a
  demonstrated player-facing fire crash.
- Scoped diff whitespace checks, new test index/UID checks and final exact image
  comparison pass. The cache-invalidation lesson is recorded in the project and
  installed gameplay-preview-contract skill reference; current status is updated.

Native reviewed evidence: `output/performance-pass-20260912/live-state-cached.png`,
`live-state-rebuilt.png`, and `airlock-blocker-feedback.png`. The latter shows a
disabled exterior-cycle button and the resource deposit's coordinates.

## Remaining limits and next action

The 25-room fit-view baseline exceeds a 16.7 ms frame budget. This pass removes
unnecessary rebuilds during specific live changes, not every dense-station cost.
Flooding/draining still legitimately invalidates the chamber floor. A later
optimization could move only that wet-floor overlay to an appropriate live layer,
but must preserve actor/door/prop ordering and pixel parity.

Full unretained diagnostic rendering has a previously recorded dark-lighting
discrepancy; it is not equivalent to direct room-content rendering with normal
station lighting. This pass does not establish or repair that broad diagnostic
mode. The original power/battery and west-turbine playtest reports, cryopod motion
quality, ongoing art/animation work, 100-room stress and integrated release smoke
testing remain separate checks. No balance changes or packaged build were made.
