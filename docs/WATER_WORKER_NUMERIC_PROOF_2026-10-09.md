# Project handoff

Updated: October 9, 2026 - Project: BrineSpace - Task: bounded numerical water workers

## Objective and acceptance

Continue the complete PC/Mac performance/release-readiness plan. Test a way to
reduce main-thread water preparation while preserving exact selected pixels/timing,
normal simulation,owner layouts/saves. Headless speedup is not gameplay acceptance.

## Accepted decisions and constraints

Keep this prototype private. Normal source and the accepted water batch are
unchanged. Only pure numerical command/geometry creation is tested on workers.
No SceneTree,GPU,image,texture,physics,navigation,save or shared-resource mutation
occurs in worker callbacks. Do not change renderer thread mode or engine version.

## Current state

Two-worker group handles three independent bay contexts. Each context exclusively
owns its mutable captures/topology;input footprint arrays are read-only. Main thread
updates inputs before dispatch and reads outputs only after joining the entire
group. Every group completion is explicitly waited,disposing task handles.

32cases cover4rotations,4airlock levels (including0,.4,.998,1),pump off/on. Each uses
three bays with staggered rotations,and3water footprints per bay. 12advancing clocks
per case,first4timing samples excluded,call order alternates sequential-first and
parallel-first. Reference and candidate use identical current normal math/helper;
private half-width change is deliberately excluded.

Initial proof:3456exact packed-command checks,zero failures,384joinedgroups. Extended
proof:3584checks/zero failures,adding96cache-bound checks and32weak-reference release
checks after joined task data is cleared. Same384groups joined. Final geometry wall
time median-of-case-medians6.282->4.803ms sequential-first,6.462->4.592ms parallel-first.
Parallel faster27/32 and32/32cases respectively;5cases slower in first order,so no
universal speedup claim. Worst parallel case median7.745ms(first order). Initial
results retained separately;extended run establishes cleanup checks,not native FPS.

Evidence D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/water-worker-proof/
(build-test.gd,build-result.json,analysis.json,logs/profiles/owner fingerprints).
Only documentation changes in checkout:this note and CURRENT_STATUS.md. No normal
or public package/source rendering change this turn.

## Verification

Exact vertex/color/index bytes and non-stroke commands checked after every joined
group (3456comparisons);numeric cache cap1024 and detached work-context release tested.
No thread safety checks disabled. QA4.7.2/headless logs clean;all2936 non-log owner
files unchanged,all processes terminal. An incorrect Python runtime environment
path prevented one launcher from starting;corrected before Godot ran. No gameplay
or GPU workload ran concurrently with these measurements.

## Next action

Private actual-render prototype: begin at most2numeric jobs while existing parent
room drawing continues,consume matching current-frame geometry on the main thread.
Use immutable input identity;keep synchronous fallback and stationary/reduced-motion
cache behavior. Transfer mutable topology exclusively while a job owns it;all task
joins must happen on consumption,invalidation,culling/removal and scene exit. Never
move simulation or GPU work,show stale/incomplete rooms or change animation timing.

First prove native full-room/lifecycle parity and actual source/branch execution.
Then matched debug=false CPU/GPU/frame comparisons must demonstrate net benefit;
background scheduling/allocator contention can cancel the headless gain. Current
normal batch retains prior evidence. Full FPS/stutter/loading/endurance/bug closure/
target hardware/Mac certification remain open; no publication authorized.
