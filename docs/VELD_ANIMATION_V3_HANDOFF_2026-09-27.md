# Veld lower-step and colour-ramp handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Continue improving the selected Veld design in motion, resolving the marching
passing poses and hue differences left after v2 brightness normalization.

## Accepted decisions and constraints
V4 design lock and authored palette remain authoritative. Preserve earlier pilots
and runtime libraries. Deterministic palette corrections preserve poses; artwork
changes use image generation. New candidates are not owner-approved by implication.

## Current state
`character/veld-animation-pilot-v3/` has 18 exports, a source edit lowering the
walk's two lifted knees, and skin/blue/neutral-cloth ramp mapping preserving source
luminance. It retains v2 registration and stationary 148px size fixes. Saved colour
masks exclude disconnected crown highlights; mask contact sheet records coverage.
Browser comparison places v2 left and v3 right. Builders/prompts/sources retained.

## Verification
Sprite validator: zero errors/warnings for 18 frames. Colour-transform checks:
18 cropped frames preserve alpha/bounds and luminance before integer rounding;
authored ramp anchors reproduce exactly. Source mask contact sheet and enlarged/
station-scale browser preview inspected. Whole-character semantic accuracy is not
proved by these checks; neutral masks can include glove/steel shadows.

## Next action
Audit remaining hair/ivory/steel material identity and test travel/heel contact in
native playback with scratch APPDATA before promotion. Inherited stride calibration
has not been accepted for the new gait. Then expand direction and helmet coverage.
No runtime edit, Godot probe, save access, commit or export in this refinement.
