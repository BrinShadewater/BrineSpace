# Draw profiler lifecycle and crossover

Updated: October 9, 2026 · Project: BrineSpace · Task: performance and release readiness

## Objective and acceptance
Measure diagnostic overhead without stale frame data. Full original release gates remain open.

## Accepted decisions and constraints
Preserve saved diagnostic snapshots, session totals, selected visuals and owner data. These private controlled runs do not certify a complete release candidate.

## Current state
Changed scripts/grid_canvas.gd to clear current-frame draw timings when profiling is disabled, while retaining cumulative totals and copied snapshots. Added tests/test_draw_profiler_lifetime.gd with its paired UID and registered it in the performance-diagnostics subsystem.

## Verification
Regression reproduced three failures before the fix; all six checks now pass. Corrected debug=false crossover completed 3,000 frames: 1,500 profiled and 1,500 unprofiled, zero stage/flag mismatches. Source guards passed, log clean, all 2,936 owner files unchanged, adapter restored.

Two opposite-order separate-process comparisons did not reproduce the first apparent multi-millisecond profiler gain. Balanced four-frame crossover median on-minus-off block differences were 0.059/0.450/0.472 ms at 1x/2x/4x; these are diagnostic observations, not an accepted FPS improvement. Trace and GPU queries remained enabled.

Full crossover workload means were 38.290/39.264/40.487 ms, p95 43.709/47.266/55.156 ms, maximum 142.868 ms. Reported texture peak 2,345.481 MiB. Performance gates still fail.

Evidence: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/draw-profiler-crossover/ (candidate.json, candidate.log, owner-pair.json, lifetime-red.log, lifetime-green.log). Stale-stage trial retained separately.

## Next action
Continue attribution of sustained grid/environment/foreground rendering and native submissions. Validate further optimizations with matched workloads, then rebuild and certify complete Windows/Mac candidates. Current-candidate loading, original bug coverage, endurance and Mac native/signing checks remain outstanding.
