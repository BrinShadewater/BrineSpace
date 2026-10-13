# Project handoff

Updated: September 29, 2026 · Project: BrineSpace · Task: original environment art

## Objective and acceptance
Owner requested continuing replacement of ocean plants/life, textures, mountains
and wrecks with original art matching the current style, theme and apparent density.
First coherent pilot: low basalt, grounded wreck timber and overhead ribbon kelp.

## Accepted decisions and constraints
Detailed matte painted surfaces, overhead projection, readable gameplay silhouettes.
Decorative replacement preserves placement/tint, collision, resources and saves.
Original sources, IDs and owner Studio marks remain. Owner acceptance is still pending.

## Current state
New assets/environment/seabed-refresh-v1 includes masters, exact prompts, reproducible
bake, 3 runtime PNGs, source ledger and native evidence. scripts/site_scenery.gd maps
uw1-188/mat-130 to the new art; sub_biome_view.gd selects the new ribbon-kelp whole
path. Both remaining bought scenery alternatives are retained. Two new native fixtures
and paired UIDs; no release export, commit or push.

## Verification
Source audit 3 identities/11 raster versions, no unregistered candidates; LFS attribute
confirmed. Runtime environment 66 checks/0 failures. Native station capture reviewed
under production lights/fog; native source/tint density sheet passes all 3 texture and
consumer binding checks. First launch blocked by concurrent Studio syntax; externally
corrected. Station shutdown emits resource teardown warnings after PASS/exit0.
Scratch profiles used throughout. Station interval real-profile changes include logs
and Studio revision metadata; first density fingerprint unchanged (2745 files).
Density v2 fixes viewport scaling and passes renderer checks; its profile fingerprint
has concurrent deltas, so no whole-session unchanged-profile claim is made.

## Next action
Owner review of pilot, then remaining alternatives, cold coral/sponges, subdued
terrain materials and blocker/wreck art. Whole environment and release packaging
are not complete. Preserve authoritative blockage/clearance and exact source hashes.
