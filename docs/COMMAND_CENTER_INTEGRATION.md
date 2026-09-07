# Command Center registered pass

Four registered operations, station systems, central table and communications
consoles now render in station, placement preview, draft and inspector. The
native 512 card uses the same embedded renderer with displays inactive. Source
v2 is unchanged. The shared hull owns all four sockets and seals unused doors;
generated east/south/west gaps are excluded. Equipment centers rotate while art
remains south-facing.

Two displays carry local sonar sweeps and two carry status traces. These are
operating-state visual cues, not real mission telemetry or clickable consoles.
They freeze on pause and disappear when inactive. Costs, production, category,
progression and saves remain unchanged.

## Evidence

`tests/playtest_command_center.gd` passes at 1280x720, 1600x900 and 2560x1440:
four rotations, full visual containment, non-overlap, per-host active/inactive/
pause pixels, cross topology, disconnected seals and 1456 center-to-port samples.
Sampled effects stay inside the physical display rectangles and outside both
reserved aisles. The native card and rotated 2560 station/draft/inspector frame
were inspected. Evidence lives in `output/production-ten/command-native-*`.

Synergy, discovery progression, polish gameplay and run balance pass. Command
stderr has no ERROR/SCRIPT ERROR entries. Card has LFS attributes and new scripts
have paired UIDs. Inherited raw-image export warnings remain.

## Remaining acceptance

Neighbor and production-actor crossings, incompatible pixel seams, economy-driven
power transitions, mature mixed-station zoom, checkout-independent packaging and
owner visual review remain. Small source-floor patches inside cable loops need
close review. This is initial integration, not full acceptance. Quarantine Cell
is the final source-only room in this ten-room batch.
