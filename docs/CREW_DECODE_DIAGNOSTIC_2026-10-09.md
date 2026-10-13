# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: crew decoder cost attribution

## Objective and acceptance
Determine whether lossless crew image reads/decompression outside presenter misses contribute to frame cost. Measure before changing cache budgets or pixel storage. This is diagnostic work, not an accepted optimization.

## Accepted decisions and constraints
Keep selected pixels, format, mipmaps, independent returned Images, frame identities and existing64MiB GPU cache. No new retained raw image cache. Normal source and frozen delivery unchanged. Every probe uses verified scratch profile and owner fingerprints.

## Current state
D:/bs-release-crew-cache-20261009/crew-decode-diagnostic/frame.gd adds bounded scalar counters/timing to original source getter and public texture-image requests. overlay.pck contains only original frame resource path. Getter still decompresses into a new independent Image. External benchmark collects phase start/end raw counters plus existing presenter counters; timings overlap and must not be summed.

## Verification
18 isolated headless checks pass for RGBA/RGB, mipmaps, dimensions, exact pixels, mutable copy independence, call/byte/timing accounting; owner2,938 unchanged. This is small synthetic coverage, not animation/gameplay acceptance.

Initial actual probe session85875 fails before gameplay because loader _ready adds a node while root is setting up children. No decoder-cost claim; workloads failure/log and owner guard retained. Corrected bootstrap defers boot until root setup completes, mounts overlay before compiling benchmark, verifies actual bank CpuFrame identity and unchanged cache budget. Fresh two-workload actual debug=false session53341 running in workloads-v2; no restart of a live process occurred.

## Next action
Poll session53341. Inspect completion/error markers and source/presenter phase deltas. Raw source calls minus nested presenter decode calls can reveal other image reads; CPU timings are nested, not additive. Require evidence before selecting CPU read caching or larger GPU pose cache. Cache budgets unchanged. Full performance/release gates remain open.

Completed session53341 exits0: two actual debug=false standard workloads/48 phases/8,640 samples, zero engine/safe-image errors, owner2,938 unchanged. Large raw source reads1,191 exactly equal presenter decodes1,191; reported1,351 equals1,351. Other source reads0 and spill allocations0 in both. Raw decoder CPU mean0.0376ms/frame large,0.0445ms/frame reported; highest phase means0.0978/0.1058ms. Submission CPU means0.0151/0.0155ms. Nested intervals must not be summed. Evidence workloads-v2/analysis.json. This rules out repeated outside-presenter reads as a hotspot in these selected workloads; does not certify every roster/scenario or justify increasing the cache budget. Next prioritize measured rendering/preparation costs.
