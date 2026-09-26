# Native large-station baseline

September 21, 2026; Godot 4.7.2 Compatibility, NVIDIA RTX 4070 Ti, Windows.

The first run's nominal 100-room sample contained 78 rooms because the fixture's
11x11 placement area exhausted available cells. tests/profile_large_station.gd now
searches a larger bounded area and explicitly rejects a missing target count.
The corrected native run completes with zero fixture failures and actual 50/100
room counts. The new placement extent changes the station shape; do not treat the
two runs as a before/after runtime optimization comparison.

| Scenario | Rooms | Loop mean ms | p95 ms | Simulation ms | Render CPU ms | GPU ms | Draw calls |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 50 overview | 50 | 52.45 | 55.98 | 1.54 | 16.39 | 14.83 | 7,655 |
| 50 close | 50 | 11.56 | 12.28 | 1.59 | 3.50 | 2.23 | 1,853 |
| 100 overview | 100 | 79.91 | 82.36 | 2.04 | 23.93 | 21.71 | 12,502 |
| 100 close | 100 | 12.69 | 13.89 | 1.60 | 3.70 | 2.37 | 1,873 |

The fixture explicitly forces drawing and enables detailed draw profiling. Loop
means therefore must not be converted into ordinary gameplay FPS. The overview
rendering burden is real within this comparison, but no optimization is claimed.
A single architect moves; active drone frames remain zero. Free building and disabled
failure conditions belong to this fixture only. Save/load/menu interactions complete;
load first-frame latency reaches 398 ms. Broader actor loads remain unmeasured.

Next: isolate overview draw submissions/retained geometry and confirm any change
with native visual parity. Do not reduce simulation fidelity or remove art merely
to obtain a lower count. Correct active-drone coverage before using this fixture
to judge drone performance.

Evidence: output/game-pass/2026-09-21-count-verified/large-render-profile.json,
its native captures, and output/performance-2026-09-21/large-count-verified.log.
The earlier 78-room evidence remains under output/game-pass/2026-09-21-current/.

## Layer attribution

An output-only native probe pauses the same 100-room fixture and hides/restores
one render group at a time; no production visibility changes. Baseline 12,597
reported draw calls. Hiding floor halves yields 9,925 and 9,753; walls 10,495;
room contents 10,921; terrain 11,221. Counts have small live/UI variation and
parent/child groups overlap, so reductions must not be summed as independent totals.
The two floor passes are the strongest initial target, followed by walls. Existing
modular floor meshes already batch tiles: locate the remaining floor submissions
before changing that path. No art removal or runtime optimization implemented.
Evidence: output/performance-2026-09-21/layer-attribution.json and layer_probe.log.

## Floor component attribution

Native output-only probes isolate one room floor, then draw only that room's
production equipment-shadow function on a separate canvas. Both exit zero. Shared
non-room baseline: 511 draw calls. Research and Med Bay each report 604 with the
floor and 599 with shadows alone: approximately 93 versus 88 incremental calls.
Other non-corridor rooms likewise spend most floor submissions on shadows (for
example Crew Hab: 40 versus 34; reactor: 53 versus 46). These are draw-call counts,
not isolated CPU/GPU timings. The standalone shadow canvas uses full light and a
fixed scale; it does not establish visual parity or a frame-rate improvement.

The corridor shadow-only result is not applicable: the grid uses a dedicated narrow
corridor renderer while `_bill_room_view` returns the nursery fallback. Exclude it
from room-shadow conclusions.

Current production shadow rendering issues three clipped projected polygons and
three rounded anti-aliased StyleBoxFlat contact bands per eligible prop, plus four
perimeter bands. Tile meshes are already batched. Next experiment should batch or
cache equivalent shadow geometry while retaining alpha-overlap order, rounded
edges, footprint registration and light response. No production rendering or owner
layout changed in this investigation.

Evidence: output/performance-2026-09-21/floor-types.json, shadow-types.json,
floor_probe.gd/log and shadow_probe.gd/log.

## Projected shadow batching installed

`rooms/whole-room/room_lighting.gd` batches each prop's three clipped projected
polygons into one indexed triangle submission. Prop order, overlapping alpha,
clipping and rounded StyleBox contact bands remain unchanged. The reference path
is available with `--reference-projected-shadows`. The RenderingServer API follows
https://docs.godotengine.org/en/latest/classes/class_renderingserver.html#class-renderingserver-method-canvas-item-add-triangle-array.

Native regression `tests/test_projected_shadow_batch.gd`: nine image comparisons
(three scales x three light levels), zero changed pixels. Fixtures include overlapping
props, footprints, clipped boundaries, hidden props and owner-shadow exclusions.
Maintained test passes, with explicit native lane override. Sample shadow and full
station overview images inspected. This is bounded render parity, not owner art
acceptance or complete room-layout coverage.

100-fit profile: 12,502 to 11,052 draw calls (-11.6%); render CPU 23.93 to 21.25 ms,
GPU 21.71 to 18.88 ms in these two instrumented runs. Timing varies between runs;
no ordinary-play FPS claim. Profile exits zero, all requested room counts reached.
Evidence: output/game-pass/2026-09-21-projected-shadow-batch/,
output/performance-2026-09-21/shadow-parity.json and shadow-regression.log.

**New fixture limitation:** the inspected 100-close screenshot shows empty space,
not rooms. Its low timing cannot support close-room performance conclusions; the
older close measurements are also unvalidated until their framing is inspected.
Correct the camera fixture and require visible rooms before further close profiling.
The overview screenshot does show the station, although its far right is clipped.
Next: fix fixture framing, then address remaining rounded-contact shadow cost with
native parity. Do not replace the current passing shadows with an unverified cache.

## Camera fixture corrected

The close fixture now supplies an occupied-cell destination directly to
`_set_grid_zoom`, avoiding its deferred restore overwriting immediate centering.
It checks at least three visible room centers before collecting timing, records
start/end counts, and fails if coverage is lost. Production camera code is unchanged.

Native run `output/game-pass/2026-09-21-visible-room-profile/` exits zero: overview
coverage is 50/50 and 100/100 room centers, close coverage 3/3 in both sizes.
The 100-close screenshot was visually inspected and shows Hab, corridor and Med Bay.
New 100-close render CPU/GPU means: 5.21/4.27 ms, 2,699 draw calls. These supersede
the empty-view close measurements; do not compare them as a performance regression.
100-fit remains 11,052 calls, 21.30/18.91 ms render CPU/GPU. Instrumented timing
limitations and missing active-drone coverage still apply.

Changed: tests/profile_large_station.gd and maintained/installed room-pipeline
references/layout-editor-and-water.md. Next: remaining rounded shadow cost, active
drone coverage, and continued Bill/room art work; release packages remain older.

## Paid-operation and active-drone coverage

The earlier fixture populated rooms but never paid their operating cycle. A state
probe showed the construction bay unpowered and its order still queued. Paying via
`_apply_room_economy()` lets the real fleet claim the order. The maintained fixture
now requires paid bay power, waits for observable launch (bounded at 300 simulation
steps), records phase samples and fails a scenario with zero active-drone frames.
No production power, cost, flight or animation rules changed.

Native run output/game-pass/2026-09-21-paid-active-drone/ exits zero. All four
scenarios record 90/90 active-drone frames. Across them: launching, outbound,
working and returning; docking was not sampled. Overview room-center counts remain
50 and 100, close counts three. The final close scenario grows from 100 to 101 rooms
when real construction completes; that count is recorded, not hidden.

100-overview: 11,457 calls, render CPU/GPU 22.27/20.18 ms. This is a newly powered,
active simulation baseline, not a same-state comparison with the prior unpowered
fixture. Native overview inspected; it does not establish close drone articulation
quality. Next animation review needs a camera near the active drone and temporal
captures, including docking and the mining/salvage variants.

## Full station comparison
Two native profile_large_station runs, with identical paid-operation fixture:
output/game-pass/2026-09-21-shadow-cache-reference/ and
output/game-pass/2026-09-21-shadow-cache-enabled/. Both exited zero, reached 50/100
rooms, kept overview centers visible and at least three close centers, and recorded
90 active-drone frames per scenario. Reference overview screenshot inspected.
100-fit render CPU: 22.122 vs 22.085 ms; calls identical at 11,467.889 average.
50-fit CPU: 13.815 vs 13.906 ms. No demonstrated overall rendering improvement.
Instrumented loop means vary in both directions (100-fit 75.84 vs 72.06 ms;
100-close 21.55 vs 28.89 ms); these do not isolate the cache or establish FPS.
station-comparison.json preserves the scoped numbers. Existing retained room
rendering limits how much repeated geometry work this optimization can remove;
grid_canvas draws these shadows in preview/floor passes, not every prop sprite draw.
Keep the claim limited to repeated geometry construction. Added
--reference-shadow-geometry to disable only geometry reuse while preserving batching
for future controlled comparisons. No further benchmark repetitions are justified
without a more specific live redraw-cost question.

## Current restored-layout baseline
Native profile_large_station run with --label=2026-09-21-restored-layouts completed
with zero fixture failures and no logged warnings/errors. Actual 50/100 room counts,
all overview centers and three close centers are visible; active-drone checks pass.
100-close grows to101rooms through construction. Screenshot100-close inspected.
Evidence: output/game-pass/2026-09-21-restored-layouts/ and
output/restored-layouts-profile-2026-09-21.log.

Render CPU/GPU means (ms): 50-fit12.91/11.62,50-close4.88/3.51,
100-fit20.04/17.89,100-close5.28/4.16. Simulation means1.57/1.81/2.19/3.04ms.
Draw calls6544/2270/10371/2714. These instrumented forced-draw measurements are
not FPS and do not isolate an optimization against the older furnishing state.
100-fit live-room stage6.64ms and door/light validation3.37ms remain notable.
Zoom-fit first frame190.30ms; load CPU365.12ms, first frame398.18ms. Profile the
load path before attributing that cost to scene reconstruction, assets or save data.

An uninstalled adjacency probe avoids copying cached port arrays for membership
queries:2304room/rotation/side cases match;100000calls take248886us original versus
213147us candidate. This isolated14% reduction does not establish useful frame-time
improvement; do not install or advertise it on that evidence alone.
Probe: output/door-adjacency-profile-2026-09-21/. Production unchanged.
Next performance investigation: break down the current load spike. Bill east
candidate remains uninstalled; owner treatment feedback and west repair remain open.

## Restore breakdown and verified artwork reuse
The reported load spike used synchronous RunSave.restore, not normal staged
Continue. Instrumentation traced300ms to companions rebuilding already loaded
textures. Companion restoration now reuses same-identity art in fresh actors with
independent mutable containers and playback. Same100-room probe CPU373.836->74.522ms,
firstframe410.391->109.474ms; companion segment300.018->0.582ms. No FPS claim.
Native staged restore and companion checkpoint tests pass; staged fixture observed
78.321ms total over5loadingframes,44.739ms longest interval. First decode remains.
See COMPANION_RESTORE_ART_HANDOFF_2026-09-21.md for scope, checks and changed files.


## Door/light helper attribution and edge reuse
A new native100-room helper profile identifies symmetric connectivity checks as
the largest measured helper:400calls and about1.15ms inclusive per validation call.
Local edge-result reuse is now installed in _door_light_state; seven complete-key
comparisons pass, including branch/rotation changes. Queries400->220; paired
instrumented means3.211->2.873ms, saving0.338ms (10.5%) for that call. Counting
wrapper overhead is present; this is not FPS or a scene-wide rendering measurement.
See DOOR_EDGE_REUSE_2026-09-21.md for exact source, reference and evidence scope.
