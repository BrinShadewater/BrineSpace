# Pre-render optimization handoff

Updated: October 5, 2026 · Project: BrineSpace · Task: PC/Mac release readiness

## Objective and acceptance

Meet the approved frame pacing, loading, memory, stability and visual gates on
actual Windows/Mac packages. Release remains blocked; no upload. Preserve selected
art, timing, owner layouts and saves. This milestone accepts a source optimization,
not a new certified package.

## Accepted decisions and constraints

Retain up to four prepared Research Lab rotations on the existing shared room view.
Own mutable layout/prop/dressing copies, invalidate on layout/geometry edits and
bypass Studio. Normal configuration still updates doors, running state and clocks.
No texture, animation or quality reductions. `--rebuild-research-rotations` provides
the matched baseline. Avoid a broad renderer refactor.

## Current state

Changed runtime: `rooms/full-wall-v1/research_lab_view.gd`.
Regression: `tests/test_research_rotation_cache.gd` and paired UID; native lane in
`tests/index.json`. The frozen **brinespace-124c70736fbfb879** package predates this
cache and remains unchanged. Previous packaged results remain in
`PERFORMANCE_PACKAGE_RESULTS_2026-10-05.md`.

Temporary profiling of 43 callback-bearing scripts was restored. One instrumented
107.3 ms frame had 80.9 ms before rendering; inclusive surface callbacks cost
36.0 ms and wall slots 14.7 ms. Draw-stage samples included Research preparation
5.4 ms and solar preparation 3.9 ms. These nested timings must not be summed as
independent components. A separate 313 ms frame spent 198.8 ms in fog drawing,
following a 91.875 MiB drone-atlas upload on the preceding frame. This correlation
does not prove the upload caused the whole stall.

## Verification

Three developer-native runs per path, large station, 1080p, 180 measured frames
per action/speed, same default quality and source, no competing native process.
Median per-run p95 (ms):

| Action | Speed | Rebuild baseline | Cached | Change |
|---|---|---|---|---|
| Zoom | 1× | 57.627 | 56.438 | 2.1% lower |
| Zoom | 2× | 65.522 | 65.869 | 0.5% higher |
| Zoom | 4× | 66.646 | 67.768 | 1.7% higher |
| Lighting | 1× | 75.247 | 70.381 | 6.5% lower |
| Lighting | 2× | 74.625 | 69.746 | 6.5% lower |
| Lighting | 4× | 75.584 | 71.866 | 4.9% lower |

Research preparation fell 73–85%; texture memory remained 4035.586 MiB on both
paths. Zoom has no consistent gain. All frame gates still fail; developer-native
outliers reach about 0.94 seconds. Do not combine these percentages with the prior
packaged improvement or compare developer outliers directly to packaged maxima.
All six runs completed without engine/script errors; 351 source scripts unchanged
during the comparison.

**453 native checks pass**, including exact pixels across rotations, shell passes,
power/clocks, doors, moved/scaled/flipped/deleted layout props, same-quarter edits,
direct edits, three zoom scales, nearest/linear filtering, bounded cache and Studio
bypass. Registration classifies the test as native. Owner fingerprints remain
unchanged: 2,936 non-log files after each batch, including UID generation.

**Sidebar report corrected:** actual debug=false frozen package at 1440p accepts
wheel input, exposes all eight hardware controls/status labels inside its scroll
viewport, and keeps the time panel fixed below it. Final screenshot inspected.
The earlier capture showed expected scroll clipping, not a reproduced overlap
defect; no UI runtime change warranted. This does not close the broader visual
matrix. The separate large idle probe reported 5151.663 MiB, a different workload
from the zoom/lighting comparison and another memory-budget failure, not evidence
by itself of sustained growth.

Evidence: `output/pre-render-2026-10-05/`: `callback-attribution.json`,
`comparison-summary.json`, `baseline/`, `cached/`, `source-comparison-check.json`,
`research-cache-r2.log`, `research-owner-check-r2.json`, and
`sidebar-release/large-2560x1440-1.json` / `.png`.

## Next action

Trace drone texture preparation/upload and subsequent engine submission against
the remaining stalls before choosing a remedy. Keep pixel identity and animation
timing; do not assume async PNG decoding makes GPU upload asynchronous. Complete a
bounded large-scene texture inventory and investigate proven transparent padding.
Re-export the accepted source cache and perform matched packaged validation before
claiming a packaged gain. Full bug/save/upgrade coverage, two-hour soak, ten scene
transitions, minimum PC/M1 measurements, Mac signing/notarization and the
unattributed exit warning remain open. No public release is authorized by this
handoff.
