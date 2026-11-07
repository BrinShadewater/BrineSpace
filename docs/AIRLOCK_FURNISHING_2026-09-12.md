# Airlock furnishing handoff

Updated: September 12, 2026 · Project: BrineSpace

## Objective and acceptance
Owner requested more wall detail and props in the empty Diving Airlock. Keep the pressure chamber, doors and crew interactions usable.

## Accepted decisions and constraints
Functional airlock furniture is an explicit exception to the general dressing filter. Other rooms retain their existing suppression. Reuse existing prepared artwork; preserve original rasters and unrelated concurrent edits.

## Current state
- Added reserve cylinders/hose rack and equipment-check bench through source regions in `rooms/underwater/airlock-v1/composition.json`.
- Enabled the original suit lockers, compressor and changing bench as live furniture using explicit `live_furniture` specs; `scripts/room_layout_store.gd` preserves ordinary dressing filtering.
- Enabled six airlock-specific wall attachments in `rooms/underwater/airlock-v4/fittings.gd`.
- Updated compressor placements/scales in the composition and four airlock default-layout entries. Removed the superseded one-off placement in the airlock view.
- New card and dependency record: `assets/airlock-furnishing-v1/`; active binding updated in `scripts/room_card_art.gd`.
- Added live-furnishing coverage to `tests/test_airlock.gd`; updated room workflow and visual bible.

## Verification
Final headless airlock test passes: all three architects, four rotations, 1,039 travel samples, equipment/return, ten interlock phases, power interruption, pause, disk saves and UI. Evidence: `output/test-runs/20260912-032328-headless`.
Layout free-placement checks passed separately. Final native room renders for all four rotations were visually inspected at `output/airlock-furnishing-2026-09-12/rotations/`; no overlapping service banks or blocked hatch artwork observed. Final q0 capture supplies the card. Card PNG uses Git LFS.
The earlier full native interaction capture run timed out at 180 seconds and is not counted as passed; final interaction verification is headless, with separate native room review. An intermediate run caught concurrent flood_visuals parse errors; later final run passes cleanly.

## Next action
Ready for owner visual review in the source checkout. No executable rebuilt or publication performed.
