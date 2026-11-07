# Galley wall and meal trolley handoff

Updated September 8, 2026. Part of ongoing wall-length asset and supporting prop production.

## Objective and constraints

Create distinct crew-space furnishings from the owner's warm fitted-interior reference. Maintain matte materials, modest equipment scale and inward controls. Standalone candidates; owner acceptance and actual placement remain pending.

## Current state

The [directional family index](family.json) now records north, south, west and east
standalone candidates, their inward faces, registrations, export hashes and reviews.
This is available art coverage, not installed or owner-accepted coverage.

`galley-wall.png` provides pantry drawers, reheater, cooking surface, preparation counter, wash basin and drink dispenser on a continuous north-wall backing. Native canvas 2006x784; intended equipment width 328 world units. The separate [meal trolley](../meal-trolley-v1/meal-trolley.png) is 1060x1484, intended width 38 units. Both folders preserve original images, exact built-in imagegen prompts, hashes, registrations and material/scale review records.

## Verification

The galley source has an opaque checkerboard; read-only exterior-neutral registration at 190 excludes it. The trolley source has true alpha. Godot source/hash/export checks pass for both, with graphical native review on dark/light grounds. The galley and trolley retain distinct equipment at intended scale. Evidence: `output/galley-wall-review.png` and `output/meal-trolley-review.png`; matching logs have no script errors. Existing reference-room raw-image packaging warnings are not asset failures or packaged acceptance.

`tools/review_registered_wall_asset.gd` now fits portrait enlarged details into the board instead of clipping them. Native previews keep their specified scale and reject excessive panel height. Both portrait and wide outputs were visually verified after this change. The skill records this distinction.

## Next action

Continue department assets and props; select actual room locations after review. The galley requires a sealed uninterrupted wall. Establish trolley floor footprint, route clearance and any directional variants during integration. Neither asset changes gameplay or current room layouts.
