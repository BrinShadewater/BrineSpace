# Floor kit v6 — September 8, 2026

32 native Godot-rendered pieces, with transparent 384×384 PNG exports. Anchor (192,192); one pixel per room unit. These are code-authored shapes, not new image-model generations. Corridor material uses the preserved v5 corridor-deck.png source.

- 5 corridor surfaces: straight, corner, T, cross, dead end. Existing straight/corner/T polygons come directly from corridor_geometry.gd. New art-only shapes use the same 72-unit mouths and 96-unit body width.
- 4 material seam overlays: straight, corner, T, cross. Place over adjoining department materials; these are neutral join strips rather than baked department pairs.
- 12 utility connectors: drain and covered cable, each straight, bend, T, cross, end cap and equipment entry. All share a 10-unit outer width and 36-unit connection radius.
- 3 flush fittings: tie-down, pipe cap, inspection plug.
- 3 condition overlays: repair, damp, corrosion.
- 5 clean replacements: access hatch, standing mat, teal marking, service marking, threshold. These replace the usable intent of the halo-contaminated v3–v5 studies. Raw studies remain unchanged; no claim of repaired source alpha.

## Usage and scope

Use floor_kit.gd in a CanvasItem draw pass or load individual exports at native scale. Draw under furniture/crew, with no emission or collision. Rotations should transform both geometry and connection anchors. Condition overlays are decorative, not damage indicators.

Integration follow-up: 16 of the 32 pieces now appear in normal rendering. Wet rooms use connected drainage strips, technical rooms covered service strips, medical floors a restrained teal marking and inspection plug, warm rooms an access hatch, and steel rooms a repair panel and flush fittings. Port-aligned thresholds provide material transitions. The three existing corridor shapes use v6 floor surfaces on their unchanged authoritative polygons. Remaining junction/condition variations, cross and dead-end surfaces stay in the library rather than being scattered into rooms without a suitable role.

All 43 selected card images were rebaked from the live room views and mapped through scripts/room_card_art.gd. Sources and previous card images remain preserved. No gameplay definitions, navigation geometry or player save formats changed.

## Verification

Run Godot with --path . --script res://tests/floor_kit_review.gd to recreate the 32 native exports and catalog under output/floor-kit-v6. The script checks transparent outer corners and rotated polygon bounds; this is not a proof of every alpha pixel or navigation topology.

Run tests/playtest_visual_refinement.gd with user argument --floor-kit-review for a dense, opt-in under-furniture fixture using all 27 non-corridor pieces. Native captures at 1280, 1600 and 2560 are preserved under output/floor-kit-v6/furnished-*.png. Inspected the 1600 capture: machinery overlaps details correctly; no visible surrounding haze. Dense placement is for review, not the normal layout. Existing operation-toggle, animation and drone-occlusion assertions passed.

All original generated source sets remain preserved. Prior department floor sources have not all been rolled into every room; this pass completes the additional connector/detail kit.

## Installed verification

See docs/FLOOR_KIT_INTEGRATION_2026-09-08.md. Native evidence is in output/floor-kit-installed, separate from the earlier dense opt-in fixture. New script/UID pairs accompany the integration. The raw exporter already includes the assets tree; a new standalone game package was not built in this pass.
