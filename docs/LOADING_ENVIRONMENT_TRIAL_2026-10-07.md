# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: first-draw environment preparation

## Objective and acceptance

Reduce loading handoff pauses while preserving pixels, clocks, complete interactive rooms and required crew loading. Full release performance/memory/loading/PC/Mac/bug/endurance gates remain open.

## Accepted decisions and constraints

Package `66929cd10addc5b0` unchanged. External diagnostic/prototype adapters only; no source admission. Keep default quality and normal diagnostics. Single cache-uncontrolled pairs do not certify cold/warm speed or a repeatable gain. Raw evidence and adapter hashes retained.

## Current state

Process-boundary/grid-heavy-profiler run identifies first New Game seabed preparation at 516.658 ms (518.100 ms cumulative after next frame). Derelict work rises 61.487→692.835 ms between the first and following post-draw snapshots: approximately631.348 ms additional work. Floor preparation adds238.636 ms. Those components explain much of the two handoff gaps; totals overlap containing categories and are not additive independent gains. Continue first handoff includes seabed498.510 ms, derelicts281.370 ms and terrain200.681 ms.

Early/late process-node timestamps show only116.394 ms between process callbacks in the second New Game1,161.415 ms gap and0.155 ms in Continue1,448.571 ms gap. Together with short render-signal intervals, this directs investigation toward deferred/canvas preparation outside these callback boundaries; it does not identify all engine work.

First prototype attaches a scene-ready callback, while ImagePrefetch remains active, calling existing seabed.prepare and attempting visible companion-view preparation. Seabed.prepare loads the six base sources but does not prepare the providers called by render_into; first seabed cost remains~413 ms. The attempted companion selection is empty in both cycles: the ready-time viewport is not the final drawing viewport. No claim of effective derelict preparation.

Refined prototype calls existing sync_site, then prepare on sub_biomes, fungi_biome, ocean_floor, tall_plants, giant_mushrooms, upright_kelp and ambient_water, servicing existing loading pumps between providers. No drawing calls, transformed pixels or replaced animation sources. New Game preparation496.359 ms; Continue46.310 ms; Prefetch active in both. New Game provider preparation includes sub_biomes188.079 ms, ocean_floor61.749 ms, giant_mushrooms41.029 ms, ambient_water30.071 ms; remaining time includes sync/base preparation and nested forced draws.

Compared with the process-profiler control, refined New Game first handoff899.149→412.305 ms; seabed cumulative518.100→28.478 ms. Later New Game maximum1,161.415→1,192.825 ms remains, with derelict/floor costs intact. Total New Game12,243.340→12,362.781 ms: no total loading improvement established. Continue maximum1,448.571→976.907 ms; elapsed4,973.993→4,509.238 ms, single uncontrolled pair only. Preparing resources earlier redistributes work and changes Prefetch request order; no repeatable gain or visual/memory acceptance claimed.

## Verification

Three actual debug=false two-cycle New Game/Studio/save/title/Continue runs: process profiling, base-only preparation and refined environment preparation. Each142checks/zero failures/errors/leaks/warnings. All owner fingerprints2,936 files unchanged; handles terminal. Original runtime inputs and normal checkout unchanged. Matched station adapter restored, experiment adapters preserved. Native exact visual checks and matched inventory/repeated loading comparisons remain before admission.

Evidence under output/drone-compiled-2026-10-07: packaged-loading-process, packaged-loading-art-prewarm and packaged-loading-environment-prewarm lifecycle logs/results, gaps JSON and owner fingerprints. QA fixture identities and preserved adapters reside in qa-helper.

## Next action

Identify derelict views/resources actually used after final deferred camera layout, then prepare only those while loading remains active. Attribute floor and terrain preparation as well. Build a production candidate with bounded loading preparation, actual visual and input/clock/lifecycle coverage, matched decoded/texture inventories and repeated cache-controlled loading. Keep unresolved steady rendering, memory and drone admission requirements active.
