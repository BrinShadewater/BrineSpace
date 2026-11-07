# Additional biome floor materials

Updated September 30, 2026. BrineSpace source checkout.

## Objective and acceptance
Add distinct biome-area floor textures matching overhead art and native density.
Brine ripple silt, coral shell flour and iron-stained clay installed and
agent-reviewed across full native habitat fields. Owner acceptance separate.

## Accepted decisions and constraints
Retain all seven habitat identities, saved centers/radii, meshes/UVs/feathering,
tint, props, fungal under-prop hook, RNG and gameplay. Original materials remain
in the mix; saved-center parity chooses old/new for the three supported habitats.
No save-format, collision, resources, discovery, commit, push or export changes.

## Current state
assets/environment/biome-floor-variants-v1: six immutable generated masters,
exact built-in generation/edit briefs, three rejected archived v1 exports and
three selected v2 1024-square opaque fields. SHA256 ledger registers all 12
rasters with dimensions/pivots. V1 rejected after full native review for coarse
grain/chips; v2 uses the installed quiet brine material as micrograin reference.
bake.py centre-crops only non-square sources and resamples isotropically, without
painting/grading; supplied masters are square. biome_floor_view.gd caches whole
paths, and sub_biome_view.gd selects material before its existing mesh draw.
tests/review_biome_floor_variants.gd and renderer have paired UIDs;
tools/verify_biome_floor_variants.py runs isolated native review.

## Verification
Source audit: 3 identities / 12 raster versions, no unregistered candidates.
Native v2 PASS, zero failures/script errors: 21 base textures and 3 alternates,
opaque 1024-square fields, actual old/new selection, unchanged region dictionaries
and deterministic props, other-biome retention, continuous UVs, feathered bounds,
static pixels, room occupancy and no missing artwork. Agent viewed all three
full-radius fields and native crops at 270 physical px/cell (9.2-cell UV span).
V1 green tests did not establish visual acceptance; its evidence remains at
output/biome-floor-variants-v1. Selected captures are under v2-native.
Final evidence output/biome-floor-variants-20260930-133621/summary.json: owner
profile unchanged. Scratch APPDATA/LOCALAPPDATA, only layouts copied. Deterministic
rebuild/hash audit, LFS attributes and scoped whitespace checks pass.
Controlled fixtures do not establish every seeded site or release acceptance.

## Next action
Owner review of output/biome-floor-variants-v1/v2-native/native-comparison.png
and the three ground captures. Further variants for sulfur/sponge/kelp/nodules
can extend the same material-selection workflow after checking current selections.
