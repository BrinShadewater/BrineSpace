# Project handoff

Updated: October 1, 2026 · Brine Space · Bill selected locomotion comparison

## Objective and acceptance
Cross-reference selected idle/walk/run identity, scale, perspective and material before further motion polish. Full set is not accepted or complete.

## Accepted decisions and constraints
Use current normal-loader selections, fixed anatomical density and shared foot baseline. Allow real pose compression; do not fit every bounding box to equal height. Shared helmets keep native component scale.

## Current state
build_review.py reads the run-v2 selected-source inventory and verifies its Bill loader-block hash. Four directional boards show16 rows: both equipment profiles × walk/run. Rows include selected idle, eight uniformly indexed walk samples or all six run frames, at148/82 anatomy. source-review.json records literal selected manifests, phase indices and image hashes. index.html provides direction selection.

## Verification
All four boards visually inspected. Broad matte material consistency looks close in these samples. This is source evidence only: no moving transition, native execution, current NPC run route, all-walk-frame or owner acceptance claim. No selected assets changed.

## Next action
Review moving idle→walk→run and reverse boundaries, run lean/head-collar posture, near/far limb counter-swing and cross-direction bob. Correct source anatomy where needed; preserve native helmet and registration/body-protection checks. Keep diagonal candidate separate until its gait and sheet seam are resolved.
