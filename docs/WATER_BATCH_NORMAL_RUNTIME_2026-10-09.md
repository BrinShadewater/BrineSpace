# Project handoff

Updated: October 9, 2026 - Project: BrineSpace - Task: normal water runtime verification

## Objective and acceptance

Continue the full PC/Mac performance and release-readiness plan. Verify the exact
integrated Moon/stroke sources in an actual release executable while preserving
visuals,simulation,owner layouts/saves. This optimization is retained after native
regressions and repeated matched gains; full candidate/release certification remains
open. No original bug-report or target-hardware closure is implied.

## Accepted decisions and constraints

Full stationary water retains cached commands. Moving/partial water uses bounded,
canvas-owned immutable index topology; current coordinates/colors rebuilt without
frame removal/downscaling/quality change. Diagnostic direct-drawing flag provides
same-pack baseline. No normal beacon/navigation change or renderer upgrade added.

## Current state

Two exact normal-source pairs (reference-first,candidate-first),actual debug=false,
1080p,RTX4070Ti,40rooms/fourcrew/three natural missions,3,000 measured idle frames at
1x/2x/4x per lane. Physical frozen Moon and stroke bytes match current normal files.
Override pack mounts before compilation; all three actual base renderers verify
compiled Moon/helper hashes,selected flag and canvas topology execution. Normal
beacon implementation used; obsolete private beacon assertions removed.

The rest of the diagnostic environment is the canonical retained PCK plus shared
private scoped/fast/indexed navigation,crew storage/drone retention and profiling
canvas controls. This isolates the two normal rendering files; it is not a full
current-checkout export or public candidate certification. Canonical/public files
were not overwritten. Both lanes share all controls except dynamic-water flag.

| Pair order | Speed | Mean ms: direct -> batch | p95 ms | p99 ms |
|---|---|---|---|---|
| reference first | 1x | 45.97 -> 38.83 | 51.84 -> 41.52 | 60.31 -> 52.24 |
| reference first | 2x | 46.22 -> 39.55 | 53.38 -> 46.10 | 65.69 -> 55.96 |
| reference first | 4x | 44.61 -> 40.48 | 56.97 -> 52.57 | 75.49 -> 68.80 |
| candidate first | 1x | 42.98 -> 38.55 | 45.35 -> 40.72 | 55.59 -> 52.43 |
| candidate first | 2x | 44.29 -> 39.44 | 50.41 -> 45.68 | 61.15 -> 55.50 |
| candidate first | 4x | 44.38 -> 40.66 | 56.48 -> 52.52 | 74.49 -> 72.85 |

Means/p95/p99 improve6/6. Mean gain3.72-7.15ms/frame. Native draw calls~6,466-6,536
become~5,019-5,025. First renderer medianCPU14.67->10.95ms/GPU12.58->8.65ms;reverse
CPU14.20->10.94ms/GPU12.18->8.63ms. Timings overlap; do not add these savings.
Candidate means38.55-40.66ms,p9540.72-52.57ms,p9952.24-72.85ms,max128.37ms: all
60FPS/stutter release gates still fail. This is retained improvement,not certification.

All compared phase crew/drone/phases/doors/lights/power/zoom/props/mission/resource
endpoints equal;final histories equal. All3 missions return/unload and full station
navigation recovers,zero scope fallbacks. All4,074 uploads and settled/peak/exit
texture memory match:peak2346.502/exit228.259MiB. No texture-memory or endurance gain
claimed from water batching. Source identities and branch execution guards pass.

Evidence: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/
water-normal-runtime/,water-normal-reverse/,water-normal-repeated-comparison.json.
Only documentation changed this turn; normal integration files remain as recorded
in WATER_BATCH_NORMAL_INTEGRATION_2026-10-09.md. Pre-edit snapshots retained.

## Verification

Native normal-source stroke180exactpairs+6159cache/scalar checks,
water493checks/244pairs,composition135checks/80pairs and default-cache independence
were completed before runtime comparisons. No redundant rerun. Source hashes
checked against both frozen copies after measurement. Current actual runs clean,
debug=false,focused,no runtime-art failures,router releases;all processes terminal,
adapters restored,all2936 non-log owner files unchanged. No save-folder writes.

## Next action

Post-change reverse candidate grid script draw median20.67ms,above the entire16.7ms
frame budget. Hierarchical stage means:live rooms12.83ms,large child bases8.06ms,
Moon bases7.34ms,Tidal0.73ms;these overlap. Exterior actors1.22ms,door/light validation
1.38ms,line pass0.99ms are smaller. Next profile/reuse static Moon shell/wall drawing
and remaining water preparation;measure actual renderer/script tradeoff and pixel
parity before changes. Keep upload/navigation stalls independently in scope.

Three identical current-version measured runs,12-room/fresh/interaction matrix,
loading,endurance,original-nine bug closure,full frozen release export and actual
Windows target-hardware/Mac certification remain required. Earlier private
interaction gains support direction but do not substitute for current full-candidate
checks. No upload/visibility change is authorized by this milestone.
