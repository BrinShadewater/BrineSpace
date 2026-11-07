# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: riser height and square-wall audit

## Objective and acceptance
Raise every exposed riser wall face by25% and review all square room-wall art for mismatched or placeholder-looking rendering.

## Accepted decisions and constraints
Riser face48 ->60 world units, fixed deck baseline-192. Caps and end returns move with the face; mounted fittings shift upward6 units without stretching. Raised lights follow the cap. This owner direction supersedes older low-riser restrictions. Footprints, hatch exclusions, doorway geometry and personal layout files remain intact.

## Current state
`riser_geometry.gd` centralizes face/cap height; `north_wall.gd`, Airlock v4 fittings and room_lighting consume it. Grid darkness now covers exposed raised faces. Eight square perimeter replacements: Current Turbine, Biomass Digester, Heat Recovery, Cold Store, Galley, Observation Room, Salvage Workshop and Airlock. Their six defining view files use `department_wall_material.gd`, with registered steel, warm habitation and medical source crops plus matching caps. Existing sources were visually inspected; no new raster art was generated. The Airlock chamber remains a bespoke assembly; only its perimeter material changed.

44 furnished-room cards are re-rendered to `assets/wall-refresh-v1/cards/`, with compact transparent framing and taller-cap clearance, and selected by `scripts/room_card_art.gd`. Three corridor cards stay current. Manifest hashes and wall-owner inventory are in the same asset directory. Audit and bake tools now accept revision output directories. The maintained and installed room repair workflow and aesthetic bible record the decisions and lessons.

## Verification
- Baseline44 rooms x4 rotations; final44 rooms x4 rotations (176 native captures each), no script/load errors. All defining wall renderers resolved. Full default contact sheets and all three alternate-orientation sheets reviewed, plus native Airlock and selected corrected room details.
- Riser adjacency assertions pass with mixed Galley/Listening Post/Airlock and a stepped northern room. Powered and forced-zero-light captures visually inspected. This checks rendering state, not a timed blackout gameplay scenario.
- Card bake44/44 and selected-path inventory47/47 pass. New PNGs resolve to Git LFS. New script UIDs are paired.
- Broader `test_airlock.gd --actor=bill` FAILED five helmet-state checks (completion, shelf release/persistence, power-loss removal and returned equipment) across836 travel samples. Its hatch aperture/rotation checks reported no failures. No claim that this broader interlock test passes; helmet logic was not modified or diagnosed by this wall task.
- Evidence: `output/wall-audit-before/`, `output/wall-audit-after/`, `output/wall-audit-final/`, `output/riser-height-final.log`, `output/room-architecture-v2/adjacency*.png`, and `output/wall-refresh-cards-compact.log`.

## Next action
Owner visual playtest of taller risers and the eight corrected perimeter materials. Separately investigate the recorded Airlock helmet-state failures. Existing Pressure Control/Listening Post alternate furnishing identities were preserved; this pass fixes square hull materials rather than generating replacement directional installations. No packaged export or publication was performed.
