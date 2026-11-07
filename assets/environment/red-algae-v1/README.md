# Red algae study

Export follow-up: `output/environment-export-v8/` verifies this source within
77 library PNGs and 53 runtime textures. The isolated executable's dedicated
red-algae meadow capture was visually reviewed. Earlier packaging-pending notes
are superseded; owner art approval remains separate.

Current status: integrated in three unequal placements near (11.5,24.5), at
0.25–0.33 cell widths, beside existing meadow plants. Its explicit renderer source
mapping is ledger-audited. Earlier study notes below preserve the review history.

`tests/playtest_red_algae_station.gd` verifies the loaded texture, captures three
window resolutions and checks unchanged occupancy/resources. The 1600 capture in
`output/red-algae-station-v1/` was reviewed: muted red fronds remain distinct from
seagrass and kelp while the nearby room stays dominant. The run log is
`output/red-algae-station-v1.log`. Packaged verification and owner approval remain
pending. This is static decorative growth, with no harvest or simulation behavior.

A short branching red-algae tuft expands the low plant library. Flattened forked
fronds and muted burgundy tones distinguish it from ribbon kelp and fine seagrass.
The original source, exact prompt and immutable hash are preserved. Actual alpha
passes the source audit in `output/red-algae-source-audit-v1.json`.

Source review finds the low overhead footprint and branching silhouette suitable
for a native scale trial. Pale tips and red saturation still need assessment under
runtime tint at 0.25–0.33 room width, beside existing plants. No live integration,
plant growth, harvest yield or packaged verification is claimed.

Native scale follow-up: `tests/playtest_red_algae.gd` compares red algae, seagrass
and ribbon kelp at 0.25, 0.33 and 0.50 cell widths with source and runtime tint.
The reviewed `output/red-algae-v1/plant-scale.png` shows distinct forked fronds;
the quarter-cell tuft is subtle, and one-third cell is a useful placement trial.
Pale tips do not dominate under tint. This flat-background comparison still needs
actual terrain/room overlap before live acceptance. Successful evidence is in
`output/red-algae-native-v2.log`; v1 records a corrected fixture parse error.
