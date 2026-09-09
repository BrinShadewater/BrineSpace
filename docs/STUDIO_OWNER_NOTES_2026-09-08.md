# Studio owner-notes handoff

Updated: September 8, 2026 · BrineSpace · room Studio and art corrections

## Objective and acceptance
Implement the owner's Studio controls, directional art, riser doorway, movement and five art-repair notes. Review is at [the illustrated landing page](../output/studio-owner-notes-2026-09-08/index.html), with a linked 47-room / 167-image catalog and previews of the three personally edited rooms. Owner visual acceptance remains pending.

## Accepted decisions and constraints
- Center-bottom Rotate Room, Next Room and Save; valid changes autosave across cached rotations of the current room. Invalid drafts remain recoverable and require placement correction before saving.
- R chooses a selected asset's next matching authored variant; otherwise rotates the room. F flips selected art. Room Default includes matching vertical variants. A rotated variant may need repositioning before save.
- South-mounted banks face inward. Direction is selected from the actual wall and door geometry, not quarter number alone. No bitmap inversion substitutes for authored rear views.
- Preserve the owner's personal layouts and unrelated work. Real layout SHA256 remains `CD5D395B06EA2A06617B47C96FA73E3727C9DEFD050DA538DEC14379EBF2BD0D`, identical to the read-only backup in the output folder.

## Current state
- Studio / persistence: `scripts/room_layout_editor.gd`, `room_layout_store.gd`, `room_asset_library.gd`; split-wall library dispatch and movable Listening Post regions retain stable IDs.
- Riser: `rooms/whole-room/room_door.gd`, `north_wall.gd`, `nursery_whole_view.gd`, plus grid and Studio rendering. North door has two retracting leaves spanning the riser. The low north edge hides only when a visible riser is present.
- `assets/studio-art-fixes-v1`: Mining/Refinery matte source repaints, prior registrations, cutout corrections for Mycelium/Lounge/Maintenance. Source PNG pixels remain untouched during vector registration. Mining crane enclosed openings explicitly excluded. Fifteen existing registrations revised.
- `assets/south-wall-facing-v3`: twelve rear-facing sources and registrations. Ten current q2 defaults use them; Radio/Quarantine retain their geometry-selected defaults and expose south variants in the tray. Earlier v1 candidates rejected for outward-facing fronts. Rear sources deliberately reveal overhead equipment and quiet backing instead of the original front elevation.
- All 44 furnished-room cards refreshed into `assets/studio-art-fixes-v1/cards`; three corridor variants retained. Default gallery excludes personal overrides; saved-layout previews load the backup without writing to it.
- Reproducible tools: `apply_studio_art_fixes.py`, `register_south_wall_facing.py`, `capture_room_catalog.gd`, `review_studio_native.py`, `build_studio_owner_review.py`; catalog/card builders accept output paths.

## Verification
- Native `test_room_layout_editor.gd`: PASS (`editor-final.log`), including drag, invalid placement, history, persistence, tray, lighting and pause restoration.
- Native `test_studio_owner_notes.gd`: PASS (`owner-tests-v3.log`): bottom actions, cached-rotation autosave, R/F, variant undo/reload/repeated runtime apply, Listening movement, distinct closed/half/open riser captures.
- Native catalog: 47 identities / 167 images; saved-layout capture: 3 identities / 12 images. Source and native south boards reviewed; five repaired rooms reviewed, including final Mining aperture correction.
- Card consistency: 47 primary/grid/variant mappings and decoded images PASS. 162 wall registrations have matching source hashes. Gallery 561 local links and landing-page 38 local links resolve. New PNGs match Git LFS filter.
- No script/errors in final fixture logs. Existing raw-image export warnings persist; this is local native validation, not a fresh exported-build or expedition route acceptance.

## Next action
Owner can annotate the gallery and export notes. Standalone recent asset records elsewhere in the catalog are still separate from fitted installations; this correction pass does not claim those historical installation tasks complete. Review new south-facing silhouettes/material identity and any desired additional room dressing.
