# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Generic seating artwork

## Objective and acceptance
Create simple generic chairs and stools matching existing artwork, with clear surfaces for seated characters. Owner visual acceptance pending.

## Accepted decisions and constraints
Owner rejected the literal 90-degree floor-plan interpretation. Existing lounge and observation seating show broad seat tops, visible front thickness and short supports. Keep neutral materials and the established painted style. The supplied generation reference is the existing sp-crew_lounge-3 master; lounge chair, observation sofa, operations console and a seated Veld source were also inspected.

## Current state
Four corrected transparent candidates in masters/: utility chair, task chair, round stool and square stool. Exact prompts and source paths are in production.json and sources.json; manifest.json records dimensions, alpha and hashes. Original generation files preserved. review-light.jpg and review-dark.jpg are resized presentation previews, not world-scale comparisons. No runtime files changed.

## Verification
All four PNGs are RGBA with transparent and opaque pixels. Reviewed composites on light and dark backgrounds. Broad sitting surfaces and short front thickness are visible. Utility chair has narrow side rails. Character overlap, seat height and animation alignment have not been tested in-game.

## Next action
Owner reviews corrected artwork. If accepted, establish world scale and seat anchors with an actual seated character before integration.
