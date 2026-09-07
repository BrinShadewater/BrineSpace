# Full-game optimization, bug and polish pass

Status: complete. Scope includes simulation, discovery, persistence, world interactions, rendering/performance, UI, and native/exported integration. Practical limits are recorded below.

## Changes

- Room lookups cache authored templates and deep-copy only the requested room. Nested caller mutations cannot alter another room or the catalog.
- Embedded room views reuse static props when rotation/layout mode is unchanged. Door edges, operation state, clocks and actors refresh per instance. Diagnostic draw timing is off by default; `--rebuild-embedded-geometry` provides a control path.
- Speed changes preserve cycle progress; keyboard panning retains fractional movement; paused menus avoid repeated blueprint drawing; HUD forecasts and styles are reused and closed journals skip rebuilding.
- Empty/incomplete checkpoint restore now rejects missing state/header fields before mutation.
- First-loop guidance explains pending drone construction and resuming time. UI/save fixtures now exercise paid reservation and completion instead of assuming instant placement.
- Full-run automation advances actual drone/cryo/crew time between economy cycles and respects obstacles/reserved cells. Discovery's explicit foundation fixture includes the authored Construction Drone Bay.
- Room route tests now exercise the live NPC collision graph. The previous fixture sampled the obsolete inactive-Bill fallback polyline; its obstruction count did not describe current crew navigation. Two-crew traffic is isolated from the independently tested third NPC.

## Performance evidence

Local Godot 4.6.1 / RTX 4070 Ti measurements, not hardware-independent guarantees:

| Measurement | Before | After | Evidence |
|---|---:|---:|---|
| 10,000 Reactor lookups | 741,993 us | 24,289 us | `output/full-lookup-before.log`, `output/full-after-test_room_lookup.log` |
| 25-room active frame, 1600x900, VSync off | 43.22 ms | 34.84 ms | `output/full-profile-stages.log`, `output/full-profile-cached.log` |

The rendering improvement is about 19%, with the same 2,515 draw calls. Main simulation callback remains about 1 ms; paused expanded frames are about 6 ms. Active expanded scenes remain below 60 FPS on this fixture. This pass does not claim a universal frame-rate target. Native small/expanded active/paused captures were inspected. Initial Performance.TIME_PROCESS readings were stale; final profiling uses direct callback timing after warmup.

## Verification matrix

| Area | Authoritative evidence |
|---|---|
| Economy, paid builds, failures, discovery and draft recovery | Final `test_synergy_manager`, `test_polish_gameplay`, `test_discovery_progression`, `test_run_balance`: exit 0, no ERROR entries |
| Drones, queued jobs, cryo, wrecks/rocks | Final `test_drone_jobs`, `test_drone_fleet`, `test_cryo_recovery`, `test_wreck_clearance`, `test_rock_clearance`: exit 0, no ERROR entries |
| Crew, death persistence, collision segments | Final `test_crew_death_save`, `test_npc_segment_clearance`, `test_branforth_crew`: exit 0; corrected two-crew `output/full-live-test_crew_polish.log`: PASS, minimum separation 20.61 |
| Every production room pair | `output/full-live-test_production_ten_walker_paths.log`: 6,400 pairs, 2,916 compatible, 67,068 collision-checked live graph segments, zero failures |
| Geometry cache and mutable data isolation | Final `test_embedded_geometry`: 140 room/rotation cases; `test_room_lookup`: mutation isolation; both exit 0 |
| Save/backup/legacy handling and invalid restore | `output/full-live-test_run_save.log`: PASS; empty/incomplete checkpoints rejected without changing resources |
| UI, keyboard, enlarged text and title/Codex | Native `output/full-final-decision.log`, `full-final-menu.log`, `full-final-title.log`: PASS; learning UI `full-current-test_learning_ui.log`: PASS |
| Full runs | `output/full-run-4404-v4.json`: ten doctrine pairs, seed 4404, two wins/eight losses, zero harness errors; normal costs/failures preserved |
| Assets and resource identity | Ten Python integration/provenance/dependency tests passed (`test_batch_two_asset_audit`, `test_composition_dependencies`, `test_sub_biome_provenance`); scanned scripts/rooms/assets/tests scripts have paired UIDs |
| Current exported executable | `output/full-game-export/BRINE.exe` and pack: `output/full-final-export-runtime.log` reports MENU RECOVERY: PASS, no ERROR entries; ran from an empty external directory, including paid reservation, in-flight save/restore, construction completion without double charge, and the new room operating for a cycle |

Final headless suite logs use `output/full-final-test_*.log/.err`. The corrected full-run policy is `curious-builder-v4-drone-time`; earlier v3 outcomes are not directly comparable. `output/full-run-4404.*` had stale harness errors and is explicitly excluded from balance evidence.

## Practical limits

This is a development pass, not a release certification or proof that no bugs remain. Balance outcomes are one seed and a limited automated policy, not human pacing evidence. Legacy inactive-walker polylines remain unsuitable for current furnishings; live crew graph routing is verified. Physical controller devices and hardware beyond the local Windows renderer were not tested. Export is local validation only; NOTICE.md still applies. No gameplay costs, failure rules, hidden recipes, stabilization requirements or progression schema were relaxed to pass tests.
