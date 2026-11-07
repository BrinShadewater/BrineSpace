# Large-station render attribution — October 19, 2026

The next optimization target is room contents and the environment, based on two controlled native rendering probes. This is diagnosis only: no game source, app package, physical save or frozen release changed; no new validation build was installed.

## Workload and isolation

Same copied 40-room/four multi-cell/52-cell fixture as the physical soak, on the Mac M4 using Godot 4.7.2 Compatibility/OpenGL-over-Metal and tablet layout at an 1180×820 window (1920×1334 design view). This synthetic station is footprint-valid, not full-port-connected organic/multi-crew acceptance. Normal game processing and its tick timer were stopped; the visual clock advanced 1/60 per process frame, with grid rendering active and pause false. Crew, simulation and camera stayed fixed. This separates render submission/compositing from simulation, but is not full gameplay or physical iPad profiling.

Both completed runner processes returned zero and asserted the real Mac profile fingerprint was unchanged using `isolated_environment`. The iPad received only a screenshot command: original cycle 64, seven-room station, paused, 4x selected. Its existing testing helper remains running. Source hashes and evidence are in [SUMMARY.json](ipad-memory-placement-evidence-2026-10-19/render-attribution/SUMMARY.json).

## Results

Each broad condition had 15 settling frames and 120 sampled process-frame intervals, repeated in reverse order. The detailed probe used 90 intervals per condition, also reversed. Uncapped native display, same process per probe; values below are medians within each condition. Native baseline drift and backend differences limit extrapolation to the iPad.

| Condition | Broad probe frame medians, ms | Median draw calls |
|---|---:|---:|
| Baseline, four brackets | 22.324–23.624 | 2800–2815 |
| Light-map overlay/render target disabled | 22.250 / 22.248 | 2796 / 2817 |
| Environment child passes transparent | 16.726 / 16.986 | 2238 / 2238 |
| Room surface/content child passes transparent | 15.143 / 15.238 | 940 / 958 |

Detailed room probe baseline brackets: **22.381–23.252 ms**, 2800–2817 calls.

| Transparent room group | Frame medians, ms | Draw-call medians |
|---|---:|---:|
| Contents | 18.972 / 19.187 | 2311 / 2329 |
| Floors | 21.505 / 21.987 | 2432 / 2450 |
| Walls | 21.842 / 22.820 | 2581 / 2599 |
| Doors | 22.799 / 22.697 | 2638 / 2659 |
| Lighting surface | 22.819 / 22.832 | 2768 / 2786 |

Alpha modulation deliberately leaves command-generation CPU work active while removing much of the group's visible render submission/compositing. It is not a proposed visual downgrade. Groups overlap structurally; timings are not additive, are not isolated GPU timings, and do not establish a guaranteed recoverable saving. Detailed CPU profiles are latest-frame snapshots, not whole-run averages. Broad texture counter stayed 1086.402 MiB because hiding retains textures; this test establishes no RAM saving.

## Lighting finding

The report's White ColorRect is 8192×8192 geometry; it is **not** an 8192×8192 allocated texture. The actual light-map SubViewport was **315×280** (one-quarter of the visible grid dimensions). Current source already schedules redraw on state changes. A fixed, lit station is an intentionally weak case for moving helmet lamps or blackout animation, so do not generalize the small light-map result to those cases.

## Rejected evidence

The initial evolving-world run encountered a discovery dialogue and became paused; its later rows are excluded. An earlier visibility-toggle version was interrupted because normal grid drawing calls `show()` on passes. The accepted probes use alpha modulation that survives those calls. Logs of rejected attempts remain outside the repository in the artifact folder.

## Next bounded work

1. Attribute room-content and environment submissions further; test batching existing textures/geometry while preserving compositing and art. Avoid a large raster cache until its memory tradeoff is measured.
2. Confirm a successful candidate on the physical iPad, including the same large fixture plus the owner's seven-room loading, Save/Continue, card return, placement and rotation.
3. Loading stalls and long-run memory growth remain separate open gates. This diagnostic run neither clears them nor changes release readiness.

[Portable evidence](ipad-memory-placement-evidence-2026-10-19/render-attribution/SUMMARY.json). Full local artifact: `/Users/Shared/BrineSpace-ipad-optimization-20261019/render-attribution`.
