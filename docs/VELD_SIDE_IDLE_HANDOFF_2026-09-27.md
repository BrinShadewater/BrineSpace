# Veld side idle handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner accepted the new side masters as much better, then requested continuation.
Build subtle idle before walk/action, preserving the approved foundation.

## Accepted decisions and constraints
Approved side-master-01.png is the only new-motion image reference. Independent
east and west, correct asymmetric gear; no mirroring or palette patching.

## Current state
character/veld-side-idle-v1: 12 authored frames, two six-frame idle clips, 184px
canvas/148px standing, 1720ms cycle. Built-in image_gen sources/prompts preserved.
Extraction uses alpha128 components and head registration; stationary source
height normalized per frame. Colours untouched. idle-review.gif compares master
and candidate at enlarged/gameplay scale. Manifest and local rebuild included.

## Verification
Both sheets have actual alpha and six isolated bodies. Manifest validator clean.
Inspected source sheets, equal-scale comparison and all-frame contact sheet.
motion-audit.json records unique frames/changed pixels, not smoothness acceptance.
No native playback or room occlusion test in this standalone draft; runtime/profile
untouched. Some generated face/contour variation remains for animated review.

## Next action
Review idle loops against approved masters; correct visible drift if reported.
Then build east/west walk and inspection from the same foundation. Earlier v12
motion remains preserved, not a new design authority. Other cast follows Veld.
