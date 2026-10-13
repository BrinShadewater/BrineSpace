# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: preserve retained navigation point lookup

**Superseded:** the point-map optimization was withdrawn after real-station
comparisons showed inconsistent FPS and increased structural crew time. The
original large-fixture evidence below remains historical. See
[real-station results and rollback](REAL_STATION_NAVIGATION_COMPARISON_2026-10-11.md).

## Objective and acceptance
Continue the full PC/Mac performance plan. Reduce placement/demolition crew spikes with exact graph/order/route and gameplay parity. Frame, loading, endurance, bugs/UI and release certification remain open.

## Accepted decisions and constraints
Muted secondary native benchmarks, isolated profiles and owner fingerprints; shared debug=false runtime, no large screenshots/runtime copies. Preserve gameplay timing, staged loading, graph ordering, disabled-node reset, ownership and UIDs. No delayed navigation or shared mutable actor graphs.

## Current state
Installed measured candidate in scripts/bill_npc.gd. Synchronous rebuild retains its existing `points` dictionary prefix and removes only entries with IDs at/after prefix_count. It no longer clears/recreates unchanged prefix lookups using thousands of AStar get_point_position calls. Zero-prefix/full rebuild still clears points; staged rebuild still clears points at its original early location. Graph removal/append/connect ordering, point IDs/weights, disabled resets, room maps, paths/goals and signature logic untouched. No new lookup table/cache. Same dictionary identity retained.

Maintained tests/test_navigation_prefix.gd adds explicit points.keys()/values() ordering parity. Existing paired UIDs unchanged. Installed bytes equal measured candidate, SHA c414f3b847062d2279fbc5bd0fcb26496d00c99ffa35ba61192916171689c5c5.

Private scripts in output/renderdoc-tools-2026-10-08: run-structural-navigation-stages.py, verify-retained-point-map[-native,-installed].py, run-retained-point-map-workloads.py, analyze-retained-point-map-workloads.py. Evidence in D:/bs-release-crew-cache-20261009/benchmark-input-isolation/{structural-navigation-stages,retained-point-map-trial,retained-point-map-workloads}.

## Verification
Stage probe: nine full phase states/cameras and fifteen action events exact. Each actor retains9174 points. Cached room/point assembly ~3–3.6ms warm per actor, James first placement7.665ms including cold work; native removal~1.0–1.2ms, geometry~1.1–1.7, boundaries~.86–.93. James goal selection still~7–13ms; route_between contributes~3.9–4.3ms, up to168calls at first placement. Method timers overlap; retained_point_count's numeric usec field stores node counts, not microseconds. Attribution only.

Initial editor-overlay parity ran twice and then runtime guard proved candidate still loaded original source due early project autoloads. These initial green logs do NOT validate the candidate. A source-code guard initially used a wrong static property API and failed parsing; corrected explicit Script cast/get_source_code. All failures retained, guards restored. Use early-pack release bootstrap for overlay tests.

Corrected debug=false executable/headless parity mounts overlays before gameplay parsing: reference runtime=false, candidate=true, exactly one run each. Both94checks/zero failures,115344 point records and888 routes. Includes warm reuse, disabled reset, hardware/room locks, moonbay boarding/submarine state, geometry revision, detached addition and suffix removal. Installed maintained-source test repeated after the production/test edits: runtime=true, same94/115344/888, zero failures/errors. This is graph/route acceptance, not render certification or direct staged-yield coverage; staged early clear preserved in source.

Three alternating large-station pairs, six real debug=false native runs/9720frames, lighting/connected placement/demolition1x/2x/4x,180frames/phase. Runtime source guard false/true in every before/after run. All27 full phase states/cameras and45 paired successful action events exact. Logs clean, no missing art.

| Metric | Before | Installed |
|---|---:|---:|
| Whole mean ms |24.920|24.544|
| p95 ms |41.313|40.569|
| p99 ms |52.546|50.773|
| Maximum ms |97.710|96.380|
| >50 / >100 frames |65/0|54/0|
| 18 structural-event crew mean ms |32.487|31.427|
| 18 structural-event frame mean ms |89.911|88.680|

Crew17/18 events better, mean -3.26% (~1.06ms). Whole mean -1.51%, all three pairs better, strongly influenced by one slower reference pair. Event whole-frame mean -1.37%. Admit a small equivalent navigation optimization, not a major FPS fix or release acceptance. Large frame gates still fail by a wide margin; no target-hardware/macOS claim. Texture unchanged3028.476MiB.

All owner guards2938 unchanged; jobs terminal/runtime override restored. Logical new evidence28.92MiB plus recorded scratch19.86MiB. Completed six traces compressed only after jobs terminal:20.90→8.01MiB allocated, content SHA before/after exact. Runtime/PCK/owner files untouched. Free C134.89/D68.93GiB; unrelated C free-space increase not attributed to this task.

## Follow-up checks

Maintained staged rebuild coverage passed both source lanes: 110 checks,
127892 point records and 984 routes in the debug=false executable (headless).
It observes actual yields and partial lookup bounds, requires no staged prefix
reuse, and compares final ordered graphs/maps/routes against fresh assembly.
The fixture is disabled and tree-attached; UID unchanged. This verifies staged
construction, not title/Continue or rendering.

The initial reported/current cross-map batch found four state differences,
all mining-bay warning arrival/order on current pairs 1 and 2 at 4x. Other state
paths and cameras matched. drone_idle_alert.gd uses a three-second wall-clock
check. V2 substitutes visual simulation time in a test-only overlay, with a
runtime source guard. Production warning behavior is unchanged. Full state
equality remains required; the initial batch is not accepted as parity evidence.
An initial v2 fixture type-inference error was corrected with explicit float;
the errored run is excluded. V2 results remain pending.

Completed initial reports compressed from 37935658 to 14389248 bytes on disk;
all twelve content hashes exact. Owner guard: 2938 files, zero changes.
No runtime copies or screenshot batches.

## Next action
Verify installed point-map change on current/reported maps and relevant staged/live scene cases before broad release acceptance. James goal selection remains the larger unexplained decision cost: route calls explain only part. Attribute candidate/target preparation, station claims and sorting without changing RNG draws/ordering, route choices or crew timing. Structural rendering still~30–35ms and recurring image uploads remain separate targets. Do not repeat rejected larger-cache/indexed/crop/screen scalar trials unchanged. Keep the full original release plan active.
