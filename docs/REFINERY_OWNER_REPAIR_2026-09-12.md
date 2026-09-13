# Ore Refinery owner repair

Updated September 12, 2026. This pass addresses the owner playtest request to
reduce orange and repair white cutouts without changing refinery gameplay,
machinery footprints, process inventory, or room layouts.

## Changed state

All three selected directional wall sources now use restrained burnt-orange
paint. Edge-connected neutral source backgrounds are transparent, removing the
filtered white seams that appeared beneath and between wall pieces. Enclosed
pale gauges and metal trim remain. Yellow logistics rails and hazard markings
remain brighter than the paint, and copper billets and ore retain their material
identity.

The separate production atlas is now
`rooms/production-ten/ore_refinery-source-v2.png`, applying the same palette to
the crusher, vessels, sorter and hopper. This prevents a color jump between the
wall bank and independent machinery. Geometry, pivots, collision rectangles,
prop IDs, and q3's separate crusher/hopper composition are unchanged in intent.

Source hashes, changed-pixel counts, transparency counts and the deterministic
rules are recorded in `assets/refinery-directional-v2/owner-repair.json` and
`assets/refinery-directional-v2/atlas-palette-repair.json`. The repaired q0 card
is `assets/refinery-directional-v2/cards/ore_refinery.png`; all three current
card consumers select it.
## Visual review and validation

Real-display OpenGL captures in
`output/refinery-owner-repair-2026-09-12/native` cover q0 west, q1 north, q2
east and q3 south. All four were inspected. The south white bands are absent;
wall and independent machinery palettes agree; yellow markings, copper billets,
ore, inward controls, and the open center routes remain readable.

- `test_preferred_room_layouts`: 176 furnished orientations pass.
- `test_side_wall_variants`: 20 variants pass.
- `test_room_catalog_cards`: 47 identities and all card bindings pass.
- `test_production_ten_connections` and `test_production_ten_walker_paths` pass.

Test evidence is in `output/test-runs/20260912-181245-headless` and
`output/test-runs/20260912-181319-headless`. No executable or export was built.

## Workflow lesson

White seams around opaque generated sources can be filtered samples from
edge-connected background even when the vector registration is correct. Remove
only that connected background; do not erase enclosed pale trim. Palette masks
must follow material roles rather than hue alone so painted orange, logistics
yellow, copper product and ore remain distinct. Newly introduced texture paths
need an explicit editor import before native review. In concurrent sessions that
import queue may include another task's assets, so its delay is not evidence of a
room-render failure.
