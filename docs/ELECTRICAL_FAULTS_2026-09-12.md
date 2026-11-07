# Electrical faults and crew repair

## Accepted direction

Owner approved warning sparks before fire, shutting down to halt escalation,
and crew repair of isolated machinery. Implemented for the existing four heat
sources: reactor, biomass digester, galley and salvage workshop.

## Behavior

At 75% heat an electrical fault latches and the inspector/alert identify it.
Powered, unsuspended faulty machinery emits intermittent sparks without flames.
Existing heat accumulation continues toward ignition at 100%; suspension cools
20 percentage points per cycle. Cooling does not erase the wiring fault.

Reachable available architects automatically service suspended faulty rooms.
The room must be below 25% water and not burning. Existing route/standing checks
choose a reachable worksite; no teleportation. Repair takes eight simulation
seconds, without materials in this first tuning pass. Other committed work and
fire/flood safety retain priority. Turning the room back on interrupts repair.
Progress is retained through interruption and Save/Continue. Completion clears
fault and heat, leaves the room suspended and logs that manual restart is needed.
Existing extinguishing also clears fault/heat; scorched hull damage remains.

## Changed files

scripts/room_fire.gd: latched fault, inspector, alert and save field validation.
scripts/electrical_repair.gd and UID: reachable crew work and safe interruption.
scripts/bill_npc.gd: work dispatch and valid persisted crew goal.
scripts/fire_effects.gd: warning sparks before ignition and isolation visibility.
tests/test_room_fire.gd and tests/test_fire_gameplay.gd: rule, physical route,
partial checkpoint, pause and completion coverage.

## Validation and remaining work

Headless fire subsystem passed (20260912-023701-headless).
Native gameplay passed including six electrical checks (20260912-023707-native).
Electrical warning screenshot reviewed. Native final capture and regression
results are recorded in the task. Owner playtest of warning lead time and repair
pacing remains; no packaged executable rebuilt or commit performed.

Final native capture run: 20260912-023818-native, passed. Save and hull-repair
regressions passed in 20260912-023742-headless.

## Focused pacing playtest

Native run 20260912-024522-native passed. Controlled reactor scenario measured
6.2 simulation seconds of crew travel and eight seconds of work: about 14.2s
of shutdown. Since production resolves every 20s, this can miss zero or one
production tick depending on when the room is suspended. This is a single
accessible layout with available crew, not a worst-case station measurement.

Current heat rates imply reactor/digester warning at approximately cycle 30
(10 minutes) and ignition at cycle 40, leaving 200s at 1x. Galley/workshop warn
at cycle 38 and ignite at cycle 50, leaving 240s. These are calculated from
continuous functioning cycles, not elapsed-time measurements of normal play.
This is a forgiving warning window; no tuning changed based on one fixture.

Separately, output/fault-normal-probe.gd exercised a fresh opening via the actual
card/grid-click handler, with free build false and failures enabled. Solar Array
cost four Metal; Hydroponics cost five Metal and one Biomass. After six accelerated
normal economy cycles, the run remained active (Power 12, Oxygen 12, Food 18,
Metal 9, Water 0, Integrity 100). Final log: output/fault-normal-probe.log, no
script errors. This opening has no fault-prone machinery, so it does not prove
an end-to-end naturally occurring electrical fault in a normal expedition.
An earlier exploratory probe bypassed the grid-click cost handler; its results
were rejected and replaced by the charged-placement run described above.

Conclusion: intervention is mechanically reliable in the controlled case and
fits well inside warning lead time. Whether shutdown becomes an interesting
production tradeoff still needs a longer expedition with working machinery,
competing crew jobs and resource pressure. No executable rebuild or balance edits.
