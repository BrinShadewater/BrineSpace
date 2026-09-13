# Current Turbine owner repair

Updated September 12, 2026. This task addresses the art portion of the owner handoff. Power generation, bonus direction and clearance behavior remain with the gameplay task.

## Selected result

North q0 no longer uses the tall frontal turbine elevation. A new low overhead companion preserves the left intake, central coupling, right generator, meter panel and teal impeller while exposing top planes and directing the elliptical intake and controls toward room center. The first generation was rejected because its large circular intake remained frontal and its orange stayed dominant. The second generation was selected after source cleanup, alpha-component repair, registration and native review.

The built-in generator returned an RGB image with an imitated transparent field. `tools/room_art_pipeline.py --keep-canvas` removed the edge-connected neutral background, and `tools/clean_turbine_north_alpha.py` removed 25 disconnected one-to-three-pixel islands. The selected alpha bounds are `(79,116)-(2097,614)` on the unchanged 2172×724 canvas. Exact prompts, source roles and rejection reasons are in `assets/turbine-directional-v4/north-overhead-prompts.json`.

East/west and south retain their accepted shapes and registration polygons. Their painted orange now uses the same 0.78 saturation and 0.68 value transform as the recent Engineering corrections, with compact indicator pixels excluded. The arrow remains owned by the room renderer and was not changed.

## Evidence

- Before: `output/turbine-owner-repair-2026-09-12/before`.
- Selected native q0-q3: `output/turbine-owner-repair-2026-09-12/native`.
- Source hashes and changed-pixel counts: `assets/turbine-directional-v4/owner-repair.json`.
- `POWER EXPANSION: PASS` in `output/turbine-owner-repair-2026-09-12/test-power-expansion.log`.
- Preferred layouts pass 176 orientations, side variants pass 20, and card bindings pass all 47 identities in `output/test-runs/20260912-173056-headless`.

The new q0 card is selected by primary, grid and variant consumers. No gameplay logic, character animation or export was changed.
