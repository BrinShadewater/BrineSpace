# Dedicated harvest-site art

Updated September 30, 2026. BrineSpace source checkout.

## Objective and acceptance
Continue original environment replacements with extraction artwork matching
current matte station steel and overhead seabed perspective. Three new paintings
installed and agent-reviewed at native density, depletion states and station scale.
Owner visual acceptance remains separate.

## Accepted decisions and constraints
Mineral and salvage sites retain existing footprints, four-piece layout, survey
corners, load labels and depletion behavior. No site capacity/reward/discovery,
drone work/power, save, pathing or collision changes. Old sources retained.
No commit, push or release export.

## Current state
assets/environment/harvest-refresh-v1 contains three selected sprites: mining v1,
frame v2 and cable v1. Four preserved generated masters, exact built-in prompts,
immutable manifest and 512px runtime exports. Frame v1 rejected for oblique
side faces; imagegen v2 corrects its projection. bake.py verifies master hashes,
trims alpha margins and resamples isotropically without painting/colour grading.
scripts/harvest_site_art.gd swaps three whole runtime paths only.
tests/review_harvest_refresh.gd and paired UID plus tools/verify_harvest_refresh.py
add focused scratch-profile native review. No owner Studio files changed.

## Verification
Source audit: 3 identities / 7 raster versions, zero unregistered candidates.
512px source loading/alpha and whole-path bindings pass. Existing finite-harvest
test PASS: stock conservation, survey, depletion, pause, saves, obstacle detours.
Native art fixture PASS: two station zooms and two close-ups; both kinds at
24/18/12/6/0 loads and individual 95px source-colour samples. Agent viewed native
depletion/production station captures and source sprites. Supplied art fixture
does not establish paid expedition or release-export acceptance.
Evidence: output/harvest-refresh-20260930-095041/summary.json; all 2,924 owner
files unchanged. Scratch APPDATA/LOCALAPPDATA; copied layouts only. Git LFS
attributes, deterministic master-hash rebuild/audit and scoped whitespace check
pass. No gameplay files beyond the artwork loader were changed.

## Next action
Owner review of output/harvest-refresh-v1/native-depletion.png. Audit current
habitat/material bindings for the next batch before assuming legacy paths mean
bought art or a missing replacement. Export verification remains separate.
