# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: remaining large-room rendering bottleneck

## Objective and acceptance

Identify a larger measured remedy for the remaining PC/Mac frame-time gap, preserving exact selected visuals, animation and ordering. No release acceptance in this diagnostic.

## Accepted decisions and constraints

Normal stationary-water geometry cache remains accepted. Do not reduce caustic detail, antialiasing or default quality. Native command retention must preserve floors → water → submarine → walls/windows → doors/beacons, including the separately tiled wet threshold. A child drawn after the entire parent would change this order.

## Current state

Two private physical mixed-40-room diagnostic fixtures explicitly preload instrumented copies of the current Moonbay renderer. Runtime normal code unchanged this turn. Fixtures use existing private crew/drone substitutions, 12 multi-cell rooms, including three Moonbays; native idle 1/2/4x, 30 measured frames each. They are attribution probes, not release benchmarks.

## Verification

First stage attribution, sums across three bays: foundation ~0.584–0.599 ms/frame; water+threshold ~3.566–3.759 ms; submarine ~0.073–0.082 ms; walls/windows ~1.027–1.058 ms; doors/beacons ~1.011–1.053 ms. Overall live rooms ~16.87–17.68 ms.

Second probe times native calls inside stationary cached-water replay. Per frame: 477 `draw_polyline` calls, six polygons, 48 rectangles. Polyline calls alone ~3.558–3.576 ms; polygons ~0.035 ms; rectangles ~0.017–0.019 ms. Counts are CPU submissions, not GPU draw calls. Fields named `setup_moon_count_*` contain counts despite being stored in the profiling map. Added per-command clocks/dictionary updates increase water-stage overhead to ~4.11–4.13 ms; do not compare that total with uninstrumented frame timing or claim an FPS gain. Findings isolate native CPU submission work; no direct GPU or internal tessellation timing was collected.

Both runs completed cleanly; each owner's 2,936 non-log files unchanged. Evidence: `output/moonbay-parts-2026-10-06/{results.json,owner.json,probe.log,station}` and `output/moonbay-command-cost-2026-10-06/{results.json,owner.json,probe.log,station}`. Prior accepted geometry reuse still has its separate 481-check/239-raster normal-source validation.

## Next action

Prototype ordered retained command layers for stationary Moonbay water, avoiding repeated native submissions. Because water is interleaved with floor/sub/wall/door commands, use explicit ordered segments or a correctly keyed retained complete base, not an overlay appended above doors. Cover all rotations, pan/zoom, inherited transforms/materials, Reduced Motion, idle/active mission clocks, pumping/fill/drain, sub damage/presence, gates, flooding, helmet visibility, placement/removal/replacement and scene exit. Then compare an explicitly verified executing candidate against the mixed-station baseline. Relevant potential is ~3.56 ms of measured CPU submission cost; no saving is established yet. Large-room Studio props (~4.3 ms combined in prior attribution) remain another major target.
