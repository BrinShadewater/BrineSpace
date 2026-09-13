# Project handoff

Updated: 2026-09-12 · Project: BrineSpace · Task: BRINE floating-tank polish

## Objective and acceptance
Higher-resolution BRINE followed by an owner-requested presentation polish pass.

## Accepted decisions and constraints
Preserve BRINE identity, size, tank placement and glass occlusion. Source pixels
remain unchanged; polish is renderer-native. No gameplay change or export.

## Current state
brine_core_view.gd samples the detailed cleaned source, adds one-degree sway on a
13-second period, lifts occupant contrast, and fades the sparse bubble in/out.
Eight-second vertical float remains. README and manifest describe the current
source. test_brine_room_v2.gd checks the rotated quad and actual hardware shutdown.

## Verification
output/brine-polish-v8.log: PASS, four rotations, 16 door entries/returns,
3,654 movement samples, 880 full-quad containment samples, sparse bubbles,
visible motion, pause equality, hardware-off equality and three viewport sizes.
Native 2560 room and separated motion poses visually inspected. Diff whitespace
check passed. Existing image-loading warnings remain in the native log.
The earlier offline failure came from toggling room power while the startup core
uses hardware power. Historical furniture count/bounds assertions were replaced
with chamber/pod checks; wall-library mounting belongs to its dedicated fixtures.

## Next action
Owner aesthetic review. No export or card replacement performed.
Preview: output/brine-polish-v8/size-2560.png.