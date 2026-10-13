# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: current renderer/backend attribution

## Objective and acceptance

Identify remaining renderer cost after admitted Moonbay/prop command retention. Diagnostic masks are not quality settings or gameplay optimizations. Full frame/memory/PC/Mac release gates remain open.

## Accepted decisions and constraints

Freeze simulation after the current deterministic mixed40-room warm-up and suppress only selected rendering layers. Preserve camera, Node visibility, gameplay state and original masks. Root-grid suppression uses RenderingServer RID visibility, not hiding the Control: Control hiding affects ScrollContainer layout.

## Current state

Private probes: `output/current-render-layers-2026-10-06`. Corrected accepted diagnostic under `camera-fixed/{probe.gd,results.json,summary.json,owner.json}`. Normal runtime unchanged this turn.

## Verification

Initial 30-phase probe preserved gameplay and Node visibility but missed camera changes. Visual review of restored capture showed station displaced; per-repeat inspection found baseline draw calls7606 before no-grid, then4867 afterward. Hiding Grid Control reset scroll layout. Initial combined medians/active-versus-frozen conclusion are rejected; initial results retained as failure evidence.

Corrected three repeats ×10 masks ×45 samples after10settleframes =30phases. Camera checked every sample (zoom0.06148148, scroll221/469), Node mask visibility checked every sample, full crew/drone/room snapshots unchanged after every phase, final visibility restored. All checks pass, clean terminal process, owner2,936files unchanged. Root RID visibility avoids layout side effects. Baseline/repeated baseline median rendererCPU14.991/14.963ms and calls7590/7590; active benchmark previously7345–7617calls/~15msCPU, so no large frozen-versus-active rendering gap is established.

Median measured renderer results:

| Mask | CPU ms | GPU ms | Global draw calls |
|---|---:|---:|---:|
| Baseline | 14.991 | 12.693 | 7590 |
| No live room contents | 6.803 | 4.678 | 3330 |
| No small-room floors | 13.823 | 11.331 | 7020 |
| No small-room walls | 14.339 | 11.652 | 7163 |
| No environment | 12.509 | 10.483 | 6565 |
| No foreground | 14.297 | 11.647 | 7228 |
| No doors | 14.699 | 12.358 | 7467 |
| No lights | 15.006 | 12.694 | 7563 |
| No grid renderer | 0.626 | 0.516 | 231 |

LIVE includes ordinary props and complete large-room base artwork/props (including their floors/walls/water). Groups overlap; CPU/GPU differences are not additive savings estimates. GPU power state/measurement variability remain. Current largest lead is LIVE (~8.19ms CPU/~8.02ms GPU difference,4260reportedcalls), then environment (~2.48msCPU difference); doors/lights have much smaller measured backend impact. No removed-layer appearance is accepted.

## Next action

Investigate equivalent combined indexed triangle submissions for prop bodies/contact shadows before more preparation caches. Matching Godot4.7.2 source reveals a relevant precision distinction: [RenderingServer mesh packing](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/servers/rendering/rendering_server.cpp) stores vertex color channels in8bits, and [GLES3 mesh attributes](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/storage/mesh_storage.cpp) consume normalized unsigned bytes; [GLES3 polygon buffers](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_canvas_gles3.cpp) retain float vertex colors. This is a concrete precision difference and a plausible cause of earlier combined-mesh shadow mismatches, not yet a reproduced causal proof. Direct indexed polygon/triangle submission may preserve original alpha precision while reducing commands; test exact raster/texture/filter/material/ordering and actual batch counts before admission. Do not revive previously rejected mesh representation unchanged or promise an8ms gain from masks.
