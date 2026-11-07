# Bounded retention of transparent drone layers

Updated: October 10, 2026 · Project: BrineSpace · PC/Mac performance work

## Objective and acceptance

Remove repeated decoding of known-transparent drone layers without changing
selected pixels, simulation, animation timing or the large-atlas cache budget.
This accepts a source fix, not complete release readiness or stutter closure.

## Accepted decisions and constraints

Keep at most 64 textures already proven wholly transparent by the existing decoder
and reduced to immutable 1×1 RGBA images. They remain available through the existing
weak-image restoration path after ordinary lookup eviction. First-use PNG decoding
still verifies each source. Release the extra ownership when the final gameplay/
Studio session owner exits. No additional large-atlas retention, image mutation,
new art, quality reduction, renderer changes or gameplay changes.

Muted secondary-display native tests, isolated user profiles, disabled physical
benchmark input and a 20 GiB free-space floor remain required. No full PCK copies.

## Current state

- `scripts/drone_animation.gd`: 64-entry ownership limit for verified 1×1 invisible
  images, leaving normal LRU/weak restoration and animation sampling intact.
- `scripts/session_art_cache.gd`: clear that ownership at final session exit.
- `tests/test_drone_invisible_cache.gd` and paired new UID: actual GPU eviction,
  ready/no-repeat-decode, identity/pixel, cap and final-session cleanup coverage.
- `tests/index.json`: performance-diagnostics registration and native lane override.

Existing script UID sidecars preserved. No packaged release or Mac certification
changed; uploads and itch.io visibility remain separate release actions.

## Verification

Bounded actual `debug=false` saved40 request trace, idle/pan/lighting at 1×/2×/4×,
90 frames per phase. The baseline trace has 777 events, candidate 700, no dropped
events in either. A 289,013,764-byte four-upload burst recurs at frame 462. It
combines new collection artwork for one mining drone and north-facing mining
layers for another, whose earlier north wheel sheet was evicted at frame 342.
All four paths were requested at frame 460 and finished together two frames later.
The transparent placeholder alone required approximately 69 ms worker decoding.

| Transparent-layer work across the traced workload | Reference | Candidate |
|---|---:|---:|
| Unique transparent source paths | 13 | 13 |
| Decode events | 49 | 13 |
| Repeated decodes | 36 | 0 |
| Summed worker decode time | 1,777.212 ms | 462.205 ms |
| Texture uploads | 49 | 13 |

Summed asynchronous worker time is not gameplay wall time or FPS. The 13 necessary
first-use decodes remain. Candidate restoration is observed directly in the trace.

Three actual release-runtime source-overlay reference/candidate pairs, alternating
lane order, same saved40 workload on Windows RTX 4070 Ti at 1080p: 4,860 measured
frames total. Each pair mean favors retention.

| Metric | Reference | Candidate |
|---|---:|---:|
| Mean frame time | 27.696 ms | 27.552 ms |
| p95 | 44.171 ms | 43.763 ms |
| p99 | 52.969 ms | 52.295 ms |
| Frames >50 ms | 38 | 35 |
| Largest sampled phase-boundary texture memory | 2,660.007821 MiB | 2,660.007855 MiB |

Mean improvement is 0.52%. The texture difference at these observations is about
36 bytes, not a material budget change. Phase boundaries do not establish peak
memory between samples. Candidate maxima include 106.542/108.774 ms: the >100 ms
stall remains reproducible, and full p95/p99/stability gates are not passed.

Physical snapshots match all 27 phase pairs. Complete saved playback observations
match 26/27; the remaining four-field last-rendered Branfort observation is the
same category documented in the preceding waveform pass. Keep it explicit; do
not redefine cached playback fields as authoritative current-time simulation.

Installed native test: **12 checks, zero failures**, including real blank PNG,
65×4 MiB synthetic GPU cache-pressure textures, unchanged transparent image identity
and pixels, immediate readiness without another PNG job/upload, 64-entry bound,
ordinary cache/worker cleanup and transparent-object release on scene exit.
Synthetic textures remain in memory only; no image batches written to disk.

After adding standalone silent/secondary-window preferences, the first test attempt
referenced a test-only helper absent from the release PCK. Its owned failed process
was stopped and configuration restored. The test now configures its own window
without that dependency; installed V3 passes. All jobs terminal, overrides restored,
focused source/index whitespace check passes, all 2,938 owner files unchanged.

This pass uses approximately 36.3 MiB evidence plus 29.2 MiB scratch, with shared
PCKs. At completion C:126.92 GiB/D:78.76 GiB free. No recursive cleanup retry.

Evidence root: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`drone-request-attribution/`, `drone-invisible-request-attribution/`,
`drone-invisible-trial/decode-comparison.json`,
`drone-invisible-gameplay-pairs/summary.json` and `state-differences.json`, and
`drone-invisible-installed-native-v3/`. Focused runners are in
`output/renderdoc-tools-2026-10-08/`.

## Next action

Prepare predictable upcoming visible atlas layers before their first use, rather
than synchronously uploading several when worker jobs finish together. Begin with
deterministic mining collection transitions and approaching work destinations;
measure request/eviction order, required decode lead time, upload scheduling,
prefetch waste and per-frame memory. Keep complete drones, exact pixels, animation
timing and the large-scene memory budget. A larger cache and cropped/row storage
already failed prior gates; do not repeat them unchanged.

Full packaged workload/loading matrix, endurance, original bug closure, target
GTX 1650/M1 testing and native Mac signing/notarization/gameplay remain outstanding.
