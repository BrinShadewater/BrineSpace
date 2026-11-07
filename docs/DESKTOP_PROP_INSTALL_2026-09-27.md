# Project handoff

Updated: 2026-09-27 · Project: BrineSpace · Task: install existing Desktop clean props

## Objective and acceptance
Owner corrected the source selection: use the props already made in Desktop/BrineSpace Clean Prop Exports, including red, blue and orange airlock suits. Existing equipment and layouts remain authoritative.

## Accepted decisions and constraints
Use the existing game-size exports, not new gray recolor generations. Preserve catalog IDs, geometry, collision and saved layouts. Desktop Review Candidates and separate concepts are outside this installation.

## Current state
Copied 323 existing game-size PNGs byte-for-byte to assets/station-props-v2. All match existing catalog canvas sizes. Refreshed 43 affected assets/room-cards-v2 cards using a scratch copy of owner layouts. Refreshed the native airlock gallery in output/airlock-integration-2026-09-26/review.html with cache-busted images. Original installed PNGs and mapping audit are preserved in output/muted-steel-2026-09-27. Earlier generated assets/station-props-steel-v1 candidates remain uninstalled and explicitly marked superseded.

## Verification
323/323 installed files exactly match Desktop exports; no dimension mismatches. Native airlock card and north gameplay capture visually checked for steel equipment and colored suits. All four native expedition runs passed with zero failures. All validation subprocesses received scratch APPDATA; cards used a copied layout. The real profile fingerprint nevertheless changed during the run (including progress/checkpoint files), so unchanged-profile verification cannot be claimed in this concurrent workspace. No real profile files were restored or overwritten by this installation. See owner-before.json and owner-after.json. Four-direction expedition validation results recorded alongside native-q*.log in the task output folder.

## Next action
Owner visual review; packaged executables need a separate rebuild to include these source changes. No claim of visual acceptance for every prop at every rotation.
