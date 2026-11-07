# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: Inward-facing, quieter side-wall art

## Objective and acceptance
Owner requested that every usable face in the latest vertical artwork face the room interior, then requested slightly darker colors to reduce visual prominence.

## Accepted decisions and constraints
Revise the six newest east/west pairs, preserving room identity and selected horizontal art. Put screens, hatches, cabinet access and operating controls on the inward long edge. Retain top surfaces/skylights for the fixed cutaway view and use closed endcaps. Use slightly darker source colors and restrained glow without flattening department identity. Preserve previous sources and personal layout files.

## Current state
Six selected sheets and four rejected intermediate sheets, with exact prompts and hashes, live in assets/side-wall-inward-v2/. Twelve active side registrations under rooms/full-wall-v1/registrations now select them. First-pass registration JSON is archived under assets/side-wall-completion-v1/registrations. Registration tooling accepts an alternate output directory so candidates can be prepared before changing runtime selection. No raster rotation, stretching, manual recoloring, or gameplay changes. Raw sources are RGB; rendering excludes their exterior through vector cutouts.

## Verification
Native full-wall review passes 15 rooms, four rotations and two states including bounds/door lanes and cryo preservation: output/side-wall-inward-review.log. Twelve-variant regression passes hashes, library loading and draft compatibility: output/side-wall-inward-variants.log. Production crew routes pass all six revised rooms through all four rotations with zero assertions/errors: output/side-wall-inward-routes.log. Visually inspected source sheets and both six-room native previews: output/side-wall-inward-v2/inward-q1.png and inward-q3.png. Brightness is a perceptual source revision, not a measured uniform 15-percent multiplier. Horizontal cards stay selected; diagnostic cards are in output. No exported build.

## Next action
Owner review of the darker inward-facing views. Previously recorded personal Research furniture overlap remains a separate draft issue; personal files were not changed. No commit/export; unrelated concurrent work preserved.
