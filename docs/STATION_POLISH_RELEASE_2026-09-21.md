# Station polish release checkpoint

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Package the accumulated navigation reliability and room polish changes for owner
playtesting. The broader objective and native Apple Silicon acceptance remain open.

## Accepted decisions and constraints
No upload, publication, commit or Higgsfield. Preserve earlier packages and owner
data. The QA override is used only beside an isolated copy, never in the deliverable.

## Current state
Windows: builds/BrineSpace-station-polish-2026-09-21.
Build brinespace-1cbb0eea0b3625a8; source SHA256
1cbb0eea0b3625a8322c550c14918360b03c17e5ae121614cf2ca38c3fd12f7c.
Git f380c42c046de276b0efe26364e7596ca2410ec7, modified worktree.
Includes the navigation cancellation fixes (replacement builds and dormant/dead
restores), Hydroponics r3, Reactor furnishing/console feedback and earlier Bill,
room and runtime changes. README, metadata, manifest, NOTICE and SHA256SUMS included.
Matching Mac package: builds/BrineSpace-mac-station-polish-2026-09-21.
ZIP, README/Apple Silicon checklist, NOTICE, metadata, manifest, validation record
and SHA256SUMS included. Same source fingerprint as Windows.

## Verification
Maintained Windows exporter completed. Exact PCK audit checks 15,167 assets with
zero missing, changed, remapped or unexpected. Actual release exits 0 with zero
failures and debug=false. The isolated harness runs the maintained navigation
regression against shipped scripts before normal title/New Game/dialogue/Continue,
simulation and F8 report checks. It clears the fixture's shared navigation cache
before New Game to avoid leaking synthetic geometry. Game capture inspected;
updated Hydroponics card is visible. Evidence: output/station-polish-release-validation-2026-09-21.
Mac maintained exporter/template checks and bundle inspection pass: Universal 2
arm64+x86_64, executable mode 100755, one PCK and no QA override. Exact extracted
PCK audit passes all 15,167 assets with zero discrepancies. Evidence:
output/mac-station-validation-2026-09-21. Ad-hoc test package, not notarized;
native Apple Silicon runtime and signing/Gatekeeper acceptance remain unverified.
This is not full expedition or owner visual acceptance.

## Next action
Run the native Apple Silicon checklist when hardware evidence is available. Continue
ordinary expedition, motion and composition review informed by owner feedback.
