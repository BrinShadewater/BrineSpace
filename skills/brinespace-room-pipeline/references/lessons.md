# Lessons and attribution

These are adapted workflow ideas, not imported external instructions or copied
engine code. Reviewed 2026-09-05; external projects may change.

## Sprite-maker / Sprite Studio

[Asset-pack harness](https://github.com/JohnKinyanjui/sprite-maker/blob/main/src-tauri/resources/skills/sprite-director/references/asset-pack-harness.md):
coordinated projection, scale, palette and complete pack manifests. Use contact
sheets to review our separate room assets; do not inherit its generation-sheet
strategy automatically when individual high-resolution rooms are needed.

[Polish script](https://github.com/JohnKinyanjui/sprite-maker/blob/main/src-tauri/resources/sprite_polish.py):
local repair regions, source hashes, reversible versions and geometric comparisons.
Adapt the principle of preserving outside-region pixels. Its corner-color keying
and 64-color remapping are not defaults for dark, detailed BrineSpace rooms.

[Quality gates](https://github.com/JohnKinyanjui/sprite-maker/blob/main/src-tauri/resources/skills/sprite-director/references/quality-gates.md):
separate technical diagnostics from visual acceptance. Its documentation contains
different animation approaches; do not combine them into one purported guarantee.
For BrineSpace machinery prefer deterministic local overlays. For generated
character strips follow the available sprite-pipeline skill and the user's brief.

## Capybara 2.5D engine

[Asset integration](https://github.com/d-liya/capybara_2d_engine/blob/main/.agents/skills/capybara-game-developer/ASSET_INTEGRATION.md):
preserve proportions, register assets in their real consumers and separate static
art from stateful overlays. Generation alone does not finish gameplay integration.

[Placement data](https://github.com/d-liya/capybara_2d_engine/blob/main/docs/recipes/map-placement.md):
named bounds provide stable placement anchors. Translate this to Godot room-local
regions; do not import its coordinate ordering, engine API, cloud keys or web stack.

## BrineSpace observed failures

- Requested transparent PNGs returned opaque white/checkerboard backgrounds.
- Requested 1280 output returned 1254 square images.
- Cross-room style references leaked extra door trim into straight corridors.
- A corner had convincing trim but no actual openings.
- A refinery conveyor visually blocked a required path.
- Deep lounge doorway cutouts and independent crop margins changed seam geometry.

Therefore: inspect alpha pixels, bind art to canonical geometry, record transformations,
review whole sets at gameplay scale and keep acceptance stages separate. Neither a
successful tool call nor a passing cleanup test is proof of production readiness.
