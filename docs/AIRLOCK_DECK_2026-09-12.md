# Diving-room floor and material handoff

Updated: September 12, 2026 · Project: BrineSpace

## Objective and acceptance
Improve the Diving Airlock's look, especially the flat chamber flooring, preserving working navigation and equipment service.

## Accepted decisions and constraints
Keep room geometry, door and interlock timing, crew density and locker handoff point. Use matte engineering materials and native-scale visual review.

## Current state
New wet-deck and dry-floor sources in assets/airlock-deck-v1 with exact prompts, dimensions and hashes. The chamber uses a fitted anti-slip insert with longitudinal drains; the old flat rectangle, hand-drawn seams and detached grates are superseded. UVs rotate with the chamber. Dry floor uses the existing modular profile path at opacity 0.85. Suit lockers reuse the matte suit/air-bank region with original physical footprint and service anchor. New card installed across primary/grid/variant consumers.

Changed runtime files: rooms/underwater/airlock-v1/airlock_view.gd and composition.json; rooms/floor-profiles-v1/rooms.json; scripts/room_card_art.gd and grid_canvas.gd. Floor workflow and visual bible updated.

The generated compressor candidate remains rejected for specular highlights; not a runtime asset. Original sources preserved. Generated dimensions differ from requested sizes; actual sizes and the ~4% chamber aspect fitting difference are recorded in manifest.json.

## Verification
All four final native room rotations reviewed: output/airlock-deck-20260912/final. Airlock test passes for three architects/four rotations, 1,039 travel samples, equipment/return, interlock phases, pause/power and disk saves (20260912-090352-headless). Native dry/wet actor visibility passes all eight comparisons (20260912-090403-native). Existing actor-first-floor regression retained. New raster assets use Git LFS.

## Next action
Owner accepted the latest diving-room look at session close. Integrated source and cards only; the Bill/airlock executable produced earlier in this session predates this revision. No publication or release rebuild performed. See BILL_AND_AIRLOCK_SESSION_CLOSE_2026-09-12.md for the consolidated record.
