# Project handoff

Updated: October 6, 2026 · BrineSpace · Exact room-card content-region scanning

## Objective and acceptance
Remove measured startup work while preserving the exact source rectangles, pixels,
scale and framing of runtime room art. Release frame/memory/platform gates remain open.

## Accepted decisions and constraints
No art, quality, filtering or save changes. Current normal Grid source has existing
unrelated changes; only `_find_content_region` changed here. Compressed crew stays
private. All probes use verified scratch profiles and preserve failed evidence.

## Current state
`scripts/grid_canvas.gd` now finds the first/last visible sample in each sampled
row instead of visiting every interior sample. It retains the original even-pixel
lattice, alpha/RGB thresholds, margin, empty-image fallback and all image formats.
Rows with no visible samples still use a full forward scan. No cache added.

Added `tests/test_card_content_regions.gd` with a frozen original method, paired
UID and render-perf registration. Generator and native profiler live in
`output/compressed-crew-2026-10-06/prepare-card-region-test.py` and
`prepare-card-profile.py`; profiler uses physical copies and per-call timers.
Do not regenerate the frozen regression reference from optimized source.

## Verification
Baseline native profile: 95 region calls, 244.572 ms GPU readback, 678.285 ms scans.
Optimized native fresh run: same 95 calls, 197.171 ms readback, 99.080 ms scans
(~579 ms less scan work). Continue: 95 calls, 149.988 ms readback, 98.525 ms scans.
Readback fluctuations are not a claimed optimization; that code is unchanged.
One old/new native comparison, not three-run release certification or overall FPS gain.

406 exact region/input-immutability checks pass, including 79 unique runtime room/
variant paths and 84 synthetic combinations across RGBA8/RGB8/RGBAF, odd/small
dimensions, threshold boundaries, dark/empty/full/odd-only/sparse content. Paired
CPU totals 447.146→49.982 ms. No unavailable runtime paths or artwork failures.
Initial test preparation had a string-escaping parse error; corrected before
algorithm evaluation, failed log retained. New UID unique in scripts/tests/rooms.

Optimized actual title/New Game/transmission/Studio/save/title/Continue: 154 checks
pass, crew restoration and sampled old-resource release pass; zero engine errors.
All 2,936 owner files unchanged. One anonymous exit ObjectDB warning remains open.
Earlier first native profile sampled only one cycle and its Router constant referred
to the original namespace; its 17 checks did not verify cloned private bank release.
The optimized profiler fixes this diagnostic namespace and verifies actual resources.

Evidence: `output/compressed-crew-2026-10-06/card-region-regression-fixed/`,
private `single-buffer/card-profile/` and `single-buffer/card-profile-fast/`.
Rectangle equivalence proves identical cropping for covered inputs; this is not
packaged visual, focus/input, minimum-hardware or Mac certification.

## Next action
Recheck loading-screen gap timing after this source change; remaining readbacks and
nursery setup can still delay updates. Prioritize the separately measured rendering/
rover upload stalls for gameplay frame pacing. Full workload, memory, warning,
endurance, original bugs and PC/Mac executable gates remain open.
