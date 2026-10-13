# Real-station selection verification

Updated: October 11, 2026 · Project: BrineSpace · Task: performance release readiness

## Objective and acceptance

Verify the installed settled-selection surface-key optimization on real station
saves, with matched gameplay/camera state and bounded test storage. Full release
acceptance still requires the frame-time, workload, hardware and platform gates.

## Accepted decisions and constraints

Preserve animation/art quality, owner layouts and saves. Native tests are muted,
positioned on the secondary display and use scratch profiles. Reuse the physical
release runtime and small source overlays; do not copy runtime assets per run.

## Current state

No additional production changes in this pass. The installed grid optimization
matches the tested candidate's normalized source. Evidence resides in
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/selection-surface-real-maps/`;
UI attribution resides in the adjacent `ui-refresh-component-trace/` directory.
Runners/comparator are in `output/renderdoc-tools-2026-10-08/`:
`run-selection-surface-real-maps.py`, `compare-selection-surface-real-maps.py`,
`run-ui-refresh-component-trace.py`, `finish-selection-real-maps-and-ui.py`.

## Verification

Twelve actual debug=false Windows release runs on RTX 4070 Ti at 1080p:
three alternating pairs each for reported 12-room and frozen current 10-room saves.
Idle, pan, selection and zoom-selection at 1x/2x/4x; 12,960 measured frames.
All 72 paired full phase states and cameras match; 648 selection-handler
applications verified. Fixed-step fixture survey/notification clocks apply to
both lanes. These are performance/state comparisons, not new visual certification.

| Map | Mean ms before → after | p95 ms before → after | p99 ms before → after | Frames >50 ms before → after |
|---|---|---|---|---|
| Reported 12 | 12.298 → 12.171 (-1.04%) | 22.243 → 19.606 | 34.835 → 35.122 | 0 → 1 |
| Current 10 | 11.958 → 11.671 (-2.40%) | 25.771 → 19.859 | 31.932 → 29.844 | 1 → 0 |

No measured frame exceeds 100 ms. Textures unchanged: 1559.51 / 1945.26 MiB.
Current station improves in all three pair means; reported station improves in
two of three. Idle/pan effectively neutral. Ordinary selection means improve
12.812→12.003 ms (-6.31%) and 12.786→11.843 ms (-7.37%). Corresponding floor/wall
repaints fall 81→0 and 84→3; remaining current-map rebuilds preserve state changes.
Reported zoom-selection mean worsens 14.153→14.412 ms; do not claim universal gain.

Both >50 ms traces inspected. Reported candidate zoom-selection at 1x:
54.967 ms, click 9.940 ms, grid draw 29.541 ms, simulation step 1.986 ms;
no current or sampled texture uploads. Current reference selection at 4x:
52.968 ms, crew 25.876 ms, grid draw 18.623 ms; no current or sampled uploads.
Times overlap in scope; these identify investigation targets, not additive causes
or proof that the optimization caused/removed either isolated tail event.

One separate instrumented 40-room release diagnostic: 270 measured frames,
27 verified selections and 28 `_refresh_all` calls. Mean refresh 7.122 ms;
inspector 3.444 ms, resources 2.022 ms, learning UI 0.571 ms, key hints 0.544 ms,
cards 0.188 ms. Attribution only, not candidate acceptance. Current source computes
next-cycle economy independently in resource refresh and placed-room inspector;
this is a candidate for scoped reuse only after dependency/side-effect checks.

Both completed owner guards: 2938 files before/after, no changes. Jobs terminal;
runtime override restored to guarded empty fixture. Evidence totals 47.52 + 3.81
MiB, with existing PCKs reused. C 123.22 / D 70.22 GiB free at final check.

## Next action

Trace forecast, inspector formatting and resource theme updates separately.
Try one narrow measured UI optimization, verify displayed values/tooltips and full
gameplay state, then compare matched workloads before admission. Preserve the
zoom-settle repaint guarantee. Frame gates still fail; target GPU/M1, Mac, full
motion/visual review, endurance and broader release certification remain open.
