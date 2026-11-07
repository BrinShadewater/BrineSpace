# Floor kit integration — September 8, 2026

The v6 library is now used by the live shared room floor and corridor renderers. Sixteen pieces have a normal placement; the other sixteen remain available variations. Installed floor decoration is sparse, non-emissive and beneath furniture. Wet and technical service strips have shared endpoints; thresholds follow each actual port and remain inside the room edge. Dark corridor floor finishes are clipped to the existing straight, corner and T polygons. Cross/dead-end art adds no gameplay room types.

All 43 current selected room cards were rebaked into assets/floor-kit-v6/cards, using live view resolution and existing sealed-card rendering. The card manifest records IDs and hashes; scripts/room_card_art.gd selects them. Original cards remain intact.

## Evidence

- tests/review_installed_floor_kit.gd: 43 rooms, 344 rotation/state render iterations, plus shared-wall and corridor-variation captures. This is rendering coverage, not approval of every artwork pixel. Corridor iterations use the existing powered surface renderer in both loop states; operating-state variation applies to non-corridor views.
- tests/test_shared_room_surfaces.gd: shared 48-unit floor grid and 72-unit door aperture; ten door frames passed.
- tests/test_corridor_detail_bounds.gd: 248 existing fitting corner samples passed. This test covers corridor fitting bounds, not the new material's visual quality.
- tests/test_preview_doors.gd: exit 0; zero failures reported.
- tests/playtest_visual_refinement.gd: operation toggle, animation and under-hull/exterior drone comparison passed. Native installed captures at 1280, 1600 and 2560 pixels wide saved under output/floor-kit-installed/station-*.png.
- Visual inspection: life-support card, rotated T corridor, rotated medical room and installed station. Details remain subordinate to machinery; door openings retain their shape. No visible surrounding halo from the registered replacements.

New raw PNG directories fall under the existing assets export root. No new standalone executable was produced; the older frozen build does not contain this integration. Raw v3–v5 halo-contaminated studies remain preserved and are not installed by this change.

Reproduction logs: output/floor-kit-v6/card-bake.log, rotations-installed.log, installed-final.log and test_*.log. The baker preserves existing exports and intentionally refuses to overwrite an earlier card run.
