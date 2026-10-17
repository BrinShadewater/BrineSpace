# Alternate biome floors

Three original opaque whole-field materials add brine current ripples, pale
coral shell flour and iron-stained clay. Selected v2 keeps quiet micrograin and
distinct natural material colors; the runtime provides underwater tint.

Built-in imagegen produced three v1 masters and targeted v2 edits using the
existing fine brine material as grain-scale reference. Exact briefs are preserved
in prompts.json and v2-prompts.json. Native v1 review rejected coarse pebbles and
shell chips despite passing load/geometry checks. All six immutable masters and
three rejected v1 runtime exports remain hashed alongside three selected exports:
12 raster versions. No local repainting, color grading or invented fine detail.
bake.py verifies immutable hashes, centre-crops a square when needed and resamples
isotropically to 1024px. All six supplied masters are square. PNGs use Git LFS.

biome_floor_view.gd caches three whole-path textures. For brine/coral/iron, a
stable saved-center calculation chooses the original or alternate material;
other biomes retain their floors. sub_biome_view.gd draws the selected material
through the existing continuous UVs and feathered mesh. Coverage, centers/radii,
props, fungal under-prop hook, tint, RNG and gameplay remain unchanged. No new
save fields or types of biome are introduced.

Native v2 evidence: output/biome-floor-variants-v1/v2-native. Three full radius-four
station views at .45 zoom show material and corresponding props under production
fog/light. Comparison sheet includes reduced field overview and 190px native crops
at the existing 270 physical px/cell calibration; full UV span is 9.2 cells.
The fixture checks 21 original textures plus three alternates, opaque 1024-square
fields, actual selection/fallback, unchanged saved geometry/seeded props, other
biomes, continuous UVs, zero-to-one boundary feathering, static pixels and occupancy.
Scratch APPDATA/LOCALAPPDATA and real-profile fingerprints are handled by
tools/verify_biome_floor_variants.py. Agent review is complete; owner acceptance,
all seeded expedition views and playable export verification remain separate.
