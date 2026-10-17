# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: Drone fixed-surface polish

## Objective and acceptance
Polish perspective/material consistency after the visual audit, retaining the
accepted design, cyan, arms, dimensions, pixel sampling and all animation behavior.
Agent visual review is separate from owner acceptance.

## Accepted decisions and constraints
Eight travel headings; four work actions in N/E/S/W; inward-curving NW tool;
0.34 world units/library pixel, 256px frames, 30fps. World footprint remains
provisional. No role, room, save, navigation or runtime integration changes.

## Current state
Imagegen v2 supplies matte painted panel/casing surfaces with subtle wear.
V1 was rejected for gloss. Existing outlines and geometry remain; east/west
sidewall shading is refined but this is not a physically reprojected camera pass.
Generated pixels are registered, masked and composited only where pixels remain
stationary throughout the original motion. Moving limbs, fans, cargo and effects
remain original. All originals are preserved. Current manifest points to polished
body frames/atlases. Baseline manifest is manifest-before-polish.json.

Changed scripts: ../polish_prepare.py, ../polish_grid.py (diagnostic),
../build_surface_polish.py, ../apply_surface_polish.py, ../build_cardinal_review.py.
Updated ../manifest.json, ../index.html, ../README.md and generated review boards.
Art: heading-polish-v2.png; derivatives under poses/, frames/, atlases/, masks/.
Comparison: surface-polish-comparison.png; all-polished-poses.png.

## Verification
See validation.json for full alpha/outside-mask equality counts and registrations.
Pack geometry/atlas parity and job transition checks are recorded in ../review/.
Final browser and visual check results are recorded after the build completes.

## Next action
Owner review in the existing localhost:8767 preview. Actual current-pack scale
beside crew and room props remains a separate native-scene review; no gameplay
scale acceptance is claimed. Rebuild steps are in ../README.md.

Final verification: 6,084 body frames preserve alpha and pixels outside fixed masks; 48 clips pass pack validation (288 atlas parity samples), all 16 complete jobs pass continuity/transfer checks. Timeline/cargo/effect/status metadata unchanged. All 24 final poses and light/dark comparisons reviewed. Browser samples cover all four actions across the four cardinals; no console errors. See final-checks.json and browser-preview.png. Vents/lenses/contrasting seams/cyan fittings are protected in both source and target; this makes the final finish change deliberately subtle. Owner review pending.
