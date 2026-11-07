# Project handoff

Updated: October 6, 2026 · BrineSpace · Script profiling and layered lookup

## Objective and acceptance
Reduce measured recurring frame work without changing art, room routing or gameplay.
Overall frame/memory/loading/release gates remain open.

## Accepted decisions and constraints
Only narrow normal classification change; no quality/settings/animation changes.
All native/headless runs use verified scratch user paths; 2,936 owner files unchanged.
Do not treat profiled frame times as release performance.

## Current state
Normal `scripts/grid_canvas.gd`: `_uses_layered_art` reads id once and checks a
constant membership table instead of repeated array membership tests. Expansion
registry lookup remains dynamic. No persistent cache/invalidation dependency.
New `tests/test_layered_classification.gd` and paired UID contain frozen original
oracle, every database room/rotation, expansion ids, StringName ids, unknown/missing/
null identifiers and input immutability. Added to render-perf test index.

## Verification
Baseline parity 709 checks, zero failures/errors; optimized 709 checks likewise.
Three focused CPU pairs of 35,300 calls: original 32.334/34.841/32.893 ms versus
optimized 10.469/11.176/10.495 ms. Same return counts. Headless microbenchmark,
not a gameplay FPS measurement. An earlier test included unsupported numeric/vector
ids which the original errors on; narrowed to actual supported input domain before
timing. Rejected logs/fingerprints retained.

Native 40-room copies differ only in classification, with original exterior drawing
in both. Idle/pan at 1/2/4x, 60 frames per phase after 180 warm-up frames, 1080p,
Godot 4.7.2 Compatibility / RTX 4070 Ti. All six full crew/drone snapshots equal,
zero errors/missing-art failures, clean exits. Candidate p95 lower in six phases
by 0.719–2.114 ms; p99 mixed. One pair does not establish aggregate FPS gain.
Candidate p95 still 38.245–48.124 ms, above 16.7 ms gate. End texture counters
3168.484/3168.333 MiB still exceed provisional large-scene budget.

Private evidence in `output/drone-coordinate-2026-10-06/layered-classification/`
and `classification-station/`; source generator freezes original oracle and must
not be rerun against optimized normal code. Initial native-copy preparation failed
on Windows default text decoding; corrected to explicit UTF-8 before gameplay.

## Profiling evidence and limits
Private `station-current/profiling/`: built-in script profiler enabled only during
six measured phases. Runtime controls: Engine.max_fps=0, VSync=0, low-processor
mode=false. Full 5.16 MiB log and parsed per-phase functions retained. States match
unprofiled current-source baseline. Startup excluded.
Godot's local profiler prints every function periodically and on stop; log output
adds hundreds of milliseconds and accumulated profiler data includes awaiting
benchmark coroutine time and worker-lambda time. Neither is main-thread gameplay
work; do not sum worker/coroutine costs into frame budget or cite profiled p95.
Verified behavior in [Godot 4.7.2 local debugger source](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/core/debugger/local_debugger.cpp)
and [EngineDebugger API](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/doc/classes/EngineDebugger.xml).

Recurring main-thread leads: animated `_draw_underwater_depth` self around
114–127 ms/60 samples (~2 ms per frame); room slot paint self ~59–62 ms, inclusive
~295–354 ms; layered classification ~40k–43k calls; topology ~360 calls and
49 ms self. Hierarchical times overlap. Profile locates candidates, not final
non-profiled cost attribution. Worker atlas decoding/upload remains separate.

## Next action
Investigate water pass's 12 transformed textured segments per wave using bounded
non-profiled counters and exact native raster controls. Preserve existing pixels,
clock, bounds, filter, layering and effects choices before admitting any batching.
Avoid merely reducing quality or assuming scripts explain all engine/render waits.
Matched repeat workloads, actual release Windows/Mac and other original gates open.
