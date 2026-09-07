# Crew Hab integration

Maintained habitation: cream structure, muted orange textiles, brown furniture,
two compact empty berths, personal desk and a chair with attached side table.
No occupants baked into art. Canonical ID, costs, production and unlocks unchanged.

The immutable 1254-square source, exact prompt and hash are recorded in
rooms/whole-room/crew-hab-generation.json. Requested output was 1280 square.
crew_hab_view.gd registers four complete furniture silhouettes. Their ground
centres rotate; artwork remains south-facing and containment includes full height.
The inherited four-port template is overridden with Crew Hab's actual tee mask.
Shared geometry owns all wall infill, 72-wide door openings and thresholds.

Both card consumers use crew-hab-card-v2.png, baked from the embedded renderer.
Draft cards use full-image aspect fit. Separate fixtures provide warm light;
desk traces animate only during operation. Empty beds and chairs stay still.
Existing power/operation separation and pause semantics are preserved.

Native evidence:

- crew-hab-effects-v1: four assemblies in four rotations; expected motion or
  stillness, inactive state, pause and effect/prop containment passed.
- crew-hab-station-v1: 404 neighbor-route samples, rotated shared wall visibility,
  station/card loading, eight operation comparisons and mixed 40-room fit passed.
- Native rotated neighbor screenshot and card v2 inspected. Owner approval pending.
- No SCRIPT ERROR/ERROR entries in either log. Existing raw PNG export warnings
  remain; this does not establish packaged-export readiness for the new assets.
- Source and active card remain covered by Git LFS attributes. Originals retained.

The wider room ledger remains unfinished; this is one integrated identity.
