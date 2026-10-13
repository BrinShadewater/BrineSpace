# Project handoff — construction fixes verified on station maps

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Measure the combined pending-room and saved-layout loading fixes on copied real saves,
and check the larger station for regressions. The full release objective remains open.

## Accepted decisions and constraints
Three alternating matched pairs per map, actual debug=false Windows executable,
RTX 4070 Ti at 1920×1080, muted secondary display, isolated resolved APPDATA and
physical input disabled. Reuse the existing runtime with small source overlays;
20 GiB storage refusal floor. No full exports, screenshots or asset copies this pass.
Reference changes only prewarm_station_views back to placed-room preparation;
candidate uses current normal source. All other source, including RoomAssetLibrary,
is identical. Experimental indexed rendering is excluded from both lanes.

## Current state
No production gameplay or rendering code changed this pass. The two previously installed
fixes remain in scripts/grid_canvas.gd and scripts/room_asset_library.gd; UIDs preserved.
Tests use the frozen current save (10 rooms, then 11 after queued construction), the
reported 12-room save, and the corrected deterministic 40-room expansion of that save.
The 40-room scene is a stress fixture, not an independently acquired real station save.

Focused runners: output/renderdoc-tools-2026-10-08/run-combined-loading-real-maps.py
and compare-combined-loading-real-maps.py. Evidence:
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/combined-loading-real-maps-20261010.
Identity, input-save hashes, individual reports/logs, comparison, owner and storage
records retained. This compares the two local fixes, not all historical optimizations.

## Verification
18 runs, 19,440 measured frames. Each run covers idle, pan, zoom and lighting at
1×/2×/4×, 90 frames per phase. Pooled uncapped samples; lower times are better.

| Map | Mean ms, before → current | p95 ms | p99 ms | Max ms | Frames >50 / >100 ms |
|---|---:|---:|---:|---:|---:|
| Reported 12 |13.239 → 13.214|19.621 → 19.725|23.396 → 23.392|31.270 → 37.604|0/0 → 0/0|
| Current 10→11 |12.635 → 12.537|18.650 → 18.220|29.425 → 28.517|106.075 → 49.045|6/3 → 0/0|
| Expanded 40 |26.587 → 26.752|44.397 → 44.554|57.417 → 59.074|88.516 → 94.757|77/0 → 84/0|

Current-save pan4× maxima: 106.075/102.020/102.091 → 28.517/30.799/29.594 ms.
Consistent targeted stutter reduction. Current pooled mean improves 0.77%, but pair
means are mixed. Reported mean changes by only −0.19%. Large mean worsens 0.62%
in all three pairs; no large-scene performance win is claimed. Preserve that result
for investigation, rather than dismissing it or comparing unmatched historical runs.

All 108 full gameplay snapshot pairs and phase camera pairs match exactly, including
the 40-room fixture. All phases start with every room fully visible; camera coverage
guards pass. No logged runtime or missing-image errors; mute/input/display guards pass.
These snapshots do not substitute for visual motion acceptance. Prior dedicated
construction pixel comparisons remain scoped evidence; this pass captures no images.

Peak sampled gameplay texture memory is unchanged in both lanes: 1558.872 MiB
reported, 1940.831 MiB current, 3028.007 MiB large. This is not a startup peak or
scene-lifetime test. Current instantiation-to-ready: before 9587–9682 ms, current
9692–9718 ms. Required work moves into loading; these runs do not certify cold/warm
loading, full title/Continue flow, target hardware, 1440p, physical input or Mac.

All jobs exited successfully; runtime override restored and test loader absent;
source identities still match. Owner fingerprint: 2938 files before/after, no changes.
Evidence plus isolated profiles totals 71.80 MiB, with C:125.08/D:74.19 GiB free.
No deletion or full runtime copy was required. This size excludes unrelated OS writes.

## Next action
All maps still fail the p95 ≤16.7 ms gate; current and large also fail p99 ≤25 ms.
Keep release blocked on performance certification. Next isolate sustained 40-room
room setup/drawing, especially lighting/zoom rebuilds and rotation preparation, using
the existing private traces. Room drawing measured roughly 3.4 ms idle/pan and 8 ms
lighting; actor-presence checks only ~0.14 ms. Test an identified cause before changing
code, then repeat matched real-map comparisons and relevant visual checks. The 0.62%
large-scene slowdown remains recorded. Mac and broader release gates remain open.
