# Room art polish — September 8

Integrated nine pairs of newly drawn side-wall installations (eighteen views):
Mycelium Nursery, Crew Lounge, Maintenance Bay, Crew Hab, Bio Lab, Clone Lab,
Mining Drone Bay, Ore Refinery and Cryo Chamber. These fill the sealed side wall
in rotations that previously fell back to the original smaller furniture.
Horizontal sources remain selected for north/south sealed walls.

Reviewed all fifteen full-wall room identities in four rotations. Pressure Control
keeps the original installation; recovered cryo configurations keep their original
one/two-pod compositions. Live mining vehicle and hatch remain separate. Existing
props relocate only into clear space; unresolved items remain available in source
art rather than being forced into an overlap. Per-rotation outcomes are recorded
in `output/full-wall-v1/previews/relocations.json`.

Repaired enclosed background gaps in ten existing horizontal registrations and
seven new side registrations. Sources, approved outer bounds and anchors are
preserved. The refinery's previous cutout correction is retained. White trim and
reflections were reviewed as materials, not blindly removed. The current cutout
ledger includes source hashes, regions and explicitly reviewed hole seeds.

Brightness was reviewed against native room floors and at gameplay zoom. Retained
department contrast: darker maintenance/refining, orange domestic textiles, cream
clinical surfaces and controlled colored glass. No further global desaturation or
brightness multiplier was applied. Native sheets are comparison evidence; source
brightness percentiles are diagnostics only.

Validation: fifteen rooms × four rotations × two operating states for installation
bounds/door clearance; native default card refresh; recovered cryo baseline equality;
all fifteen rooms × four rotations exercised with scheduled production crew routes,
zero assertion failures. Gameplay compositions captured at 52% zoom. Three Python
regression tests cover all thirty-three source hashes, registered aperture exclusion,
idempotence, hash-mismatch rejection and artwork-seed rejection. No packaged build
was produced; existing raw-image warnings remain separate from native acceptance.

Evidence lives in `output/room-polish-2026-09-08/` and
`output/full-wall-v1/previews/`. Updated maintained room skill and its installed
snapshot with full-wall lessons; source-sync check reports no differences. Generator
reruns now preserve reviewed registrations. The repair tool makes future enclosed
gap corrections without recomputing accepted silhouette bounds.
