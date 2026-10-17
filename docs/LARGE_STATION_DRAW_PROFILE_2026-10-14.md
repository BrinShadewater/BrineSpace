# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: large-station drawing and submission

## Objective and acceptance

Profile the rebuilt Windows candidate's large station and move it toward 60 FPS,
preserving art, animation, compositing and owner layouts. Require matched actual-release
measurements and native image comparisons before admitting a renderer change.

## Accepted decisions and constraints

Godot 4.7.2 Compatibility, RTX 4070 Ti, 1920x1080, maintained mixed-large fixture:
40 rooms / 52 occupied cells, all four large rooms, active production/crew/drones.
GPU work serial, muted secondary-display QA with physical viewport input disabled.
Scratch APPDATA and resolved-profile guards throughout; all 2,948 owner files unchanged.
Marsh polish, object growth and Clone Lab gameplay remain parked. No art reduction,
engine change, commit or publication. Existing Windows delivery is unchanged.

## Current state

`scripts/grid_canvas.gd` now gathers actor display cells once during the synchronous
LIVE room paint. It keeps the exact named-crew getters and companion active/cell rules,
then disables the snapshot before child drawing. Calls outside that paint still query
current state, including changes made within one engine frame. Also removed a branch
that queried exterior drone-door openings although `_drone_door_frame()` always returns 0.
No refactor or other runtime-file change in this profiling task. Existing UID retained.

Source admission is modest CPU work reduction, **not 60 FPS acceptance**. The change is
not in candidate `brinespace-2fe5a9922a7a63cf`; no new export was made for this task.

Evidence: `C:/bs-large-profile-20261014/`; replayable drivers:
`output/large-profile-20261014/`. Measured private Grid overlay has reference/candidate
switches in one script, loaded before Main in an actual debug=false release copy.
`source-verification.json` verifies installed source code equals the measured candidate
path after removing trial switches and comments.

## Profile findings

Original three valid release runs: idle 25.15 / 25.98 / 26.16 ms averaged at 1x/2x/4x.
At 1x, grid draw callbacks average 11.72 ms; simulation step 2.16 ms; the CPU interval
between render signals averages 7.42 ms. Delayed viewport queries report render CPU
7.01 ms / GPU 6.07 ms. These overlapping/query-delayed measurements must not be added.
Live-room work includes large child callbacks; its 6.32 ms contains the 2.12 ms large
base callbacks. Door/light validation averages 1.21 ms, content callbacks 1.94 ms.

Fresh RenderDoc capture of the same candidate at the settled full-station camera:
**3,213 draw calls**, 2,594 single-instance draws; 1,784 default attribute/mesh draws,
1,213 ordinary canvas draws, 1,336 draws on Godot's white 4x4 texture. There are 6,284
texture binds and 6,899 vertex-array binds. Mesh command fragmentation matters alongside
texture switching. Capture: `station_frame298.rdc` (SHA256
`d0911fcbb1d42c2f9e183fbeead4c72d643816b44ba09b904117d19011a79697`),
`batching-analysis.json`. Capture overhead is excluded from performance acceptance.

Paused native submission census, baseline 3,212 calls:

| Layer hidden in diagnostics | Calls removed |
| --- | ---: |
| Large rooms, including contents | 517 |
| Walls | 504 |
| Environment passes | 472 |
| Ordinary retained room contents | 461 |
| Floors | 399 |
| Doors | 188 |
| Foreground actors/effects | 181 |
| Lights | 22 |
| Still seabed | 11 |

The whole grid removes 2,926 calls (286 UI calls remain), with delayed render CPU
6.75 -> 0.79 ms and GPU 4.92 -> 0.31 ms. This hides drawing only, retaining script work;
it is attribution, not a playable optimization. Conditional deltas can include newly
merged batches; groups overlap and timings are not additive. `census.json` preserves
all samples and individual large-room counts (Moonbay largest: 244 calls removed).

## Verification

Three complete matched actor-cache/dead-branch pairs, idle/pan/zoom at 1x/2x/4x,
180 samples per phase: **9,720 frames**, 27 exact simulation-state pairs. Mean frame
times, reference -> candidate: 28.273 -> 28.139, 29.886 -> 28.479,
29.554 -> 28.073 ms. Live-room callback reduction averages 192 / 482 / 465 us.
Whole-frame savings vary 0.13-1.48 ms and include timing noise; do not attribute all of
the larger frame deltas to this small script change. **0/27 candidate phases pass**
p95 <=16.7 / p99 <=25 / maximum <=100 ms. `actor-trial-analysis.json` and referenced
phase JSONs preserve the distributions and exact-state comparisons.

One intervening pair was minimized and rejected; its standalone candidate is excluded.
Two complete retry pairs hold the test window above others, retaining visibility guards.
No errors/missing art in completed timing runs. Reference and candidate share settings
within each pair; the first pair does not use the retry's always-on-top setting.

Native image comparison: 12/12 byte-exact adjacent comparisons at fitted zoom
0.13081395, 0.25 and 0.5, sequence reference/reference/candidate/candidate/reference.
All frozen state snapshots match. Initial invalid comparison contained a discovery
popup animation; subsequent drift was confined to an exterior drone even between
identical candidate settings. Hiding the popup, freezing simulation/processing and
waiting for pending drone textures to finish/retain produces zero differences.
`parity-ready.json` is final evidence; earlier failed/diagnostic captures remain.
Final station screenshot reviewed. This covers three frozen views, not all motion or Mac.

Installed-source headless checks pass: actor occupancy/call counts/next-paint refresh/
same-frame outside queries (zero failures), workshop retention guards (10 checks).
Private reference/candidate occupancy test also passes. Independent final diff review:
no actionable findings. Diff whitespace check passes. No required side effects in asserts.

## Next action

The next worthwhile rendering change should reduce ordered triangle submissions in
walls/environment or retained room bodies, selected from the capture rather than a
broad cache rewrite. Walls and environment each cost roughly 470-500 calls in this
fixture; large drawings are distributed across base, props and live layers.

A narrow monitor-waveform triangle packet could remove about 76 calls (38 waveforms
currently submit core plus two AA feather strips). This is an inference from matching
54/55-vertex draws, not yet a proven attribution or improvement. Existing WaterStrokes
helper is a possible implementation; requires waveform-specific exact pixels and
matched timings. Prior three-surface and persistent waveform mesh trials regressed:
do not reinstall/repeat them unchanged. A rectangular fast path in nursery's polygon
helper has little reach because most library bodies bypass it and use shaped triangles.
The prior Tidal static/live split also regressed and remains rejected.

Rebuild after the next meaningful accepted submission improvement. Full-action frame
gate, endurance/object growth, target PC and native Mac release acceptance remain open.
