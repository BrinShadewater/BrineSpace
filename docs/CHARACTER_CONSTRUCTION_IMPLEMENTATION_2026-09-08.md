# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: playable character-led construction

## Objective and acceptance

Owner accepted the proposed first playable version: an architect builds from an existing room with a blowtorch while the new room gradually assembles. The opening now uses the architect rather than BRINE's emergency drone.

## Accepted decisions and constraints

Normal paid placement reserves the blueprint's cost and footprint. A reachable matching connection in an existing room is required; the character stays inside the sealed station. Manual construction retains the previous ten seconds of active work, with real walking time added. One available dry, unhelmeted architect handles manual work at a time. Powered dedicated drone bays take unassigned orders and retain their six-second work duration. No resource costs, failures or discovery rules were waived.

Construction progress belongs to the paid order and survives pause, station power/door holds, builder loss and disk Save/Continue. Interrupted architects release ownership without deleting paid work. Old in-flight emergency drone orders migrate with their completed work. The room becomes operational only at completion.

## Current state

- `scripts/crew_construction.gd` plus UID: assignment, reachable sealed-side approaches, work and interruption handling. `bill_npc.gd` adds the shared welding state; `main.gd` connects crew-led opening construction and inspector feedback.
- `scripts/drone_fleet.gd`: reserved crew jobs, progress/validation, dedicated-builder exclusion and old-job migration.
- `scripts/room_construction_art.gd` plus UID: work-driven foundation, deck plates, pressure frame, destination hull and furnishing stages. `grid_canvas.gd` draws them and loads the new sprite pack. Unfinished rooms remain outside occupancy/navigation.
- `character/crew-construction-v1/`: generated sources, prompts, rebuild script, twelve directional loops / 72 PNG frames, manifests, contact sheets and GIFs. Bill's wrong-facing north/south source rows were replaced; originals retained. All raster files use existing LFS attributes.
- `scripts/room_content_canvas.gd`: authored full-wall props now use their own registered drawing instead of inherited legacy machinery passes. Native completion review exposed the mismatch; this keeps the completed machinery consistent with construction.
- `tests/test_crew_construction.gd` plus UID: paid-build/save/interruptions, dedicated/legacy jobs, three architects x four directions and native preview. `tests/test_run_save.gd` now advances the real opening crew simulation in its paid-placement setup.

Unrelated checkout edits are preserved. No commit, push, release or package rebuild.

## Verification

Godot 4.6.1: twelve actor/direction cases complete, with walking speed, clear standing positions, facing and valid snapshots checked. Focused checks cover payment, non-operational reservation, pause, power/door hold, death, malformed progress, disk save/restore, exactly-once completion, dedicated ownership and emergency-drone migration. Existing drone-fleet, crew-polish and run-save assertions pass. The normal paid-opening fixture completes both one- and two-generator setups and survives five simulated minutes with costs/failure rules enabled; this is bounded gameplay evidence, not human pacing acceptance.

All 72 frames pass the sprite skill's validator with no warnings. Native stage screenshots cover all twelve actor/direction cases. A 100-sample Bill east construction preview includes final room completion. Native visual review corrected torch distance and the cached full-wall rendering mismatch. Logs and captures are under `output/crew-construction*`, `output/construction-test_*` and `output/construction-paid-opening.log`. Earlier headless runs reported Ogg resources alive at shutdown; the native construction run is clean. Known unrelated wreck-image export warnings remain. No export acceptance is claimed.

## Next action

Final completion check: cached/direct native renders of the completed Life Support room are pixel-identical. `output/crew-construction/review.json` records the comparison; `construction-preview.gif` is the compact 100-sample native clip, with `construction-stages.jpg` as a static companion. The focused native preview rerun passes after the full-wall dispatch correction. `git diff --check` reports no whitespace errors for the changed code.

Owner playtest the opening's walk/work pacing and animation feel. The first pass uses direct walk/idle-to-weld transitions; dedicated tool-draw/holster sheets and helmet-equipped welding remain future polish. Full catalog/large-station construction traffic is outside the twelve-case fixture. The generic frame is code-rendered; final room furnishings reuse their authored art.
