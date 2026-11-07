# Project handoff

Updated: September 29, 2026 · Project: BrineSpace · Task: large rooms in Layout Studio

## Objective and acceptance

Show all four 2×2 special rooms in the Layout Studio, let the owner place station props around fixed equipment, save each rotation, and show those props in live rooms with correct navigation.

## Accepted decisions and constraints

The painted room shells, four station doors, ocean fittings, and large centerpieces remain fixed. Studio edits use the existing `room_layouts.json` format. Owner layouts and tileset marks are not reset. Free placement retains the Studio default; constrained mode checks the 2×2 floor, doors, ocean face and fixed equipment.

## Current state

Branch `codex/large-rooms`. `rooms/large-rooms/studio_view.gd` supplies a 2×2 Studio view and cached live prop overlays. `scripts/room_layout_editor.gd` lists the four rooms and handles their preview, guides and prop validation. `scripts/grid_canvas.gd` renders saved props and includes them in crew blockers; `tools/bake_large_room_cards.gd` uses the same overlay when cards are rebaked. `scripts/drone_dock.gd` fixes Studio-close cleanup of a completed worker task. `tests/test_large_room_studio.gd` is registered in `tests/index.json`. No game balance or fixed room art changed.

## Verification

Focused headless and native Studio tests pass; four native captures in `output/large-room-review/studio-*.png` were visually reviewed. Existing `test_large_room_integration.gd` and native `test_room_layout_editor.gd` pass. The card baker rendered 16 review rotations with the saved overlay; Moonbay rotations 0 and 1 were inspected. All Godot commands used scratch `APPDATA`; the focused test file is present there. A before/after fingerprint of the owner's real profile differed in five files and one new bug report during this work window; these were not restored because other activity may own them. No test was directed at the real profile.

## Next action

Owner hands-on review of the large-room Studio views and saved layouts. The current large-room editor offers props only; character preview and floor, wall, light and effect authoring would need separate 2×2 support if requested.
