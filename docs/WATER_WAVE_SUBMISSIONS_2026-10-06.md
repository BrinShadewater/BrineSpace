# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: water-wave rendering attribution and prototypes

## Objective and acceptance

Continue the full PC/Mac performance/release plan, preserving selected art, animation and quality. This turn measures live water-wave cost and compares two implementations; normal game code is unchanged. No release gate is certified.

## Accepted decisions and constraints

Keep original clocks, visible-cell envelope, thirteen path points, twelve segment rectangles, texture regions, filtering and tint. Use isolated profiles and fingerprint the owner folder. A promising primitive rewrite must pass actual Grid and material/layer checks before normal admission.

## Current state

Private files only: `output/water-wave-profile-2026-10-06/` and `output/water-wave-triangles-2026-10-06/`. The latter retains rejected `wave.gd`, direct-command `direct.gd`, both native probes/results, and `station/` reference/candidate fixtures and comparisons.

Measured mixed 40-room, 1080p workload after installed seabed plant changes: later 60-frame phases draw ~281–284 wave cells/frame, twelve segments each (~3,370–3,408 textured rectangles). Path preparation ~0.394–0.400 ms/frame; existing segment submission ~1.087–1.104 ms/frame. These are bounded nested CPU diagnostics with instrumentation overhead; first-phase cumulative startup data is excluded.

## Verification

- Combined world-space triangle prototype: 192 nonblank native pairs, 103 mismatches (17 nearest/current-tint, 30 nearest/white, 19 linear/current-tint, 37 linear/white). Original/candidate first mismatch captures inspected. Rejected for normal admission; no source changes. Do not attribute all mismatches to clipping without further evidence.
- Direct rectangle-command prototype: retains original transforms/rectangles/region clipping and caches current item/texture RIDs locally. All 192 exact, nonblank native pairs pass across clocks/phases/fractional scales, nearest/linear and current/white tint. No shader, source texture or segment-count change. Actual Grid material/layer/lifecycle checks remain pending.
- Native matched 40-room pair: six 60-frame idle/pan phases at 1×/2×/4×, private crew/drone providers identical in both. All recorded crew/drone/door/light/power/zoom states and texture counters match. All five later phase submission means lower by ~0.260–0.270 ms; path preparation and segment counts essentially unchanged. No render-backend submission-count reduction claimed.
- p95 reference→candidate: idle1× 41.290→43.589; pan1× 42.904→44.753; idle2× 40.752→41.729; pan2× 42.822→44.224; idle4× 46.045→46.483; pan4× 48.213→48.077 ms. Whole-frame results mixed and remain far above release targets. CPU savings alone do not establish whole-frame improvement.
- Native processes terminal, successful logs checked for engine errors. Every completed lane used verified scratch user data; all 2,936 owner non-log files unchanged. The rejected visual probe deliberately exited 1 for mismatches, with no engine errors. No normal code/test index/UID changes, export, commit or upload this turn.

API references: [CanvasItem region rectangles](https://docs.godotengine.org/en/4.6/classes/class_canvasitem.html#class-canvasitem-method-draw-texture-rect-region), [RenderingServer rectangle/transform commands](https://docs.godotengine.org/en/stable/classes/class_renderingserver.html#class-renderingserver-method-canvas-item-add-texture-rect-region). Installed native engine behavior, not documentation alone, supplies pixel evidence.

## Next action

Check direct commands through actual Grid drawing with parent transforms, materials, region bounds, fallback textures and transform restoration; accept only if those pass and the bounded preparation improvement persists. Avoid broadening a 0.27 ms saving into a universal FPS claim. Then prioritize larger steady renderer costs and private lossless crew/drone lifecycle/admission, alongside original normal memory/loading, packaged bugs, endurance and Windows/Mac release gates.
