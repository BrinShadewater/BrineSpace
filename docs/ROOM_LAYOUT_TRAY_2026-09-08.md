# Room Layout Studio: tray and free placement

Return selected to tray now accepts original room props and selectable floor decorations, alongside library additions. Original items use null overrides so saves retain the removal; returning an item to the room restores its position entry. Undo/redo and rotation drafts preserve these states. Fixed baked slices can be returned and restored at their authored position; moving their internal artwork remains unsupported.

Free placement explicitly bypasses editor placement rejection, allowing artwork outside the hull or overlapping other art. The setting is saved per layout/rotation. With it disabled, the previous checks remain active. Runtime respects removed props and floor detail overrides; routes attached to explicitly removed hosts are skipped while unknown-host assertions remain in place for unrelated errors.

Verification: tests/test_room_layout_editor.gd passed existing drag, collision rejection, library, rotation, save/reload and reset coverage, plus native removal, tray restore, undo/redo, decoration persistence, runtime removal and outside-placement persistence. Evidence: output/layout-editor/tray-test-final.log and library.png. Tests use isolated layout/default files; the owner's room_layouts.json was not written. No executable was rebuilt.

## Riser authoring controls

Flip controls now explicitly say left/right and up/down. Independent Riser wall and Foundation toggles show architecture in the editor without changing gameplay display settings. Selecting Riser decorations enables the wall preview. Windows and mounted fittings use stable riser IDs; drag/nudge, flip, tray removal and layout persistence use the existing undo/save system. Live risers resolve the same saved positions. The specialized airlock face remains outside the editor's current 15-room catalog.

Verified native riser drag, left/right flip, reload and runtime mount resolution, plus the existing editor regression suite. Evidence: output/layout-editor/riser-editor-final.log and riser-editing.png. Owner saves remain untouched by isolated test files.

## Studio usability pass

Added middle-button panning, pointer-anchored wheel zoom and Fit view reset; wrapped editing toolbar; synchronized selected list rows; disabled object actions without a valid selection; Delete-to-tray guarded while typing; and undoable Reset selected object. Reset affects only the selected object's authored placement, size and flip. Newly inserted library assets keep their placement and reset size/flip.

Native checks cover navigation transforms, reset/undo, Delete and typing focus, existing layout persistence and a 1280×900 capture. Evidence: output/layout-editor/ux-pass-final.log and ux-1280.png, visually inspected. Larger follow-up opportunities: multiple selection/group movement, atomic Save All rotations, and catalog expansion beyond the current 15 installation rooms. These remain future work, not implemented features. Owner layout saves were not modified by tests.

## Common asset tray

Added 35 shared assets: seven furniture pieces, 24 everyday wall fittings and four hull/window fittings. The catalog reuses existing source registrations through rooms/full-wall-v1/common-assets.json, preserving native aspect ratios and practical initial sizes. Sidebar filters separate common assets from room installations. Existing placement, flip, resize, return-to-tray and save handling applies. One instance of each library item per room/rotation remains the current limitation. Use Free placement for wall mounting outside floor bounds.

Native editor suite passed template loading/filtering, common chair placement, flipping, resizing and save/reload. Evidence: output/layout-editor/common-assets-final.log and common-assets.png, visually inspected. No owner layouts or packaged executable were changed by verification.

The later [layout expansion](ROOM_LAYOUT_EXPANSION_2026-09-08.md) supersedes the earlier one-instance and 15-room limits, and implements the seven requested follow-ups.
