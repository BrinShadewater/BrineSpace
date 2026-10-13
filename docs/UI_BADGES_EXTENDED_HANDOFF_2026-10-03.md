# Extended badge handoff

Updated: 2026-10-03 · Project: BrineSpace · Task: Continue badge auditions

## Objective and acceptance
Additional matching badges for visual review, covering room conditions, signed resource flow, crew vitals, navigation counts and station totals.

## Accepted decisions and constraints
Preserve the existing matte petrol badge styling, original icon artwork, 28/36px sizes and muted rims. Samples use caller-supplied state; no gameplay or unlock changes. Live screens remain unchanged.

## Current state
scripts/ui_badges.gd adds readout, flow and vital factories. Values retain their signs/units and do not inherit the 99+ notification count cap; percentages clamp to 0–100.
tools/audition_ui_badges_extended.gd (+ UID) reuses the first audition harness and shows six families, including 320px wrapped context badges.
Preview: output/ui-badges-2026-10-03/badges-audition.png.

## Verification
Godot 4.7.2 native: 74 checks, zero failures/errors, exit 0. Checks include loaded icons, content fit, intended height, compact wrapping, signed/zero/large resource values and percentage bounds. Native 1440x1000 preview visually reviewed. Scratch APPDATA; all 2,931 owner non-log files unchanged. Evidence: output/ui-integration-2026-09-30/ui-badges-extended.log and matching -verification.json. UID creation also isolated and clean.

## Next action
Owner visual review pending; integrate accepted badges into live screens when requested, using actual game state.
