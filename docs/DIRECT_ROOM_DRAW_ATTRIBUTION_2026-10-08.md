# Project handoff

Updated: October 8, 2026. Project: BrineSpace. Task: direct room draw attribution.

## Objective and acceptance
Continue full PC/Mac readiness; explain historical2advance/13draw mismatch before private candidate admission. No release/FPS/visual acceptance from diagnostics.

## Accepted decisions and constraints
Keep art, simulation, owner data and ordinary cache unchanged. Trace actual immutable release room source, not an assumed current version. Bound events4096 per room, final4xzoom only.

## Current state
Extracted large_room_canvas.gd from retained release PCK; SHA7c6c5d67b1f5b55df7d537c9963aa11b70bdd13c5386129653cea1ea8810efe5 matches current source. First helper mounted in SceneTree._init/root project and timed out40s; subprocess terminated/no engine remains. Corrected extraction follows maintained auditor: deferred run from empty project, succeeds. Private direct-room-traced.gd and run-hot-guard-direct-draw.py record direct advances/paints, process/action frame, clock, bounds, visibility, slot kind and counters. compare-direct-room.py keeps full differences on disk; initial overlong console output corrected to focused summary. Normal source/art unchanged.

## Verification
Actual40room old/fixed diagnostic pair terminal/clean, owners2936same, loader/adapter restored. No per-room event caps reached. Exact historical difference reproduced REVERSED: baseline19216advances/117544live draws, candidate19214/117531. At(16,16)Tidal:51vs50advances/1243vs1238paints. At(24,16)Storage:51vs50advances/1812vs1804paints. Other ten rooms total counts equal. Five plus eight fewer paints explain13, one fewer advance each explains2. Drawing clocks equal at matched action frames; bounds differ during zoom (e.g.frame4 Tidal size105.1253vs100.9606); atframe63 baseline paints19Tidal/27Storage, candidate no calls. Frame15/76 prepare-vs-live differences also observed. This is direct evidence of viewport-edge room work differing during zoom, not proof of changed animation timing, nor yet proof of harmless output. Broader frame/bounds differences26frames; edge room differences79 including absolute counters. Full raw events/comparison and compact summary in hot-guard-direct-draw.

Grid visible-room list uses _view_rect and _rooms_in; sync hides rooms absent from list. Camera movement waits for _prepare_zoom_art and cover groups. Next trace must distinguish readiness/cover wait versus viewport deferred state; current events cannot identify exact gating cause. Instrumented FPS not acceptance. Peaks2348.739/2411.622MiB/exits228.259 equal control/candidate. Reclaimed18 verified duplicate scratch JSON/PNG26.546MiB using hot-report-reclamation.json; primary inputs/evidence retained.

## Next action
Trace zoom wait reason/target/current scale, scroll viewport rectangle and room membership at the exact frame63 boundary; confirm bounds/clock and visual convergence while preserving async preparation. Do not fix deterministic benchmark by changing gameplay or ignoring real output. Then repeat performance evidence and integrate only justified optimizations. Full original performance, bug, endurance, PC/Mac and packaging gates remain open.
