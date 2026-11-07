# Catalog mat containment follow-up

The native resolved-host audit now accepts `--check-mat-bounds`. It evaluates
every live `RoomDressing` helper discovered through the actual station dispatcher,
including helpers not named `dressing`, after each room's final rotation rebuild.
It reports the same host-relative rectangle drawn by the floor helper. The
optional gate does not change the default export host-identity audit.

`output/catalog-mat-bounds-v1.log`: 35 catalog identities, 33 room views,
32 profiles, 128 rotated mat placements. Fifteen exceed the conservative
`[-180,-180,360,360]` interior; child 1 is the expected failed audit, not an engine
error. These are eight room identities, not fifteen different rooms.

| Room | Flagged quarters | Host |
| --- | --- | --- |
| Hydroponics | 1, 2 | hydro_harvest |
| Data Archive | 1, 2 | archive_service_cart |
| Gravity Loom | 2, 3 | loom_calibration_bench |
| Reactor | 2, 3 | reactor_service_table |
| Life Support | 3 | life_service_cart |
| Crew Hab | 1, 3; chair 2 | hab_desk, hab_chair |
| Anomaly Lab | 1, 3 | anomaly_recording_cart |
| Maintenance Bay | 2 | maintenance_repair |

`tools/capture_mat_bounds_review.gd` renders only flagged room/rotation pairs,
with exterior margin at 2 pixels per world unit. `output/catalog-mat-review-v1`
contains fifteen 1100x1040 PNGs and a manifest with rectangle coordinates and
output hashes; child 0, no engine/script errors. These sealed-room offline
diagnostics do not represent station lighting or crew interaction. Only the
Hydroponics q1 image has been visually inspected in this pass.

## Next repair priority

Hydroponics q1 visibly extends a large harvest mat through the west hull. The
profile uses offset -76 and width 168 against an 88-unit bench. Its q1 rectangle
starts at x-248. This is an authored oversized/offset mat, not an undersized room.
Study a bench-related rectangle without moving the bench, changing walls or
clipping the whole floor pass. Then refresh its card and profile provenance.

Inspect the other flagged views before deciding repairs: several overrun the
interior by only 2–4 units, while others extend visibly farther. Do not silently
clamp all mats or treat their bounds as collision. Routes, arbitrary decals,
procedural floor art and light envelopes remain outside this particular audit.

The default host audit still exits 0 after the optional extension. Editor import
generates the capture tool's paired UID and passes without script errors. No
production art, profiles, room positions or card selection changed in this pass.
