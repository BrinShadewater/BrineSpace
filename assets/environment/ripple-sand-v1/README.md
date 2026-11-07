# Current-ripple sand

One preserved opaque ground source with short interrupted ripple marks. Exact
prompt and immutable hash are recorded; no image processing was applied.

Native four-panel review uses ordinary and mirrored repetition at four room cells
per source width, in source colors and habitat tint. Ripples remain restrained.
Faint bilateral seams appear in mirrored sampling; this is not a certified seamless
tileset. Select a bounded feathered patch trial rather than broad uninterrupted coverage.
Native station integration passes; packaged verification passes below; owner review remains pending.

Evidence: `output/ripple-sand-source-audit-v1.json`,
`output/ripple-sand-native-v1.log`, and the catalogue repetition preview.

## Native patch integration

A feathered patch centered at (6.5, 12), radius (2.5, 2) cells, uses the existing world-space ground mesh below scenery and station geometry. The 1600 station capture was inspected: short ripples remain subdued and the perimeter blends into silt. Three resolutions pass with unchanged occupancy/resources in `output/ripple-sand-station-v2.log`. Captures remain in `output/ripple-sand-station-v1/`. The first log failed because concurrent main.gd text contained invalid UTF-8; it was corrected externally before the rerun. No main.gd edit was applied by this work. Source registry audit v2 passes.

## Packaged verification

Isolated Windows debug export `output/environment-export-v21/` passes 92 exact source PNGs, 21 packs, 65 runtime textures, three station resolutions and eleven habitats. The ripple-sand habitat capture was visually inspected. The material remains a bounded feathered patch with known mirror symmetry, not a certified seamless tileset.

## Composed shelf

The current layout extends the radius to (4.0, 1.8) cells and frames an open center with rocks and sparse life. See `docs/ENVIRONMENT_COMPOSED_SITES.md`; export v23 verifies this revised placement. Earlier smaller-patch captures above are historical.
