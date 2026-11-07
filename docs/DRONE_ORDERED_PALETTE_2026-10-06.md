# Project handoff

Updated: October 6, 2026 · BrineSpace · Ordered palette drone provider prototype

## Objective and acceptance
Integrate palette storage without changing complete drone drawing, filtering,
texture references or scene ownership. Whole-station performance acceptance remains.

## Accepted decisions and constraints
Normal game/art/settings untouched. One selected South mining body only; original
RGBA fallback for linear, unknown filters and unsupported materials. Scratch user
paths verified; all 2,936 owner files unchanged. No export or admission.

## Current state
Private `output/drone-coordinate-2026-10-06/ordered/` and `ordered-session/`.
Physical copy of current drone sampler changes only texture construction/accounting
and emission endpoints. Ordered reusable child slots capture every body/wheel/
cargo/effect/circle call. Palette materials cached per slot; current submersion
parameters copied, unknown shaders inherit original RGBA rendering.

Display wrapper preserves atlas dimensions, metadata, resource identity and original
`get_image` pixels; GPU indices/palette immutable. Original RGBA texture created
lazily for ordinary RID use/fallback. Cache accounting includes that extra allocation
when created (72,299,520→216,806,400 source-data bytes). Retained linear fallback is
not an admitted eviction policy and increases residency; actual budgets remain open.

Session owns bank/resources, factory uses a weak bank reference, multiple node owners
register once. Last tree exit automatically clears jobs/cache/factory and bank.
Cached command/material resources release on group exit. No permanent global bank.

## Verification
First prototype: 50 checks / 40 exact complete-drone raster pairs. Expanded:
136 checks / 120 exact pairs, zero failures/engine errors, clean exits. Actual current
sampling/draw function, unloaded/loaded cargo, five mine frames (including nonempty
effect ranges), two scales, inherited nearest/linear, dry/current flood/unknown
shader modes, fractional parent translation, nonuniform scale and tint/alpha.
Two overlapping complete groups match the original order.

Wrapper identity, dimensions, original GPU/image bytes, encoded/fallback cache
bookkeeping pass. First owner exit preserves live shared bank/wrapper identity;
last owner exit clears cache/jobs/factory automatically. Weak display/index/palette/
RGBA fallback/bank references all die after observable frames. Owner unchanged.

Two private preparation type errors were corrected before evaluation; only the
verified failing probe processes were stopped. Failed logs and owner fingerprints
retained separately. Successful results in each directory's `results.json`.

These are transformed offscreen rendering/lifecycle tests, not gameplay integration,
CPU preparation, frame-time, whole-scene memory, packaged Windows or Mac acceptance.

## Next action
Integrate the provider into a physical 40-room station copy. Preserve ordering of
harvest art, construction, each drone's dust/body layers, admin lines and survey
probe: attaching all drone bodies beneath an unchanged parent would reorder these.
Bind session to actual scene lifetime; validate dock/undock, visibility, actor
removal, pause/speeds/focus and surrounding layers. Compare matched workload state,
actual upload/frame/memory counters and preparation overhead before source admission.
Linear fallback retention, sidecar PNG/manifest/hash validation, other atlases and
platform/release gates remain open. Raw test binaries are not release assets.
