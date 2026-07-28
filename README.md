# BrineSpace

BrineSpace is a Godot 4 passive roguelite space-station builder prototype. You play BRINE, a damaged AI core rebuilding a dead orbital station through blueprint drafting, modular room placement, passive production, orbital events, and discovered adjacency synergies.

> **BRINE // ORBITAL CORE V0.1**
>
> *"The station is quiet. That does not mean it is empty."* 🛰️

## Status

BrineSpace is actively prototyping its foundational loop. It is playable, deliberately imperfect, and built for discovering which placement decisions become satisfying before the systems grow teeth.

- **Playable now:** drafting, modular placement, passive production, room-door connectivity, synergies, orbital objectives, drones, and a test crew walker.
- **In progress:** balance, room coverage, pathing polish, clearer events, and the first real meta-progression hooks.
- **Not production-ready:** saves and unlocks are prototype-level, testing mode keeps building free, and failure conditions are currently disabled while systems are exercised.

## What It Is

Each reboot begins with a damaged core and a small hand of room blueprints. Place compatible modules, make the station self-sustaining, and keep enough slack in the system to survive whatever orbit throws at it. The game is meant to be thoughtful and watchable, not a frantic RTS.

BRINE occasionally has opinions about the work. They are not always comforting. 🧠

## Requirements

- Godot 4.6 or newer
- Git LFS when cloning from GitHub (`git lfs install`)

Open `project.godot` in Godot and run `res://scenes/main.tscn`.

## Prototype Loop

- Select one of the three blueprint cards in the bottom hand.
- Click an empty station-grid cell adjacent to an existing room to build it.
- Use `WASD` to pan; mouse wheel zooms around the cursor.
- Press `Space` to pause/resume time.
- Use the `1x`, `2x`, and `4x` controls to change simulation speed.
- Selected room cards show a rotated hologram preview before placement; press `R` to rotate it.
- Rooms produce and consume resources each cycle.
- Adjacent compatible rooms discover permanent synergies.
- Discovered synergies are recorded permanently in the run/meta archive data.
- Orbital POIs periodically trigger events.
- POIs have progress, deadlines, work types, and completion rewards.
- Mining and salvage drone bays show tiny drones travelling toward the active POI marker and contribute work to matching POIs while powered.
- Failure opens a Reboot Summary and preserves in-memory meta progression.

## Main Files

- `scripts/room_database.gd`: data-driven room card definitions.
- `scripts/main.gd`: run state, UI, placement, resource cycles, fail/reboot flow.
- `scripts/grid_canvas.gd`: 40x40 grid rendering and click handling.
- `scripts/synergy_manager.gd`: adjacency synergy discovery and cycle bonuses.
- `scripts/orbit_manager.gd`: POI/event timer layer.
- `scripts/meta_state.gd`: persistent unlocked blueprints, research, and discovered synergies saved to `user://brine_save.json`.
- `rooms/`: prototype room art used by the station grid renderer.
- `character/Major_Bill/`: prototype human sprite rotations and animation frames.

## Current Scope

This is an early 2D prototype with production-ready room, character, drone, door, UI, and icon assets. The core loop is still deliberately small so drafting, placement, passive production, discovery, and reboot behavior can be iterated quickly.

Power is treated as generated capacity plus stored reserve. Surplus generation charges reserve up to the current cap. Battery Arrays add reserve capacity. Rooms with Power demand run while the station can cover them; shortages leave lower-priority powered rooms offline for the cycle. The BRINE Core is powered first, and the run fails if it cannot be powered.

Room art and card thumbnails are loaded directly from PNG files at runtime so newly added assets do not need manual import setup before the prototype can run.

Room placement uses six prototype layout archetypes based on the path guide. Each room has doors and an internal walk-path model; press `R` while placing a selected card to rotate the room before connecting it to matching adjacent doors. Door and walk-path overlays are hidden during normal play and can be toggled with `F3` for admin/debug topology inspection.

Testing mode currently has free room building enabled and fail conditions disabled.

Major Bill is currently a pathing test walker. He spawns at the BRINE Core and wanders through rooms only when matching doors create a connected route. He switches between idle breathing, walking, running, and short breaks to make path testing feel more alive. Cryo/cloning spawn rules will replace this test behavior later.

## Development Notes

The current prototype roadmap, known limitations, and immediate polish priorities live in [Development Notes](docs/DEVELOPMENT_NOTES.md). The short version: keep the station readable, make every room placement legible, and let the passive systems create interesting decisions rather than busywork.

## Repository Notes

- Raster art is stored with Git LFS to keep normal Git history lean.
- Godot import cache, local asset backups, and one-off layout audits are ignored.
- Game state saves are written to `user://brine_save.json` and are not versioned.
