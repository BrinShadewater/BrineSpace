# Project handoff

Updated: October 6, 2026 · BrineSpace · Palette effect composition

## Objective and acceptance
Validate lossless palette rendering against selected effects before ordered gameplay
integration. Exact pixels alone do not admit the backend or certify frame pacing.

## Accepted decisions and constraints
Normal game/art/settings unchanged. Original filtering fallback retained. Isolated
native probes verify scratch paths; all 2,936 owner files unchanged.

## Current state
Private `output/drone-coordinate-2026-10-06/palette/effects/` prepares a copy of
current flood-submersion shader with palette decoding supplying its original source
color. Water equations, uniforms and world coordinates otherwise unchanged.
Fixture also uses current underwater-fog shader as a separate overlay, CanvasModulate
and an actual PointLight2D. Single South mining body/index/palette data from H28.

## Verification
192/192 exact native pixel pairs, zero engine errors, repeated original-atlas
controls exact. All 192 pairs differ from their corresponding hidden-body control:
the tests are not passing because an opaque overlay hides the art.
12 selected frames cover all six columns; two scales (0.125/0.73), integer/half
origins, tint/alpha, nearest filtering. Four cases: ambient/point light, depth 0.4,
depth 0.95 at a different clock, actual fog overlay plus point light. This proves
specific shader composition; not every effect setting, motion join or gameplay case.
Fog reduced motion/pause and effective inherited filters are still untested here.

Original generated report inherited stale seven-frame/linear scope wording.
`results-scope-corrected.json` records actual scope without replacing original log/
results. Generator wording corrected for future runs; no pixel result altered.

Source inspection: drone exterior rendering shares a canvas with other atlas layers
and circles. Assigning one palette material to that whole canvas would decode
ordinary RGBA layers incorrectly. A child only for the indexed body would reorder
it against wheels/cargo/effects/lamp; do not use that shortcut. Exterior actor pass
also contains harvest art, construction, debug lines and the survey probe.

## Next action
Build a private ordered layer provider for the complete drone draw, preserving
Texture2D identity/get_image metadata, effective filter fallback and shared session
ownership. Check mixed original/indexed layers, overlaps, inherited transforms,
cache accounting and old-resource release, then compare the actual 40-room workload.
No normal palette admission, CPU decode/loading, first-use gameplay stall, other
atlas/platform, memory-budget or packaged release acceptance yet.
