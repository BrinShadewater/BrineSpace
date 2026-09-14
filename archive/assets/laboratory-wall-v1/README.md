# Laboratory wall handoff

Updated September 8, 2026. Standalone continuous laboratory wall, part of ongoing wall/prop production.

## Objective and constraints

Translate the owner's fitted retro-industrial references into a matte science bench with adjoining human-scale bays. North backing stays straight; controls face inward/south. Owner review remains pending.

## Current state

`laboratory-wall.png` is the 2121x741 transparent export, intended equipment width 328 world units. Six bays provide sample drawers, an analysis terminal, specimen examination, preparation space, wash basin and sterilizer. Raw V1/V2 images and exact built-in imagegen prompts are preserved. `manifest.json` and `material-scale-review.json` record provenance, hashes, reference roles and review stages.

## Verification

V1 was superseded for a bright chamber reflection. V2 corrects the material but returned an RGB checkerboard; `registration.json` excludes that exterior without modifying the raster. The Godot review tool verified source hash and native alpha export. `output/laboratory-wall-review.png` was inspected at 328-unit width on light/dark grounds beside existing furnishings/crew. Fine controls simplify at scale. Two existing raw-image export warnings came from the reference room; no script errors occurred. This is standalone review, not room integration or packaged acceptance.

## Next action

Owner review, then select a sealed wall and validate actual placement, clearance and any required directional variants. Continue producing distinct department assets and supporting props. Do not put this continuous bank across a doorway or treat it as an installed room.
