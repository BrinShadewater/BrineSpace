# Small ocean-floor details

Updated September 30, 2026. BrineSpace source checkout.

## Objective and acceptance
Add original smaller underwater floor details consistent with current overhead
art, density and matte natural materials. Shell fragments, empty urchin tests
and abandoned worm tubes installed and agent-reviewed at native sizes and in
production underwater light/fog. Owner visual acceptance remains separate.

## Accepted decisions and constraints
Geology and habitat sediments were already replaced concurrently; preserve
those selections. This batch adds three sparse decorative clusters only, not
more geology replacements. Existing habitat placements/RNG, collision, occupancy,
resources, saves and discovery remain unchanged. No commit, push or export.

## Current state
assets/environment/floor-details-v1 contains four immutable generated masters,
exact built-in imagegen prompts, three 512px exports and hashed manifest with
dimensions/pivots. Tube v1 rejected for upright barnacle shapes; v2 selected for
low curved tubes. Visible tube count differs from the brief; no exact-count
gameplay requirement. bake.py preserves colour/alpha while cropping significant
alpha bounds with two-pixel padding and isotropically resampling.
floor_details_view.gd caches three whole-path textures and anchors one cluster
to the first existing brine/nodule/sulfur prop, widths .24/.20/.22 cells and
offset .32/.23 cells. sub_biome_view.gd invokes it after existing habitat props.
tests/review_floor_details.gd and renderer both retain paired UIDs;
tools/verify_floor_details.py provides isolated native review.

## Verification
Source audit: 3 identities / 7 rasters, no unregistered candidates. Deterministic
rebuild/hash audit, PNG LFS attributes and scoped whitespace checks pass.
Native PASS, zero failures or script errors: textures/512px/alpha, deterministic
three-cluster placement, empty/duplicate input handling, unchanged base props
and fixture room occupancy. Agent viewed 120px/60px source/tint/pale/dark board,
.25/.45 station captures and .65 close-up. First fixture left urchins in a dark
lighting gap; adding a middle battery room exposes all three under production
lighting. Final evidence output/floor-details-20260930-130102/summary.json:
all 2,924 owner files unchanged. Scratch APPDATA/LOCALAPPDATA, layouts copied only.
Controlled art placements do not establish visibility at every seeded site or
playable release acceptance.

## Next action
Owner review of output/floor-details-v1/native-details.png and station-45.png.
Further ocean-floor variety can use burrows, small detritus or low sponge remains;
inspect current selections first to avoid duplicating concurrent asset work.
