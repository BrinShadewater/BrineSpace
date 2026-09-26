# Gameplay and Studio preview contracts

Verified September 12, 2026. See `docs/GAMEPLAY_POWER_HANDOFF_2026-09-12.md` and
`docs/GAMEPLAY_STUDIO_MENU_2026-09-12.md` for revision-specific evidence.

## Scale review in Studio

Use **Scale: Bill -> Standing / Walking** in the Studio side panel. **Place** moves
the preview to clear floor. It uses the currently selected Bill catalog, the normal
65.28 world-unit standing height, source pivot and room depth sorting. No new body
art is produced. Preview state is not furnishing data: it must not dirty a draft,
enter undo/recovery, autosave an actor, or affect live crew. Clean preview keeps the
scale actor visible; Hidden removes it.

Walking checks registered collision boxes (including mirrored corner notches),
10-unit clearance and corridor hull shape. Room/rotation/geometry changes rebuild
the local route graph. Spawn in a usable connected area rather than preserving a
point stranded inside changed equipment. Use exact rectangle sweeps as well as
shape sampling, and keep a displayed movement step on one clear segment at a turn.
Choose facings actually supplied by the selected pack; do not assume eight-way idle
coverage from eight-way movement directions.

This is a scale and local-clearance aid, not proof of a live crew's complete job
journey, whole-station connectivity or owner acceptance of room composition. Review
standing and continuous walking with actual room orientations. Test no-draft-mutation
alongside visual size/occlusion and normal/compact controls.

## Paid operation versus forecast

Current machine service must use the funded operation state. After consuming the
last stored input, recalculating next-cycle affordability can incorrectly stop a
bay that already paid for this cycle, including prepaid charging. Keep next-cycle
forecasts explicitly labeled. Test the last reserve unit, next unpaid cycle,
pause, hardware-off, saved charge and newly built bay's first paid cycle.

Resource feedback distinguishes generation, requested/supplied consumption, stored
energy and charge/discharge. Between-cycle charging is separate from room rates.
For directional machinery, display the actual tested cell and blocker. Art orientation
and a moving effect are not evidence of production; validate simulation separately.

## Menu evidence

Test saved-loop panels with a disposable valid checkpoint and without a checkpoint.
Keep summary/schematic separate from central actions, verify compact and normal
bounds/overlap, inspect rendered captures, and confirm preview does not mutate the save.

## Startup, emergence and exterior hatches

Opening effects use saved simulation time: dark room, lights, consoles, then pod.
Preserve total recovery duration and distinguish emergency presentation from funded
machine operation. Reduced motion suppresses flicker. Cold mist and temporary human
tint preserve source frame metadata and must not modify shared animation textures.
Optional emergence fields require save validation; legacy saves do not replay them.
Check native direct and retained paths, pause, power off and Continue separately.

An exterior hatch is not a connected station doorway. Its closed north face must
still render on the raised hull. Derive aperture from the interlock phase, include
it in render cache keys, and close only after the diver clears the doorway.
Keep the chamber flooded while away; wait for reopening before return entry.
Test phase save validation, power/suspension holds and complete paid expeditions.

Retired decorative power cables are filtered at service-run and floor-detail
placement/drawing owners. Keep equipment pipes and salvage scrap. A general
decoration toggle must not resurrect explicitly removed cables or their bridge
plates. Native empty/cable/pipe comparisons distinguish removal from broken drawing.

Incoming transmissions can pause native fixtures. Probe actual state before changing
timing expectations. Isolate comms only when testing a separate subsystem. Flush
pending scene/layout callbacks before choosing an evidence camera; a passing test
can still capture the wrong room. Inspect the images. See
`docs/GAMEPLAY_STARTUP_HATCH_HANDOFF_2026-09-12.md` for scoped evidence.

## Live-state optimization checks - September 12 performance pass

Measure cache rebuild counts as well as frame time. Keep only values that affect
static pixels in shell keys: airlock water paints its floor, while aperture and
pressure affect live machinery. Removing the entire phase dictionary without
retaining water produces stale wet floors. Compare retained pixels against a
forced rebuild at the identical simulation state, and assert that rotation,
lighting and water still invalidate. A capture-only parity fixture is not an
automatic image comparison. Runner-detected script errors override exit code zero
and printed success. Keep native fixtures complete when renderer contracts grow.
See docs/PERFORMANCE_BUG_POLISH_PASS_2026-09-12.md for scoped measurements.

## Editor edits versus review snapshots — September 13

Keep authored defaults, local `user://room_layouts.json` overrides and generated review captures distinct. A difference from defaults does not establish when the owner made it. When tracking an editing session, preserve a read-only before snapshot of the override file as well as source hashes; compare exact keys afterward. Without that baseline, report saved differences without attributing them to the latest session. A file modification time is not per-room edit history.

Label catalog captures that isolate owner overrides, and refresh deliberately when reviewing the owner's live edits. Static HTML galleries do not update when Studio saves. Apply layout configuration before placing a review crew actor, and leave that actor out of production cards.

## Fire transitions, diagnostics and performance evidence - September 13

A hazard refresh must not replace every room's funded current-cycle operation
with next-cycle affordability. Ignition/extinction updates the affected compartment;
unrelated rooms retain paid service even when the reserve is now empty. Bootstrap
fixtures through the normal economy step, not a hazard presentation refresh. Test
both ignition and extinction beside a bay that spent its last reserve unit.

F7 is the lightweight performance overlay, F8 the local bug report, and F9 Studio.
Manual reports retain bounded current-process timing history and a separate live
station snapshot. Pause/focus flags and bucket-end context matter: wall intervals
include vsync, focus loss and menus; static engine memory is not total memory.
In-memory timings cannot survive a crash. Do not enable heavy draw profiling during
ordinary evidence collection or infer asset causality from an FPS screenshot alone.

Before terrain or room-render optimization, freeze the selected source and asset
bindings, phase, viewport and workload. Measure the affected work separately from
whole-frame timings. Compare identical-state pixels and exercise excavation,
lighting, water, rotation and camera movement. Retaining static terrain or reducing
room setup are candidates for measurement, not approved visual simplification.
Safe-room fire scans can be skipped without changing substep order, water allocation
or damage. Compare resulting state as well as time; a function microbenchmark is
not a whole-game FPS improvement. See docs/FIRE_PERFORMANCE_POLISH_PASS_2026-09-12.md
and docs/PERFORMANCE_DIAGNOSTICS_2026-09-12.md for scoped evidence.

Repeated setup is part of live-room acceptance. Isolation Vault once looked correct
in a single card render but deleted saved library props on later configure calls.
Perform legacy-prop cleanup on geometry rebuild, not every embedded configure.
Test repeated same-rotation setup and rotation return with saved bought props;
then inspect a real station capture. A cached empty prop list can otherwise look
already applied. See test_isolation_layout_reconfigure.gd (September 21).

Bought-layout activity checks must establish furniture contact, not just reachable
floor. Galley fixed meal coordinates passed clearance while missing the new
counters entirely. Resolve approaches from effective prop rectangles and verify
an actual arrival. Seated activities additionally need pose/pivot alignment: a
new sofa cannot inherit the retired desk chair's fixed visual offset unreviewed.

When promoting local furnishing to shipped defaults, merge the saved override
with its existing authored entry first. Promote only explicitly selected room/
rotation keys; never copy the whole player layout file or reset Studio marks.
Compare native views with local overrides against candidate defaults with empty
user data. Galley/Isolation/Cold Store matched all 12 views exactly before their
September 21 promotion. Keep visual acceptance and actual release testing separate.

Service arrivals must work when crew already stand beside the equipment. The
32-unit wandering minimum previously rejected a freezer approach 22.6 units away.
Apply that minimum only to non-station destinations; preserve station collision,
occupancy and route checks. Exercise near-counter starts as well as cross-room trips.

Paid finite-resource comparisons must include setup time, setup deliveries and
remaining site stock. A longer construction sequence can harvest much of a pile
before the observation counter resets. September 21 salvage tracing found both
stations collected all 12 units; the two-generator run finished sooner despite its
smaller post-setup total. Do not infer a throughput regression from that total alone.
Keep controlled-blueprint, manually stepped fixtures separate from human playtests.


When a funded build fixture cannot place a room, record all tested rotations and
current resources at failure. Reporting only the last rotation can hide that an
earlier rotation became affordable on the final simulation step. Wait for the
resource condition before construction, or recheck it after the last step; do not
grant resources or relax normal rules to conceal a setup-boundary error.

For construction-dialogue reproduction, the optional dialogue_trace.log is now
included in F8 bundles with the normal 2 MiB log-tail cap. Correlate its session
header with the report; an existing trace can predate the current launch. Keep the
original timing issue open until the offending line is captured. An isolated
report-test PASS line is invalid if the engine log also contains compile/script
errors. Copy real transitive source dependencies, use a fresh profile with
application/config/custom_user_dir_name, and confirm OS.get_user_data_dir before
treating profile isolation or previous-log assertions as established.

For checkpoint previews, keep an untouched evidence copy and load a disposable
copy: RunSave adopts the loaded file's _path and expedition conclusion can delete
it. Fail on an empty disk read instead of rendering a fallback new loop. Check the
restored camera at visible, settled viewport dimensions in addition to room and
crew equality. Continue intentionally focuses BRINE; do not restore arbitrary pan
as a speculative fix. Hidden staged layout previously displaced the focus by half
a viewport (docs/CONTINUE_CAMERA_FIX_2026-09-22.md).


## September 23: legal placement versus functioning generation

A normal paid checkpoint can contain a legal but nonfunctional turbine. The
cycle-22 continuation had a Current Turbine facing a resource deposit: generation
was three against five demand, causing repeated blackout/recharge cycles. Earlier
automated placement checked only `get_placement_problem`, which did not establish
that the intake was clear. This is fixture strategy evidence, not a balance bug.
For automatic build choices, check `_turbine_intake_problem` for the proposed
position/rotation and avoid covering any existing `_turbine_intake_cell`. Record
`power_generated`, `power_used`, reserve and `offline_reasons` before attributing
slow progress to crew motion. Use normal paid rerolls/building or mining decisions;
never delete the blocking deposit or grant resources merely to make a run pass.

Also inspect live drone battery, phase, `route_wait`, remaining site stock and
actual route reachability. A saved half-charged battery did not explain the whole
stall: the live drone reached full charge while both remaining mining deposits
had no route. Keep resource exhaustion and rock-barrier clearance separate from
power starvation. Schedule exposed basalt through the normal work control rather
than removing it directly in a normal-play comparison.

Load shedding can also pause construction: its `work_cell` must not be suspended.
In the same normal continuation, Veld held the paid turbine order because its
approach was in the suspended cryo ward. Once new generation supplied the margin,
resuming that room through the ordinary control completed the order. Inspect the
saved order and actor activity before diagnosing a stuck worker; preserve the
access gate. Final actual-release checkpoint: cycle35, eleven rooms, no orders.
