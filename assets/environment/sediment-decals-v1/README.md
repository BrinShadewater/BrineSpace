# Sediment decal study

Current status: v2 is integrated beneath the mooring plate at 30% opacity. The
reviewed preview offset is converted to cell units and follows the mooring center.
The decal draws before the mooring and all station geometry. It remains subtle
on pale shoal; no moving particles, excavation state or collision are introduced.

Native evidence: `output/sediment-decals-station-v1.log` and corresponding capture
directory. Three window sizes pass with unchanged occupancy/resources; the 1600
layered view was inspected. The source registry passes the immutable ledger audit.
Packaged evidence: `output/environment-export-v10/isolated-run.log` and
`output/environment-export-v10/captures/debris-mooring.png`. All 80 preserved
environment PNGs and 55 runtime textures pass in the isolated Windows build;
the layered mooring/scour capture was visually inspected. Earlier pending-status
notes below are historical. Owner approval remains pending.

Current candidate: `silt-scour-v2.png` replaces the ring with an elongated shallow
drag smear and a single stronger ridge. Its source shape is suitable for native
composition review, with actual partial transparency verified in
`output/sediment-decal-source-audit-v2.json`. Both originals remain preserved.
The following v1 notes explain the rejected direction. Neither source is integrated.

Native opacity study: `tests/playtest_sediment_decals.gd` places the revised source
beneath half-cell mooring debris at 15%, 30% and 50% opacity on shell sediment and
ash. The reviewed `output/sediment-decals-v1/opacity-comparison.png` favors 30%
for a subtle pale-ground trial; 50% produces a conspicuous streak on ash. Current
registration trails beneath the chain rather than the plate and needs correction
before integration. The native log is `output/sediment-decals-native-v1.log`.
Loading and alpha pass; placement acceptance remains open.

Registration follow-up: `output/sediment-decals-v1/plate-registration.png` moves
the 140-pixel scour canvas to (-90,10) relative to the 90-pixel prop's top-left.
The scour tip near normalized (0.87,0.15) now meets the plate center near
(0.35,0.35), rather than the chain. Native visual review favors 30% on pale shoal.
Evidence is `output/sediment-decals-native-v2.log`. Station integration remains
pending; convert these offsets using the same cell scale rather than fixed pixels.

The first scour source is preserved with its exact prompt and immutable hash.
It has real exterior and partial transparency, but its broad paired arcs read as
a ring. It is rejected for the intended short displaced-silt scrape and is not
integrated. The ledger's selected_source identifies this study candidate only;
it does not indicate runtime acceptance.

Next revision: a narrow asymmetric broken drag smear with one small sediment
ridge and irregular trailing grains. Avoid crescent, horseshoe and ring language
that encourages a circular composition. Review beneath actual debris before
accepting it as a static decal. `kind: effect` enforces partial alpha in the source
audit; it does not imply animation, excavation activity or hazard mechanics.
