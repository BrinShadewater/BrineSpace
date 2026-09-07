# Crew Lounge registered pass

The existing lounge now uses source-v2 registered sofa/rug, communal table,
galley and game seating in station, placement preview, draft and inspector.
The native 512 card uses the same embedded renderer. Separate polygon pieces
exclude source floor between chairs; the intentional rug stays with the sofa.
The shared hull owns east/south/west sockets and seals unused openings.
Furniture centers rotate while art remains south-facing.

The galley display has a local operating cue. Seating, food, plants and tables
remain still. This does not simulate drinks or occupancy. Costs, crew effects,
room category, unlocks and saves remain unchanged.

## Evidence

`tests/playtest_crew_lounge.gd` passes at 1280x720, 1600x900 and 2560x1440:
four rotations, full visual containment, non-overlapping footprints, per-host
active/inactive/pause pixels, tee topology, disconnected seals and 1092
center-to-port samples. A further 1600 run checks sampled effects against actual
rendered pieces and both reserved aisles, not only the enclosing assembly bounds.
The native card and rotated 2560 station/draft/inspector frame were inspected.
Evidence is under `output/production-ten/lounge-native-*` and `lounge-pieces-native-1600`.

Synergy, discovery progression, polish gameplay and run balance pass. Lounge
stderr has no ERROR/SCRIPT ERROR entries. Card has LFS attributes; new scripts
have paired UIDs. Existing raw-image export warnings remain.

## Remaining acceptance

Neighbor and production-actor crossings, incompatible pixel seams, economy-driven
power transitions, mature mixed-station zoom, checkout-independent packaging and
owner visual review remain. Assembly floor collision reserves a full group;
the gaps between seats are visual cutouts, not new seating navigation. No
occupancy interaction is claimed. This is initial integration, not full acceptance.
Command Center and Quarantine Cell remain source-only in this ten-room batch.
