# Crew CPU and 4× placement trials — October 15, 2026

**No runtime change admitted.** Two small GDScript trials preserve graph and
gameplay output, but do not establish a useful overall frame-pacing improvement.
The prior accepted placement/navigation code remains installed. No art, quality,
renderer, simulation clock, crew scheduling, export or routing policy changed.

## What remains expensive

Fresh actual-release diagnostics use the same frozen large-station cohort as the
previous placement/navigation pass: 40 rooms, 52 occupied cells, four large rooms,
1920×1080, Godot 4.7.2, Compatibility/OpenGL, RTX 4070 Ti. This private cohort
includes the distant-room LOD and one-spare viewport experiments; it is not a
full-current-source release candidate or Mac certification.

The reference diagnostic records these nested scopes:

| Scope | Normal idle | 4× idle | 4× placement frame |
|---|---:|---:|---:|
| Whole crew phase | 0.949 ms | 0.869 ms | 27.090 ms |
| Topology reads | 0.296 ms | 0.325 ms | 1.180 ms |
| Fire-state refresh | 0.015 ms | 0.016 ms | 0.019 ms |
| Two companion graph rebuilds | — | — | 23.969 ms |
| Rebuild suffix removal/prefix application | — | — | 5.053 ms |
| Rebuild point/link assembly | — | — | 12.717 ms |
| Link helper alone | — | — | 8.362 ms |

Do not add these scopes: the crew phase includes companion updates, rebuilds
include their component stages, and point/link assembly includes the helpers.
The trace times script regions and native calls together; it does not isolate
GDScript dispatch from native AStar allocation/connection work.

At the 4× placement action, two companions rebuild 24 cell templates each.
Each graph retains 8,580 nodes and ends with 14,673. At normal speed the retained
prefix is 14,097 of 14,382 nodes, so much less suffix assembly is needed.
Placement's own call remains about 1 ms, plus about 1.4 ms site finding. The
two-companion rebuild is the stronger target than duplicate fire scans.

Main and the base crew update do repeat fire/topology checks. Main's first checks
are outside `crew_frame_usec` but inside whole-crew timing. A future reuse context
must be synchronous and actor-local: previous actors can change rooms during the
same rendered frame, rebuild must record a fresh final signature, and Marsh has
additional update/charging paths. No such context or frame-wide cache was added.

## Private trials

1. **Contiguous link IDs:** reuse the packed IDs produced by point assembly and
   connect template indices by `first_id + relative_index`. Only the proven
   nonempty packed-point path supplies that first ID. Direct calls, empty
   results and disabled packed-point assembly retain the original arbitrary-ID
   lookup and pair order.
2. **Flatter topology key:** use one captured row per occupied cell instead of
   separate value/type/wrapper arrays. Preserve every type-sensitive value,
   Moonbay state, query order, lock side effect, post-query layout revision,
   sorted signature and deep ownership copy.

An initial link variant saved about 0.72 ms per actor on a warmed middle-edit
microbenchmark. The refined variant does not reproduce that gain: warmed means
are 2.502→2.420 ms for warm graphs, 3.082→3.071 ms for an append and
14.425→14.404 ms for a middle edit. All 20 pairs alternate execution order;
the warmed comparison uniformly omits pair zero, and the full raw data remains.
This does not establish a dependable assembly improvement.

The topology-only actual-release check makes 100 calls per batch, 20 alternating
pairs. Mean cost is 110.980→104.374 µs per call; both execution-order subsets
improve. This is about 6.6 µs per call, too small to materially address the hitch.

The combined diagnostic still records 25.296 ms for the two graph rebuilds,
12.474 ms for point/link assembly and 6.333 ms for suffix/prefix application.
Its idle crew phases are 0.949 ms normal and 0.813 ms at 4×. These separate
diagnostic launches are not a controlled CPU acceptance comparison, but confirm
that the large rebuild scope remains after the trials.

## Controlled release comparison

Four fresh serial processes: reference → candidate → candidate → reference;
180 warm frames then 120 frames per idle/placement phase at normal and 4× speed.
**1,920 measured frames; eight exact gameplay/camera endpoint/camera-path pairs.**
All 22 overlay files are frozen and their packs hashed. Actual loaded-source
checks include Main, its synergy constant, crew/navigation and render dependencies.
The process guard has 251 samples,
zero foreign Godot processes, duplicate-game detections or errors, and maximum
sample gap 0.691 seconds. The visible-window guard passes in every phase.

| Pooled phase | Reference average FPS | Trial average FPS | Reference/trial p95 |
|---|---:|---:|---:|
| Normal idle | 50.69 | 51.36 | 22.880 / 22.239 ms |
| Normal placement phase | 47.99 | 50.46 | 26.524 / 23.373 ms |
| 4× idle | 43.06 | 44.74 | 37.724 / 37.344 ms |
| 4× placement phase | 41.04 | 40.97 | 38.500 / 39.290 ms |

Whole-workload average is 45.37→46.48 FPS. A noisy reverse reference includes
73.878 ms after normal placement and 110.760 ms during 4× idle. Retain those
valid observations, but do not attribute the resulting average gain to the code.
Normal idle improves only 0.012 ms in forward order versus 0.498 ms in reverse.
No trial phase meets both the mean and p95 16.667 ms / 60 FPS gate (0/8).

| Placement action frame | Reference | Trial | Crew CPU reference/trial |
|---|---:|---:|---:|
| Normal, forward | 45.948 ms | 45.427 ms | 8.390 / 7.964 ms |
| Normal, reverse | 46.899 ms | 47.164 ms | 8.135 / 8.668 ms |
| 4×, forward | 80.285 ms | 79.202 ms | 33.217 / 27.893 ms |
| 4×, reverse | 72.669 ms | 69.076 ms | 26.674 / 26.232 ms |

The action call including site search stays 2.22–2.43 ms. All four action frames
sample zero atlas upload time. Lower 4× action peaks do not establish better
following-frame pacing:

| Following 60 frames | Max reference/trial | Frames over 50 ms reference/trial |
|---|---:|---:|
| Normal, forward | 35.364 / 38.126 ms | 0 / 0 |
| Normal, reverse | 73.878 / 35.724 ms | 2 / 0 |
| 4×, forward | 51.562 / 64.076 ms | 1 / 2 |
| 4×, reverse | 58.707 / 59.211 ms | 1 / 2 |

The 4× follow-up means and maxima worsen in both orders; p95 improves forward
but worsens reverse. The counts are small and do not prove a causal regression.
They do fail to establish the requested dependable pacing gain. **Keep the
trials private instead of adding the code to the game.** No unchanged rerun is
needed to make that admission decision.

## Correctness, selected source and profile integrity

- Private combined graph oracle: 1,609 checks, 259,265 ordered graph records,
  2,328 routes, 126,528 sorted targets; zero failures. Includes direct arbitrary
  ID and contiguous-ID connection/weight/disabled-state/route comparisons.
- Private topology oracle: 14,567 checks; zero failures, including same-tick
  locks, rotations, types, aliases, Moonbay and geometry revision mutations.
- A temporary API regression fails against the old assembler and passes against
  the private candidate. Its frozen copy remains with the evidence. The source
  test was restored to the previous accepted version and passes: 1,488 checks,
  259,265 records and 2,328 routes. It matches the prior frozen oracle after
  rebinding its two private preload paths.
- Independent bounded source review finds no actionable correctness issue in
  either trial. The admission rejection is for insufficient performance evidence.
- No new image comparison is claimed for the rejected trial. Selected runtime
  and art are unchanged, retaining the previous pass's visual acceptance.
- All 23 owner-profile guards pass. The final 2,948-file non-log fingerprint
  equals the prior **post-recovery** baseline. This does not undo or erase the
  [previous test-isolation incident](TEST_PROFILE_INCIDENT_2026-10-15.md): two
  legacy metadata files from that earlier incident remain as previously reported.
- No task-owned Godot/game remains; the owner's idle editor PID 46624 remains.

Selected Bill SHA256:
`b7e0a3cc21b8d928a38e874f7ac493a73e9489eab73ca4150362cc79f663c53a`.
Selected Synergy SHA256:
`00f3c72e25e4b3a4d463b3f824c36bfb8659b74f7e9eb8aadc12d02937a03261`.
Script UIDs are unchanged. Normal Main, companion and fire-safety files were not
edited. No executable export, commit or PR was created.

Two initial diagnostics were refused by source identity checks because the new
Main check decoded UTF-8 source using Windows' default encoding. Explicit UTF-8
fixed the guard; neither failed launch contributes samples. One topology-micro
harness had a duplicate local variable parse error and was stopped using its
verified task-owned executable path, output argument and PID; its corrected
successor supplies the micro results above. These are excluded harness attempts,
not game regressions or profile changes.

Evidence: `C:/bs-crew-cpu-20261015/`: `focused1-analysis.json`, four
`focused1-*.json` runs, process/owner guards, `trace3-summary.json`,
`trace4-summary.json`, `links1/links2*-analysis.json`,
`topology-micro2-analysis.json`, frozen source/pack files and `final-audit.json`.
Helpers: `output/crew-cpu-20261015/`.

Next useful investigation: a genuinely bulk graph-assembly path, or safely
retaining more graph work while proving exact IDs, connection ordering and
routes. Establish where script dispatch versus native graph work consumes time
before committing to a native extension or a scheduling change. The present
evidence does not justify changing crew timing or clearance.
