# Project handoff

Updated: October 9, 2026 - Project: BrineSpace - Task: post-batch preparation attribution

## Objective and acceptance

Continue the full PC/Mac performance/release-readiness plan. Find the next measured
CPU bottleneck while retaining selected visuals/timing and normal simulation.
No frame/quality reduction,renderer upgrade or owner-data changes authorized here.

## Accepted decisions and constraints

Normal water batch remains as previously verified. New component timers and
half-width optimization are private diagnostics/prototypes only. A headless
geometry-build gain is not a full gameplay or packaged rendering acceptance.

## Current state

Actual debug=false 40-room/1080p/four-crew/full-mission census after batching:
3,000 measured idle frames at1/2/4x. Per-component counters snapshot after warmup
and subtract phase boundaries,so all phases exclude startup/warmup totals.

| Component (combined three bays) | 1x ms/frame | 2x | 4x |
|---|---:|---:|---:|
| Water group,including threshold grating | 5.188 | 5.375 | 4.488 |
| Moving-water command/geometry construction | 4.664 | 4.805 | 4.030 |
| Moving-water native submission | 0.424 | 0.460 | 0.370 |
| Shell/floor | 0.631 | 0.637 | 0.547 |
| Walls/windows | 1.076 | 1.093 | 0.934 |
| Doors | 0.444 | 0.478 | 0.422 |
| Beacons | 0.589 | 0.574 | 0.488 |

Build/submit are subscopes of water; do not add them to that total. Construction
includes numeric gradient/shadow command capture and ordered stroke triangles.
Water remains the larger opportunity than retaining static shell/walls (~1.5-1.7ms).
Instrumentation adds overhead; diagnostic FPS is not a matched optimization claim.

Private invariant-width trial: compute the rounded half-width once per stroke,
instead of repeating an identical scalar conversion at each vertex. Native180
visible exact pixel pairs+6159cache/scalar checks pass. Advancing-water24pairs,
25checks pass. Native CPU comparison still strongly depends on redraw order:
large-bay median deltas reference-first~-199us,candidate-first~+26us. Not a gain claim.

Follow-up headless construction-only test excludes GPU/native submission and uses
64 advancing builds per case,first8 discarded,alternating call order. All24cases
compare final packed vertex/color/index bytes exactly. Large-bay8cases save73.5-118us
when reference-first and104-149.5us candidate-first. This establishes a small
intrinsic preparation saving,not an actual frame gain; keep prototype private.

Evidence: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/
water-normal-components/(analysis.json,candidate.json,identity,logs),water-half-width/
(build-result.json,build-analysis.json,native results/sources). Normal source unchanged.
Changed checkout files: this handoff and CURRENT_STATUS.md.

## Verification

Actual census source/branch identities pass;all3missions return/unload and full
station graphs recover,zero fallbacks;focused/debug=false/no missing art/log errors.
Peak2346.502/exit228.259MiB/uploads4074 unchanged diagnostic scope. New probes clean;
all2936 non-log owner files unchanged,all processes terminal,adapters restored.
The geometry-only proof is QA/headless;native pixel tests remain separate.

## Next action

Measure cheaper numerical geometry construction or overlap it with existing main
thread work. A bounded worker prototype is plausible because _record_water builds
only numeric commands; no SceneTree/GPU/image/simulation calls should move to workers.
Each task must exclusively own mutable buffers/topology until joined,avoid modifying
shared resources,and be joined/released even on scene exit or invalidation. Preserve
current-frame input identity and synchronous fallback;never display stale/incomplete
room state. First prove packed-byte parity and scheduling benefit outside gameplay,
then actual release and visual/lifecycle comparisons before selecting that approach.

Primary research: [WorkerThreadPool](https://docs.godotengine.org/en/stable/classes/class_workerthreadpool.html)
provides task scheduling/joining and requires completion waits for cleanup;
[thread-safe APIs](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html)
limits scene/GPU/shared-resource access and concurrent container resizing. These
are constraints for a prototype,not evidence that threading this game improves it.
Keep CPU-side half-width candidate separate so its small effect is measurable.
Full original release gates,bug closure,endurance and Mac certification remain open.
