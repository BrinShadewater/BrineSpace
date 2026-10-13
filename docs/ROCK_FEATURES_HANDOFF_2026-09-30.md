# Seabed rock variety and features

Updated September 30, 2026. BrineSpace source checkout.

## Objective and acceptance
Create varied rock graphics/features matching current overhead art, matte
materials and physical density. Three variants installed and agent-reviewed
in native comparisons and production station lighting. Owner acceptance separate.

## Accepted decisions and constraints
Decorative rock variety at existing scenery placements. Preserve .20-.38-cell
widths, tint, positions, small companion stones, original selection and timber
families. No site RNG, save format, navigation, collision, resource or mining
changes. Preserve originals/rejected candidates. No commit, push or export.

## Current state
assets/environment/rock-features-v1 contains selected split slab v1, layered
ridge v2 and porous basalt v1. Four immutable masters, exact built-in imagegen
prompts/camera correction, three 512px exports, hashed dimensions/pivots and bake.
Ridge v1 rejected for oblique/tall side faces. Packaging crops significant-alpha
bounds plus two pixels, isotropically resamples and preserves colour/retained alpha.
rock_feature_view.gd caches explicit whole paths. scripts/site_scenery.gd adds
coordinate/family selection among original and three new rock graphics; existing
companion rendering and fallback remain. Renderer and tests/review_rock_features.gd
have paired UIDs; tools/verify_rock_features.py provides isolated native review.

## Verification
Source audit: 3 identities / 7 rasters, zero unregistered candidates. Native PASS,
zero failures or script errors: textures/512px/alpha, actual deterministic helper,
unchanged placement dictionaries, all four art outcomes, timber exclusion and
unchanged fixture occupancy. Agent viewed 95px source/tint/pale/dark comparisons,
.45 production station and .65 close-up (also .25 capture available).
Evidence output/rock-features-20260930-131417/summary.json: owner folder unchanged,
scratch APPDATA/LOCALAPPDATA and layouts copied only. Deterministic rebuild/hash
audit, LFS attributes and scoped whitespace checks pass. Controlled fixture
does not establish every seeded expedition or playable release acceptance.

## Next action
Owner review of output/rock-features-v1/native-rocks.png and station-45.png.
Further distinctive geology can use eroded arches, exposed seams or larger
outcrop silhouettes after inspecting current selections and native scale.
