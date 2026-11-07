# Project handoff

Updated: 2026-09-09 · Project: Brine Space · Task: Window-free room risers

## Objective and acceptance
Create more room-specific risers, leave spaces for future separate windows and document them. Work delivered for owner visual review; no new owner acceptance recorded.

## Accepted decisions and constraints
No baked windows in new riser art. Preserve central 92-unit doorway reserve and 384 × 60 face geometry. Baked end fittings provide room identity. Existing V2 art remains installed.

## Current state
Six sources, registration metadata, six cards, 24 native previews, prompts, placement notes and guide-toggle gallery in assets/room-risers-v3. Updated catalog merge and card bindings in rooms/whole-room/riser_catalog.gd, scripts/room_card_art.gd and scripts/grid_canvas.gd. Updated visual bible and repository room-pipeline reference with owner direction.

## Verification
Native review fixture output/room-risers-v3/review.gd passed source bounds, ratio and entry-zone checks and captured all 24 rotations. All six sources and default furnished views inspected; sample opposite rotations inspected. Card consistency passed all 47 room identities and decoded PNGs. PNGs covered by LFS. Future window props require actual fit and furniture occlusion review. No executable rebuilt.

## Next action
Owner visual review in assets/room-risers-v3/review.html. Window props can be authored later using WINDOW_PLACEMENT.md; not part of this asset pass.
