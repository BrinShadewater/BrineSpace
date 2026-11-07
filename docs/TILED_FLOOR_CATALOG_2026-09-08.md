# Tiled floor studio catalog rollout

All 43 identities in the current Layout Studio catalog now enable modular floor tools. This pass added the remaining 28. Default department materials, rims, thresholds and floor details remain separate from painted material overrides.

The studio catalog had stale view paths for several rooms. Its existing entries now point to the current views recorded in the floor profiles; asset/save keys are unchanged. This fixes editing an older room implementation instead of the current floor consumer.

Native checks passed: 112 default-material comparisons for the new 28 identities, visible paint changes in every new room, undo/redo, save/reload and reset. The earlier five-identity and eight-identity floor tests and the comprehensive layout editor suite passed again. Logs and checks.json are in output/tiled-floor-catalog. Updated furnished captures were inspected in final-review.jpg. The comparison fixture verifies floor material mapping; room captures verify integration. No new raster art or whole-game performance claim.

Remaining: Observation Room, Salvage Workshop, Galley and Cold Store have profiles but are absent from the studio catalog. They are not counted as supported by this rollout. The old Windows pilot export still predates these source changes; packaging remains separate.
