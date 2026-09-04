# BrineSpace

BrineSpace is a Godot 4 passive roguelite space-station builder prototype. You play BRINE, a damaged AI core rebuilding a dead orbital station through blueprint drafting, modular room placement, passive production, orbital events, and discovered adjacency synergies.

> **BRINE // ORBITAL CORE V0.1**
>
> *"The station is quiet. That does not mean it is empty."* 🛰️

## Status

BrineSpace is actively prototyping its foundational loop. It is playable, deliberately imperfect, and built for discovering which placement decisions become satisfying before the systems grow teeth.

- **Playable now:** doctrine selection, finite blueprint decks, rerolls, modular placement, passive production, room-door connectivity, stackable synergies, placement cascades, Resonance tiers, three-stage run directives, orbital objectives, victory/failure summaries, doctrine mastery, drones, and a test crew walker.
- **In progress:** full-run balance, directive variety, room coverage, population systems, pathing polish, and clearer orbital events.
- **Not production-ready:** saves and unlocks are prototype-level, progression values are first-pass, and the current run needs broader playtesting across all doctrine pairs.

## What It Is

Each reboot begins by pairing two doctrines around a damaged core. That pair determines the run's blueprint deck and strongest combo routes. Place compatible modules, complete three escalating reconstruction directives, make the station self-sustaining, and keep enough slack in the system to survive whatever orbit throws at it. The game is meant to be thoughtful and watchable, not a frantic RTS.

BRINE occasionally has opinions about the work. They are not always comforting. 🧠

## Requirements

- Godot 4.6 or newer
- Git LFS when cloning from GitHub (`git lfs install`)

Open `project.godot` in Godot and run `res://scenes/main.tscn`.

## Prototype Loop

- Select two doctrines to compile a focused blueprint deck for the reboot. The chooser previews deck breadth, crossover rooms, available link patterns, and each doctrine's mastery bonus.
- Select one of the three blueprint cards in the bottom hand.
- Click an empty station-grid cell adjacent to an existing room to build it.
- Use `WASD` to pan; mouse wheel zooms around the cursor.
- Press `Space` to pause/resume time.
- Use the `1x`, `2x`, and `4x` controls to change simulation speed.
- Selected room cards show a rotated hologram preview before placement; press `R` to rotate it.
- Building spends the selected blueprint, moves it to the discard pile, and draws a replacement. The discard pile reshuffles when the draw pile is empty.
- Right-click a card to replace it, or use `REROLL HAND`; both consume one of the run's limited reroll charges.
- Rooms produce and consume resources each cycle.
- Connected compatible rooms form stackable links; repeated copies of a pairing each contribute their own cycle bonus.
- A placement that completes one or more new links fires an immediate resource pulse and scores a Signal Cascade. Multi-link placements score increasingly more Resonance.
- Resonance tiers award run resources, and Resonance contributes to research at the Reboot Summary.
- Each run rolls three escalating directives with visible targets, cycle deadlines, and completion rewards. Stage two asks you to develop both selected doctrines, while overlapping rooms can advance both halves of the objective. Final directives can demand station scale, Resonance, stacked links, or several distinct active patterns. Complete the final directive to stabilize the station and win.
- Discovered synergies are recorded permanently in the run/meta archive data.
- Orbital POIs periodically trigger events.
- POIs have progress, deadlines, work types, and completion rewards.
- Mining and salvage drone bays show tiny drones travelling toward the active POI marker and contribute work to matching POIs while powered.
- Resource collapse or a missed directive deadline ends the run. Victory and failure both open a Reboot Summary and persist earned research, discoveries, and eligible doctrine mastery.

## Main Files

- `scripts/room_database.gd`: data-driven room card definitions.
- `scripts/main.gd`: run state, UI, placement, resource cycles, fail/reboot flow.
- `scripts/run_manager.gd`: doctrine definitions, constrained deck construction, and staged directive pools.
- `scripts/grid_canvas.gd`: 40x40 grid rendering and click handling.
- `scripts/synergy_manager.gd`: connected-link discovery, stackable cycle bonuses, and the expanded synergy catalog.
- `scripts/orbit_manager.gd`: POI/event timer layer.
- `scripts/meta_state.gd`: persistent unlocked blueprints, research, discoveries, doctrine mastery, and victory count saved to `user://brine_save.json`.
- `rooms/`: prototype room art used by the station grid renderer.
- `character/Major_Bill/`: prototype human sprite rotations and animation frames.

## Current Scope

This is an early 2D prototype with production-ready room, character, drone, door, UI, and icon assets. The core loop is still deliberately small so drafting, placement, passive production, discovery, and reboot behavior can be iterated quickly.

Power is treated as generated capacity plus stored reserve. Surplus generation charges reserve up to the current cap. Battery Arrays add reserve capacity. Rooms with Power demand run while the station can cover them; shortages leave lower-priority powered rooms offline for the cycle. The BRINE Core is powered first, and the run fails if it cannot be powered.

Room art and card thumbnails are loaded directly from PNG files at runtime so newly added assets do not need manual import setup before the prototype can run.

Room placement uses six prototype layout archetypes based on the path guide. Each room has doors and an internal walk-path model; press `R` while placing a selected card to rotate the room before connecting it to matching adjacent doors. Door and walk-path overlays are hidden during normal play and can be toggled with `F3` for admin/debug topology inspection.

The current combo layer rewards spatial planning directly. Each concrete room-to-room link stacks, the card hand prioritizes a relevant link hint, and multi-link placements produce a short cascade banner rather than a permanent overlay over the station.

Normal play spends room costs and enforces both station-failure and directive-deadline conditions. The dedicated test harnesses can still opt into isolated free-build or failure-disabled states where needed.

Major Bill is currently a pathing test walker. He spawns at the BRINE Core and wanders through rooms only when matching doors create a connected route. He switches between idle breathing, walking, running, and short breaks to make path testing feel more alive. Cryo/cloning spawn rules will replace this test behavior later.

Run `Godot --headless --path . --script res://tests/test_synergy_manager.gd` to verify link stacking, door connectivity, cascade rewards, doctrine deck constraints, opening-hand guarantees, directive flow, and mastery persistence.

## Development Notes

The current prototype roadmap, known limitations, and immediate polish priorities live in [Development Notes](docs/DEVELOPMENT_NOTES.md). The short version: keep the station readable, make every room placement legible, and let the passive systems create interesting decisions rather than busywork.

## Repository Notes

- Raster art is stored with Git LFS to keep normal Git history lean.
- Godot import cache, local asset backups, and one-off layout audits are ignored.
- Game state saves are written to `user://brine_save.json` and are not versioned.
