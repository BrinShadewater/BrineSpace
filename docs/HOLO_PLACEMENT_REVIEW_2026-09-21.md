# Project handoff

Updated: September21,2026 · BrineSpace · Holographic Core placement and effects

## Objective and acceptance
Continue meaningful furnishing and animation repair, preserving owner layouts.
The full project goal remains unfinished. No Higgsfield or publication.

## Current state
Fixed rooms/full-wall-v1/holographic_core_view.gd: q0's legacy calibrator position
is now only a fallback when the merged layout has no explicit holo_calibrator key.
Extended tests/test_removed_bank_restoration.gd (existing UID retained) with Holo
explicit-placement coverage. No saved/default layout, source art or card changed.

Staged candidate-r1 in output/holo-composition-2026-09-21 restores the calibrator,
hides its old cart and small loose emitter, and enlarges the bought projector.
Do not install: native review exposes coarse projector pixels against the more
detailed calibrator, and greater scale alone does not resolve the art mismatch.

## Verification
Native regression reproduces two q0 placement failures across repeated setup before
fix; afterward four rooms/four views/two setup cycles report zero failures.
Draft four-view review passes640 walking samples; all four native stills inspected.
Calibrator operating animation changes remain within its bounds in all four views;
off and held-clock images are stable. This is not actual station-pause evidence.
Live funded isolated fixture completed52/75-percent views; native room crop reviewed.
Byte guards confirm saved layout and defaults are identical to pre-review snapshots.

The bought spa-109 projector and cyb-146b chart have no operating_screens or animation
metadata; their visible projection is baked source imagery. Restoring calibrator
motion does not fix this. Current exports predate the placement fix.

## Next action
Prepare a room-specific layered projector (retained housing, separately switched
projection) that matches native crew/material detail without enlarging coarse pixels.
Inspect source housing and projection extents before editing, preserve original pack,
and test offline/operating/held-clock behavior. Revisit layout after the main prop is
visually suitable; draft geometry acceptance is not room-art acceptance.
