# Project handoff

Updated: October 8, 2026 - Project: BrineSpace - Task: guarded water batch interactions

## Objective and acceptance

Continue the full PC/Mac performance and release-readiness plan. Preserve selected
pixels/timing/default quality and owner layouts/saves. An optimization needs matched
runtime gain plus relevant settings/lifecycle tests before normal-source admission.
No release gate or original bug-report closure is established here.

## Accepted decisions and constraints

Retain stationary command caching. Dynamic batching applies only when clock is
nonzero or water is partial; level<=0.001 still draws nothing. Reduced motion freezes
the clock through the existing setting and must retain full-water cache reuse.
Do not reduce quality or slow gameplay. Keep the guarded implementation private
pending normal-source/layout/removal regression checks and integration measurement.

## Current state

New native guard test first fails8/36 checks against the previous always-batch
prototype: stationary cache bypass, warm rebuild, pause and four reduced-motion
rotations. Minimal guard then passes36checks/21exactrasterpairs. Active/resume and
partial water with frozen clock still execute the batch; cached geometry remains
bounded16 and dynamic topology1024; owning canvas releases. Red source/log/result
are retained. No normal source is edited.

Actual guarded release pair: same private PCK/source,debug=false,RTX4070Ti,1080p,
40rooms/fourcrew/three natural missions,360frames each for idle/pan/zoom/lighting at
1x/2x/4x (4320 measured frames per lane). Reference first. Both use identical
scoped/fast/indexed navigation and beacon batching; only water flag differs.
This is an additional interaction pair, not three identical standard-workload
runs or target-hardware release certification. Trace is bounded4096 frames while
phase aggregates cover all4320. Profiling enabled equally.

| Action | Speed | Mean ms: reference -> batch | p95 ms |
|---|---|---|---|
| idle | 1x | 42.20 -> 37.66 | 44.59 -> 40.03 |
| pan | 1x | 42.89 -> 38.41 | 46.62 -> 42.40 |
| zoom | 1x | 48.19 -> 43.09 | 61.12 -> 55.32 |
| lighting | 1x | 47.58 -> 42.71 | 63.45 -> 58.40 |
| idle | 2x | 43.97 -> 39.02 | 49.78 -> 45.44 |
| pan | 2x | 43.43 -> 39.00 | 48.73 -> 45.08 |
| zoom | 2x | 48.13 -> 43.84 | 59.67 -> 55.31 |
| lighting | 2x | 46.58 -> 41.85 | 63.97 -> 59.84 |
| idle | 4x | 44.60 -> 39.74 | 53.99 -> 49.03 |
| pan | 4x | 42.44 -> 39.10 | 53.86 -> 50.71 |
| zoom | 4x | 48.77 -> 45.85 | 72.60 -> 67.86 |
| lighting | 4x | 41.41 -> 38.55 | 59.58 -> 56.86 |

Means/p95 improve12/12; p99 improves11/12. Exception: idle2x p9957.844->60.170ms.
Mean savings2.86-5.10ms. Median renderer CPU13.94->10.67ms/GPU11.58->8.26ms;
CPU/GPU timings overlap, do not sum. Candidate max128.481ms versus134.378ms reference;
lighting1x max grows83.628->95.050ms, so worst frames do not uniformly improve.
60FPS/p95/p99/stutter gates still fail.

All compared phase endpoints equal: crew/drone/phases/doors/lights/power/zoom/props/
mission state and resources. Final mission histories equal; all3 naturally return,
unload and recover full graphs,zero scope fallbacks. Compiled Moon/stroke/navigation/
canvas identities and both selected branches verified; focused/no safe-image failures.
All6744 uploads match. Texture start1548.995/end1920.326/peak2469.002/exit228.259MiB
match exactly. No memory-saving or endurance claim.

Evidence: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/
water-stationary-guard/ and water-guard-interactions/ (comparison.json, sources,
identities, isolated profiles and full logs). Changed checkout files: this handoff
and CURRENT_STATUS.md only. Canonical/public delivery files remain unchanged.

## Verification

Guard red36/8fail,green36/0 with21rasterpairs. The preceding6592stroke checks and
529fullcomposition/motion checks remain separate supporting evidence, not rerun
or silently attributed to this guarded source. Guard preserves the baseline
stationary implementation; dynamic geometry code is unchanged.

Both actual runs and guard profiles isolated,resolved directories guarded,all2936
non-log owner files unchanged; logs clean after intentional assertion failures,
all processes terminal,adapters restored/router released. Native tests are QA;
actual runtime pair uses debug=false. Runtime exporter/manifest certification,
Mac playback and full owner visual acceptance remain separate.

## Next action

Prepare the equivalent normal Moon/stroke source changes without private beacon
or navigation additions. Run maintained stroke/water/full-room tests,including
layout changes,culling,room replacement/removal and owner-cache release against
that source. Keep stationary/reduced-motion guard coverage. Then measure normal
integration in an actual private packaged candidate before admitting it.
Continue broader rendering/stall/loading/endurance/original-nine/Mac requirements;
full original objective remains active and no upload is authorized here.
