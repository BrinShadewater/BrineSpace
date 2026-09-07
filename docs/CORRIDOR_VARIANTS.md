# Corridor routing variants
Three flush deck variants (standard, grated service, marked transit) now use the
existing saved art_variant assignment for straight, corner and new T corridors.
The T blueprint costs 3 Metal, starts unlocked, and uses the west/east/south tee
layout. Its hull and crew clearance polygon share the same rotation contract.
All nine card captures use production surfaces and geometry; original sources and
cards are preserved. New PNG paths use the existing Git LFS filter.

output/corridor-routing-v2.log verifies all three shapes at four rotations,
10-unit crew clearance sampled along each T branch, all three reciprocal door
connections and rejection of the fourth side. The native T capture was visually
inspected after excluding narrow corridors from the full-cell raised wall layer.
output/corridor-variants-cards-v1.log verifies nine 512px card captures.
No standalone export or end-to-end walking animation tour is claimed.
Review: rooms/underwater/corridor-review.html.


## Hallway dressing
Hull-ledged barrels/crates and bundled cables now follow rotated mount positions; upright supplies remain screen-facing and render after risers. Horizontal north-facing hull edges gain 35-unit risers when the north cell is unoccupied and raised walls are enabled. Wide spans use ocean windows or ventilation; short spans use vents, with conduit on wider bays. New dressing-v1 cards preserve routing-v1 evidence. Native all-shape rotation/clearance/connection regression passes in output/playtest_corridor_routing-dressing-v2.log; nine cards pass in output/bake_corridor_variants-dressing-v2.log. T card visually inspected for upright props and riser attachment.


Dressing v2 separates the variants further: strapped supply cases for standard, an extinguisher and cable reel for service, and an intercom for transit. Broad risers gain directional signs. All props retain upright silhouettes and hull-ledged mounts. Nine cards rebuilt; rotation/clearance/connection fixture passes in output/playtest_corridor_routing-dressing-v3.log. Service T card visually inspected.


## Style alignment pass
Compared against the furnished Hab reference and room art-direction guidance. Added barrel side shading and lid bungs, crate top planes, recessed wall panels and deeper window frames. Halved the repeating service-grate placements to quiet the floor. Preserved clean construction and restrained colors. Nine cards and native rotation/clearance/connection checks pass (output/playtest_corridor_routing-style-v1.log). Service T card visually inspected. Procedural small props remain simpler than the painted room furniture; this pass improves consistency rather than establishing identical finish.


## Rotated riser returns
Raised vertical side returns now follow rotated corridor hulls with a restrained six-unit outward width and 18-unit rise. Rear faces retain full height. Neighbor suppression is per touching cell boundary; a northern room no longer hides inset rear walls elsewhere within a corridor cell. Native output/corridor-risers-v1.log passes three shapes at four rotations and existing clearance/connection assertions. Rotated T native capture visually inspected. Existing card captures predate this side-return pass.


Tapered risers now draw directly from diagonal hull segments with a shaded face and highlighted cap, rotating with all three corridor shapes. Native output/corridor-tapers-v1.log passes the rotation/clearance/connection fixture; rotated T capture visually inspected. Review native captures show this pass; older card thumbnails remain earlier evidence.


Taper coverage audit: production taper_face geometry is now checked for all five corner chamfers and six T chamfers at every quarter-turn (44 faces total). Each must retain its hull endpoints, rise above the edge and triangulate into two triangles. output/corridor-taper-coverage-v1.log records the result alongside native rotation captures. Review now includes all four corner captures.


Review correction: the top nine thumbnails still referenced pre-taper style-v1 captures despite updated native images below. Rebuilt all nine as card-tapers-v1, visually inspected Corner and T, and updated both runtime card registries plus the review page. All 17 review image references resolve. Log: output/corridor-taper-cards-v1.log. Future geometry changes must refresh every visible review consumer before claiming the review is current.


Wall join correction: side returns previously ended 17 units below the taller rear/taper faces. Side tops now rise 35 units with a connecting cap. Rebuilt all nine cards and native four-rotation captures under joins-v1; clearance, connections and 44 taper faces still pass. Corner card visually inspected. Both runtime card registries and all review images now reference this revision.
