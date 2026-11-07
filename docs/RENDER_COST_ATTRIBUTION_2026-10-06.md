# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: sustained render-cost attribution

## Objective and acceptance

Continue full PC/Mac performance readiness. Identify the largest sustained rendering cost before changing commands or quality. Diagnostic omissions are attribution experiments, not shippable optimizations or release certification.

## Accepted decisions and constraints

Normal source/art unchanged. Physical private twelve-source dock-sharing control reused, without new eviction policy. Same deterministic mixed40 workload, 1080p, uncapped/VSync off, active crew/drones/production, idle1x/2x/4x. Suppress selected renderer canvas RIDs at frame_pre_draw while keeping scene-node visibility, layout, simulation, preparation and game settings intact. Scopes overlap and are not additive.

## Current state

`output/render-attribution-2026-10-06/`: native benchmark scripts, isolated runners, ten complete JSON/log/capture sets, three comparison tables and owner fingerprints. `output/prepare-render-attribution.py` records initial fixture generation. Fine station/live scripts retain actual canvas paths and pre-draw application counts. Existing full control reused for fine comparisons rather than repeatedly benchmarking unchanged work.

## Verification

Ten native lanes, three measured phases each; all processes complete, no engine/art errors, warnings or leaked-instance diagnostics. All27 intervention phase comparisons preserve recorded full crew/drone/door/light/power/zoom states. Minimum180 mask callbacks validated. All2,936 owner files unchanged in each batch. UI, station, environment and large-base captures visually inspected: intended scopes actually disappear while surrounding rendering remains. Environment mask covers retained environment passes and seabed-still, not every effect directly drawn by Grid.

At1x, observed renderer omission results:

| Omitted scope | Draw calls | Renderer CPU ms | GPU ms | Frame mean ms |
|---|---:|---:|---:|---:|
| None |6513|13.225|11.591|38.618|
| Adjacent interface canvases |6269|12.699|10.766|38.077|
| All station surface passes |1646|4.786|3.292|29.279|
| Retained environment/seabed-still |5263|10.649|9.673|35.792|
| Live station surface |3155|7.423|5.924|32.424|
| Ordinary floor passes |5943|12.199|10.441|37.450|
| Walls/doors/lights |5936|12.186|10.873|37.556|
| Ordinary retained room contents |6140|12.314|11.056|37.556|
| Large-room bases |3826|8.803|7.509|33.686|
| Large-room props |6220|12.626|11.472|37.683|

Same ordering broadly persists2x/4x. Large bases account for approximately2,687 draw calls at1x, renderer CPU difference4.42ms/GPU4.08ms; this is an omission delta from single lanes, not an achievable optimization promise. Current full p95 remains41.355/41.705/41.923ms; target16.7ms failed. Even suppressing station rendering leaves substantial simulation/preparation overhead, so a render patch alone is not proven sufficient.

Source inspection: `rooms/large-rooms/common.gd` draws repeated floors, hull segments and port art; `department_wall_material.gd` issues individual48-unit textured strips plus original shadows/caps. Large-base caching already reduces preparation but retains these GPU commands. Ordinary prop and UI work are materially smaller in this scene. No texture-count/asset-size assumption explains the measured command burden by itself.

## Next action

Prototype combined textured triangle submissions for repeated large-room floor/wall pieces, preserving original float coordinates, crops, partial tiles, UVs, colors, order and transforms. Start with native exact raster comparisons across scales/rotations/filter/flood and complete room compositions; then matched current station CPU/GPU/draw-call/frame comparison. Keep selected default quality, original PNG loading and owner layouts. Provider/lifecycle/memory loading gates, packaged nine reports, endurance and actual Windows/Mac certification remain open.
