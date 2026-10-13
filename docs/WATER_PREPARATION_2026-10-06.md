# Project handoff

Updated: October 6, 2026 · BrineSpace · Animated water preparation optimization

## Objective and acceptance
Reduce recurring water pass CPU work while preserving commands, pixels and clocks.
Overall PC/Mac frame, memory, loading, visual and release gates remain open.

## Accepted decisions and constraints
Normal narrow function change only. No wave removal, batching, frame reduction,
shader replacement, art change, downscaling or settings change. Every native run
uses verified scratch user directory; all 2,936 owner non-log files unchanged.

## Current state
`scripts/grid_canvas.gd::_draw_underwater_depth` prepares the 12 immutable source
rectangles once per pass, reads texture dimensions once and reuses per-wave tint.
Resizes each 13-point array once instead of growing it. Original sin arithmetic,
segment transforms, destination/source crop arithmetic, draw order and fallback
polyline preserved. Preparation waits for the first eligible wave, so empty/nonwave
ranges and rect-only passes do not load wave art. No permanent resource cache added.

Permanent native test `tests/test_water_depth_preparation.gd`, fixture
`tests/water_depth_fixture.gd`, paired UIDs and render-perf index entry.
Oracle freezes original function; fixture invokes actual current normal Grid method.
Do not regenerate original oracle from optimized normal source.

## Verification
Private prototype: 145 checks, 144 exact native image pairs, zero failures/errors.
Actual normal method: final 147 checks / 144 exact pairs, zero failures/errors,
clean exits. Covers textured/fallback waves, nearest/linear, four fractional sizes,
three clocks, all/lines/rects, negative cell coordinates, fractional translation,
nonuniform scale and tint/alpha. Added no-wave range loading check exposed eager
preparation (147 checks, one failure); lazy preparation fixes it. Failed evidence
retained rather than replacing results.

Final three native CPU pairs, 899 cells / 300 waves / 3600 original segments,
30 callbacks per pair: old means 2023.567/2013.600/2016.567 us versus new
1578.400/1575.767/1579.400 us. Roughly 22% less CPU work in this pass; draw command
count unchanged. GPU/readback/swap time outside callback timing, no FPS claim.

First 40-room pair confirmed ~0.415–0.442 ms less water pass work. After lazy fix,
new matched pair confirms every phase: old 1.839–1.924 ms, new 1.437–1.502 ms.
Same 1080p deterministic fixture, 180 warm-up frames, 60 idle/pan samples at 1/2/4x,
Godot 4.7.2 Compatibility / RTX 4070 Ti, VSync disabled. All six full crew/drone
states equal, texture end counters equal 3168.333 MiB, no errors/missing art, clean
exits. Whole-frame p95 mixed, candidate 38.323–48.381 ms: still fails 16.7 ms gate.
No general frame-pacing or loading acceptance established.

Evidence in `output/water-preparation-2026-10-06/`: prototype, normal-source,
lazy-before/after, station and station-lazy results/logs/owner fingerprints;
latest station comparison retained. UID uniqueness and test-index JSON checked.
Private generators under `output/drone-coordinate-2026-10-06/` preserve inputs.

## Next action
Investigate rendering command volume and remaining frame work with bounded counters;
water still submits 12 transformed textured segments per wave. Any proposed batching
must pass exact native raster comparisons, including crop/UV/filter and transformed
scene cases, and prove net benefit in matched station workloads. Do not infer whole
frame causality from this isolated CPU improvement. Room slot work, navigation,
upload stalls, memory budgets and packaged Windows/Mac/endurance gates remain open.
