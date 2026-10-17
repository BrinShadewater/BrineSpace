# OpenGL zoom and placement stalls — October 15, 2026

The trace identified separate upload and construction costs. A small navigation
change is installed: preserve the unchanged position lookup when most graph nodes
are retained. **Normal placement frames fell from 59.6–59.8 ms to 54.9–56.9 ms.**
Overall average frame time is essentially flat; this does not establish 60 FPS
or solve the independent large-atlas zoom stalls.

## Trace scope and limits

Windows, RTX 4070 Ti, official Godot 4.7.2, actual debug=false release executable,
Compatibility/OpenGL 3.3, 1920×1080 on the secondary display, Dummy audio,
VSync disabled and uncapped FPS. Reused the frozen 40-room private LOD QA cohort
from the [renderer comparison](GODOT_RENDERER_COMPARISON_2026-10-15.md), with its
checkpoint-owned Branforth pilot. This is separate from current normal-source
export or Mac acceptance.

WPR was not already recording. A uniquely named CPU/GPU recording attempt failed
with Windows policy error `0xc5585011` under the non-admin token. Recording did
not start and no ETL was captured. Evidence is
`C:/bs-opengl-stalls-20261015/wpr-capability.json`.

Instead, `diagnose1` adds bounded, nested function markers and query-only Windows
thread accounting to four zoom/placement phases. It records 1,056 samples of the
earliest-created process thread, without suspending it. Its cumulative CPU time
is approximately 97–99% of wall time over phase windows. That includes native
engine/driver execution and possible busy-waiting; it does not separate ready,
blocked or GPU queue states. Cycle counts are not converted into elapsed time.
[GetThreadTimes scope](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getthreadtimes),
[QueryThreadCycleTime limitations](https://learn.microsoft.com/en-us/windows/win32/api/realtimeapiset/nf-realtimeapiset-querythreadcycletime).

Frame/action/simulation and render-signal intervals use the existing collector.
Function scopes can nest. Render signals are not GPU durations; delayed viewport
queries and previous-second engine maxima are not additive per-frame costs.
The final A/B series removes the additional function markers and thread sampler.

## What causes the observed stalls

### Zoom: atlas creation/upload calls

The independent audit of both clean `pacing3` OpenGL traces finds all five
normal-speed fitted-zoom frames over 50 ms coincide with large sampled drone
uploads. All 56 large zoom uploads across both speeds are initial cache-image
records, not native-context fallback records. Frame IDs and upload timestamp
containment were checked; a latest-upload record alone was not used as attribution.

The new diagnostic reproduces a 103.141 ms four-times zoom frame:

| Nested observation | Measured time |
| --- | ---: |
| After simulation, before render signal | 94.535 ms |
| Render-signal interval | 6.694 ms |
| Exterior-actor callback | 76.159 ms |
| Two texture-creation/upload calls inside that work | 49.200 ms |

The two initial RGBA8 images are `mine-north.png` and `mine-south.png`, each
2688×13440 / 144,506,880 bytes: **275.625 MiB combined**. Formats are now recorded
directly by the diagnostic. These intervals establish expensive native API calls,
not completed GPU transfer duration. They must not be summed into a frame total.
The installed navigation change does not alter this loading/storage path.

### Placement: navigation plus substantial drawing

In the prior clean renderer cohort, placement takes 60.3–66.1 ms with no large
sampled upload. The direct placement operation costs about 8 ms, crew work about
13–14 ms and accumulated draw callbacks about 27–32 ms. The finer diagnostic
confirms graph rebuilding and drawing, rather than a large upload, on the
normal-speed placement event.

Navigation already retains an unchanged leading graph prefix. However, rebuild
cleared its position-to-ID dictionary and repopulated every retained node through
`AStar2D.get_point_position()`. One observed prefix retained 14,097 of 14,382 nodes.
That repeated lookup construction was a concrete avoidable cost.

## Installed change

[BillNPC.rebuild()](../scripts/bill_npc.gd) now keeps the lookup when the unchanged
prefix exceeds the removed suffix. Each removed node's coordinate is erased
before graph removal. Retained entries keep their original insertion order;
new suffix entries append in the original order. If at most half the old graph
is retained, the original clear/repopulate path remains cheaper in operation
count and is retained. Staged loads still clear immediately.

Graph ownership, point IDs, weights, ordered edges, disabled-state reset, boundary
validation, routes and synchronous/staged behavior stay the same. No additional
persistent cache or texture is introduced. Disjoint cell-local point domains
prevent suffix coordinates from aliasing retained coordinates. Independent source
review found no actionable correctness issue; that reviewer ran no native jobs.

Installed source SHA256:
`43fcb3827a4751123e8ef1b20c684fb58c13c1e944541cd0ea9be464ee202086`.
It matches the tested private V2 bytes exactly. The existing script UID is preserved.
The [maintained prefix test](../tests/test_navigation_prefix.gd) adds middle-room
rotation/removal/reappend, negative-coordinate suffixes and exactly
0/¼/½/¾/all-prefix cases for Bill and Marsh.

## Final V2 benchmark

**`ab2`**, four serial processes: reference → candidate → candidate → reference.
Each has 180 warm steps, then 120 frames per idle/zoom/placement/demolition phase
at normal and 4× speed: **3,840 measured frames**. All 16 matched gameplay snapshots,
camera endpoints and per-frame camera paths agree. The 340-sample process guard
finds no foreign Godot, duplicate game or monitor error; maximum gap under 0.867 seconds.
Actual runtime/backend and loaded-source identities are verified in every process.

| Placement event | Crew CPU, reference → candidate | Crew CPU saved | Frame wall, reference → candidate |
| --- | ---: | ---: | ---: |
| Forward, normal | 13.050 → 9.253 ms | 3.797 ms | 59.560 → 54.883 ms |
| Reverse, normal | 13.827 → 9.910 ms | 3.917 ms | 59.803 → 56.863 ms |
| Forward, 4× | 14.984 → 11.536 ms | 3.448 ms | 84.716 → 77.165 ms |
| Reverse, 4× | 15.423 → 11.210 ms | 4.213 ms | 77.215 → 75.086 ms |

Normal placement has no sampled atlas upload. The four-times events also contain
11.5–13.7 ms upload calls, so the whole-frame differences there are not entirely
attributable to lookup reuse. Demolition crew CPU improves in all four event
pairs, by 2.451–7.142 ms; drawing and upload variation affect the frame result.

![Placement CPU and wall intervals, both process orders](C:/bs-opengl-stalls-20261015/opengl-placement-pacing.png)

| Whole measured workload | Reference | Candidate |
| --- | ---: | ---: |
| Forward mean | 23.110 ms | 23.355 ms |
| Reverse mean | 22.791 ms | 22.628 ms |
| Forward p95 | 33.812 ms | 35.715 ms |
| Reverse p95 | 34.893 ms | 33.135 ms |
| Frames >50 ms, forward / reverse | 14 / 11 | 12 / 11 |
| Maximum, forward / reverse | 87.940 / 77.215 ms | 77.165 / 75.086 ms |

Mean frame time is +1.06% forward and −0.72% reverse; combined difference is
approximately +0.18%. That is **no established average-FPS improvement**. Phase
p95 improves in 5/8 phases in each order, but overall pacing is mixed. None of the
16 candidate phases passes mean and p95 ≤16.67 ms. This change is admitted for
its repeatable construction-time CPU saving and exact behavior/output.

Private V1 always retained the lookup when a prefix existed. Its clean `ab1`
series is retained as exploratory evidence; V2 `ab2`, which adds the small-prefix
fallback, is the final result.
The historical ~53 FPS and three-renderer cohort are not direct controls for
this shorter action sequence.

## Verification and retained evidence

- Seven relevant normal-source navigation regressions pass in
  `output/test-runs/20261015-132102-headless/`: prefix, boundary reuse, ownership,
  rebuild staggering, companion topology, topology signature and segment parity.
  Expanded prefix: **1,384 checks, 217,077 exact ordered graph records, 1,944 routes**
  and 126,528 sorted targets. Segment parity adds 153,824 comparisons; boundary
  reuse checks 46,840 records and 447 paths. Zero failures.
- Frozen native appearance: six zoom/light cases, two captures each, in independent
  reference/candidate processes. **All 12 cross-process images are pixel-exact**;
  all 12 within-process repeat pairs also match. Full checkpoint state, camera and
  visual sidecar agree. The reference fitted image also matches the previously
  reviewed `visual-gl-j` image exactly. The placement plot was visually reviewed.
- All **20** completed profile guards preserve all **2,948** non-log owner files.
  Normal tests use scratch APPDATA and copied layouts. Changes are limited to
  Bill navigation, its existing regression test, diagnostics and documentation.
  Artwork, renderer settings, both existing UIDs and delivery are unchanged.
- Source/test whitespace checks pass. No export, commit or publication occurred;
  Mac and actual current-source release gameplay remain separate validation.

Artifacts: `C:/bs-opengl-stalls-20261015/`. Key files: `ab2-analysis.json`, raw
`ab2-*-*.json`, command/source identities, `visual-parity.json`, installed-source
identity and `agent-evidence/FROZEN_TRACE_EVIDENCE.md`. Drivers:
`output/opengl-stalls-20261015/{probe,analyze_ab,images,plot_events}.py`.
The private probe caps its diagnostic frame map at 2,048; it does not ship.

## Remaining work

The next application-side target is the broad live-room/surface preparation and
redraw still seen on structural frames. The separate atlas bursts need a new
bounded lifetime/admission or storage hypothesis, with exact pixels and memory
evidence; prior rejected prewarm/reuse/crop experiments should not be repeated
unchanged. Kernel CPU/GPU scheduling attribution still needs a capture-capable
Windows session. Current evidence does not assign every remaining millisecond
or establish physical VRAM pressure.
