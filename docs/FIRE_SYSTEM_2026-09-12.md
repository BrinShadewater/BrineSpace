# Project handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: first playable fire system

## Objective and acceptance

Implement the owner's approved first pass: machinery faults start local fires; fire grows, damages rooms and interrupts production; powered sprinklers spend stored water; floodwater extinguishes fire; crew avoid burning rooms; pause and Save/Continue preserve state. Source implementation and agent visual review complete. Owner gameplay and pacing acceptance remain pending.

## Accepted decisions and constraints

- Fire is local to a compartment in this pass. Existing room costs, failure conditions, hidden discovery and paid hull repairs remain active.
- Implementation tuning: Reactor and Biomass Digester gain 2.5% machinery heat per functioning cycle; Galley and Salvage Workshop gain 2%. At 75%, the HUD and journal warn; at 100%, ignition starts at 12% intensity. Inactive machinery cools 20% per cycle. These rates are provisional, not owner-approved balance.
- Fire grows 1.2 percentage points per simulation second, and adds hull-crack severity at intensity × 0.15 percentage points per second. Damage persists after extinction and uses the existing paid welding job.
- Armed sprinklers activate only in burning rooms. Each Water purchases five seconds for that compartment; suppression removes nine intensity points per second before growth. Unused purchased time persists across pause, power loss and saves. Emergency power requires the master switch and stored Power or a functioning generator; a burning generator cannot supply itself. Safe rooms spend no water.
- Water depth of 25% extinguishes a compartment fire. Extinction restores eligibility for normal operation; other resource and room restrictions still apply.
- Crew seek an accessible dry refuge, respect locked doors and refuse burning destinations. Companions drop their activities and retain their movement animation. Existing smoke/crew survival mechanics are unchanged; the new smoke is visual.

## Current state

- `scripts/room_fire.gd` (+UID): heat, growth, finite suppression, damage, validation, inspector, HUD warning and procedural flame/smoke rendering.
- `scripts/fire_safety.gd` (+UID), `bill_npc.gd`, `companion_npc.gd`, `crew_construction.gd`: safe routes, evacuation and work interruption; existing graph-disabled states are preserved.
- `scripts/main.gd`, `grid_canvas.gd`, `station_hardware.gd`, `hardware_panel.gd`, `station_ui_insights.gd`, `run_save.gd`: simulation, all three economy passes, controls, rendering, advice and checkpoint validation.
- `tests/test_room_fire.gd`, `tests/test_fire_gameplay.gd` (+UIDs), `tests/index.json`: focused `fire` subsystem; native fixture includes actual door travel and disk save/restore.
- Unrelated ongoing artwork, layout and documentation edits were preserved. No executable export, commit or upload in this task.

## Verification

- Checkout index and HEAD both contained 18,164 tracked paths before edits.
- Headless fire fixture: 35 checks, zero failures (`output/test-runs/20260912-015451-headless`). Covers warnings, cooling, growth, water starvation/resupply, multiple fires sharing the last Water, absent emergency power, pause, invalid clocks/save fields, timestep subdivision, escape and blocked entry.
- Native fire fixture: 25 checks, zero failures (`output/test-runs/20260912-020030-native`): disk Save/Continue, legacy checkpoint compatibility, all three economy passes, real reactor evacuation, suppression, extinction and companion work interruption. Isolated native rendering proves animation changes with simulation time and remains pixel-identical when paused. The companion transition probe observed a direction change at elapsed 0, followed by elapsed 0.1 on the next movement update; the check now waits for that observable state.
- Total: 60 focused checks, plus eight existing regression fixtures. UTF-8, paired script UIDs and scoped diff whitespace checks pass.
- Existing flood retreat, hull repair, room flooding, companion repair, companion water, crew construction and run-save fixtures passed; native eight-control hardware fixture passed including two-size bounds. Logs: `output/test-runs/20260912-014613-headless`, `20260912-015117-headless`, `20260912-015456-native`.
- Native screenshots visually inspected: `output/fire-burning.png`, `output/fire-suppression.png`, `output/fire-extinguished.png`. First blocky flame draft was refined to smaller irregular pixel flames. This is source/native evidence, not a release build test.
- Two initial native fixture failures came from the artificial station setup: an incomplete architect record and an uncleared companion wreck under the test corridor. Fixed by using the normal core awakening and relocating the fixture's unopened Josh site; no gameplay save validation was weakened.

## Next action

Play a normal expedition with the owner and tune heat buildup, warning lead time, suppression cost and damage. Fires take 40 uninterrupted functioning cycles in a Reactor/Digester or 50 in a Galley/Workshop; suspend a warned room to cool it or keep sprinklers armed and Water/Power available. Use `python tools/run_tests.py --subsystem fire` and the same command with `--native` for future changes. Rebuild a playable executable through the release workflow when requested.
