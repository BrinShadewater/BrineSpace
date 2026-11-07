# Mining Drone Bay registered pass

The bay now uses registered underwater ROV, servicing cradle, closed deployment
hatch and tether reel assemblies in the station, placement preview, draft and
inspector. Source polygons, pivots, uniform scale and wall samples are recorded
in `rooms/production-ten/mining_drone_bay_view.gd`. The shared hull owns the
north/south sockets and seals unused ports. Assembly centers rotate; art remains
south-facing. The source PNG is unchanged and card v2 uses the final renderer.

Three hosts show operating diagnostic cues. The hatch stays closed, and docked
thrusters and drills stay still. The legacy line-and-drone flight across station
walls is suppressed for layered mining bays. Resource production, costs and
mission progression are unchanged; no physical deployment sequence is claimed.

## Evidence

`tests/playtest_mining_drone_bay.gd` passes at 1280x720, 1600x900 and 2560x1440.
It checks per-host active/inactive/pause pixels, all four rotations, full visual
containment, non-overlap, straight topology, sealed disconnected walls, 728
center-to-port samples, and sampled effect envelopes outside both center aisles.
The first layout failed the latter check; narrower assemblies at symmetric
quadrant centers pass. Final card v2 was additionally tested in the 2560 consumer.

The native 512 card and rotated 2560 station/draft/inspector frame were inspected.
Passing evidence lives under `output/production-ten/mining-v2-native-*` and
`mining-final-native-2560`. Matching final/v2/regression stderr has no ERROR or
SCRIPT ERROR entries. Four suites pass: synergy, discovery progression, polish
gameplay and run balance. Source/card have LFS attributes; scripts have paired UIDs.

## Remaining acceptance

Neighbor and production-actor crossings, incompatible pixel seams, economy-driven
power transitions, mature mixed-station zoom, checkout-independent packaging and
owner visual review remain. Inherited raw-image export warnings persist. Source
floor patches inside machinery loops require close review. Deployment needs a
real hatch/mission route before animation. This is initial integration, not full
acceptance. Four of the ten requested rooms still await registration.
