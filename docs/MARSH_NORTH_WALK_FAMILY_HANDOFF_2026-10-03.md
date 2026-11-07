# Project handoff

Updated: October 3, 2026. Project: Brine Space. Task: Marsh animation consistency.

## Objective and acceptance

Continue the full master-matched animation set and cross-family polish. North
walking now has a complete staged material family; runtime and normal admission
remain open. Full goal active.

## Accepted decisions and constraints

Original six gait poses govern geometry; own North idle governs identity/grade;
unpainted master torso crop governs panel construction. Whole-pose edits only.
Raw alpha retained through fixed whole1254-to184 resampling. No fit, splice,
recolour, alpha cleanup or translation. All six final crowns, soles and occupied
heights exactly match original bounds. Initial phase4 -2 and phase5 +1 sole
errors repaired through two whole-pose edits; original attempts retained.

## Current state

- Bank: `character/marsh-north-walk-family-detail-v1`, six final frames and staged
  manifest, eight raw generations, request/result receipts, references and reviews.
- Helpers: `tools/prepare_marsh_north_walk_family_v1.py` and
  `tools/review_marsh_north_walk_family_v1.py`.
- Four reviewed boards: family joins, heads2x, closing join at source/station
  density and all30 phase-specific stop poses. Acceptance receipt binds hashes.
- Pipeline, bible, current status and canonical/installed repair skill updated.
- Current normal inventory remains post-West:228states/1190slots/91body manifests.
  No North normal selection change.

## Verification

All eight raw full figures and four complete source boards inspected. Final
crowns24,25,23,24,25,23; soles172,170,170,171,170,170. Height ratios all1.0;
opaque silhouette IoU .910878-.956616, phase5lowest. Camera and subdued rear
material grade coherent in held review; loop perception still needs checking.
Catalogue and all91 body manifest hashes exact. Two Python syntax checks;
all27 bank PNGs use LFS. No Godot run or save-folder access this pass.

North stopping is six keys `walk-stop-p0-north` through `walk-stop-p5-north`,
five frames each. Generic `walk-stop-north` lookup failed in the initial review
helper; actual state keys now reviewed. Do not port West's generic stop fixture
by text replacement. Source bounds alone do not prove native/2D contact or cadence.

## Next action

Build actual North staged player/actor/main/grid route verification, exercising
phase-specific stops, start, pause and restores with scratch APPDATA and owner
fingerprints. Make original comparison capture visibility an explicit check;
West's prior missing-actor crop limitation must not be silently repeated.
Then inspect native captures and cyclic motion before normal admission. Continue
South walking and broader natural/water/equipment/furniture/fullSave consistency.
