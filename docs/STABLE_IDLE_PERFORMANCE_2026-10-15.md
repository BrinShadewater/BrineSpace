# Stable-ID 4× idle investigation — October 15, 2026

The earlier 4× idle slowdown does **not reproduce as a consistent stable-ID
penalty**. Both new series use byte-identical V3 code and binaries, with no runtime
fix. Direct counters find no rebuilds or detour searches during this idle workload.
Drawing and render submission dominate the changing frame costs. The specific
OS/driver cause of process-to-process variation is not established.

The placement improvement survives all four new action comparisons: mean
68.916→60.534 ms, about 12.2% shorter. Whole-frame pacing remains mixed, including
one worse following window. Keep V3 private; this is not a 60 FPS acceptance.

## What was investigated

The [previous result](STABLE_NAV_PERFORMANCE_2026-10-15.md) measured 4× idle at
46.52→44.63 FPS. Crew time changed only ~0.797→0.824 ms per frame, while total
frame time changed 21.498→22.405 ms. The excess sits mostly before render and
between render signals, rather than inside simulation. These are CPU wall
intervals; draw callbacks nest within them, upload timers can nest within draw
callbacks, and viewport GPU/CPU queries can be delayed. Do not add those measures
or read them as a stack profile. Cached `Performance.TIME_PROCESS` values are not
used to attribute individual frames.

New evidence freezes the same 40-room / 52-occupied-cell cohort, four large rooms,
private distant-room LOD and one-spare setup. Actual release Godot 4.7.2
`ed1daf0bf`, Compatibility/OpenGL, RTX 4070 Ti, 1920×1080, debug=false. It is
separate from normal runtime or public-export acceptance. Each series runs
reference→V3→V3→reference, with 180 warm frames and 120 measured frames in each
of idle/placement at 1×/4×. Simulation steps, action sites and camera paths are
unchanged.

Two production-lane series produce **3,840 new measured frames and sixteen exact
phase-end-state/camera-endpoint/per-frame-camera-path pairs**. Actor state is not
compared on every frame. All eight runs also match the preceding study's
corresponding phase-end states and camera paths. Existing benchmark frame, draw
and upload observers remain; these lanes omit the new navigation wrappers used
only in diagnostics. No guard-valid sample was discarded, including the slower
placement trial.

## Why the idle regression is unconfirmed

| Series | 4× idle mean frame, reference → V3, ms | Mean FPS |
| --- | ---: | ---: |
| Previous study | 21.498 → 22.405 | 46.52 → 44.63 |
| New repeat 1 | 22.412 → 21.514 | 44.62 → 46.48 |
| New repeat 2 | 21.968 → 21.580 | 45.52 → 46.34 |
| All three, including previous | 21.959 → 21.833 | 45.54 → 45.80 |

The new within-order V3-minus-reference differences are −1.831, +0.035, −0.077
and −0.699 ms. The old within-order differences were +0.381 and +1.435 ms. A
consistent idle regression is not supported by these samples; the pooled slight
gain does not establish a dependable steady-FPS gain or a new fix. These are short
windows with variable render costs, not a statistical equivalence proof.

A separate four-process diagnostic series adds only Bill function counters/timers
to each lane. Its **1,920 frames and eight phase-end-state/camera/path pairs** are kept
separate from final FPS results. During every 120-frame 4× idle phase, both lanes
have:

- Zero graph rebuilds, detour reachability calls, dictionary detour calls or crew-detour searches.
- Exactly two ordinary route requests, totaling 90–124 microseconds per phase.
- Exactly 240 topology checks; mean cost ~0.304–0.326 ms per frame across runs.

The probe remains below its 2,048-frame capacity; startup rebuilds and the two
4× placement rebuilds are recorded as positive controls. Loaded-source checks
verify the instrumented Bill script. The sparse dictionary fallback cannot cause
this benchmark's 4× idle difference because it does not run there. This finding
does not apply to idle generally or establish its cost in a crowded traffic scenario.

At 1× idle, each lane does perform two detour-reach calls. Their combined cost is
11.150/11.198 ms for dense graphs versus 15.043/15.983 ms for stable IDs in the
two diagnostic orders: ~3.9–4.8 ms extra per 120-frame phase, or ~0.032–0.040 ms
per frame averaged over that phase. Dictionary timers nest inside reach timers
and are not added to them. This is a real cost to consider for future traffic
work, but it does not explain the sampled 4× slowdown.

The eight new production-lane 4× idle captures each record 1,568 draw callbacks and
1,409,253,252 diagnosed upload bytes. Uploads span 68–69 sampled frames. The work
quantity is similar, but its measured cost varies. For example, the slower repeat
1 forward reference has 12.070 ms mean draw-callback time and 5.972 ms between
render signals; its V3 pair has 10.960 and 5.622 ms. Simulation changes only
1.701→1.616 ms. The largest old penalty and largest new improvement both chiefly
track these broader drawing/render intervals. This localizes the variance; it
does not prove a particular hardware scheduling, driver or power-state cause.

## New average FPS and placement results

Both new series pooled, 480 samples per lane per phase; FPS is 1000/mean frame
milliseconds. Diagnostic runs are excluded.

| Phase | Mean FPS, reference → V3 | Mean frame, ms | p95 frame, ms |
| --- | ---: | ---: | ---: |
| 1× idle | 52.86 → 52.72 | 18.919 → 18.969 | 21.167 → 20.810 |
| 1× placement | 51.22 → 51.64 | 19.525 → 19.365 | 23.987 → 21.587 |
| 4× idle | 45.07 → 46.41 | 22.190 → 21.547 | 37.043 → 37.177 |
| 4× placement | 43.21 → 42.81 | 23.142 → 23.359 | 36.617 → 41.210 |

No new V3 phase passes both mean and p95 ≤16.667 ms: **0/16**. The 4× placement
phase's average and p95 worsen despite its faster action frames; that result is
retained and must not be hidden by averaging only the action itself.

| 4× placement action | Frame, reference → V3, ms | Crew phase, ms |
| --- | ---: | ---: |
| Repeat 1, forward | 68.934 → 58.330 | 26.193 → 15.106 |
| Repeat 1, reverse | 69.774 → 65.730 | 26.361 → 16.990 |
| Repeat 2, forward | 70.180 → 57.930 | 26.851 → 14.737 |
| Repeat 2, reverse | 66.776 → 60.145 | 24.946 → 15.799 |

All four action frames improve. Sampled action-frame atlas upload time is zero.
V3 again finishes retaining 52 cells / 14,075 existing nodes, rebuilding two cells
and ending at 14,673 graph points. Normal placement is still the earlier
unconnected append; the later 4× action opens Life Support's additional doorway.
There is no new 4× invalidation rule or simulation change.

Following sixty frames exclude the action:

| 4× following window | Mean, ms | p95, ms | Worst, ms | Frames >50 ms |
| --- | ---: | ---: | ---: | ---: |
| Repeat 1, forward | 23.433 → 23.045 | 37.656 → 45.033 | 56.780 → 56.214 | 2 → 1 |
| Repeat 1, reverse | 23.324 → 26.256 | 35.800 → 41.210 | 58.110 → 67.979 | 1 → 3 |
| Repeat 2, forward | 23.591 → 23.164 | 36.617 → 36.717 | 56.713 → 56.767 | 1 → 1 |
| Repeat 2, reverse | 23.409 → 23.117 | 35.615 → 35.731 | 56.690 → 59.550 | 1 → 1 |

Mean following-window cost improves in three comparisons, but p95 does not.
Placement spikes and subsequent rendering bursts remain separate unresolved
pacing costs. No claim that all placement work has been removed or safely deferred.

## Correctness, safety and reproducibility

Reference and V3's 22 selected frozen source files, PCKs, native source and DLL
match the prior study byte for byte. The native DLL is unchanged:
`ccc5debfd91df60c9940ac217e1859841363c265ccd343f9c1c19643f783a23d`.
Only separate diagnostic Bill overlays add observers. Native API remains 3.
No production routing, actor restrictions, clocks, rendering or assets were
changed. Normal installed sources, paired UIDs and navigation test retain their
pre-task hashes; no native integration, Mac package, export, commit or upload.

The prior 3,157 native assertions, 2,530 integrated graph checks / 2,872 routes,
2,216 extension-absent checks and seventeen exact cross-process image pairs plus
twelve repeats are reused as evidence for those identical bytes. They are **not
reported as fresh test runs**. The new release timing image was visually inspected.
New within-series and cross-study state/camera comparisons pass. Long-session
memory and platform packaging remain outside this investigation.

All **15 new owner guards**, **12 native binary guards** and three process/window
series guards pass. Final 2,948 non-log owner files equal the task's initial and
prior protected fingerprints. Only the owner's idle editor PID 46624 remains.
The [earlier profile incident](TEST_PROFILE_INCIDENT_2026-10-15.md) and its two
legacy metadata differences remain documented; no further changes occurred here.

Evidence: `C:/bs-stable-idle-20261015/`; helpers:
`output/stable-idle-20261015/`. `prepared.json`, `study-analysis.json`,
`diagnostic-analysis.json`, `summary-metrics.json` and `final-audit.json` retain
source identities, paired results, per-frame attribution and guards.

Keep the stable-ID prototype available for placement work. The measured idle
costs chiefly lie in drawing and render intervals, with recurring upload bursts; investigate those
costs rather than changing an unused detour fallback to explain this result.
The precise source of process-to-process timing variation is still unknown, and
the broader pacing, memory and Windows/Mac packaging gates remain before adoption.
