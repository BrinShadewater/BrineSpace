# Seabed life art handoff

Updated September 30, 2026. BrineSpace source checkout.

## Objective and acceptance
Continue original environmental art replacements while preserving overhead
perspective, matte treatment and physical density. Three replacements installed
and agent-reviewed in native comparisons and production station light/fog.
Owner visual acceptance remains separate.

## Accepted decisions and constraints
Keep habitat distribution, .3-.65-cell sizes, sediment, tint and existing hydroid
motion. No occupancy, collision, discovery, resource, save or other gameplay
changes. Preserve originals and rejected candidates. No commit, push or export.

## Current state
assets/environment/seabed-life-refresh-v1: holdfast v1, brittle stars v1 and
hydroids v1 selected; hydroids v2 retained/rejected for skeletal branching.
Four generated masters, exact prompts, SHA256 manifest, three 512px exports and
deterministic bake.py. Significant-alpha crop + two-pixel padding and isotropic
resampling preserve colour and alpha. sub_biome_view.gd adds three whole paths.
tests/review_seabed_life_refresh.gd and paired UID plus
tools/verify_seabed_life_refresh.py provide focused native scratch-profile review.

## Verification
Native PASS, zero fixture failures or script errors: all 21 textures load; selected
sources retain alpha/512px width; explicit bindings and seeded placement pass;
actual hydroid pixels move and freeze under Reduced Motion. Agent viewed 120px
old/new/pale/dark comparisons, .25/.45 station captures and .65 close-up.
Initial fixture Array assignment error corrected using clear() on the typed array.
Final evidence: output/seabed-life-20260930-101736/summary.json. All 2,924 owner
files unchanged; scratch APPDATA/LOCALAPPDATA, layouts copied only. Source audit
registers 3 identities / 7 rasters with no unregistered candidates. Deterministic
rebuild, LFS attributes and scoped whitespace check pass. This art fixture does
not establish paid expedition or release packaging acceptance.

## Next action
Owner review of output/seabed-life-refresh-v1/native-comparison.png. Next audit
remaining sulfur/brine/mineral habitat materials against current selections
before choosing another batch. Release validation remains separate.
