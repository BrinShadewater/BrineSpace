# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: current crew-cache reporting

## Objective and acceptance

Expose the installed crew cache in normal stall/F8 diagnostics so the next
performance investigation can attribute decode/upload work and cache pressure.
Preserve previous report fields, animation behavior and bounded collection.

## Accepted decisions and constraints

The frozen Windows/Mac candidate cab0dd6874401f88 is unchanged and excludes these
later checkout diagnostics. No new memory/FPS acceptance follows from unit tests.
Submission intervals measure CPU API time, not GPU execution or physical VRAM.

## Current state

Changed scripts/crew_storage/router.gd and slots.gd, scripts/grid_canvas.gd,
scripts/performance_monitor.gd and tests/test_performance_monitor.gd; UIDs retained.
Reports add crew_storage while retaining crew_texture_sharing. Source decoded/
compressed byte counters, references, resolved/missing/shown counts and bounded
presenter snapshot include hits, uploads, spill counts/peak source bytes, slot
count/capacity, budget, evictions and decode/submission aggregate intervals.
No source iteration, pixel readback or timing reset occurs in the report snapshot.

## Verification

New regression first fails for the two missing reporting capabilities; green
passes. Production Grid script load/can_instantiate and JSON/counter isolation
checks pass in the final targeted performance-monitor run:
output/test-runs/20261009-165505-headless. Added cost/repeated-collection coverage
passes in output/test-runs/20261009-165634-headless: 10,000 synthetic snapshots
average5.5162us/call; lifetime counters unchanged. This CPU snapshot estimate on
the current host (Mac export also active) is not full gameplay collection overhead.
Scratch resolved-directory guards and
owner-before/after checks pass (2,938 unchanged). Evidence retained under
D:/bs-release-crew-cache-20261009/cache-reporting/{red,red-provider,green,green-compile,green-cost}.
Initial red harness expected its filtered console output to contain the error;
the actual child log proves the intended failure. Harness repaired to inspect
the exact per-test log; second red run confirms both expected failures.

## Next action

Mac export/audit session96515 subsequently completes with identical PCK to Windows;
packaged profiling-overhead session34751 completes with matching selected states
and no consistent large profiling penalty proven. Next attribute actual rendering
costs. Benchmark acceptance needs competing engine activity absent. For profiling
these new report fields, use a separately identified QA overlay or a later freeze;
do not attribute new fields to the already frozen candidate. Large-station sustained cost
and construction/demolition stutters remain open, as do full release gates.
