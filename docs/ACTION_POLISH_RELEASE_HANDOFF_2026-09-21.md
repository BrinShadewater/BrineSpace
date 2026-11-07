# Action polish release handoff

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Package the repaired Bill action family and latest room compositions for playtesting.
The broader animation, room, gameplay and performance goal remains unfinished.

## Accepted decisions and constraints
Preserve owner-edited rooms, library marks and earlier builds. No Higgsfield,
commit, upload or publication. Apple Silicon is the available Mac test hardware.

## Current state
Windows deliverable: builds/BrineSpace-action-polish-2026-09-21.
Build brinespace-7d3072b5bf3f53a0; source SHA256
7d3072b5bf3f53a0e8558f9d6b67340cc40aa7fb2acc9920c3d16bbd620a0443.
Git f380c42c046de276b0efe26364e7596ca2410ec7, modified worktree.
Contains side-walk and south/north/west action repairs, Data Archive and Life Support
r4 furnishing, plus prior runtime and room polish. README, NOTICE, expected manifest,
build metadata and SHA256SUMS accompany the executable and PCK.

## Verification
Maintained Windows exporter completed. Exact PCK audit: 15,167 assets checked;
zero missing, changed, remapped or unexpected. Actual release EXE exercised normal
title, New Game, architect, dialogue, Continue, simulation and F8 reporting in an
isolated profile: zero failures, debug=false, process exit 0. Game and report captures
were visually inspected. The override remains only in the isolated validation folder.
Evidence: output/action-polish-release-validation-2026-09-21.
This startup fixture does not prove normal expedition or full animation acceptance.

## Matching Mac package
builds/BrineSpace-mac-action-polish-2026-09-21 has the same build ID and source
fingerprint. Maintained exporter/template checks, Universal 2 architectures,
executable mode 100755, single-PCK/no-override inspection and exact 15,167-asset
audit passed. Evidence: output/mac-action-validation-2026-09-21. README/checklist,
NOTICE, metadata, manifest, validation and SHA256SUMS accompany the ZIP.
Native Apple Silicon runtime, Gatekeeper and signing acceptance are unverified.

## Subsequent station-review finding
output/bill-paid-station-review-2026-09-21 preserves a failed native fixture:
paid controlled-blueprint setup followed by manual 30 Hz updates, no forced actor
direction/equipment. It raised a missing room key at bill_npc.gd:578 and captured
no completed action cycle. Do not count this as animation acceptance.
Architect thaw starts rebuild(game,true) without awaiting it; release performs a
synchronous rebuild. The older coroutine can resume over dictionaries replaced by
the newer rebuild. Accelerated setup crosses thaw without render-frame yields,
so a focused interleaving regression and normal-play scope check are needed.
No production fix has been made, and both packages retain this potential issue.

## Next action
Isolate and repair superseded staged navigation builds, rerun the failed station
review, then resume motion/composition review. Native Apple Silicon testing and
owner acceptance remain open. Do not re-export merely for these documentation edits.
