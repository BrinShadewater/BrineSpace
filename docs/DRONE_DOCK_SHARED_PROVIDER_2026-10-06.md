# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: private dock/exterior texture sharing

## Objective and acceptance

Continue full PC/Mac performance readiness. Remove selected-sheet ordinary/indexed duplication across actual dock and exterior consumers while preserving complete dock pixels, clocks, transforms, flooding and filter fallback. Whole-station gains must be measured separately.

## Accepted decisions and constraints

Private prototype only, original art and normal source unchanged. Retain selected quality and gameplay. Clearing the ordinary cache while normal docks still use it is not an acceptable fix. No provider admission based on isolated images or one mixed performance pair.

## Current state

`output/drone-activity-indexed-2026-10-06/provider/dock.gd` adapts the current dock's ordered primitives to the indexed group, sharing Motion with exterior drones. Group supports original arc commands. `room-content.gd` intercepts retained registered/native dock slots, keeping slot ordering, inherited material and source flip transforms; reused non-dock slots release/hide old commands. Private twelve-source Grid creates the shared session before retained content, assigns it to docks and routes zoom preparation through the private dock. Six-source control unchanged. Preparation scripts and `dock-probe.gd`, `dock-content-probe.gd`, isolated runners retained.

## Verification

- Direct dock: 480 exact native raster pairs, 1,022 checks, zero failures/errors/warnings/leaks. Docked/launching/docking, five elapsed values, cargo/no cargo, operating/stopped, nearest/linear, dry/flood, widths160/290, transformed/modulated parent; indexed and fallback paths both exercised. Owner2,936 unchanged.
- Retained content adapter: same 480 exact pairs/1,022 checks and clean native exit; provider ownership closes. Owner2,936 unchanged. Current matrix covers registered mining docks; source-native variants, flipped props, other dock types, reused-slot cleanup and full room layering still require direct acceptance.
- First station attempt emitted missing-metadata errors from `get_meta(key,null)`; rejected and exact verified test process stopped. Fixed using `has_meta` before lookup, then retained probe above passed. Rejected logs preserved in `station-results-rejected-dock-metadata`; its timings excluded.
- Corrected native matched40 comparison completed cleanly. All six full crew/drone/door/light/power/zoom states equal; no missing art, engine errors or selected-sheet ordinary duplicates in any phase. Owner2,936 unchanged. Results/logs/captures in `station-results`; twelve final screenshot inspected, not motion certification.
- Six/twelve readiness12.288/11.955s, one observation. p95: idle1 42.838/41.413; pan1 44.291/43.928; idle2 41.555/43.049; pan2 43.050/43.101; idle4 46.395/45.205; pan4 48.591/50.188ms. Frame/loading targets still fail; no consistent performance win.
- Texture endpoint differences candidate minus control: idle1 -61.04MiB; pan1 +31.04; idle2/pan2 +92.29; idle4 +61.60; pan4 -61.12. No aggregate/peak/normal-release reduction claim.
- Actual indexed cache69.14MiB plus ordinary230.32MiB during idle2; exterior reports zero fallback draws. South/West wheels and drive retained in indexed cache while ordinary unselected storage fills its own budget. Shared trim only evicts stale indexed entries; recent indexed layers plus ordinary storage can exceed combined budget. This is evidence for the next residency investigation, not attribution of every global-monitor byte.

## Next action

Inspect ordinary per-path last-use/accounting and held dock commands. Test a genuinely combined residency policy without evicting visible required layers or adding reload stalls. Complete native/flip/other-dock/reuse/full-room layering and actual save/title/Continue ownership coverage for this dock integration. Preserve normal fallback when private palette mode is disabled (current private zoom preparation requires a mode guard before broader use). Then matched memory/upload/CPU/render comparison and repeatability. Normal provider admission, sustained-render cost and all original PC/Mac release gates remain open.
