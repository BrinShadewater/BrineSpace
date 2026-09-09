# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: Retire placeholder floor artwork

## Objective and acceptance
Use the finished floor materials and artwork throughout live rooms and cards, without the old procedural decorative paint layered over them.

## Accepted decisions and constraints
Removed generic aisle outlines, corridor stripe/grate variants, short service ticks and filled-polygon furnishing decals. Existing authored rugs, mats, drains, utility sprites and department floors remain. Primitive utility runs and research/command/BRINE mats now use existing finished artwork. Lighting, contact shadows, structural hull geometry and functional intake/status indicators remain. Historical source files and save variant IDs are preserved; they do not restore the retired paint in live rooms.

## Current state
Shared changes: rooms/whole-room/room_floor.gd, room_dressing.gd, room_services.gd; rooms/underwater/corridor_surfaces.gd. Room-specific cleanup: power_room_view, crew_lounge_view, hydroponics_view, med_bay_view, airlock_view, biodome_view, clone_lab_view, cryo_chamber_view, xeno_lab_view and brine_core_view. tests/review_floor_profiles.gd accepts a new output directory to preserve previous evidence. scripts/room_card_art.gd selects all 43 new PNGs in assets/placeholder-cleanup-v1/cards/; manifest hashes verified and PNG LFS attributes checked. Diagnostic-only unprofiled floor fallback remains outside live catalog use.

## Verification
Final native review passed: 43 rooms, 344 rotation/power-state renders, plus shared-wall samples. All 43 cards baked without engine errors. Reviewed full-catalog contact sheet and BRINE close-up in output/placeholder-cleanup-v2/. Logs: output/placeholder-cleanup-review-final.log and output/placeholder-cleanup-cards-final.log. Existing raw-image export warnings remain; no package produced.

Separate floor-detail anchor audit exited 1: 308 placed and 12 unavailable. Research q3 and Xeno q1 each lack clear floor for a detail; Listening Post has eight references to a missing full-wall host; Isolation Vault q1/q3 have no clear floor for inspection plugs. These are current layout/profile follow-up issues; this cleanup did not alter those host definitions or placement rules. Do not report the anchor audit as passed. Details in output/placeholder-cleanup-anchors-final.log.

## Next action
Owner visual review. Resolve the recorded host/space issues in a dedicated furnishing pass before claiming complete floor-detail placement acceptance. Unrelated concurrent checkout edits preserved; no export or commit.
