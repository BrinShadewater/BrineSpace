# Project handoff

Updated: 2026-09-09 · Project: BrineSpace · Task: camera shimmer

## Objective and acceptance
Reduce the apparent room shaking during camera movement while retaining crisp art and existing controls.

## Accepted decisions and constraints
Preserve room layouts, nearest-neighbor art, zoom range, camera travel and HUD. No global filtering change, export, commit or push for this task.

## Current state
`scripts/grid_canvas.gd` aligns the world canvas translation to physical screen pixels immediately before rendering. A shared rendering-only correction moves every retained floor, wall, prop and actor layer together. Logical ScrollContainer positions remain authoritative for input and saves. The inverse transform accounts for fractional window scaling.

Added paired `tests/test_camera_pixel_stability.gd` / `.uid`. The native test compares translated BRINE crops, unchanged HUD pixels and logical input positions across four window sizes, two zooms and horizontal/vertical/diagonal/reverse pans.

## Verification
Reproduced at 1600x900: stationary art in a 270x240 crop changed up to 43,363 pixels during a tiny pan after integer translation compensation. The final correction reduces this to at most 98 in the same captures. The final 64-case regression passes at 960x540, 1280x720, 1600x900 and 1920x1080; maximum changed fraction 0.001302 (0.13%), below the 0.5% tolerance for edge rounding. Native navigation/fit checks pass. Final still visually reviewed for sharpness.

Evidence: `output/camera-shimmer/` contains before/after captures (`before-*` and final `affine-*`), diagnostics and regression.json. Intermediate `after`, `biased`, `trace` and `phase` captures are superseded experiments. Test logs are under `output/maintenance-20260909/`, with final pixel regression `test_camera_pixel_stability-native-1788985750869351300.log`.

The broad UI fixture reports missing decoration route hosts thermal_pumps and thermal_service_table in the Solar Array blueprint hologram. Isolated follow-ups both with alignment disconnected and with the final correction pass without these errors. The earlier intermittent report remains recorded rather than attributed to a confirmed cause; no all-rendering-clean claim. Continuous zoom resampling and low-framerate judder are outside this correction.

Implementation reference: Godot Transform2D documentation specifies affine_inverse for scaled bases: https://docs.godotengine.org/en/stable/classes/class_transform2d.html#class-transform2d-method-affine-inverse.

## Next action
Owner review of panning in the source project. No executable rebuilt. If the intermittent blueprint-decoration assertion returns, investigate its shared preview/layout state separately. Final isolated UI workspace run passes: test_ui_workspace-native-1788985938383575800.log.
