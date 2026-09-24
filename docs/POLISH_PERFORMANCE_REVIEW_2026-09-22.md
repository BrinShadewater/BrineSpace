# Current polish performance review

Updated September 22, 2026. Godot 4.7.2, Compatibility, RTX 4070 Ti, Windows.

## Objective and constraints
Measure current simulation/render load after interaction and art changes before
choosing another optimization. Preserve visuals, owner layouts and gameplay rules.
No production optimization was made from these measurements alone.

## Verification and findings
Maintained test_soak_budget.gd passes: 40/40 cycle callbacks, 800 updates,
mean 1.67 ms, worst 24.9 ms at cycle 37, 178 route searches. Fixture budgets are
8 ms mean and 90 ms worst. This is a free-building synthetic CPU gate, with
accelerated economy callbacks; it is not a normal expedition or rendering FPS.

Native profile_large_station.gd completes with zero failures and actual 50/100
room counts. Draw profiling and forced rendering are enabled; means cannot be
converted to ordinary gameplay FPS. Every scenario has 90/90 active-drone frames.

| Scenario | Simulation ms | Render CPU ms | GPU ms | Draw calls |
| --- | ---: | ---: | ---: | ---: |
| 50 overview | 1.83 | 14.86 | 12.47 | 6360 |
| 50 close | 1.85 | 5.26 | 2.99 | 2261 |
| 100 overview | 2.35 | 21.16 | 18.47 | 10037 |
| 100 close | 3.41 | 6.23 | 4.23 | 2678 |

Visible centers are respectively 50,3,100,3; overview screenshot inspected.
Bill's net displacement is 68.44/20.69 units in the 50-room samples and zero in
both 100-room samples. The latter is not evidence of moving-crew workload or a
stuck actor; state telemetry would be needed to distinguish work from idle/stall.
No many-crew performance claim is supported.

Fit View has the largest measured first frame, 205.895 ms. Load's first frame is
111.228 ms (synchronous interaction CPU 72.285 ms). These include instrumented
render/transition work, not pure setter costs. No controlled before/after runtime
change was measured; differences from older baselines are not claimed as gains.

Evidence: output/crew-performance-2026-09-22/soak.log and large.log;
output/game-pass/2026-09-22-polish/large-render-profile.json and native captures.
Both processes exit 0. No source, layouts, cards or packages changed in this pass.

## Next action
Investigate first-frame overview/zoom redraw work, distinguishing scene setup,
render submission and GPU/resource costs. Require paired native parity and timing
before installing any optimization. Include crew state telemetry if using the
100-room fixture to make crew-simulation claims. Native Mac and owner acceptance
remain separate and open.
