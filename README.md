# BrineSpace

BrineSpace is a Godot 4 passive roguelite space-station builder prototype. You play BRINE, a damaged AI core rebuilding a dead orbital station through blueprint drafting, modular room placement, passive production, orbital events, and discovered adjacency synergies.

> **BRINE // ORBITAL CORE V0.1**
>
> *"The station is quiet. That does not mean it is empty."* 🛰️

## Status

BrineSpace is actively prototyping its foundational loop. It is playable, deliberately imperfect, and built for discovering which placement decisions become satisfying before the systems grow teeth.

- **Playable now:** 30 room blueprints, 25 discoverable patterns, three-cycle blueprint decryption, current-run prototypes, a spoiler-safe discovery journal, room-local functioning effects, room suspension, doctrine decks, cascades, directives, orbital objectives, mastery, and optional post-victory expeditions.
- **In progress:** full-run balance, directive variety, room coverage, population systems, pathing polish, and clearer orbital events.
- **Not production-ready:** saves and unlocks are prototype-level, progression values are first-pass, and the current run needs broader playtesting across all doctrine pairs.

## What It Is

Each reboot begins by pairing two doctrines around a damaged core. That pair determines the run's blueprint deck and strongest combo routes. Place compatible modules, complete three escalating reconstruction directives, make the station self-sustaining, and keep enough slack in the system to survive whatever orbit throws at it. The game is meant to be thoughtful and watchable, not a frantic RTS.

BRINE occasionally has opinions about the work. They are not always comforting. 🧠

## Requirements

- Godot 4.6 or newer
- Git LFS when cloning from GitHub (`git lfs install`)

Open `project.godot` in Godot and run `res://scenes/main.tscn`. On a fresh checkout, let asset import finish first (or run `Godot --headless --path . --import`).

## Prototype Loop

- A clean save starts with twelve foundational blueprints; experiments uncover the remaining room blueprints.
- Select two doctrines to compile a focused blueprint deck. The chooser previews deck breadth, crossover rooms, already-learned patterns, and mastery bonuses. Every pair includes basic food and life-support options.
- Select one of the three blueprint cards in the bottom hand.
- Click an empty station-grid cell adjacent to an existing room to build it.
- Use `WASD` to pan, `Shift + mouse wheel` to zoom, and `F` to fit the station into view.
- Press `Space` to pause/resume time.
- Use the `1x`, `2x`, and `4x` controls to change simulation speed.
- Selected room cards show a rotated hologram preview before placement; press `R` to rotate it.
- Building spends the selected blueprint, moves it to the discard pile, and draws a replacement. The discard pile reshuffles when the draw pile is empty.
- Right-click a card to replace it, or use `REROLL HAND`; both consume one of the run's limited reroll charges.
- Rooms need power and their consumable inputs to function. Input-starved rooms stop instead of spending nonexistent supplies. Click a built room to inspect or suspend it; resuming takes effect next cycle.
- Connected compatible rooms form stackable links only while both rooms function. Repeated copies each contribute their cycle bonus.
- A placement that completes one or more new links fires an immediate resource pulse and scores a Signal Cascade. Multi-link placements score increasingly more Resonance.
- Resonance tiers award run resources, and Resonance contributes to research at the Reboot Summary.
- Each run rolls three escalating directives with visible targets, cycle deadlines, and completion rewards. Stage two asks you to develop both selected doctrines, while overlapping rooms can advance both halves of the objective. Final directives can demand station scale, Resonance, stacked links, or several distinct active patterns. Complete the final directive to stabilize the station and win.
- Discover a pattern by letting it function for a cycle. Keep at least one copy functioning for three consecutive cycles to stabilize it; losing all functioning copies resets unfinished progress, not the discovery.
- Stabilization permanently unlocks a blueprint and places one prototype on top of this run's draw pile, even outside the selected doctrines. Some late patterns award Research instead. Existing unlocks are preserved without duplicate prototype rewards.
- Press `J` for the discovery journal. It pauses time and shows only patterns you have actually learned, their current status, and their rewards. Hidden recipes, partners, and rewards stay hidden.
- Six motion profiles give learned functioning links distinctive doorway pulses and room effects. Dormant links become quiet; first discoveries briefly flash across the participating rooms.
- Orbital POIs periodically trigger events.
- POIs have progress, deadlines, work types, and completion rewards.
- Mining and salvage drone bays show tiny drones travelling toward the active POI marker and contribute work to matching POIs while powered.
- Resource collapse or a missed directive deadline ends the run. Victory and failure both open a Reboot Summary and persist earned research, discoveries, and eligible doctrine mastery.
- After victory, choose **Continue Expedition** to keep the station and its experiments without directive deadlines. Survival systems remain active. **Menu → Conclude Expedition** banks further earned research without repeating victory or mastery rewards.

## Main Files

- `scripts/room_database.gd`: data-driven room card definitions.
- `scripts/main.gd`: run state, UI, placement, resource cycles, fail/reboot flow.
- `scripts/run_manager.gd`: doctrine definitions, constrained deck construction, and staged directive pools.
- `scripts/grid_canvas.gd`: 40x40 grid rendering and click handling.
- `scripts/synergy_manager.gd`: connected-link discovery, stackable cycle bonuses, and the expanded synergy catalog.
- `scripts/discovery_manager.gd`: functioning-link filtering, stabilization transitions, and unlock-graph validation.
- `scripts/orbit_manager.gd`: POI/event timer layer.
- `scripts/meta_state.gd`: persistent unlocked blueprints, research, discoveries, doctrine mastery, and victory count saved to `user://brine_save.json`.
- `rooms/`: prototype room art used by the station grid renderer.
- `character/Major_Bill/`: prototype human sprite rotations and animation frames.

## Current Scope

This is an early 2D prototype with production-ready room, character, drone, door, UI, and icon assets. The core loop is still deliberately small so drafting, placement, passive production, discovery, and reboot behavior can be iterated quickly.

Power is treated as generation plus stored reserve. Surplus charges reserve up to its cap. The BRINE Core is powered first; the run fails if it cannot be powered. A shared start-of-cycle input budget prevents two rooms spending the same Water, Biomass, or Data; outputs are available as inputs on the following cycle. HUD projections use the same operational rules, but do not reveal unlearned bonuses. Crew recovery respects two emergency core berths plus two per Crew Hab.

Room art and card thumbnails have a direct PNG fallback. Import is still required for resource icons embedded in UI text. The interface uses a scalable 1920×1080 design and opens at 1600×900 by default.

Room placement uses six prototype layout archetypes based on the path guide. Each room has doors and an internal walk-path model; press `R` while placing a selected card to rotate the room before connecting it to matching adjacent doors. Door and walk-path overlays are hidden during normal play and can be toggled with `F3` for admin/debug topology inspection.

The current combo layer rewards spatial planning directly. Each concrete room-to-room link stacks, the card hand prioritizes a relevant link hint, and multi-link placements produce a short cascade banner rather than a permanent overlay over the station.

Normal play spends room costs and enforces both station-failure and directive-deadline conditions. The dedicated test harnesses can still opt into isolated free-build or failure-disabled states where needed.

Major Bill is currently a pathing test walker. He spawns at the BRINE Core and wanders through rooms only when matching doors create a connected route. He switches between idle breathing, walking, running, and short breaks to make path testing feel more alive. Cryo/cloning spawn rules will replace this test behavior later.

## Verification

Run these scripts with `Godot --headless --path . --script res://tests/<name>.gd`:

- `test_synergy_manager`: topology, cascades, all ten doctrine-pair decks, directives and mastery.
- `test_discovery_progression`: the unlock graph, secrecy, three-cycle progression, save compatibility, prototypes and feedback order.
- `test_polish_gameplay`: water viability, input starvation, forecasts, placement, real power loss, orbit unlock guards, containment and pause effects.
- `playtest_polish`: a deterministic paid-build sequence through two blueprint discoveries, prototype reuse, suspension, modal input, responsive layout, expedition and reboot. It controls draft order and time; it is not a random full-run balance sweep.

For native screenshots, omit `--headless` and append `-- --capture-dir=<absolute-output-directory>` to `playtest_polish`. It captures gameplay, menus, 1280/1600/1920/2560 layouts, all six effect profiles, and two motion frames. Add `--viewport-width=2560` after `--` to repeat the full discovery sequence at 2560×1440. Test saves are isolated from `brine_save.json`. Check logs for `ERROR:` as well as the process exit code.

## Development Notes

The current prototype roadmap, known limitations, and immediate polish priorities live in [Development Notes](docs/DEVELOPMENT_NOTES.md). The short version: keep the station readable, make every room placement legible, and let the passive systems create interesting decisions rather than busywork.

## Repository Notes

- Raster art is stored with Git LFS to keep normal Git history lean.
- Godot import cache, local asset backups, and one-off layout audits are ignored.
- Game state saves are written to `user://brine_save.json` and are not versioned.
