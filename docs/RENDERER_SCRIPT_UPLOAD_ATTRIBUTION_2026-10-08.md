# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: actual renderer/script/upload attribution

## Objective and acceptance
Continue full performance/bug/PC-Mac readiness plan. Identify dominant ordinary-frame cost before another small navigation change. Diagnostic measurements do not certify FPS or GPU attribution for individual stutters. No publication/normal source edits.

## Accepted decisions and constraints
Renderer counters are supported/nonzero in this actual Compatibility runtime. CPU/GPU times overlap; do not add them. draw stage hierarchy overlaps and GPU queries may represent buffered render results. Current-frame upload grouping is association, not an isolated causal comparison. Stage label setup_large_child_base actually wraps child _draw; not cache submission/setup. Correct earlier provisional interpretation.

## Current state
D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/render-attribution/ independent actual debug=false bootstrap/patch copies, runner, candidate.json, analysis.json, identity-candidate.json, owner-candidate.json. Same private combined navigation/beacon inputs as earlier, one diagnostic candidate, trace/render timing/draw profiler enabled. Bounded trace3,000 frames below4,096 cap. Added already-collected draw/system/stage values to trace. No per-primitive new instrumentation or default quality change.

## Verification
Actual native1080p40rooms/four crew/three natural missions;3,000idle1/2/4x frames. Complete lifecycle, no route fallback, assignments released/full graphs recovered. Exact compiled NPC/mission SHA and optimization counters verified. Logs clean/no warnings/errors/leaks/missing art. Owner fingerprints2,936same/adapters restored/process terminal.

All3,000 renderer CPU/GPU samples nonzero. Renderer CPU median15.277ms/p9518.336/max24.462; GPU median13.016/p9515.695/max20.454ms. Phase mean draw calls6,390/6,465/6,419. Total frame median46.552/p9559.306/max138.103ms; more instrumentation than unprofiled42–45ms runs, not matched performance comparison. Simulation step median1.282ms/p953.146 (graph spikes remain); aggregate script grid draw median21.334ms. CPU boundary before render median28.720ms/render signals15.813ms; boundaries wall time, not GPU timer substitution.

No current-frame drone upload2,660 samples: medians frame45.934ms/draw21.104ms/step1.269ms/renderer CPU15.266/GPU13.001ms. Current uploads340 samples: frame55.555ms/draw27.825ms/step1.617ms/renderer CPU15.440/GPU13.129ms. Recorded upload events can omit prior queued work; do not infer zero upload/driver cost from group. Trace collection median81us/p95140/max268us outside sampled frame interval, other instrumentation overhead unmeasured.

Stage means live_rooms13.057ms, setup_large_child_base7.758ms, actors_effects1.802ms, door/light validation1.473ms, environment1.521ms, exterior actors1.448ms, lines1.058ms. Hierarchical, not additive. Source inspection scripts/large_room_canvas.gd: MoonBase/StaticBase/ImmediateBase _draw call record_draw("large_child_base"), which also increments live_rooms. Hence major base field is actual room module drawing; StaticBase.submit snapshot cache is a different operation. Prior idle cache hit evidence does not eliminate active base draw cost. Current Grid _draw_room hands active appearance/clock/ports to retained canvas; dynamic Moonbay/Tidal bases need room-type attribution next.

Worst4x frame653138.103ms: step46.493ms, aggregate grid draw65.457ms, uploads289,013,760 bytes, renderer14.841CPU/11.600GPU (not exact GPU stall cause). Another4x frame196118.651ms: step1.278ms/draw92.242ms/uploads289,013,764bytes.1x frame494113.474ms: step2.747ms/draw86.405ms/uploads337,182,720bytes. Both ordinary base rendering/submission and upload-related CPU/draw spikes remain. Peak2,346.502MiB/exit228.259MiB/uploads4,074 same fixture endpoint, no saving claim.

## Next action
Split large_child_base draw timing/count by actual room type in private runtime, then target dominant repeated static geometry while preserving dynamic water/doors/beacons/layer order/pixels. Measure renderer CPU/GPU and script reductions together; avoid cache-key micro-optimization based on misleading setup label. Separately profile upload preparation versus API/driver wait; immutable memory budgets remain. Third/reversed admission evidence, native visuals/moved props/combined full checkpoint/title controls and all original loading/memory/endurance/PC-Mac release gates remain open.
