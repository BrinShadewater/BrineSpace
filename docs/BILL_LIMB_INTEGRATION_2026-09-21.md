# Bill limb integration handoff

Updated: September21,2026. Project: BrineSpace.

## Objective and acceptance
Improve Bill's side-walk leg surfaces and retain leg identity through crossings. Integrated for playtesting after agent pose-transition and native phase review. Full owner motion acceptance and in-expedition visual review remain open. The broader game-polish goal is unfinished.

## Accepted decisions and constraints
Original boots, upper body, movement timing and stride are preserved. East/west sources are independent; no Higgsfield. Owner rooms untouched. Source-level knee detail follows its own limb rather than being independently redrawn in each pose.

## Current state
Canonical rebuild_bill_art.py and standalone repair_bill_walk.py now apply retained limb sources via build_bill_limb_candidate.py. Historical candidate CLI name remains; review export stays beneath output/. Sources, exact prompts and registrations are retained under character/major-bill-v3/sources/limb-study-2026-09-21.
Full rebuild initially failed before frame writes because construction provenance was archived September13. Added a narrowly scoped source_path resolver for character/crew-construction-v1 in rebuild and validator. All25archived contract inputs match original hashes; frozen contract unchanged. No files restored or moved out of archive.

## Verification
Full rebuild completed:175body states/1134frames,168equipment states/1080frames,504source crops reproduced. Snapshot comparison shows exactly24side-walk PNG changes, no other generated image/metadata changes. All24installed PNGs match reviewed candidate pixels exactly. Existing3surface/reproduction tests pass. Complete validator:780source frames,113source manifests unchanged; zero errors/border touches. Evidence: output/bill-limb-integration-2026-09-21.
Native installed-versus-backup comparison completed60captures without logged errors; frame040 inspected. Source transition board includes all adjacent poses and5-to0wrap for both directions. These sampled visual checks do not certify every aspect of natural motion. No new release export.

## Next action
Review Bill in a real station at gameplay scale, including turns and transitions to other actions. Address remaining gait/style problems from that evidence. Then refresh stable Windows/Mac builds when the next gameplay milestone is ready. Existing packages predate this integration.

## Station follow-up
Native five-Storage-room fixture completed walking north/west/east, idle, kneel, repair and stand captures with no logged errors. Inspected walk-east full station and repair crop. Separate four-rotation segment/doorway/smoothing regression passes. Evidence: output/bill-limb-station-2026-09-21. This is a controlled free-build/failure-disabled fixture, not a normal expedition or broad motion acceptance. It waits for startup_complete and uses isolated save/settings paths.
An apparent open-floor work target was investigated with actual per-frame state: maintenance/repair at local(-112,16), facing south,26units above current library/tileset-mb-230 shelving at(-174,42). All recorded props are current bought furniture. No removed-prop target proved; no behavior change made. Camera/pose makes the equipment relationship less obvious and may merit later visual refinement. Probe and repair-target.json retain evidence.
