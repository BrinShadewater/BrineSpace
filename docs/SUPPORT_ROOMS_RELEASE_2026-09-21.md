# Project handoff

Updated September21,2026 · BrineSpace · Support-room release checkpoint

## Objective and constraints
Package recent accepted-for-playtest furnishing and display repairs alongside prior
Bill/drone/renderer work. Preserve owner layouts and older builds. No Higgsfield,
commit, upload or publication. Broad goal remains active; visual acceptance is open.

## Artifacts and identity
Windows: builds/BrineSpace-support-rooms-2026-09-21.
Mac: builds/BrineSpace-mac-support-rooms-2026-09-21.
Both build brinespace-0b2b3ab132bb4781, source SHA256
0b2b3ab132bb478139a654430a7a9c6d3b144d517b086db804492e2ff9a6d88a.
Git f380c42c046de276b0efe26364e7596ca2410ec7, modified worktree.
Manifest15,500files/1,637,307,642source bytes. Runtime PCK1,681,146,444bytes.
Includes Gravity Loom, Clone, Shield, Radio, Workshop and Holo furnishing; Radio/Holo
saved-placement fixes; layered projector/analysis chart. Earlier Bill/drone/room/
render fixes retained. Raw Holo generation/reference excluded from runtime closure;
normalized housing and both registrations included. Deliverable README, NOTICE,
build_info, expected-manifest and SHA256SUMS supplied; Mac adds validation.txt and
Apple Silicon test checklist. No override shipped.

## Verification
Manifest suite6tests passed. Maintained Windows and Mac exporters completed.
Both exact-PCK audits:15,173assets; missing/changed/remapped/unexpected all0.
Actual Windows EXE exit0, debug=false,0failures and clean stderr. Covers navigation
replacement and inactive/dead restore; eleven rooms/four rotations/repeated setup;
Holo asset decoding/live classification/authored placement; native rendered Holo
three animated regions with off/held-clock stability in four quarters; normal title,
New Game, architect, transmission Continue, simulation, visible station, card setup,
and F8 trace ZIP. Exported gameplay and Holo off/on captures inspected.
Fixture uses isolated profile BrineSpaceSupportRoomsRelease0b2b3ab1. No product
changes or failed application test required a second export.

Mac verified official4.7.2template, Universal2 arm64+x86_64, executable100755,
onePCK/nooverride. ZIP1,687,343,877bytes. Actual inner PCK audited, matching source
identity independently checked. Ad-hoc test ZIP, not notarized. Native Mac runtime,
Gatekeeper, sound/input/save behavior remain unverified on owner's Apple Silicon.
Evidence: output/support-rooms-release-2026-09-21 (logs, fixture, manifests, captures,
Mac inspection and final release-checklist.json). Older broad49-room/31-pair native
parity belongs to its earlier snapshot; this checkpoint has focused room evidence.

## Next action
Native Apple Silicon checklist on owner hardware; ordinary paid expedition and
Bill/room motion/art acceptance. Continue remaining source-detail/perspective work,
Radio static-panel feedback, measured performance and unresolved real-session bugs.
This is a tested local checkpoint, not public-release or full-objective completion.
