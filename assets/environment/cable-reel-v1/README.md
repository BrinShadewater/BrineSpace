# Collapsed cable reel

One original transparent wreckage source: corroded teal flange, missing wedge,
exposed dark coil and attached curved cable with a frayed end. Exact prompt and
immutable source hash are preserved. No source processing was applied.

The source reads as a damaged reel lying flat, with a shallow lower flange.
The tail emerges through a collar beside the exposed winding; part of the
connection is occluded. Native terrain review checks 0.40, 0.50 and 0.65-cell
canvases. Select 0.50 on pale sediment: flange and coil stay distinct while the
thin cable fades more on ash. Decorative wreckage only; no salvage state.
Native station integration passes; packaged verification passes below; owner review remains pending.

Evidence: `output/cable-reel-source-audit-v1.json`,
`output/cable-reel-native-v1.log`, and the native terrain preview.

## Native integration

One half-cell placement at (10.8, 14.8) uses the existing service-wreckage tint and draws beneath station geometry. The native 1600 capture was reviewed: flange, coil and cable remain readable beside a room. `output/cable-reel-station-v1.log` passes three verified resolutions with unchanged occupancy/resources; source registry audit v2 passes. This does not add a salvage job or room blocker.

## Packaged verification

Isolated Windows debug export `output/environment-export-v22/` passes 93 exact source PNGs, 22 packs, 66 runtime textures, three station resolutions and eleven habitats. The dedicated `debris-cable-reel.png` capture was visually inspected; flange and trailing cable remain readable. This verifies decorative integration and packaging. Owner approval remains pending.
