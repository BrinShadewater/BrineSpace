# Project handoff — real station performance verification

Updated: October 10, 2026 · BrineSpace · PC/Mac release readiness

## Objective and acceptance
Verify the private targeted indexed/batched/prewarm provider against current normal
source on real station saves, preserving simulation, visuals and owner data. This
milestone establishes measured tradeoffs and reproducible stalls; it does not admit
the provider or certify release performance.

## Accepted decisions and constraints
Actual debug=false Windows executable, RTX 4070 Ti, 1080p, uncapped measured frames,
muted secondary display and disabled physical viewport input. Scratch APPDATA with
resolved-path guards; owner saves/layouts copied read-only. Reused runtime plus small
overlays, no full package copies, 20 GiB storage refusal floor. No automatic quality
changes, gameplay rule changes, provider installation, art deletion or itch action.

## Current state
Changed tools/release_benchmark.gd (UID preserved): save action now requires a successful
synchronous checkpoint write and validated readback. Dedicated fixture flags are
suspended only for the write and restored immediately. Runtime save logic unchanged.
Large fixture no longer reactivates mining sites beneath occupied cells; its drone
snapshot must pass normal save validation before measurement. One occupied mining site
was excluded. Earlier large reports used the prior fixture and remain historical evidence.

Correction: the earlier camera/action handoff's save commands did not prove writes.
RunSave rejects fixture flags, and the old action ignored that failure. New isolated
fresh and corrected40 runs each pass three actual writes/readbacks (1x/2x/4x).

Focused runners under output/renderdoc-tools-2026-10-08:
run-benchmark-save-readback-verification.py, run-indexed-real-stations.py,
compare-real-stations.py. Real inputs: archived reported12 and read-only frozen copy of
owner brine_loop.save. Current save starts10 rooms, completes its queued construction
to11 during4x zoom. Phase coverage checks now use each phase's actual room count;
the initial fixed-count assertion failed after the first completed current-save run.
That run remains valid and was reused; completed reported runs were also reused.

## Verification
Three alternating pairs/map, idle/pan/zoom/lighting at1x/2x/4x,90frames/phase:
18 runs,19,440 measured frames. Pooled percentiles; matched workload and inputs.

| Map / lane | Mean ms | p95 ms | p99 ms | Max ms | >50 / >100 | Peak texture MiB |
|---|---:|---:|---:|---:|---:|---:|
| Reported12 normal |12.918|19.581|22.907|34.646|0 / 0|1558.872|
| Reported12 candidate |12.892|18.914|22.845|28.732|0 / 0|1528.343|
| Current10→11 normal |12.315|18.046|27.225|101.305|6 / 3|1940.831|
| Current10→11 candidate |12.676|18.516|24.530|102.784|6 / 3|1911.626|
| Corrected40 normal |26.025|44.048|57.139|81.239|67 / 0|3028.007|
| Corrected40 candidate |26.032|42.561|52.369|82.033|44 / 0|2629.355|

Reported mean -0.20%, mixed pairs: effectively unchanged; memory -30.529MiB.
Current mean +2.93%, mixed pairs: regression; memory -29.204MiB. Large mean +0.027%,
mixed pairs: unchanged; memory -398.652MiB (13.17%), >50 count -34.33%, p99 -8.34%.
All p95 fail16.7ms gate. Current recurring >100 and large p99 fail. No consistent
average speed gain, and memory savings alone do not justify production admission.

All108 phase camera start/end pairs exact. All36 reported and36 current full gameplay
snapshots exact. Large30 exact, six cached Branforth playback phase differences of
~2.73e-8 at1x zoom/lighting; all other values exact. Differences recorded explicitly,
not normalized or treated as whole-animation acceptance. Required backend/safe-image,
input/mute/display guards pass. Actual keyboard/trackpad and whole-scene motion remain open.

All123 frames over50ms retained in slow-frames.json and inspected by timing category:
- Current: pan4x frame60 reproduces in all six runs,100.617–102.784ms. Grid callback
  accumulator92.792–93.734ms, step0.976–1.102ms; no sampled/current-frame drone uploads.
  Evidence points to CPU draw preparation/callback work; exact layer/function unproven.
- Current: zoom4x frame27 reproduces53.207–60.468ms, crew30.325–33.496ms, draw15.960–
  18.770ms. No sampled/current-frame drone uploads. Exact crew operation needs tracing.
- Large:111 over50 across both lanes, predominantly zoom/lighting. Draw accumulator
  20.974–62.259ms, step1.919–5.283ms;67 have sampled/current drone uploads. These can
  coincide with other work; retained latest-upload fields are not evidence of same-frame
  causality. Nested callback accumulators and engine GPU timing are not additive.

All jobs terminal; runtime configuration restored. Owner2,938 nonlog files unchanged
after save checks, initial assertion failure, and resumed run. Focused diff check clean.
166.88MiB combined evidence and this-turn scratch (30 short profiles, including resume
allocations); C126.87/D77.41GiB free. No multi-GiB build/snapshot batches.

Evidence root: D:/bs-release-crew-cache-20261009/benchmark-input-isolation/
indexed-real-stations-20261010 (comparison.json, slow-frames.json, identities, frozen
input hashes, per-run reports/logs/screens, owner.json, storage-summary.json).
Save validation evidence: sibling benchmark-save-readback-verification-v2.

## Next action
Use the frozen CURRENT10→11 save to reproduce pan4x/frame60 with bounded per-frame
layer/callback timings; identify the function behind93ms before changing redraw or cache
policy. Separately trace crew zoom4x/frame27. Compare matched runs and relevant pixels/
gameplay after any fix. Keep private provider out of normal source; full scene motion,
fallback/loading/title/Continue resource lifetime still required for admission.
Target hardware, loading/endurance, original bugs, latest Windows/Mac freeze and actual
M1/signing/notarization remain open. The release goal is unfinished.
