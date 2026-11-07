# Project handoff

Updated: October 6, 2026 · BrineSpace · Draw callbacks and large uploads

## Objective and acceptance
Attribute remaining stalls and identify a measured memory remedy while preserving
selected pixels, timing, layouts and quality. No release or platform certification.

## Accepted decisions and constraints
No normal renderer/atlas/art change in this interval. Temporary per-layer timing
uses physical Main/Grid copies and a 512-event buffer drained each measured frame.
Do not equate callback counts with whole-station redraws or stale last-upload
metadata with a current-frame upload. Original crop/storage remapping remains
unaccepted because of its recorded sampling differences.

## Current state
Updated tools/release_benchmark.gd: drain warm-up draw timing and collect the
accumulator every measured sample, including fast frames; preserve field names,
add draw_timing_scope. Engine-wait duration now ends at frame_end and excludes
report collection. Previously hitch-only reads could accumulate earlier drawing;
other observers can also drain the accumulator. Earlier frame-time, actor timing,
state-parity and memory results remain valid; earlier draw totals require this scope.

Evidence: output/layer-detail-2026-10-06/. First diagnostic Grid copy conflicted
with the global GridCanvas class; stopped only its verified test process, removed
the duplicate class declaration from the physical copy and reran. Failed logs
retained under failed-class-copy. Normal game source/UID unchanged.

## Verification
Two native normal-renderer 40-room trace runs exit 0, no runtime art failures.
Corrected run: 15 phases × 60 frames, 59 hitches, no trace events dropped in those
records. All completed probes preserve 2,936 owner non-log files.

First trace: exterior actor callback 51.197 ms in engine frame 486, including
mine-north atlas upload in that same frame: 144,506,880 bytes (~138 MiB),
2688×13440, ImageTexture creation 36.551 ms. Its sample is 84.213 ms.
The later 97.166 ms sample has 76.159 ms between render signals, but still carries
the old upload metadata; delayed driver work is not established as its cause.
Corrected repeat reproduces an exterior callback at 48.853 ms. Typical floor
rebuild callbacks cost ~10/8 ms; mining-bay prop drawing reaches ~8.7–10 ms when
a 96 MB unload atlas uploads. These are attribution results, not FPS improvements.

Counter/trace sums still differ by ~6–7 ms on five corrected zoom hitches despite
zero dropped trace events. Check floor-rest callback coverage and sampling boundaries
before treating that trace as a complete exclusive draw-time sum. Largest named
callback intervals and upload costs remain directly measured.

Separate native feasibility probe uses the existing private Veld loader:
1,800 distinct Image objects, 383,095,296 raw bytes → 28,583,336 lossless Zstd bytes
(365.34→27.26 MiB), zero byte mismatches. Encoding ~255 ms total; per-image decode
p95 59 µs, p99 82 µs, max 2.145 ms. Full eager images remain alive in this probe:
this proves neither actual runtime RAM/VRAM savings nor animation/frame parity.
No selected source file was recompressed/replaced; GPU atlas upload volume is unchanged.

## Next action
The bounded compressed-bank prototype and matched native results are now recorded
in `docs/COMPRESSED_VELD_STORAGE_2026-10-06.md`; default runtime remains unchanged.

Prototype a lossless compressed source bank with bounded decoded working storage
for private presentation, preserving frame objects/metadata and leased draw ownership.
Resync its loader selection against current normal Veld before comparison. Validate
exact bytes/native filtering/movement and full-station CPU/RAM/texture memory; the
earlier eager bank reduced textures but raised Windows working memory and stays
unadmitted. Compression alone cannot fix large rover atlas transfers: keep their
exact sampling/storage remedy separate. Resolve missing zoom callback coverage.
All performance/memory/endurance/original bug/Windows/Mac release gates remain open.
