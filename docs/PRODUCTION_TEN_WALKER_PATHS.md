# Ten-room production walker path samples

`tests/test_production_ten_walker_paths.gd` passes all 6,400 ordered room,
rotation and side pairings. The actual `_connected_neighbor_cells()` selection
agrees with RoomDatabase-compatible sockets. For 2,916 compatible pairs, 294,516
samples from `get_test_walker_position()` plus the rendered foot offset remain
clear of registered footprints and shared hull collision. Perimeter anchors
are therefore exercised as implemented, rather than replaced with ideal lines.

The test constructs MainScript without starting a run or writing a save. It uses
no previous room, so it covers initial departures and arrivals, not every possible
turn through a room after entry from another side. It samples production path
code but does not advance the autonomous state machine or draw the sprite.

Evidence: `output/production-ten/walker-paths.log` and `.err`; exit zero and zero
failures. Raw-image export warnings remain. This is stronger movement geometry
evidence, not sprite occlusion, pixel-seam, autonomous movement or full acceptance.

## Ingress-turn follow-up

The fixture now includes no previous room plus every available ingress side for
each compatible departure. The first expanded run found 1,964 collisions in
Command Center's legacy perimeter path. Its database layout now uses the central
cross path, matching the registered console aisles and preserving all four doors.
The rerun passes 1,199,880 samples across the same 6,400 pairings, with zero errors.
Evidence: `walker-turns.log/.err` (failure) and `walker-turns-fixed.log/.err` (pass).
Synergy, discovery progression, polish gameplay and run balance regressions pass.
This supersedes the initial-departure-only limitation above. Previously serialized
room dictionaries retaining an old layout are not migrated by this art change.

`tests/playtest_production_ten_seams.gd` also produced forty native 1600 captures:
each requested room beside Battery Array, four rotations, actual walker path
midpoint and economy-derived operation. All connections are asserted. The
Quarantine east-door frame was inspected and the walker is within the doorway.
The remaining captures are evidence awaiting visual review, not accepted seams.
They predate the Command Center path correction. Evidence: `seams-native-1600/`
and `seams-1600.log/.err`. No ERROR/SCRIPT ERROR entries. Autonomous state-machine
movement and complete sprite/seam review remain outstanding.
