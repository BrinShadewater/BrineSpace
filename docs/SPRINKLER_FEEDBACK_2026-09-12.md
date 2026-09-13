# Sprinkler feedback and suppression check

Owner requested visible spray, room-level operating feedback and a containment
playtest. Existing procedural rain is now two nozzle spray fans using pixel
rectangles and simulation time. Burning rooms show SPRAYING, OFF, READY,
NO POWER or NO WATER. The inspector uses the same status function; unpowered
rooms retain feedback instead of disappearing behind the old power early return.
Safe rooms do not acquire persistent status labels.

Changed scripts/station_hardware.gd and scripts/room_fire.gd; tests extend
room-fire status/timing coverage and native spray/pause/interruption captures.
No suppression rates, costs or gameplay mechanics changed.

Headless fire subsystem passed: output/test-runs/20260912-025426-headless.
Native fire subsystem passed: output/test-runs/20260912-025428-native.
Reviewed output/fire-suppression.png, fire-sprinkler-no-power.png and
fire-sprinkler-no-water.png. Native motion/pause capture includes sprinkler spray.

Controlled uninterrupted suppression measurements (0.1s simulation steps):
12% fire: 1.6s, 1 Water. 70%: 9s, 2 Water. 100%: 12.9s, 3 Water.
Each unit buys five seconds; unused charged time remains per existing rules.
These are isolated containment measurements, not a full expedition balance test.
Existing tests cover dry reserve, power failure, resupply and simultaneous fires.
Owner visual/pacing review remains; no executable rebuilt or commit performed.

## Two-compartment interruption follow-up

Added five native checks in tests/test_fire_gameplay.gd: one finite Water funds
one room while the other reports NO WATER; resupply starts the waiting room;
power interruption preserves paid spray seconds; restoring power resumes those
seconds; both fires extinguish after resupply. Native fixture passed and the
station-fit screenshot output/fire-sprinkler-shared-water.png was visually reviewed.
Water allocation follows existing room order; no priority/fairness tuning changed.
No gameplay implementation changes or executable rebuild in this follow-up.

Final follow-up run: output/test-runs/20260912-025624-native. Fire gameplay
and station hardware fixtures passed, including control persistence, master
power, pump/suspension interaction, door routing and two-size panel bounds.
