# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: room drawing attribution and screen preparation trial

## Objective and acceptance
Continue performance improvements toward the full PC/Mac release plan. Identify drawing costs using matched station workloads; accept changes only with useful measured performance and preserved visuals/behavior.

## Accepted decisions and constraints
Muted secondary display, isolated profiles, owner fingerprints; reuse existing debug=false runtime. No large capture/runtime copies. Preserve default quality, animation pixels/timing, owner layouts/saves and source UID pairs.

## Current state
No production logic changed. Corrected private room-content probe uses the current deterministic selection/zoom/UI fixture. Private candidate precomputes fixed monitor blip positions/angles, waveform grid lines and colors, retaining identical draw APIs and animation formulas. Candidate is NOT admitted: whole-workload results effectively neutral and p99 worse. Production prepared_library_screens.gd still equals private reference.

Private scripts: output/renderdoc-tools-2026-10-08/run-live-room-paint-attribution-v2.py, verify-screen-invariants.py, run-screen-invariants-workloads.py, analyze-screen-invariants-workloads.py. Evidence under D:/bs-release-crew-cache-20261009/benchmark-input-isolation/{live-room-paint-attribution-v2,screen-invariants-trial,screen-invariants-workloads}.

## Verification
Corrected 40-room probe: 1080 frames; 12 full phase states/cameras and 54 UI snapshots exact against ordinary installed control; no missing frame records/overflow/errors. Paint category means: library live 1.506 ms/frame, props .469, prop passes .343, crew .235, library bases .094. Renderer binding/restoring only .180 ms/frame combined across categories, far below dynamic paint. Largest single labels mining ROV dock .416 ms/frame and BRINE chamber .294. Nested/diagnostic timers have overhead and do not establish whole-frame causality.

Prepared-screen private trial: 448 exact command cases / 4480 commands; 20 rendered pixel cases exact at four scales/five clocks, with command coverage of mirrored/unmirrored, negative/positive anchors, three monitor shapes, off/on and reduced motion. No capture files saved. Native Godot 4.7.2 for pixel checks; debug=false release exe for station runs.

Three alternating large-station pairs, six native runs / 6480 frames, all 36 full phase states/cameras and 162 UI snapshots exact. Mean 24.026→23.952 ms (-.307%, mixed pairs); p95 34.817→34.706, p99 46.985→48.847; >50 ms 26→27; max 87.357→83.696; no >100. Texture unchanged 3028.686 MiB. Content paint mean 2.574→2.579 ms (slightly worse), grid draw 9.933→9.886, renderer CPU 6.237→6.215, GPU 4.737→4.748. Counters overlap. Do not claim useful gain or install this trial.

All three owner guards 2938 unchanged. Jobs terminal, shared runtime override restored, logs clean. New evidence 32.35 MiB and scratch 20.81 MiB retained; C 122.52 / D 69.17 GiB free. No cleanup bypass.

Engine source checked: Godot 4.7.2 canvas_item.cpp draw_arc constructs points and calls draw_polyline; float arithmetic fidelity makes conversion a separate unverified change. This trial retains draw_arc. Source: https://github.com/godotengine/godot/blob/4.7.2-stable/scene/main/canvas_item.cpp#L816

## Next action
Investigate reducing repeated drawing commands/tessellation while preserving exact pixels, rather than more invariant scalar caching. Candidate avenue: batch independent radar sweep segments with their existing per-segment alpha, first verify engine multiline color semantics and rendered parity; do not assume equivalence. Measure actual radar counts/command reduction before another multi-run workload. Other sizeable costs include exterior actor painting and door/light setup, already with caches; avoid repeating rejected cache/provider trials. Full release performance/loading/endurance, bug/UI, hardware and Mac certification remain open.
