# Storage Bay registered pass

Storage Bay now uses separate secured crates, supply shelving, handling platform
and strapped rack in station, placement preview, draft and inspector views.
Its maintained grey/yellow Logistics finish remains independent of its legacy
Engineering gameplay category. No category, capacity, cost or unlock changes.

`rooms/production-ten/storage_bay_view.gd` owns source polygons, ground pivots,
uniform world scales and registered wall samples. The immutable 1254-square
source remains on disk. Shared geometry provides all four potential sockets,
flush unused walls, floor grid and boundaries. Equipment centers rotate while
art and collision orientations remain south-facing.

Cargo and the idle handling platform are static. This preserves the passive
capacity room without inventing an automatic cargo or power-consumption system.
Fixtures still use the existing independent room-lighting path. Both PNG maps,
variant selection and draft aspect-fit use the native-baked 512-square v1 card.
Original variants remain intact.

## Evidence

`tests/playtest_storage_bay.gd` passes at 1280x720, 1600x900 and 2560x1440.
Each run covers four rotations, per-host operating/inactive/pause stillness,
complete visual containment, non-overlapping footprints, cross topology,
disconnected seals and 1456 center-to-port samples. Native v1 card and rotated
2560 station/draft/inspector frame were inspected. Evidence lives under
`output/production-ten/storage-native-*` and `storage-*.log`.

Synergy, discovery progression, polish gameplay and run balance suites pass.
No ERROR/SCRIPT ERROR lines appeared in Storage test stderr logs. Inherited
raw-image export warnings persist. Source and card have LFS attributes, and new
scripts retain paired UIDs.

## Remaining acceptance

Native neighboring-room crossings with production actors, incompatible/disconnected
pixel seams, economy-driven lighting, mature mixed-station zoom, checkout-independent
packaging and owner visual approval remain. Outer silhouette registration can retain
source floor within rack gaps; close extraction/occlusion review is still required.
This is initial integration. Six other requested rooms remain at source stage.
