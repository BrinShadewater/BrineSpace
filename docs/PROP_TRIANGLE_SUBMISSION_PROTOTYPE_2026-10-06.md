# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: combine equivalent prop body/shadow submissions

## Objective and acceptance

Reduce renderer submissions while preserving exact pixels, texture identity/filtering, shadow order and materials. Private prototype only; no normal-source admission or release certification.

## Accepted decisions and constraints

Combine ordered shadow/body polygon triangles for each eligible existing library_base slot into one RenderingServer indexed triangle command. Use original transformed points/UVs, original triangulation order and float colors. Cache arrays on existing slot, replace on artwork change, no global resource table. Keep Texture2D references through slot artwork; no new image upload/atlas/engine change. Live effects remain separate and ordered.

## Current state

Private helper `output/prop-triangle-submission-2026-10-06/triangles.gd`; synthetic/actual-art/native station fixtures and evidence in same folder. Physical candidate explicitly preloads custom content renderer for ordinary and large rooms. Normal scripts/tests/settings/art unchanged this turn.

## Verification

Synthetic native96/96 exact raster pairs pass, including all shadow cases previously failed by combined ArrayMesh. Expanded native160/160 exact pairs includes eight current source sheets (crew-cinema2–5/fitness1–4), two filters/scales and flooding material; partial alpha, overlapping concave polygons, mirror/floor classification and inherited affine modulation covered. This is a limited artwork sample, not full room/Studio/lifecycle or all prop acceptance. First runner expected wrong result filename despite successful native96pairs; recovered actual context.json and corrected runner without repeating that test.

Matched native mixed40-room 1080p six idle/pan1/2/4x phases,60samples each: actual candidate execution40canvases,149→157geometry holders/builds,251→266base callbacks. RendererCPU consistently lower (~0.8–1.1ms/frame; exact rows in station/renderer-comparison.json), global reportedcalls lower~427eachphase. GPU means lower, with normal GPU power/history variability. Callback work mostly retained already; this primarily changes backend submission count. Whole-frame p95 improves5/6 phases (4xidle64.073→64.461ms regresses), stillfailsreleasegates. Do not claim universalFPSgain or savings equivalent to fullLIVE removal.

Full actual crew/drone/door/light/power/zoom state comparisons pass. Both180simulationwarmframes; candidate had extra rendering/setup callbacks but no snapshot mismatch. Texture counters match first3/final phases and differby~61.25MiB withopposite intermediate signs, causeunassigned/no memoryclaim; final3036.131MiB. Private compressed crew/drone anddebug=true fixtures, notpackagedrelease/minimumhardware. All successful processes clean andterminal; each2,936ownerfiles unchanged.

## Next action

Verify full actual room/LIVE composition, dynamic artwork invalidation, hidden/deleted/replaced slots, effective inherited filters/materials and scene-owner release. Add permanent normal tests only after admission decision; repeat matched performance when integration changes justify it. Engine source precision distinction remains a supported mechanism, not exclusive causal proof: [mesh packing](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/servers/rendering/rendering_server.cpp) uses8bit colors while [GLES polygon buffers](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_canvas_gles3.cpp) usefloat colors. Public indexed triangle API follows [Godot4.7.2 RenderingServer definition](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/doc/classes/RenderingServer.xml). Preserve default selected quality and full PC/Mac frame/memory/loading/bug/endurance gates.
