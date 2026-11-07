# Salvage Drone Bay registered pass

Recovery drone, winch, sorting bench and sealed hatch now use source-registered
polygons in station, placement preview, draft and inspector views. Card v1 is
512 square, baked from the embedded renderer. Source art is unchanged. The
shared hull owns canonical north/south sockets and seals unused doors; equipment
centers rotate while art remains south-facing. Full recovery claws are retained.

Operating cues are local control-panel diagnostics on three hosts. The closed
hatch, crane, recovery claws and unloaded winch stay still. Layered salvage bays
no longer emit the legacy flight that crossed hull walls. Resource production,
costs and mission progression are unchanged; physical deployment is not implemented.

## Evidence

`tests/playtest_salvage_drone_bay.gd` passes at 1280x720, 1600x900 and 2560x1440:
per-host active/inactive/pause pixels, four rotations, full visual containment,
non-overlapping footprints, straight topology, disconnected wall seals, 728
center-to-port samples and sampled effect envelopes outside both central aisles.
The native card and rotated 2560 station/draft/inspector frame were inspected.
Captures and logs live in `output/production-ten/salvage-native-*` and matching logs.

Synergy, discovery progression, polish gameplay and run balance pass. Salvage
stderr contains no ERROR or SCRIPT ERROR entries. Source and card have LFS
attributes; both new scripts have paired UIDs. Inherited export warnings persist.
A follow-up 1600 run verifies the shared fixture now labels its final result
`ROOM SCENE PASS [salvage_drone_bay]` instead of the misleading nursery name.

## Remaining acceptance

Neighbor and production-actor crossings, incompatible pixel seams, economy-driven
power transitions, mixed-station zoom, checkout-independent packaging and owner
visual review remain. Small source-floor patches within machinery loops still
need close review. A real hatch-and-mission route is required for deployment.
This is initial integration, not full acceptance. Crew Lounge, Command Center
and Quarantine Cell remain source-only in this ten-room batch.
