# Ore Refinery registered pass

The existing Ore Refinery now uses registered crusher, processing vessels, sorter
and collection hopper assemblies in station, placement preview, draft and inspector
views. Source art remains immutable at 1254 square. The native 512-square v1 card
uses the same embedded renderer, and draft cards fit the entire image.

`rooms/production-ten/ore_refinery_view.gd` records source polygons, pivots,
uniform scales, footprints and wall samples. The shared hull owns north/south
sockets and sealed unused walls. Assembly centers rotate while art stays south-facing.
Conveyors remain entirely within their machinery groups; none connects across a
walking aisle. Source exteriors and painted checkerboards are never rendered.

Three operating hosts have local belt/flow cues; collection storage stays still.
These are overlay cues over static machinery/ore art, not animated ore transfer,
crusher deformation or a new processing simulation. Existing costs, production,
storage, discoveries and saves are unchanged.

## Evidence

`tests/playtest_ore_refinery.gd` passes at 1280x720, 1600x900 and 2560x1440.
Each run checks four rotations, per-host active/inactive/pause pixels, complete
visual containment, non-overlapping footprints, straight topology, disconnected
wall seals and 728 center-to-port samples. Sampled effect envelopes across four
seconds remain outside both reserved center aisles in every rotation.

The v1 card and 2560 rotated station/draft/inspector frame were inspected. Logs
and captures are in `output/production-ten/refinery-native-*` and `refinery-*.log`.
Synergy, discovery progression, polish gameplay and run balance suites pass.
No ERROR/SCRIPT ERROR entries appear in refinery stderr logs. Inherited raw-image
export warnings remain; the new PNG card has LFS attributes and scripts have UIDs.

## Remaining acceptance

Neighbor/production-actor crossings, incompatible/disconnected pixel seams,
economy-driven power states, mature mixed-station zoom, checkout-independent
packaging and owner visual review remain. Source-floor patches inside service
loops and belt-cue appearance against static ore need close review. This is
initial integration, not full acceptance. Five requested rooms await registration.
