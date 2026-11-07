# Project handoff

Updated: October 6, 2026 · BrineSpace · Exact atlas sampling and lossless GPU palette feasibility

## Objective and acceptance
Reduce measured large drone uploads while preserving selected pixels, filtering,
dimensions, clocks and layering. This is feasibility evidence, not runtime admission.

## Accepted decisions and constraints
Normal source/assets/settings unchanged this interval. No downscaling, lossy art,
larger permanent cache or renderer upgrade. Original PNG remains unchanged (SHA-256
recorded); every native probe verifies scratch user data, owner 2,936 files unchanged.

## Current state
Private experiments: `output/drone-coordinate-2026-10-06/`.
Godot 4.7.2 source confirms normalized source rectangles using reciprocal texture
dimensions in [the Compatibility canvas renderer](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_canvas_gles3.cpp),
and per-fragment region clamping in [its canvas shader](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/shaders/canvas.glsl).
These explain relevant operations, not the exact hardware error mechanism.

Two cropped-frame attempts remain rejected: normalized-coordinate remapping fails
354/416 native pairs (146 nearest/208 linear); reciprocal-coordinate plus nearest
texelFetch fails 386/416 (178/208). Original source pixels and same-atlas controls
match. Full-size atlas with passthrough shader matches all 416 pairs, ruling out
that shader's tint/material path as sufficient to explain these mismatches.

Palette trial retains original atlas dimensions/UVs, replacing GPU RGBA8 data
with exact RG8 color IDs plus a small RGBA8 lookup texture. Selected South mining
body: 2688×13440, 11,351 distinct RGBA colors. Offline reconstruction byte-exact;
generated index data are private test outputs, not shipped assets. Linear filtering
uses unchanged original atlas, with no palette-linear benefit claim.

## Verification
Native RTX 4070 Ti / Compatibility: palette nearest 208/208 exact render pairs,
26 sampled frames covering all columns, four scales, integer/half-pixel origins,
tint/alpha. Additional 208 linear pairs exercise original fallback, all exact.
Same-atlas controls exact, clean exits/zero engine errors, owner unchanged.
This is one selected body atlas; wheels, effects, full motion and other GPUs untested.

Upload payload RGBA 144,506,880 bytes (~138 MiB) → indexed+palette 72,299,520
(~69 MiB). Separate fresh native monitor probe reports allocation deltas
192,675,644→96,398,810 bytes (~183.75→91.93 MiB), equal across three pairs.
Engine-reported texture accounting differs from source data bytes; neither is a
direct driver VRAM measurement or whole-scene memory certification.

| Pair | Original API upload ms | Indexed + palette ms |
|---|---:|---:|
| 0 | 25.898 | 6.433 |
| 1, reversed order | 14.659 | 5.998 |
| 2 | 14.021 | 6.272 |

Median API upload 14.659→6.272 ms; median paired saving 8.661 ms. Images already
prepared; decode/encoding and subsequent shader/draw work excluded. Readbacks settle
resources outside timers. No actual gameplay FPS or first-use stall claim.

## Next action
Prototype one real atlas behind a session-owned provider, preserving original
Texture2D frame/reference semantics, metadata and effective filtering. Preserve
original fallback for linear and unsupported/overlarge palettes; never downgrade
quality. Check flood/lighting/material composition, alpha/effects, all headings,
water/layering, scene release, actual cache accounting, build-manifest/PNG loading,
CPU preparation and matched full-station pacing before source admission.
Do not ship raw 72 MB test binaries or infer Mac savings. Recurring interface/CPU
cycle work is independently available; memory/frame/endurance/bug/platform gates open.
