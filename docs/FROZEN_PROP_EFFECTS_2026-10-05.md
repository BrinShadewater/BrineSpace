# Project handoff

Updated: October 5, 2026 · BrineSpace · R8 frozen library effects

## Objective and acceptance

Avoid rebuilding unchanged prop effects while preserving selected pixels,
normal animation, explicit settings, layout changes and flood materials.

## Accepted decisions and constraints

Inactive ordinary library props already retain commands. The remaining verified
gap is the split ordinary library live pass under Reduced Motion: all its
screens/effects use time zero. Retain only that proven pass. Custom, portable,
drone, aquarium and authored animation semantics remain live. No automatic
quality change, raster cache, texture eviction or art change.

## Current state

`scripts/room_content_canvas.gd` now retains frozen `library_live` commands.
Settings transitions trigger repaint on both submit and advance-only paths;
layout/state/transform/visibility invalidation still repaints. Flood material
updates continue independently. Reference switch: `--reference-frozen-prop-effects`.
New `tests/test_frozen_prop_effects.gd` and paired UID are registered in the native
performance lane. No packaged export, commit or upload.

## Verification

Godot 4.7.2 native Compatibility renderer, RTX 4070 Ti. Scratch APPDATA with copied
owner layouts; resolved user directory checked before test writes. 373 checks,
zero failures, including 204 exact retained/reference pixel comparisons across
selected life support, hydroponics and crew habitation, all four rotations.
Both settings transition paths, held updates, power, flooding/draining, moved
props, zoom/pan origin and hide/reveal covered. Wet hydroponics and animated life
support captures inspected. These are prop-pass captures, not whole-game review.

Three alternating matched pairs per room, 60 updates each, normal and Reduced
Motion: 2,160 measured frames. Under Reduced Motion reference effect drawing
medians are 74 us habitation, 124 us hydroponics, 110 us life support; retained
effect drawing is zero because no effect paint executes. Across these reduced
samples, 1,800 repeated command rebuilds disappear. Material/render work still
exists. Normal animation has identical draw counts; sampled medians are 75→74,
124→124 and 111→111 us. No full-station FPS or memory improvement claimed.

Existing split-prop retention test: 181 checks / 144 exact pixel comparisons,
zero failures. Test index parses and scoped diff check passes. Both isolated
groups preserve all 2,936 owner non-log files; no engine errors. Evidence, logs,
JSON measurements, six PNGs, source hashes and runner:
`output/frozen-prop-effects-2026-10-05/`.

## Next action

R8 is enabled within this narrow scope. Prioritize a measured full-roster memory
remedy and long-stall attribution; avoid extending retention to procedural output
without complete dependencies and matched evidence. Prior texture eviction and
worker candidates remain rejected for their recorded timing/state failures.
Texture budgets, target hardware, packaged gameplay, endurance and native Mac
certification remain release blockers. Frozen release inputs are unchanged.
