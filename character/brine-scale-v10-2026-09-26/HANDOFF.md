# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: Brine size and tube cleanup

## Objective and acceptance
Make Brine slightly bigger and remove the central blue line from her tube.

## Accepted decisions and constraints
Keep existing likeness, suit, label and smooth eight-second animation. Continue isolated preview work.

## Current state
preview_room.gd inherits v9 and increases body dimensions by 10%, centered on the previous position. source-atlas.png is an imagegen edit removing the baked central cyan line. tools/preview_brine_corners.gd targets this revision. Original versions preserved. GIF rebuilt from 200 native samples.

## Verification
Native capture passed animation loop and rigid-face assertions; owner save fingerprint unchanged. Reviewed tube crop: enlarged character fits under cap and above base, center line absent. Logs: output/brine-corner-preview/session-7621c130db2e4db0b3e3deed01046cbc.

## Next action
Owner visual review. Production integration remains separate from this preview study.

## Owner follow-up: remove label
Removed the unreadable BRINE lettering via a no-op draw_nameplate override in preview_room.gd. Refreshed the 200-frame GIF and visually verified the clean collar. Native verification passed; owner save unchanged. Logs: output/brine-corner-preview/session-aa8bf2d1568f413fa675606c2f569d1d.
