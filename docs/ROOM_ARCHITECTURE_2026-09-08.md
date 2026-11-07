# North-wall placement and architectural preview

Owner direction: remove the bright added Listening Post wall installation; show its riser and foundation; raise large north-wall art into the upper wall edge.

The Listening Post now retains the original connected U-console instead of the added deepwater-listening-wall installation. Sources are preserved. Shared full-wall artwork on sealed north walls has a -22-unit visual offset, putting its top at -196 against the -192 wall edge. Ground footprints and side/south installations remain unchanged. Existing local Layout Studio overrides remain authoritative.

All 43 current cards were refreshed into assets/room-architecture-v1/cards and selected in room_card_art.gd. Native architectural previews use the existing north_wall.gd riser and the registered silt foundation, with no change to the player's raised-walls setting. Previews show isolated sealed rooms.

Validation: 15 installation rooms × four rotations × both operating states passed visual envelope and door lane assertions; native architecture captured four rotations per room. Listening Post, Research Lab, and the full north-facing sheet were visually inspected. Corrected the preview fixture to disable its standalone GridCanvas processing; the final log has no script errors. No executable was rebuilt.

Evidence: output/room-architecture-v1, output/room-architecture-review-final.log, output/north-wall-placement-check.log, output/north-wall-cards.log. These later placements supersede the September 8 floor snapshot's selected card paths; its original evidence remains preserved.

## Textured riser revision

Replaced the procedural riser panels, window and decorations with registered hull-kit and wall-fitting sprites. Department tint remains restrained. Exposed left/right ends extend the current room's vertical wall material to the crown; adjoining raised walls omit those returns. Adjacency requires a layered non-corridor room with no room directly north, rather than mere side occupancy. Airlock keeps its specialized wall face and receives the same end treatment.

Native revision evidence: output/room-architecture-v2 (15 rooms, four rotations); output/riser-wall-review-final.log. tests/test_riser_adjacency.gd exercises isolated, adjoining and stepped boundaries in the actual scene with raised walls enabled only in the test process. Existing player display settings remain unchanged. Source sprites were reused; no new raster generation was needed. Cards retain the low-shell framing; architectural previews include riser and foundation.

## Riser pass 3: department compositions

Seven authored families replace the repeated panoramic-window-and-two-fittings arrangement: crew, cultivation, medical, science, acoustic/command, data/containment, and engineering. Windows use aspect-preserving fits; medical gets a small pressure porthole, science twin portholes, crew a medium window, while secure data/containment uses access and instrument panels. Mounts remain within the 48-unit wall face, with restrained source modulation. Airlock retains its specialized face. Reused registered sources; no generated replacements or new gameplay effects.

Review expanded from the 15 installation rooms to all 40 non-corridor rooms, four rotations each. Evidence is output/room-architecture-v3 and output/riser-pass3-all.log. Listening Post, Crew Lounge and Med Bay were visually inspected. Existing low-shell cards and player raised-wall preference are unchanged. No packaged build acceptance is claimed.

## Corner seal revision

Added continuous opaque structural backing under exposed riser returns from y=-249 to -184, overlapping the lower wall corner. This closes transparent bevels and room-specific cap offsets without replacing the approved surface art. Adjoining risers still omit exposed-end returns.

Native evidence: output/room-architecture-v4, 40 rooms × four rotations; output/riser-corner-seal.log has no script errors. Pixel inspection of both inner corner strips (x=82..101 and 658..677, y=9..101 in 760×850 previews) found background holes in 16 previous v3 captures and zero in all 160 v4 captures. Med Bay was visually inspected. This is bounded seam evidence, not a packaged-build claim.
