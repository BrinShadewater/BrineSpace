# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: retained large-base sequence and repeatability

## Objective and acceptance

Verify actual retained canvas transitions and repeat measured benefit before normal admission. Preserve selected pixels, correct state invalidation, bounded memory and gameplay. Entire original PC/Mac release scope remains active.

## Accepted decisions and constraints

Do not waive an unexplained texture mismatch, change quality/filtering, or equate fewer script draw callbacks with an overall FPS gain. Keep earlier raw reports and failed postprocessing. No normal source/art/backend admission or publication.

## Current state

Native sequence `output/large-local-retention-2026-10-07/sequence.gd`, runner `output/compressed-crew-2026-10-06/run-large-local-sequence.py`; results/owner/log under trial directory. It instantiates the actual original/candidate inner StaticBase classes with real farm/depot renderers, comparing their viewport output throughout sequential transforms and invalidations. Two further gameplay pairs use the same physical private inputs/benchmark; runner `repeat-large-local-retention.py`, reports/logs/PNG/hashes under trial `repeats/`.

## Verification

- Native348 checks/0failures;176 pixel-exact retained sequence comparisons. Both rooms/filters;32 fractional transforms plus ignored machine_clock reuse a single candidate draw, then8 rotation/water/wall/partial-door changes each redraw. Layout revision/reduced-motion changes redraw; nonsquare fallback and return to square exact. Each room/filter original44 versus candidate13 draws. Complements prior640 isolated transform comparisons; not Retina or all motion certification.
- Three current-source native1080p40-room pairs, idle/pan/zoom1/2/4×,60 measured frames/phase; second order reversed. All27 entire recorded crew snapshots/drone dictionaries/door/light entries/zoom/power/phase states equal. Every process clean, no missing art/warnings/leaked instances; source inputs recorded, normal unchanged.
- All9 zoom base callback comparisons lower. Median1/2/4×1.404→1.208 /2.357→2.020 /2.719→2.264ms. Whole-frame p95 mixed: zoom medians51.292→49.397 /75.405→72.244 /64.716→59.210ms; idle4×48.719→52.160 and pan4×53.638→55.975ms worsen. No60FPS or no-regression acceptance. One control4× zoom max104.846ms remains a stall to investigate; action-only timings do not identify its cause.
- Strict repeat-summary exits1 for **one texture endpoint exception**: reversed pair2 zoom2× candidate+64,225,188bytes (~61.25MiB). Other26 phase endpoints exactly equal; subsequent and final endpoints match. This is not a serialization-rounding difference. Complete named retained texture inventory was not collected, so a transient cache lifetime, additional source or framebuffer allocation remains unassigned. Do not identify a particular atlas from arithmetic alone.
- `repeats/summary-with-exception.json` honestly postprocesses existing measurements with all_texture_endpoints_equal=false and the explicit exception. The original strict assertion remains unchanged; no additional measurement rerun to hide failure. State equality and scoped CPU benefit remain supported within their separate scope.
- Owner2,936 non-log files unchanged; all processes terminal. No new test UID or normal script change. Historical pixel capture remains a final still with partial toast occlusion, not full release visual matrix.

## Next action

Collect bounded named texture/cache and framebuffer metadata at each measured phase, without GPU readback or lazy image materialization, to explain the exception. Investigate >100ms zoom stall with per-frame trace separately. Before source admission, also check mixed high-speed idle/pan results. Official [Godot4.7.2 Node2D implementation](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/scene/2d/node_2d.cpp) shows position/scale setters forwarding a transform update even for unchanged values; optional equality guards would avoid redundant calls, but this source fact does not establish the cause of either observed regression or texture exception. Avoid speculative implementation claims. Full original memory/loading/frame gates, bug/UI/motion/endurance, target PC and native Mac release certification remain open.
