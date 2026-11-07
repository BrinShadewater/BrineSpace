# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: correct timing scope and measure viewport-query overhead

## Objective and acceptance
Continue full PC/Mac readiness. Separate script, renderer and display costs before changing quality/renderer. Check whether benchmark-only GPU timing creates apparent slowdown. Full original release gates remain open; no FPS certification.

## Research and accepted interpretation
Official Godot4.7.2 main/main.cpp updates Performance process/physics time from process_max/physics_process_max once per reporting second, then resets maxima. Therefore legacy engine_process_ms/process_ms_latest are latest reported peaks, not current-frame costs. Averaging those samples does not yield average CPU frame cost and does not explain a directly timed frame interval.

Official GLES3 storage/utilities.cpp retrieves timestamp queries from frame-2 via GL_QUERY_RESULT and reports texture allocations plus render buffers. Viewport CPU/GPU timings are delayed scoped results; do not add them to script/wall timing. These are engine-source interpretations, not proof of costly blocking in this game. Native timing-measurement comparison tests actual overhead separately. Sources:
- https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/main/main.cpp (process_max/update/reset)
- https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/storage/utilities.cpp (capture timestamps)
- https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_gles3.cpp (frame/render/presentation boundaries)

## Changes
Normal scripts/performance_monitor.gd snapshot adds engine_process_time_scope. tools/release_benchmark.gd adds engine_process_time_scope and render_timing_scope. Existing schema/field names/collection behavior preserved; no art/gameplay/render quality/settings change or GPU-query default change. UID files unchanged. Scope descriptions alone do not retime or correct historical samples.

Private run-render-timing-overhead.py uses identified deferred diagnostic bootstrap/control256MiB, combined private fourcrew provider/current Main/Grid and weak badge overlay. Only viewport measure_render_time toggled on/off; both retain heavy draw profiler and normal automatic reporting. Explicit root focus and sampled focus/cap/VSync metadata. Not the normal title entry or fully audited delivery candidate.

## Verification
Matched actual debug=false40room180frames×nine idle/pan/zoom1/2/4x phases each, then three43room paused scratch disk/staged restores per lane. Both logs clean/0missing. Both0unfocused samples/Engine.max_fps0/VSync mode0. All full crew/drone/door/light/power/zoom state equal; texture peak2348.739303MiB both. All restore room/crew equal/router released, restored2006.029565MiB flat; warm/final exits234.533917MiB flat. Automatic reports1both; pregame report overhead not certified by this active sample.

GPU timing on/off P95 idle/pan/zoom1x34.169/35.437,35.926/36.730,52.097/52.750ms;2x37.873/41.559,39.771/39.618,52.586/56.015ms;4x43.334/43.642,42.550/42.332,62.329/60.008ms. Three improve/six regress when off; mean results mixed. No reliable improvement/no cause claim. All fail16.7ms. Max87.627/85.673ms. Earlier101ms redraw burst remains unresolved.

Final-phase prop counters differ again: onadvances19216/live117544, off19214/live117531; prepares2196/static29467/slots228/canvases12 equal. This is rendering work, not automatically a simulation difference. Prior12room observer proved matching submitted clocks there; uninstrumented40room discrepancy remains open. No full prop animation closure.

Relevant isolated headless validation: test_performance_monitor PASS failures0; synthetic observe cost0.1881us/sample (not native GPU/collector acceptance). Updated maintained benchmark loads/can_instantiate, compilePASS/clean. Both test owner2936unchanged. All native/test processes terminal, private adapter restored, original normal QA/full PCK intact. Evidence `output/all-crew-storage-2026-10-07/render-timing-overhead-2026-10-08/{identity,owner,on,off,comparison}.json`, logs/images/restores; timing-scope-check-2026-10-08 logs/owner.

## Next action
Check heavy draw-profiler overhead separately, since it remains enabled in both lanes and default gameplay leaves it off. Use matched workload/current-frame wall timings and explicit scope, then profile material renderer/backend costs. No optional-GPU-query change justified as a game optimization by this pair. Preserve all original pixel/timing/memory/endurance/targetPC/Mac/ninebugs/package certification gates.
