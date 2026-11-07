# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: single-buffer PNG sharing

## Objective and constraints
Avoid duplicate PNG decoding without extra file-read/hash passes. Preserve runtime
PNG loading, independent frame wrappers/metadata, immutable pixels and bounded
prefetch. This is a private experiment, not normal-backend admission.

## Current state
Generator: `output/compressed-crew-2026-10-06/prepare-single-buffer.py`.
Candidate/evidence: `bounds-cache/single-buffer/` under that directory.
The loader first takes an independent prefetched image when available. Otherwise
it reads encoded bytes once, hashes that buffer, and either reuses a live weakly
indexed immutable source or decodes that same buffer. Successful fresh decodes
enter the existing bounded prefetch cache. Invalid sources fall back to ordinary
SafeImage diagnostics; no permanent image cache, art/quality or normal loader change.

## Verification
One matched native loader pair without prefetch: three-bank preparation
**8,394.501→7,259.178 ms** (1,135.323 ms / 13.5% less). Avoids 3,267 alias decodes;
unique source counts unchanged (Veld 1,800, James 3,477, Marsh 557).

All three complete selected-bank consumer runs pass: Veld 48,579 checks,
James 167,285, Marsh 20,136, zero failures. Pixels, dimensions, frame metadata,
effective filters, boundary selection and 30/60/120 FPS clock/snapshot replay
compare against normal players. Reading-specific Veld coverage remains separate.

Separate matched bounded-prefetch pair, each variant with a fresh isolated manifest:

| Loader-bank preparation | Decode-before-sharing | Single buffer |
|---|---:|---:|
| First load / empty prefetch order | 8,664.892 ms | 7,521.910 ms |
| Second load / recorded prefetch order | 2,694.205 ms | 2,728.557 ms |

Cold here means an empty prefetch manifest, not a flushed OS disk cache. Warm means
the second load in the same process. These bank timings exclude scene startup and
prefetch shutdown. No meaningful warm improvement established. Both warm runs submit
9,102 workers, peak at 96 pending jobs and 34,652,160 decoded bytes (~33.05 MiB);
recent-cache budget remains 16 MiB. Worker decoding still includes identical aliases:
the optimization skips duplicate main-thread decoding, not worker work already done.
All completed runs cleanly exit without engine errors and preserve 2,936 owner files.

## Next action

Follow-up failure/title lifecycle coverage is recorded in
[SINGLE_BUFFER_LIFECYCLE_2026-10-06.md](SINGLE_BUFFER_LIFECYCLE_2026-10-06.md).
Private error handling now preserves placeholders without assertions; normal
backend admission and longer warning/endurance gates remain open.
Keep the faster candidate private pending matched full-scene readiness/memory/frame
comparisons and repeatability. Test actual title loading/progress and save/Continue,
plus error fallback paths, before admission. Any worker-level deduplication needs
separate scheduling/ownership evidence; do not infer it from lower main-thread time.
Anonymous exit warning, sustained frame/loading targets, full memory budgets,
original reports, endurance and actual Windows/Mac release remain open.

Full-scene follow-up: three native 40-room pairs now show startup savings in every
pair (783–1,293 ms; median paired 1,212 ms), with full crew/world snapshots equal
in all 45 phases. Texture footprint unchanged, no FPS gain; readiness/frame gates
still fail. See `SINGLE_BUFFER_STATION_2026-10-06.md`. Normal backend remains unchanged.
