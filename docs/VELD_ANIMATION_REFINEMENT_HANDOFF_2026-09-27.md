# Veld animation refinement handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner found the first pilot better, but requested brightness consistency, size fixes
and walk repair. Produce a directly comparable refinement of the three pilot clips.

## Accepted decisions and constraints
V4 selected design and palette targets remain authoritative. Preserve v1, source
provenance and runtime libraries. Deterministic exposure/registration is authorized;
new limb artwork uses image generation. No runtime promotion is implied by review.

## Current state
`character/veld-animation-pilot-v2/` contains 18 frames, reproducible builders,
material exposure matching, original/revised sources and prompts, manifests,
animated comparisons, contact sheet and browser proof. Idle and inspection are
148px throughout (inspection previously 144-153). Head-band registration removes
arm-dependent horizontal alignment. Walk uses a constant clip scale and retains
144-149px pose height. Opposing leg passes and arm counter-swing were repaired;
the first eight-frame candidate failed leg alternation and is retained as rejected.
Final six-frame source is the targeted arm correction after leg correction.

## Verification
Geometry/alpha validator: 18 frames, zero errors/warnings. Contact sheets and
browser playback checked at enlarged and approximate 45px station scale. Same-mask
source median luminance spread on a 0-255 scale: skin 35.47 -> 3.86, blue 28.26 ->
0.92, graphite 20.00 -> 0.79. These measure exposure consistency, not exact palette
compliance or native foot contact. PNG LFS attribute verified. No Godot execution,
runtime edits or access to the player's save folder.

## Next action
Review the revised stride in native motion, especially lifted-knee height, slight
shoulder-angle variation and heel contact. Preserve the source's gait bob instead
of forcing every walk bounding box to 148px. Exact semantic palette/hue enforcement
against v4 remains separate from this luminance correction. Pilot is not installed;
full-direction, helmet and other-character expansion follows representative quality.
