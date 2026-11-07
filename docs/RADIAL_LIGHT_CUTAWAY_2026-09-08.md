# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: radial lighting and riser cutaways

## Objective and acceptance

Remove floating fixtures when their supporting riser is hidden and replace beam
illumination with soft radius-based lighting, as requested by the owner.

## Accepted decisions and constraints

Fixture housings follow supporting-wall visibility. Illumination and saved light
positions remain stable through cutaway toggles. Room costs and gameplay unchanged.

## Current state

Follow-up: the owner spotted a south exterior fixture below the foundation legs.
Its mount now sits at local Y=198 on the solid deck rim, replacing Y=304 in open
water. Native `test_riser_lighting.gd` passes with a south mount regression check;
reviewed `output/layout-editor/exterior-outward.png` after the correction.

- `rooms/whole-room/radial_light.gd` (+ UID): cached radial gradient, clipped to the
  interior deck; reused without deck clipping for exterior lights.
- `rooms/whole-room/room_lighting.gd`: interior radial pools replace cone bands.
- `scripts/grid_canvas.gd`: housings gated by raised walls, wall hardware and north
  neighbors; wall hardware included in fixture cache invalidation.
- `scripts/room_layout_editor.gd`: housings follow the Studio riser toggle.
- `scripts/station_hardware.gd`: radial exterior lights and supporting-wall gates.
- `tests/test_riser_light_visibility.gd` (+ UID): cutaway regression and captures.
  `tests/test_riser_lighting.gd` updated for radial geometry.

## Verification

- Native visibility fixture passes: hidden/visible riser, walls off, north neighbor.
  Reviewed `output/riser-light-hidden.png` and `output/riser-light-visible.png`.
- Native Studio/legacy migration/power/exterior checks pass; reviewed Studio hidden
  riser capture at `output/layout-editor/riser-fixtures-hidden.png`.
- Light renderer compatibility check passes (zero pixel difference between modes).
- Godot 4.6.1 editor import exits 0; new script UIDs generated; diff whitespace check
  passes. Native runs retain existing raw environmental image-load warnings.

## Next action

Owner visual review. No remaining implementation blockers; no commit or push made.
