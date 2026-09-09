# Power rooms v1

**Current turbine selection — 2026-09-08:** Owner prefers the original brighter turbine. `current_turbine.png` now uses `current_turbine-bright-source-v1.png` unchanged, with no additional machinery dimming. The native card is updated and four rotation/state checks pass (`output/bright-turbine-native.log`). The darker revision is preserved as `current_turbine-muted-v1.png`; the rejection history below is superseded for this room.

Three new gameplay identities: Current Turbine, Biomass Digester, Heat Recovery Room. See [gameplay and verification](../../docs/POWER_ROOM_EXPANSION_2026-09-07.md).

`manifest.json` records selected sprites, raw source hashes, native dimensions, alpha bounds, cards, composition profiles and reused texture dependencies. `prompts.json` preserves the exact built-in image-generation prompts. These were text-driven generations; the existing thermal room was inspected for construction/camera context, not supplied as an image edit target. The turbine's first generated sprite was the edit target for its darker revision.

The initial bright turbine is retained as a rejected candidate. Its darker revision returned an opaque checkerboard; the existing authorized cleanup tool removed edge-connected light neutrals and the two reviewed enclosed gaps at (650,650) and (650,450), preserving native coordinates. A first proposed gap seed at (681,637) was rejected by the cleanup tool before any output was written. Digester and Heat Recovery preserve their native generated RGBA unchanged. Actual native sizes are recorded rather than claiming the requested 1280px canvas was honored.

Each room owns its script identity, composition profile and card. The common view registers the new machinery skid, an existing Life Support control console and a supported Engineering service bench. Raw sprites are loaded from PNG bytes. Footprints and hulls are code-owned; art stays south-facing as room positions rotate. Recessed floor runs are decorative and traversable. Console and machine rendering use muted multipliers to honor the owner's brightness feedback.

Native checks: `tools/review_power_rooms.gd` writes the three cards and 12 rotation/state captures; `tests/test_power_expansion.gd` checks the economy and opening deck; `tests/playtest_power_expansion.gd` performs paid full-scene construction, actual discovery, crew survival, disk Save/Continue and native captures. Run each with Godot 4.6.1 `--path . --script <script>`; use `--headless` for the economy test only. Fixtures isolate save writes. Store output logs and check for script errors as well as exit status.

Assets are integrated and native-verified. Final owner art approval and a newly exported build are not implied. All PNGs remain subject to the repository's Git LFS rules.

**Larger machinery - 2026-09-08:** Main widths are now 250 units (turbine), 220 (digester), and 270 (heat recovery), previously 144 each. Skids occupy the south work area; console and bench sit behind them. Door masks rotate while these authored furniture positions stay fixed. Cards rebuilt; all 12 native rotation/state checks and production crew routes pass. Focused station captures: `output/power-room-preview-large-v1/`. Brighter turbine remains selected.

**Turbine brightness follow-up - 2026-09-08:** Owner requested slightly less brightness after enlargement. Selected bright source is preserved; turbine renderer now uses neutral 0.90 RGB modulation. Card rebuilt and native card/station preview reviewed in `output/power-room-preview-soft-v1/`. Native checks pass.

Turbine brightness follow-up: owner requested another 10% reduction; renderer modulation is now 0.81 (0.90 x 0.90). Card rebuilt and visually reviewed; station machinery reviewed in `output/power-room-preview-soft-v2/current_turbine.png`. Native state/rotation checks pass on isolated rerun after concurrent capture failed an operating-cue assertion. Paid preview passes.

Turbine south-wall placement (2026-09-08): owner requested machinery at far south given east/west doors. Skid now ends at y172 for those rotations; north/south door rotations retain rear access. Registered visible source region (18,260,1218,652) excludes faint alpha padding without editing source; rotor anchor adjusted. Brightness remains 0.81. View, card and manifest updated. Native card reviewed; 12 rotation/state checks and real turbine crew routes pass (`output/power-turbine-south-routes.log`). Ready for owner placement feedback.
