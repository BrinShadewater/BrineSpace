# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: cap geometry reuse tested in actual private release

## Objective and acceptance
Continue the full PC/Mac performance/release plan. Preserve selected art pixels and default quality; require matched native packaged workloads for optimization acceptance. All original release gates remain open.

## Accepted decisions and constraints
Canonical Node2D wall scaling remains rejected for pixel mismatch. Original-transform cap geometry reuse remains private: scoped pixels pass, but reliable frame-time benefit is not established. Do not adopt solely from microbenchmarks or two improved p95 phases.

## Current state
Normal runtime source/art restored byte-for-byte. New diagnostics/trials live in `output/wall-render-stage-2026-10-07/`, `wall-cap-geometry-2026-10-07/`, `wall-cap-context-2026-10-07/`, `wall-cap-pixels-2026-10-07/`, `wall-cap-release-2026-10-07/`.

Focused normal-render instrumentation: eight rooms/four rotations,3,200checks/32rows. Warmed median render sub-stages: draw_world226.5us, retired-prop filtering12us, layout apply1us, after-layout hook1us, recovery1us. Instrumentation adds timers; this is not a frame-rate comparison. The first edit failed from CRLF/LF mixing; stopped owned child, preserved invalid log, restored original, normalized generator, reran clean. First cache generator also rejected at compile; syntax corrected and direct isolated check passed before native rerun.

Private cap cache preserves original geometry arithmetic/draw calls/transform. Per-view material pools limited16, each limited128 geometry entries; no texture copies. First generic callback cache median paired saving15us/20of32 improved; revised per-context material lookup with reversed microprofile lane order saving20us/24of32 improved (6,400checks/64rows each). Cache-on/off raster1153checks/768pairs pass exactly across8room types,4rotations,2wall settings,3zooms,2fractional shifts,shell+crown. These compare cached/uncached candidate paths; full selected Studio material/edit coverage and lifecycle remain pending.

## Verification
Actual debug=false frozen crew release dbe44a995a5708be,1080p uncapped active40-room pan/zoom at1/2/4x,60frames/phase. Original packed renderer vs11,760-byte one-script cap overlay, source-selection guard confirms baseline/cache path. Six phases: p95 control35.813/45.374/34.348/47.032/49.941/64.914ms; cache37.776/44.381/35.269/49.221/51.580/59.175ms. Four worse/two better; no reliable FPS gain. Max89.673/87.877ms, no measured frame>100ms; not whole-session stall acceptance. Wall-slot averaged CPU changes about0.0007/0.0241/0.0005ms in the three zoom phases, not a major gain. Full crew/drone snapshots, doors/lights/power/zoom, large props, private counters and texture endpoints match. End3037.838MiB each. Clean logs. Final candidate screenshot viewed: art/portraits/cards present, bottom station occluded by hand, not full visual acceptance.

Base PCK unchanged; QA benchmark adapter restored; actual benchmark identity includes the correct adapter hash and overlay/source hashes. Tiny overlay remains in QA/evidence and is not loaded by the restored ordinary adapter. All processes terminal. All2,936owner non-log files unchanged; physical nursery/painted-shell originals verified byte-for-byte.

## Next action
Do not spend more admission work on this minor cache unless a larger redraw remedy uses it. Return to matched worst-frame profile and attribute remaining live-room preparation/large-prop/environment cost. Preserve cached geometry trial as evidence, not an accepted source change. Current crew provider remains private; FPS, peak/lifetime memory,12-room, loading anomalies,endurance,original bugs and targetPC/Mac certification remain open.
