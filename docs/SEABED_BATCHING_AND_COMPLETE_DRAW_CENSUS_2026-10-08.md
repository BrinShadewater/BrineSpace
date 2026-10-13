# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: complete draw census and exact silt geometry batching

## Objective and acceptance

Continue the full performance and PC/Mac readiness plan, preserving selected pixels, animation clocks, layers and default quality. Three matched measurements per candidate; owner data isolated. No new release delivery, publication, renderer upgrade, atlas, downscaling or art mutation.

## Current state

Complete structured-command analysis of retained `station_frame253.rdc` replaces the earlier biased188-draw sample for draw-count classification. Reads372,538 capture chunks without event-by-event seeking or GPU timers. All5,096 draw commands accounted for:4,355 indexed instanced,740 array instanced,1 ordinary array.4,284 actions have one instance. Default unlit polygon/mesh program accounts for2,908 draws, all single-instance; default rectangular program1,888; primitive program109; remaining191 are other programs. Program→fragment-shader relationships verified through resource metadata. Texture-unit0 has the4×4 fallback binding on2,394 draws; this is a recorded binding, not proof every shader samples it. Capture is injected early gameplay with discovery popup, not settled FPS evidence.

Official Godot4.7.2 GLES3 source explicitly starts a new batch for each polygon or mesh; rectangles/primitives can batch under compatible texture/material/filter/clip/state. Therefore retaining polygon commands avoids script rebuilds but does not automatically merge their render submissions. First RenderDoc inspection incorrectly used `.children`; corrected to documented `NumChildren/GetChild`, failed evidence preserved. Portable tool UI configuration restored in each runner's finally; no global installation.

Private `output/renderdoc-tools-2026-10-08/silt-batch-background.gd` changes only the contiguous still-layer silt tile block: append original per-tile vertices, mirrored UVs, Geometry2D triangulation and triangle order to one native triangle-array submission. Same image/filter/tint/coordinates/layer order; no mesh-colour quantization, image conversion or permanent cache. Geometry arrays are local to still-layer rebuilds. Normal `assets/environment/seabed-v1/seabed_background.gd` remains unchanged; identified override PCKs are private.

## Verification

Native exact visual test:48 cases/zero failures/clean log. Both filters, cell sizes64.125/96, grid sizes41/44, zoom.23/1, three pan locations and fractional screen offset. Compares complete original and candidate still-layer images, including unchanged sub-biome ground, not just isolated tile interiors. Reviewed candidate screenshot. Native result/owner/profile paths under `silt-batch-native`.

Actual debug=false40-room/four-crew, idle/pan/zoom1/2/4x,180 frames each, three runs per lane. Pair2 runs candidate before control; immutable candidate PCK hashes equal between first trial and confirmation. Default quality, cap0/VSync0, focused, detailed profiler and viewport GPU timing off. All logs clean, no missing art, router released. Every compared crew/drone/door/light/power-count/zoom field equal in all27 paired phases. These are not every production/save/animation invariant.

Median per-run mean improves in9/9 phases,0.142–1.409ms (about0.45–4.10%); p95 improves6/9. Examples: idle2x34.354→32.945ms; zoom1x37.582→36.462ms. Idle1x p95 worsens34.077→35.173ms, pan2x38.611→39.671ms, idle4x45.857→46.094ms. Candidate median p9534.533–58.130ms: still fails60FPS. Maximum pairs93.961/89.335,91.855/88.777,90.064/92.631ms. No blanket stutter improvement claim. Percentiles are medians of three per-run values, not pooled percentiles.

Measured mean draw reduction approximately194.5–199.1 per frame; nominal silt tile block196→1. Dynamic scene counter differences can shift the total slightly. Texture postdraw peak2348.739303MiB and settled exit228.259212MiB exactly equal in all six runs; uploads4297 all. No memory or loading improvement claim.

Absolute large-prop counters match for the first eight phases in every pair. Final4x zoom differs in pairs1/2: control19216advances/117544live draws versus candidate19214/117531; pair3 matches. These counters include setup/warmup and visible preparation, but the cause remains unassigned. Do not dismiss this as noise, infer unchanged every-frame animation from endpoint state, or mark historical similar differences closed. Keep source admission pending a frame-by-frame clock/visibility/preparation explanation.

All owner fingerprints2936files unchanged; each actual runner restored its adapter byte-identically. All native/replay/controller/runner handles terminal. Full release/base pack, previous prototypes and source art preserved. Evidence: `batching-analysis.json`, `batching-summary.json`, `silt-batch-native`, `silt-release-trial`, `silt-release-confirmation/{identity,comparison,owner}.json`. Confirmation summary's console Unicode arrow failed under cp1252 after writing complete JSON; corrected ASCII formatting and reran analysis only, no gameplay restart.

## Next action

Instrument the final zoom workload before/after rendering with per-room machine clock, visibility and prepare/advance/draw deltas to explain the two-advance difference before normal admission. Reuse this same identified candidate and fixed workload. Then extend ordered triangle batching to measured compatible polygon groups, maintaining exact colours/geometry rather than converting native commands blindly to meshes or primitives. This small silt gain establishes a working method; thousands of remaining submissions and active preparation still dominate. Complete combined source admission/export, nine issues, save/UI/endurance/loading/stutter/memory gates and target PC/M1/signing/notarization separately; full goal remains active.

Primary implementation: [Godot4.7.2 GLES3 canvas renderer](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_canvas_gles3.cpp); [RenderDoc1.46 structured data API](https://raw.githubusercontent.com/baldurk/renderdoc/v1.46/renderdoc/api/replay/structured_data.h); [Godot RenderingServer triangle-array API](https://docs.godotengine.org/en/stable/classes/class_renderingserver.html#class-renderingserver-method-canvas-item-add-triangle-array).
