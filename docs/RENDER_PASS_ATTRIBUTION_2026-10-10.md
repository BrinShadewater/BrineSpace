# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: native rendering cost attribution

## Objective and acceptance

Identify which retained passes contribute renderer work on the40-room station.
This is diagnostic visibility subtraction, not an optimization or release acceptance.
The full PC/Mac goal remains open; preserve default quality in production.

## Accepted decisions and constraints

Actual debug=false shared QA executable/current modules, RTX4070Ti/1080p. Scene
paused/frozen, node updates disabled, original visibility restored after each case.
17groups forward/reverse,30measured frames per reference/hidden condition after
20query-drain frames:34records/2,040measured frames. Engine-global draw counters and
delayed viewport CPU/GPU timing queries; intervals/deltas are not additive. No
simulation, upload transition, physical-input or target-hardware acceptance here.
Muted secondary display, verified scratch profiles, no full package copies.

## Current state

Normal source/packages unchanged. Private fixture/driver under
output/renderdoc-tools-2026-10-08: `render-pass-attribution.gd`,
`run-render-pass-attribution.py`. Evidence under
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/render-pass-attribution-v5/:
`pair1-candidate.json`, `analysis.json`, `post-validation.json`, source/owner guards.

## Verification

All34cases restore game state and requested visibility. Loaded Main/Grid source
strings equal mounted source and current checkout hashes, after CRLF normalization.
Native matrix completed with no engine errors. Mean cost differences, reference
minus temporarily hidden group:

| Group | Draw calls | Render CPU | Render GPU |
| --- | --- | --- | --- |
| Environment aggregate |1,049|2.326ms|2.427ms|
| Terrain + derelicts |630|1.329ms|1.546ms|
| Room contents |535|1.128ms|1.380ms|
| Walls |535|1.197ms|1.655ms|
| Floor pair |439|0.919ms|1.056ms|
| Foundations |320|0.746ms|1.241ms|
| Doors |210|0.439ms|0.975ms|
| Foreground |201|0.511ms|0.994ms|

Aggregate environment includes its child groups; do not sum it with them. Frozen
exterior actors have only63calls and noisy near-zero CPU delta: this does not reduce
the separately established large animation-sheet upload problem during motion.
Atmosphere lookup found0nodes, so its zero delta is unmeasured, not proof of low cost.
Smaller resource/fog/light timing differences include negative/noisy values; do not
rank those as reliable gains. No inference that removing any pass is acceptable.

Visual restoration limitation remains explicit: only1/34final cases is byte-exact
against the initial full-screen capture. Earlier V1/V2 reproduce11changed pixels
on a tilted card border, despite a stable untouched baseline and identical game
state; V3 attempted fixed hidden hand/toast, V4 recursive hiding/source audit, then
V5 recorded pixel equality per row while retaining full UI and enforcing state/
visibility restoration. Those attempts are retained. A precise redraw/raster cause
is unresolved. This diagnostic does not pass visual acceptance or authorize a
pixel-changing batching implementation; unchanged exact optimization gates apply.

Native V5 completed, but the runner's post-check raised KeyError because the early
diagnostic exit omitted safe_image_failures. Post-validation inspects completion,
all34state/visibility checks, source equality and owner guard. That art-failure field
is unknown for this run; no zero invented. Future fixture now records it, no rerun
just to fill the missing field. Jobs terminal/shared config restored. Owner2,938
unchanged on all five attempts. New evidence8.34MiB plus24.77MiB scratch/10profiles;
no deletion retries or full copies. C126.98GiB/D79.03GiB free,20GiB storage floor.

## Next action

Split terrain/derelicts attribution, inspect their command generation, then prototype
an ordered batching/caching remedy for the measured contribution. Require exact
candidate/reference pixels and matched moving workloads before admission. Retain
the redraw/raster discrepancy as unresolved diagnostic evidence. Standard workload,
original bug/UI/save coverage, endurance, GTX1650/M1, latest-source packaging and
Mac signing/certification remain outstanding.
