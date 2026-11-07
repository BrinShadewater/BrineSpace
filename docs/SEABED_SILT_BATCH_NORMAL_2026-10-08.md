# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: seabed batch in normal source

## Objective and acceptance
Continue the complete PC/Mac performance and release plan. Preserve selected pixels, animation timing and effects. This is a source milestone, not release certification.

## Accepted decisions and constraints
The still seabed now uses one ordered triangle array for its original silt tiles. Preserve original positions, mirrored UVs, per-quad Geometry2D triangulation, texture, tint, filter and layer order. No image mutation, texture cache, downscaling or animation change. Prior three actual matched pairs and independent camera/culling checks support this narrowly scoped admission; the historical two-advance/thirteen-draw zoom difference remains open, not attributed to this change.

## Current state
Changed assets/environment/seabed-v1/seabed_background.gd only within render_still; code outside that function matches the retained backup. Added tests/test_seabed_silt_batch.gd and paired uid://dtxtrs1vdqq1y; registered performance-diagnostics in tests/index.json. Test embeds the original renderer, so it has no dependency on disposable private output.

## Verification
Installed source: 1,152 checks, zero failures; 576 exact native composed pixel pairs with the production fog as a separate overlay, actual quality presets, reduced motion, caustic clocks and lights, filters and transforms. Composed reference calls 207/236 versus 12; silt-only earlier 196 versus one. Clean log, owner fingerprint 2,936 files unchanged. Evidence D:/BrineSpace-performance/2026-10-08/silt-install-draw-proof/; original source and status backups under silt-install/.

Earlier three actual debug=false 40-room pairs: median means improve in all nine phases by 0.142–1.409 ms; p95 improves six of nine and still fails 60 FPS. Texture peak/exit/uploads unchanged. See SEABED_BATCHING_AND_COMPLETE_DRAW_CENSUS_2026-10-08.md for the original private trial; its source-admission statement is superseded by this milestone. No refreshed combined packaged-game acceptance yet.

## Next action
Reduce larger measured rendering/submission and preparation costs. Complete combined source export, original nine packaged issues, saves/UI, endurance, cold/warm loading, stalls and texture lifetime gates; verify target Windows hardware and M1, signing/notarization/Gatekeeper. New diagnostic outputs and isolated profiles use D:/BrineSpace-performance rather than the full C drive. A byte-identical generated bootstrap EXE moved to D:/BrineSpace-performance/2026-10-08/retained-bootstrap/ (relocation.json); restore it before using old C-bootstrap runners. Canonical release and all packs remain intact; no player files moved.
