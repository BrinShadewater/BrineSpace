# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: current room art audit and owner catalog

## Objective and acceptance
Check current room art and provide the complete illustrated room list for owner notes. The latest standalone additions are not all installed; this remains an integration backlog, not a completed all-prop rollout.

## Accepted decisions and constraints
Preserve existing room machinery, door geometry and saves. Latest standalone art is not automatically a replacement: seed and communications host studies record rejected overlaps. Multiple directional sources and companions are not additional room identities. No room layout or gameplay changes in this pass.

## Current state
- `output/room-catalog-2026-09-08/index.html`: searchable 47-room catalog, 167 native images, 75 standardized recent prop records, browser-local notes and Markdown export. `contact-sheet.jpg` provides all 47 named rooms on one board.
- `assets/room-catalog-refresh-v1/cards/`: 44 fresh furnished-room PNGs and provenance manifest. `scripts/room_card_art.gd` and primary/variant mappings in `scripts/grid_canvas.gd` select them. Existing three corridor cards and alternate corridor decorations remain selected.
- New tools: `capture_room_catalog.gd` (paired UID), `build_room_catalog.py`, `install_catalog_cards.py`. Regression: `tests/test_room_catalog_cards.gd` (paired UID).
- Old cards remain available. The checkout already contained extensive unrelated work; these changes are local and uncommitted.

## Verification
- Native Godot 4.6.1: all 47 database identities captured; 167 images cover q0 plus supported furnished-room rotations. Default layouts, offline stills. Full q0 contact sheet visually reviewed; alternate poses supplied for owner review, not blanket visual acceptance.
- 150 full-wall registration source hashes match. All 75 standardized candidate export hashes match. Nine candidate references are library entries in common-assets.json; library availability alone does not establish room installation.
- Card consistency regression passes for all 47 IDs, decoding and primary/grid/first-variant agreement. Native portrait-card preview passes and its 1600x900 result visually reviewed. No SCRIPT ERROR or ERROR in those logs. Capture log has existing raw-image export warnings; no new package was tested.
- Browser layout visually reviewed; Hydroponics filtering and note persistence across reload checked. Temporary test note cleared. Note-download button is implemented but its downloaded file was not independently inspected.

## Next action
Review the catalog and return room numbers/names with corrections or exported notes. Continue fitting the standalone libraries into authored room layouts: resolve known seed/communications overlaps, then verify doors, wall contact, supported accessories and occupied crew access. This audit does not establish that all newest props are installed. Rebuild captures after subsequent room changes.

Local preview server: Python HTTP server on 127.0.0.1:8766, PID 121724. The catalog also opens directly from disk with relative image links.
