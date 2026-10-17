# Project handoff

Updated:2026-09-30. Project:BrineSpace. Task:Veld cargo half-turn family.

## Smooth-shell revision -2026-09-30
Owner reported a bun compartment in helmet/north-south. Built-in generated
helmet-shell-source-v2 and exact prompt saved. repair_helmet.py registers edited
source and grafts only region(100,68)-(157,105) onto six accepted head poses.
helmet-head-repairs/ preserves all pixels outside that region, including body,
case and boots. Half-turn builder reuses repaired heads wherever the same
north/east source poses occur, preserving identical seams. Installed quarter-turn
sources and live selection unchanged. Before/after comparison saved.
408 packaging and435 native checks pass; scratch APPDATA, real profile unchanged.
Smooth-shell-v2 remains staged for owner review. Historical derived-v1 details
below describe original construction; source pixel provenance now includes six
locally repaired head assets, not only accepted quarter-turn images.

## Objective and acceptance
Owner accepted south/west planted-v1; installed with123 actual-selection checks.
Four180-degree turns staged, not installed: east-west,west-east,north-south,
south-north, each bare/equipped. Owner visual review pending.

## Accepted decisions and constraints
Reuse accepted quarter-turn poses, no generation, mirroring or new grade.
Standing planted endpoints replace earlier walking endpoint substitutions in
these derived clips only. Original12slots,680ms nonloop timing, facings/dry cargo
metadata, canvas256,pivot128/224,standing height148 preserved. Equipment ownership
and route direction preserved from original metadata. Existing quarter-turns
and directional carrying gait remain unchanged.

## Current state
build.py selects accepted frame sources and saves exact source provenance hashes.
Routes: east-west via south; west-east via north; north-south via east;
south-north via west. Shared canonical standing poses overwrite quarter endpoints
only in this candidate; seam slots5/6 identical. Canonical endpoints from accepted
north/east and north/west and south/west standing turns.96frames,two manifests,
eight GIFs, contact/native/browser preview and original-states/provenance saved.
GIF playback triples original timing; encoder may merge duplicate seam frames.

## Verification
402 packaging checks pass: original metadata, exact accepted source pixels,
identical seams, clipping and decoded GIF exterior.435 native checks pass,
including all four directions/both variants, candidate pixels and runtime turn
selection/return to carry frame zero. Contact/browser inspected visually.
Probes used scratch APPDATA. Half-turn interval real-profile last_session.json
delta unattributed. Installed south/west interval progress save/backup,startup
image list/session deltas unattributed; details in its native-installed checks.
No owner-profile restoration attempted. Native handoff is functional evidence;
authored stationary turn and live stepping gait differ visually. Identical seam
slots do not certify surrounding cross-master material/pose continuity.

## Next action
Owner half-turn review, then install on acceptance. Cargo turn matrix will then
have selected replacements for all opposite/adjacent directions. Existing accepted
east/south quarter-turn still retains its earlier walking endpoints. No commit,
push or export.


## September30 master helmet replacement
Bare half-turns installed with veld-unified-turn-helmet-v1 equipment family.
This old smooth-shell-v2 helmet is retained as comparison, not selected runtime
helmet. New family owner visual acceptance remains open.
