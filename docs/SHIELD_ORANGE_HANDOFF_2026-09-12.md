# Shield Generator orange correction

Updated September 12, 2026. This is an art-only milestone under the owner room-art handoff.

The weak `hull_panel_cradle` was already absent from all four current preferred layouts. The remaining selected wall family still used bright orange over long rails, tank straps, corners and controls. `assets/shield-directional-v2` now supplies muted north, paired-side and south sources. The measured HSV repair lowers painted orange value to 68% and saturation to 78%, preserves compact high-value amber/yellow indicators, and changes no geometry, registration polygon, placement or gameplay state.

Native q0-q3 captures in `output/shield-orange-repair-2026-09-12/native` show the wall assembly on each selected edge, the cradle still absent, independent equipment retained and orange subordinate to graphite/steel. The q0 card was refreshed from the live selected room. Source hashes, changed-pixel counts and parameters are recorded in `assets/shield-directional-v2/orange-brightness-repair.json`.

`test_preferred_room_layouts` passes 176 orientations, `test_side_wall_variants` passes 20 variants, and `test_room_catalog_cards` passes all 47 identities in `output/test-runs/20260912-171817-headless`. No export was built.
