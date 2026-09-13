# Project handoff

Updated: 2026-09-12 · Project: BrineSpace · Task: BRINE tube floor contact

## Objective and acceptance
Owner reported that the tube looked detached from the floor and cast odd shadows.

## Accepted decisions and constraints
Preserve ceramic tube artwork, occupant animation and placement. Correct the
renderer-owned floor contact; no generated art or gameplay changes.

## Current state
brine_core_view.gd replaces the broad offset oval with three narrow source-aligned
contact bands following the base. The chamber registration owns its contact shadow.
room_lighting.gd honors that flag so the tube does not also cast the generic
rectangular machinery shadow. Only BRINE currently sets the flag.

## Verification
Native room captures visually reviewed at 2560 width and all four rotations.
The dark rectangular projection and detached oval are removed; shade hugs the
ceramic skirt. output/brine-grounding-v9.log reports PASS: four rotations,
16 door entries/returns, 3,654 movement samples, motion/pause/hardware-off checks,
full occupant containment and three viewport sizes. Diff whitespace check passes.
Existing image-loading warnings remain. No export or card replacement.

## Next action
Owner reviewed the preview and confirmed: "That looks better." Tube floor-contact treatment accepted; retain this version. No further work requested and no export performed. Preview: output/brine-grounding-v9/size-2560.png.