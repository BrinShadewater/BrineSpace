# Project handoff

Updated: 2026-09-09 · Project: BrineSpace · Task: game maintenance pass

## Objective and acceptance
Fix reproducible game/UI issues, remove measured drawing overhead, and validate affected behavior in native Godot 4.6.1. This is a broad regression pass, not a claim that every possible run is bug-free.

## Accepted decisions and constraints
Preserve authored room arrangements, the restored BRINE exception, hidden discoveries, real resource costs and pause-on-dialogue. Retain the taller inspector when space permits. Work alongside existing local changes; no export, commit or personal-save edits.

## Current state
- `scripts/main.gd`: invalidate obsolete delayed camera requests; preserve camera center during resize; keep time controls visible with the guide by sizing the inspector to available space. Inspector returns to 520 design pixels without the guide.
- `scripts/flood_alerts.gd`: tolerate pre-HUD updates and defer unannounced flood escalation until gameplay resumes, retaining hysteresis and deduplication.
- `scripts/room_layout_store.gd`: use cached prop flip axes without evaluating an unused fallback that copied layout dictionaries for every draw.
- New paired tests: `test_flood_alerts.gd`, `test_prop_flip_rendering.gd`. Extended `test_navigation_badges.gd` for startup/resize camera center and guide-dependent inspector height.
- Corrected fixtures: `test_ui_workspace.gd` clears its isolated placement cell; `test_marsh_battery.gd` uses a southern route away from River's derelict; `profile_station.gd` dismisses dialogue and asserts that active samples actually run.

## Verification
18 distinct regression suites pass across gameplay, economy/discovery, save/restore, station operations/systems, loading, comms, menu, inspector/HUD, flooding, Marsh battery/recall, live layouts and prop flips. Native camera-fit and navigation checks pass; 1600x900 and 960x540 captures reviewed. Flood tests cover pause/resume, duplicate suppression and hysteresis. Prop flip captures are pixel-identical for four directions and uncached draft fallback.

A focused 4,000-call cached flip benchmark improved from 24.8–31.0 ms to 2.2–2.6 ms. Full-station samples are mixed (expanded active 25.84→25.74 ms; close active 13.97→15.33 ms), so no overall FPS claim. Native culling parity passes. Original profile samples were incorrectly paused by introductory dialogue and are explicitly superseded by `profile-active-before.json` / `profile-active-after.json`.

Two headless fixtures emitted Ogg playback shutdown resource warnings; their native equivalents finish cleanly. A later Marsh fixture failure was traced to a room overlapping River's derelict, not a damaged checkpoint; the route is corrected. Existing raw-image import warnings remain consistent with the runtime PNG loading design.

Evidence: `output/maintenance-20260909/` contains per-run logs, isolated userdata, snapshots of changed runtime files before this pass, focused diffs, profile results and native captures.

## Next action
Ready for owner playtesting in Godot. No executable rebuilt. Continue with any newly observed gameplay issue rather than another unmeasured broad refactor.
