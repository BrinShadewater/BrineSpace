# Floor tile editor polish

The material picker now displays swatches using the actual source regions. Swatches are reused until the room source changes. A variation toggle allows disabling the effect with undo support, and loaded layouts synchronize the seed and toggle. Reset floor only clears legacy tile rearrangements as well as material overrides before restoring authored defaults. Changing tool or brush finishes an active stroke, and the first painted cell updates the live draft immediately.

Native test_floor_tile_polish passed across the four newer rooms, including visible painting, swatches, variation toggle/undo, legacy reset, save/reload and reset state. Original test_modular_floor also passed. The final Galley editor capture was visually inspected; evidence is in output/floor-tile-polish. This pass changes editor controls and behavior, not raster art or default floor appearance. It is in the current checkout and postdates the complete-floor Windows package.
