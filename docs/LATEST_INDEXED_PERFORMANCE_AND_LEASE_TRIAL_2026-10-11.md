# Latest indexed performance and descriptor-lease trial

Updated: October 11, 2026 · Project: BrineSpace · Task: performance release readiness

## Objective and acceptance

Measure the latest private lossless renderer without screenshot readback, using
installed UI/grid changes; test a specific retained-image ownership hypothesis.
Keep full frame, memory/lifetime, visual, workload and PC/Mac release gates intact.

## Accepted decisions and constraints

No production changes. Lossless provider and descriptor lease remain private.
Scratch profiles, muted secondary display, disabled input, owner fingerprints,
20 GiB storage floor. Reuse existing runtime/art packs; script overlays only.
No screenshot output during these measurements.

## Current state

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`latest-indexed-uncaptured-maps/`, `indexed-command-lease-probe/`,
`indexed-command-lease-candidate/`, `indexed-command-lease-workloads/`,
`indexed-command-lease-materials/`. Runners/comparators in
`output/renderdoc-tools-2026-10-08/`.

Latest-provider inputs include hardened loaders, current surface-key/inspector
changes, unchanged default light behavior, and paired fixture-only survey/toast
clocks. Private motion telemetry adds one bounded common diagnostic event per
factory call. Indexed-factory event time includes decode/factory work and may
reuse storage; event bytes are not necessarily new allocation or physical bus traffic.

## Verification

Eighteen actual debug=false native Windows RTX 4070 Ti 1080p runs, three alternating
pairs each reported 12/current 10/deterministic 40 rooms; idle/pan/zoom/lighting at
1x/2x/4x, **19,440 measured frames**. All **108 paired full phase states and camera
endpoints** exact. Candidate execution verified in every phase: 21 indexed sources,
enabled factory, complete bounded node scan, palette draws, no ordinary duplicate
indexed paths or fallback draws. Upload-event lists complete in all sampled frames.

| Map | Mean ms reference → indexed | p95 ms | p99 ms | Texture MiB reference → indexed | >50 ms |
|---|---|---|---|---|---|
| Reported 12 | 12.300 → 12.458 (+1.29%) | 17.773 → 17.807 | 21.683 → 21.971 | 1558.872 → 1528.343 | 0 → 0 |
| Current 10 | 11.961 → 12.145 (+1.53%) | 17.427 → 17.999 | 25.309 → 22.902 | 1940.747 → 1911.543 | 0 → 0 |
| Large 40 | 25.333 → 25.485 (+0.60%) | 41.486 → 41.138 | 53.075 → 51.148 | 3028.007 → 2629.355 | 49 → 36 |

No >100 ms frames. All nine pair means worsen slightly. This confirms a large
memory saving (~398.652 MiB), not an FPS improvement. Current-map captured peak
increase from the previous turn does not reproduce here; uncaptured current peak
saves ~29.204 MiB. Frame gates still fail on this GPU/workload, before target PC/M1.

All 85 large >50 ms traces examined. Reference 34/49 and indexed 23/36 have
creation events; others do not. Reference slow frames: 30 zoom/19 lighting;
indexed: 24 zoom/11 lighting/one idle. Mean grid draw 40.894/38.703 ms and event
time 8.301/5.566 ms, overlapping scopes. Preserve redraw and simulation work as
separate targets; do not attribute all tails to textures.

Tiny actual-native ownership reproduction: after only a drawing command retains
an indexed image, baseline loses the reusable descriptor while GPU image remains
alive; the bank allocates a different image on the next request. Candidate adds a
descriptor reference only to an indexed command, preserving same-image reuse.
Both paths release the GPU image after command teardown. Ordinary fallback leaves
the command unchanged, avoiding extra indexed-storage retention for that path.

Six paired native indexed-vs-indexed 40-room runs / **6480 measured frames**, differing
only by that lease. All **36 paired phase states/cameras** exact. Mean
25.459→25.795 ms (+1.32%), p95 40.971→41.396, p99 50.525→52.499,
>50 ms 34→38, >100 zero, texture peak unchanged 2629.355 MiB. One pair improves,
two worsen; factory-event work does not fall. **Do not adopt as a performance fix.**
Toy ownership issue is real, but this does not establish it as a station hotspot.
Thirty-one material checks/ten R8/RG8 rendered cases pass with the lease; still private.
All 72 lease-workload >50 ms traces retained and examined; 22 in each lane have events.

All five owner guards: 2938 files unchanged. Jobs terminal; runtime override restored
to guarded empty fixture. Evidence ~70.83 MiB; C 122.98 / D 69.82 GiB free.
No runtime/art copies or screenshot batches added.

## Next action

Keep the lease out and avoid rerunning it unchanged. Prioritize the measured floor/
lighting redraw work on frames without creation events and 4x crew/navigation spikes.
Use fresh bounded per-stage attribution before another remedy; preserve layer order,
visible animation bounds, selected quality and simulation behavior. Private provider
can still be evaluated as a memory remedy, but do not claim FPS or release readiness.
Full workload/loading/lifetime/endurance, target PC/M1 and packaged platform gates remain.
