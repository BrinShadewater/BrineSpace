# Sulfur and brine habitat art

Updated September 30, 2026. BrineSpace source checkout.

## Objective and acceptance
Continue original environment replacements with consistent overhead perspective,
matte materials and gameplay density. Three mineral/biological crust selections
installed and agent-reviewed at native scale and in station light/fog. Owner
visual acceptance remains separate.

## Accepted decisions and constraints
Retain .3-.65-cell widths, seeded distribution, sediment, tint, static rendering
and all gameplay rules. Preserve previous art. No Studio/save, collision, room,
resource, discovery, commit, push or release-export changes.

## Current state
assets/environment/mineral-habitat-refresh-v1 contains anhydrite v1, bacterial
mat v1 and salt plates v1: three immutable generated masters, exact built-in
imagegen prompts, three 512px exports, hashes/dimensions/centred pivots and bake.py.
Packaging crops significant-alpha bounds with two-pixel padding and resamples
isotropically without changing colours or thresholding retained alpha.
sub_biome_view.gd adds three whole runtime paths. Native fixture
tests/review_mineral_habitat_refresh.gd and paired UID plus
tools/verify_mineral_habitat_refresh.py provide focused scratch-profile review.

## Verification
Source audit: 3 identities / 6 raster versions, zero unregistered candidates.
Native PASS, zero failures or script errors: all 21 textures load; selected alpha,
512px width, whole-path bindings, deterministic distribution and static salt
pixels pass. Agent viewed 120px old/new/source/tint/pale/dark comparison,
.25/.45 production station captures and .65 salt close-up. Bacterial growth
stays subdued against sediment; pale vent/salt details remain readable.
Evidence: output/mineral-habitat-20260930-103837/summary.json. All 2,924 owner
files unchanged; scratch APPDATA/LOCALAPPDATA, only room layouts copied.
Deterministic rebuild/hash audit, LFS attributes and scoped whitespace check pass.
This art fixture does not establish paid expedition or release acceptance.

## Next action
Owner review of output/mineral-habitat-refresh-v1/native-comparison.png. Audit
remaining seep stones, nodule clusters and iron ledges, followed by remaining
habitat sediment materials, before choosing the next replacements.
