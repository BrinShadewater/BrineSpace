# Battery Array orange-brightness correction

Updated September 12, 2026. This is an art-only source milestone under the room-art handoff; gameplay and character animation were left to their existing tasks.

## Change

The selected Battery Array wall family used large, high-value orange frames, especially in the side and south overhead views. `assets/battery-directional-v2` now provides muted north, paired-side and south sources. A deterministic HSV transform lowers orange value to 68% and saturation to 78% while preserving source hue, texture, wear, geometry, alpha and all non-orange pixels. Small high-value yellow/amber indicator pixels are explicitly excluded so functional readouts remain legible.

All eight split registrations now select the new sources without changing their polygons, placement rectangles or section inventory. The q0 catalog card was refreshed from the selected live room.

## Evidence

- Before and after native q0-q3 captures: `output/battery-orange-repair-2026-09-12/before` and `output/battery-orange-repair-2026-09-12/native`.
- Source parameters, changed-pixel counts and hashes: `assets/battery-directional-v2/orange-brightness-repair.json`.
- Reproduction tool: `tools/reduce_battery_wall_orange.py`.

The revised family keeps graphite battery lids dominant, uses rust-brown frames as construction, and retains compact amber gauges. The existing north source still carries more elevation than the current top-down owner contract allows; this palette correction does not claim that later camera conversion is complete.

## Validation

`test_preferred_room_layouts` passes 176 orientations, `test_side_wall_variants` passes 20 variants, and `test_room_catalog_cards` passes all 47 identities in `output/test-runs/20260912-171332-headless`. No export was built.
