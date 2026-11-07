# Project handoff

Updated: September 29, 2026 · Project: BrineSpace · Task: original environment art

## Objective and acceptance
Owner continued after the basalt/timber/kelp pilot and first habitat comparison.
Habitat pack now replaces lace coral, vase sponges, cup corals, sea fans and coral
sediment with original matching artwork.

## Accepted decisions and constraints
Strict overhead silhouettes, detailed matte painted materials, apparent density
at gameplay scale. Preserve source-color/tint separation, existing placement and
gameplay. Originals, owner marks and save data remain. No Higgsfield or release work.

## Current state
assets/environment/habitat-refresh-v1 contains 5 immutable generated masters,
5 runtime derivatives, prompts, reproducible bake, ledger and validators.
sub_biome_view.gd SELECTED_PATHS has five full paths beside retained ribbon kelp.
tests/preview_habitat_refresh.gd and paired UID produce native comparison/station
images. First seabed pilot remains installed. No commit, push or export.

## Verification
Raster: 5 identities/10 PNGs, hashes/alpha/rebake pass; LFS attributes confirmed.
Six earlier master/runtime hashes unchanged. Runtime environment: 66 checks/0 failures.
Current native fixture: 21 textures, deterministic placement and 5 selected bindings
pass; source/tint/mirror and station
lights/fog captures reviewed. First native failure was fixture mesh lifetime/mirror
geometry; v2 retains mesh and uses reflected transform. Both failed and passing
evidence retained in output/habitat-refresh-20260929-224004 and -224202.
Earlier two scratch-profile intervals leave all 2753 real-profile files unchanged.
Latest companion checks in output/habitat-refresh-20260929-230800 pass independently;
wrapper exit1 records full-profile log-only deltas (2761 files). All non-log profile
files match; scratch APPDATA/LOCALAPPDATA throughout. No repeat to chase log stability.

## Next action
Owner review of output/habitat-refresh-v1/native-comparison-v3.png (new companions)
and native-station-v3.png (all four species). Continue remaining
habitat species and scenery alternatives, then blocker formations and wreck art
without changing authoritative occupancy/clearance. Packaged/release review pending.
