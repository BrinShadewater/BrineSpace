# Mooring debris study

Packaged follow-up: v9 verifies this source in the isolated Windows debug build,
within 78 environment PNGs and 54 runtime textures. The exported mooring capture
was visually reviewed on pale ground. Evidence: `output/environment-export-v9/`.
This supersedes earlier packaging-pending notes; owner approval remains separate.

Current status: integrated at cell (10.5,16.1) on the pale shoal, at half-cell
width. Its source registry is ledger-audited. Native fixture captures at three
window resolutions pass with unchanged occupancy/resources. The reviewed 1600
capture keeps plate and chain readable beside a room. Evidence:
`output/mooring-debris-station-v1/` and `output/mooring-debris-station-v1.log`.
Earlier pending-integration notes below are historical. Packaged verification
and owner approval remain pending; no clearance or salvage mechanics were added.

A corroded steel anchor plate and broken chain add a low exterior attachment
silhouette. The chain connects through the central eye; four bolt holes and the
broken terminal link describe an abandoned mounting rather than an active system.
Original pixels, exact prompt and source hash are preserved. Transparency passes
the immutable audit in `output/mooring-debris-source-audit-v1.json`.

Native review remains pending at half-room width, including chain opening clarity,
dark-steel contrast over silt and ash, and room overlap. No live integration,
salvage yield, obstruction or packaged verification is claimed.

Native comparison: `tests/playtest_mooring_debris.gd` renders the prop at 0.40,
0.50 and 0.65 cell widths over shell sediment and volcanic ash with runtime tint.
The reviewed `output/mooring-debris-v1/terrain-scale.png` shows clear plate/chain
separation on pale sediment. On ash, the plate becomes faint at the smaller sizes;
do not scatter it indiscriminately across dark ground. A half-cell placement on
pale sediment is the first integration candidate. Small link openings merge at
distance, while the broken chain silhouette remains readable. Evidence is in
`output/mooring-debris-native-v1.log`; room overlap remains pending.
