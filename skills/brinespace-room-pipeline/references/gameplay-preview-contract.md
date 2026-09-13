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
