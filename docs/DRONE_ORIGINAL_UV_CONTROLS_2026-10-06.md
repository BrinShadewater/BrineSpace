# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: drone original-coordinate sampling controls

## Objective and acceptance

Reduce giant drone transition uploads without changing selected animation pixels, effective filtering, timing, scale, roots or ordering. Full release requirements remain open.

## Accepted decisions and constraints

Private probes only; normal source unchanged. Do not admit direct cropping or manual nearest pixel lookup on the current evidence. Prior palette nearest success does not establish indexed linear equivalence: its linear lane explicitly falls back to original RGBA.

## Current state

output/drone-original-uv-2026-10-06/probe.gd draws the original full texture/source rectangle to preserve renderer vertex UVs, then samples an exact cropped frame in a custom shader. sampler-control/probe.gd instead samples the original full texture itself: normal texture sampling for linear; manual floor(UV*original_size)/texelFetch for nearest. Full textures remain allocated in these controls; no memory/performance benefit claimed.

## Verification

Frame-backed original-coordinate shader:144pairs/45mismatches, same rejection count as direct cropping. Same-sheet sampler control:144pairs/10mismatches, all nearest at .613 scale; all72linear comparisons exact, all synthetic nearest exact. Thus even unchanged texture dimensions/source UVs do not make manual nearest selection equivalent to the actual renderer/hardware sampling. This isolates manual nearest selection as an insufficient substitute; it does not prove the specific hardware quantization algorithm. Linear cropped remapping remains independently nonexact. Both runs expected exit1 for rejected raster cases, no engine errors, owner2936 non-log files unchanged, terminal.

Primary engine source inspected: Godot4.7.2 GLES canvas vertex computes normalized region corners then interpolates; fragment clamps region UVs by half a texel and samples the texture. Sources:
https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/shaders/canvas.glsl
https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_canvas_gles3.cpp

## Next action

Test full-coordinate lossless indexed storage on the actual mining West sheet, extending the existing nearest hardware-sampled palette prototype rather than assuming South covers the stall. Measure encoded upload cost and exact nearest raster output. Preserve original RGBA for effective linear filtering until an exact alternative is verified, account for fallback retention and duplicate caches, and reject the approach if its upload/memory tradeoffs do not improve matched active transitions. Full-sheet indexed upload may still stall; report that measurement explicitly before normal admission. Runtime PNG compatibility, worker decode/encoding cost, session ownership and other headings remain required.
