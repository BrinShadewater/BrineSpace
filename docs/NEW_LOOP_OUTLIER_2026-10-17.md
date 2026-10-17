# New Loop loading outlier investigation — October 17, 2026

The retained **9.546-second** New Loop sample did not recur in **16 new primary visits or four diagnostic New visits**. Fresh-profile loading is effectively tied between the two unchanged Windows builds in this cohort. The old sample contains a substantial near-idle process interval, but its cause remains unproved. No production fix, new export or claimed resolution of the rare stall follows from this investigation.

## Frozen inputs and scope

- A: **brinespace-3a0ae1af0283fa01**, `D:/bs-visible-art-20261016/windows`; PCK `fdb06cdb4782730ab0a149eac05e86894542cf8ce65dd52b49174bd5463bbd7b`.
- B: **brinespace-5dd3aea89a5b1c1f**, `C:/Users/Alex/Documents/BrineSpaceQA/structure-loading-20261016/windows`; PCK `cc05a0b90e6628f2f357d339372f2577457b3e8e2f301a21072d0b713b60ee55`.
- These are the existing pre/post surface-preparation packages from [the previous investigation](INITIAL_SURFACE_LOADING_2026-10-17.md), not a new treatment. Physical QA copies receive only external adapters. Frozen source and deliveries are not edited. Matching **d3cfa1890bafefe7 Windows/Mac** remain the owner's Mac comparison target.
- Native visible secondary display2,1600×900, Compatibility/OpenGL, Godot4.7.2, RTX4070Ti, Dummy/silent audio. The same title/button adapter, pre-ready New site seed1928894317 and owner-layout copies are used. Fresh profiles have no learned startup order; repeats retain it. Initial wrecks/view state and critical profile inputs match within pairs.
- Evidence/helpers: `C:/Users/Alex/Documents/BrineSpaceQA/new-outlier-20261017/`. Working helpers: `output/new-outlier-20261017/`. No runtime, art, camera, lighting, crew/navigation, save schema or gameplay changes. No commit, promotion or Mac rebuild.

Timing starts at the New/Continue button action, not executable bootstrap. A fresh profile is not cold OS cache. Remaining gameplay RNG, desktop variability, global driver/OS caches, silent audio and small samples limit conclusions. Prior cohorts and the slow sample remain separate; none are silently pooled or replaced.

## What the original slow sample establishes

The valid first fresh pair in the previous cohort remains:

| Endpoint | A | B |
|---|---:|---:|
| Observed startup ready | 5.946s | 6.874s |
| Initial-art stage | 582.784ms | 1,239.598ms |
| Ready → loading screen gone | 616.136ms | 2,671.182ms |
| Action → loading screen gone | 6.562s | 9.546s |

The additional~2.983s spans setup and presentation: initial art adds~657ms, observed readiness~928ms overall, and the post-ready tail adds~2.055s. It is not isolated to crew setup or to the new floor/wall preparation. Both builds leave the single opening room's floor/wall caches lazy, with identical New worker-hit counts.

Retrospective250ms process accounting finds **1.505s of consecutive near-idle samples** in B's slow run: under10ms process CPU and under64KiB logical reads per sample. No such interval appears in the other seven primary New visits from that cohort under the same detector. Its approximate position falls within the post-ready tail. The old external samples have no exact Godot clock anchor; this is approximate alignment, not stack-level attribution. Logical read counters are not physical disk latency, and aggregate process CPU is not main-thread scheduling data.

This supports a wait contributing to the outlier. It does **not** identify a GPU/driver wait, scheduling delay, decoder wait, filesystem/security delay or application cause. The original run has no render-boundary or stack trace capable of deciding between them. Four earlier fresh controls also failed to reproduce it; those remain in the previous report. Applying the same approximate detector to all16 new primary New visits finds no near-idle interval meeting that threshold; this is not an absence-of-all-waits claim.

## New primary benchmark

**16 actual-release visits**, four fresh/repeat pairs per build, A/B order reversed on alternating rounds. All visits pass the recorded runtime, art, simulation, decoder, window and process guards; complete crew identities match the frozen reference. Initial floor/wall caches are empty at New readiness in both builds.

| New Loop visit | Median observed ready A → B | Median loading gone A → B | Median paired uncover change |
|---|---:|---:|---:|
| Fresh profile | 5.805 → 5.813s | **6.465 → 6.475s** | **+19.432ms / +0.31%** |
| Repeat | 5.230 → 5.147s | **5.960 → 5.765s** | **−157.624ms / −2.63%** |

Medians summarize four samples each; the change column is the median of paired effects, not a ratio/difference of independent medians. Fresh B is faster in2/4 pairs; repeat B in4/4. This is repeated measurement of existing builds, not a speedup caused by a change in this task.

Fresh uncover ranges: A **6.416–6.638s**, B **6.402–6.742s**. Repeat ranges: A **5.771–6.053s**, B **5.739–5.905s**. Fresh initial art is A570–612ms/B560–597ms; no repeat of the old1,240ms sample. Across all16, ready→uncover is597–758ms, compared with the old2,671ms. The rare stall is not proven fixed or impossible, and these samples do not establish its frequency.

## Separate boundary and drawing diagnostics

Four additional fresh New visits, B/A/A/B order, use an external observer with bounded pre/post-render signals, descendant draw counters, scene/main readiness, loading state/removal, focus/window state, decoder activity and an exact wall/Godot clock anchor. These are labeled diagnostics and excluded from primary timing. The draw window extends five seconds beyond the first observed process callback with startup complete; sums reconcile performance-monitor counter resets and are not clipped.

Observed startup readiness in the headline adapter is a process-frame observation. `main.ready`, `scene_changed`, `first_complete_process` in the observer and loading disappearance are distinct events; do not substitute one for another.

| Diagnostic interval | A, two visits | B, two visits |
|---|---:|---:|
| Loading gone | 6.535–6.542s | 6.492–6.502s |
| Setup-last-ready → first render-pre | 301–329ms | 292–298ms |
| Grid CPU methods in that interval | 218–230ms | 215–219ms |
| Observed-ready → loading gone | 621–725ms | 621–745ms |
| Grid CPU methods in that tail | 580–584ms | 582–590ms |
| Largest render pre/post signal span before uncover | 14.4–18.0ms | 14.2–15.2ms |

Scene-change → first deferred marker is78–109ms across these visits; decoder activity goes from one pending task/active to zero/inactive by that marker. This bounds cleanup together with other scene/deferred work; it is not a direct timer around `ImagePrefetch.end`. No seconds-long cleanup or render-signal wait occurs in these four visits. This does not retrospectively exclude either from the old outlier.

The repeatable New presentation cost remains CPU drawing. The tail contains **337–343ms in the derelict pass**,~54ms live contents,~40ms each in two environment passes,~26ms floor slots,~29–31ms wall shells and~40–41ms north crowns. Nested stage clocks overlap and are not GPU execution times or a complete decode/upload/geometry split. These are measured follow-up targets for ordinary loading, not the established cause of the rare stall.

## Validation, harness correction and limits

One initial visit was rejected because the existing task-local timing guard sampled our exact game PID/path while Windows was still returning the `Popen` handle. The archived record identifies the same PID as both rejected and ultimately bound child. Its game checks pass, but its timing is excluded; it is not the historical9.546s outlier.

The new task's guard buffers those early observations, then reconciles every PID/name/path against the exact bound child and retained Windows handle. Other processes are still rejected; missing owned paths are accounted for, and unresolved samples fail acceptance. Five focused checks pass for early owned/foreign snapshots, wrong paths, late foreign processes and handle-bound missing paths. Their initial red run fails at the missing `observe` API; the archived native false rejection establishes the actual race. The shared/previous guard is unchanged. Rejected artifacts remain under `rejected-launch-race`; primary profiles were restarted under a new prefix. No player-folder probe or production change is involved.

All primary New complete lossless clip/source/metadata/timing/filter/historical-bank crew identities equal the frozen reference. The16 primary whole-process private peaks span~2,126–2,314MiB and include post-timing identity/visual QA. Repeat decoded peak remains237.48MiB; the pending96/compression8 and recent16MiB cache policy is unchanged. Startup workers/results/recent images/path order release. No memory gain, exact startup RSS delta, leak/endurance, FPS, placement or zoom acceptance follows from this loading investigation.

## Final comparison controls and integrity

Four separately labeled unchanged Continue controls use the original twelve-room checkpoint, restored before every visit, with critical profile/checkpoint hashes equal and learned order retained for repeats. One pair per visit, B then A: first-profile uncover **7.608→7.492s (−116.667ms)**, repeat **6.714→6.558s (−155.977ms)**. This small control supports the earlier Continue direction; it is not a new treatment or pooled extension of the New cohort.

All **24 accepted visits** have288 retained passing runtime checks, clean recorded art/errors/simulation/decoder/window/process guards and complete crew identities equal to the corresponding frozen New/Continue reference. Parent visual review of actual packaged B New/Continue images finds coherent rooms, floors/walls, cards and UI, with no missing artwork. Fresh read-only review independently recomputes the paired effects, complete crew identities, historical idle interval and diagnostic counters, reviews guard behavior and four A/B images, and finds no material issues. Its scope/limits are retained in `review.md`; it does not claim to rerun gameplay, tests or full delivery hashing.

Final verification confirms **all136 protected delivery hashes and all2,948 owner files unchanged**, exact QA EXE/PCK equality to the canonicals, primary overrides restored and no remaining game processes. Verified task-owned EXE/PCK duplicate cleanup recovers **7,476,735,641 bytes /6.963GiB**; final C:/D: free space is **100.360/28.976GiB**. Canonical source/packages, raw reports/images, rejected evidence, helpers, manifests and QA restoration map are retained. `verified-integrity.json`, `final-guards.json`, `runtime-restoration.json` and final `HANDOFF.md` record acceptance and cleanup.

The requested investigation and benchmark are complete. The rare stall remains unresolved; reproducing it with synchronized render/loading boundaries and thread/stack/wait accounting would be needed for a justified root-cause fix. The repeatable derelict drawing cost is a separate ordinary-loading optimization target. Matching d3 Windows/Mac and all compared candidates remain frozen, with native Mac validation still the owner's pending task.
