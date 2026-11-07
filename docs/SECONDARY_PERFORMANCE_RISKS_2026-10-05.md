# Secondary performance risks

Updated: October 5, 2026 · BrineSpace release readiness

## Objective and acceptance

Investigate causes beyond art submission count. Separate demonstrated behavior
from unmeasured contributions to the reported frame-time and memory failures.
Preserve report usefulness, checkpoint safety, effects and owner layouts.

## Findings

### Floor mesh retention: controlled growth reproduced

`rooms/whole-room/modular_floor.gd` caps its lookup at 96 entries but moves evicted
mesh batches into a static `retired` array. This keeps meshes alive for retained
canvas commands, intentionally. No release path was found in the inspected module
or runtime callers; deleting entries indiscriminately would risk missing geometry.

Isolated native probe requests 240 distinct floor-variation seeds, without retaining
returned batches in the caller or creating drawing canvases:

| Variants requested | Lookup entries | Retired entries |
|---|---:|---:|
| 0 | 0 | 0 |
| 120 | 96 | 24 |
| 240 | 96 | 144 |
| After another process frame | 96 | 144 |

This demonstrates that total mesh retention is not bounded by the lookup limit.
It does **not** quantify real gameplay memory growth, GPU bytes, or establish that
this explains the multi-GiB texture budget failure. Repeated identical keys reuse
entries; changing layouts/material variation is the relevant trigger.

Evidence: `output/retention-research-2026-10-05/`. Zero engine errors, all 2,936 owner
non-log files unchanged. No production changes. Remedy candidate: canvas-owned
mesh references or scene-generation ownership, retiring only while a live command
list needs the mesh and releasing after its replacement/destruction. Validate title/
Continue transitions and Studio edits before clearing anything.
[Godot static resource lifetime guidance](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#static-unload-annotation).

### Automatic diagnostics can add a secondary pause

`performance_monitor.gd::_watch_for_stalls` synchronously reads the viewport image
then calls `bug_report.gd::save_report`. That routine gathers snapshots/files,
encodes PNG data and writes a ZIP synchronously. The path is limited to three
automatic captures per session and at least 90 seconds apart. Breadcrumb writes
also occur every five seconds in normal sessions.

Therefore diagnostics can add work after an original stall, but cannot explain the
initial trigger. Script-based benchmark fixtures disable automatic capture, so
their failures cannot be blamed on this path. No report duration measured here.
Next: time GPU readback, snapshot gathering, PNG encoding and archive writes as
separate stages in an isolated normal-play process. If significant, capture a
consistent immutable snapshot on the main thread and send only independent CPU/
file work to a bounded single writer. Keep pending jobs bounded, handle scene exit,
preserve F8 feedback and report errors; do not access live scene state on a worker.
[Godot threading and GPU synchronization guidance](https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html).

### Light-map viewport renders continuously

`rooms/whole-room/room_lighting.gd` creates a SubViewport with `UPDATE_ALWAYS`.
Its content signature already avoids rebuilding ambient/light commands when
unchanged. That does not stop the viewport rendering the retained commands.
Disabling effects hides the overlay and returns early but does not explicitly
disable that viewport. This is an unnecessary-work candidate, not a measured
dominant bottleneck.

Candidate: request `UPDATE_ONCE` when content, camera offset, viewport size or
visibility changes, and disable when effects are off. **Do not use the current
content signature alone:** scrolling moves child canvases without changing that
signature. Preserve crew lamps, blackout beacon phases, fades and pause behavior;
verify the first frame after re-enabling, resizing or changing scenes.
[SubViewport update modes](https://docs.godotengine.org/en/stable/classes/class_subviewport.html#enum-subviewport-updatemode).

### UI burst scheduling and synchronous saves: unmeasured hypotheses

Main's operations refresh already runs at 0.5-second intervals and skips some
hidden panels. Several alerts, integrity status, stuck checks and inspector work
share that interval. This can concentrate CPU work in a single frame, but existing
per-system timings must establish an actual spike before staggering it. Keep input
feedback immediate and gameplay checks at their required cadence.

`RunSave.write` captures, validates, serializes, hashes, flushes, backs up and replaces
the checkpoint synchronously. The examined main callers are explicit save/menu/
quit paths; this review does not establish periodic autosave as a stutter cause.
Preserve validation, backup recovery and successful completion before quitting.
Instrument stage durations before changing the I/O design. Do not drop flush or
backup steps to make a benchmark look faster.

## Next action

Keep shadow batching and zero-alpha terrain omission as the first rendering
implementations. Add mesh lifecycle ownership to the endurance work. Measure normal
report creation separately, and prototype dirty-triggered light-map updates with
motion/resize tests. Do not blame the unresolved Windows message-pump stalls on
these game paths: those stalls were also reproduced outside the game.

No runtime files, owner data, package inputs or public releases changed in this pass.

## Further research: routing, terrain invalidation and log bursts

### Blocked travelling drone retries: reproduced

October 5 implementation follow-up: R4 is now enabled, with a bounded per-fleet
failure cache and immediate blocker-content invalidation. Production-caller
comparison and limits are in [the implementation handoff](DRONE_ROUTE_CACHE_2026-10-05.md).
The original research below records the pre-fix behavior.

`drone_routes.gd::travel` treats an empty route as needing a new search each call.
`drone_fleet.gd::advance` calls this in outbound/returning phases; its existing
one-second idle retry applies to docked assignment, not blocked travelling drones.
The route search tries exterior routing, then repeats with room traversal allowed.
The fleet currently builds boolean blockers and explicitly allows travel beneath
rooms, so this fallback cannot change traversability for those boolean-only maps.
Other callers may supply room dictionaries; preserve their port-aware fallback.

Controlled native experiment uses the original route implementation with only
search/expansion counters added: start (2,2), goal (20,20), all four goal neighbors
blocked. Sixty travel calls with unchanged blockers produce **120 searches and
191,400 expanded cells**, taking **173.682 ms total** in this run (about 2.9 ms per
call). The drone remains waiting with an empty route. This is an instrumented
algorithm probe, not a 60-frame gameplay benchmark; it does not establish how often
the real station reaches this configuration or what its gameplay p95 cost is.

Evidence: `output/routing-research-2026-10-05/` includes source-copy generator,
isolated guarded fixture and results. Zero engine errors and all 2,936 owner
non-log files unchanged. No runtime source changed.

Recommended remedy: key failed-route results by origin, destination and blocker
topology revision; retry immediately when any relevant blockage changes. A revision
must represent topology, not a newly allocated dictionary each frame. Preserve
backing out of newly blocked segments, target changes, cancellation and restore.
For boolean-only blocker maps, avoid the equivalent second search. Do not impose
a blind cooldown that delays recovery after a passage opens, or truncate searches
in a way that turns reachable work into unreachable work.

Godot's navigation guidance independently warns against repeated path queries and
notes the increased search cost of unreachable goals. BrineSpace uses its own BFS,
so NavigationServer settings are not a direct fix here.
[Navigation performance guidance](https://docs.godotengine.org/en/4.4/tutorials/navigation/navigation_optimizing_performance.html).

### Excavation defeats whole-terrain retention: source-confirmed

`grid_canvas.gd::_environment_terrain_key` includes every wreck's exact `progress`
and the selected room cell. A change marks the entire STATIC_TERRAIN pass dirty.
That pass repaints rock/wreck drawing plus glow plants. Therefore retention still
permits whole-layer rebuilding during active excavation or selection changes.
This explains a mechanism for bursts, not their measured share of gameplay cost.

Keep base rock geometry/material separate from progress cracks/bars and selection
outlines, or invalidate only affected terrain chunks. Preserve cross-cell rock
connectivity and buried-site revelation when a blocker clears. Compare an idle
station with active excavation and selection changes; include renderer-stage time
and frame tails. Do not lower the visual progress update rate just to reduce work.

### Error-log polling is not bounded by its group limit

`error_watch.gd::poll` runs every three seconds and reads **all** new log bytes,
decodes them, splits them into lines, then groups errors. MAX_GROUPS=40 bounds
retained distinct messages, not read/parse work; `carry` also grows with an unfinished
line. An error storm or verbose logging could therefore add CPU/allocation bursts.
No such storm was established in the current successful native probes.

Candidate: bounded bytes/lines per poll with backlog reporting, bounded partial
line storage, and continued draining without dropping error counts silently. Test
UTF-8 split boundaries, backtraces, log rotation and repeated messages. Fix the
underlying repeated error first if one exists. Normal quiet logs need no rewrite.

## Revised priority

After integrating the already pixel-tested shadow and mineral-draw candidates,
blocked-route result reuse and narrow terrain invalidation are now concrete CPU
targets. Mesh lifetime remains an endurance concern. Report/log work and UI bursts
remain conditional hypotheses until observed durations justify changes. Avoid a
generic navigation rewrite, thread migration or frame-rate cap as a substitute for
these targeted fixes. Animation clocks examined in main use delta scaled by the
selected simulation speed; this review found no new demonstrated timing defect.
