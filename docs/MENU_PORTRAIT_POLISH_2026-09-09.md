# Menu, portrait and comms handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: Continue portrait, wider dialogue, simpler menu

## Objective and acceptance
Improve the Continue Loop portrait, give dialogue more horizontal text space, and simplify the in-game menu.

## Accepted decisions and constraints
Continue uses the existing approved 256×272 selection portrait instead of enlarging a 32×34 gameplay crop, with proportional drawing and linear filtering. Dialogue width increases from 520 to 720 design units while staying within the map. The main menu has five actions; Crew Comms moves into Help & Station. Clearer labels identify research, the building guide, desktop quit and ending/restarting a loop. Existing save/quit and pause behavior remain.

## Current state
Changed `scripts/checkpoint_preview.gd`, `scripts/crew_comms.gd`, `scripts/main.gd`, and the width bound in `tests/test_compact_comms.gd`. Existing UIDs retained. No new assets or executable.

## Verification
Four native Godot 4.6.1 fixtures pass: UI workspace, compact comms, station navigation, menu recovery. Reviewed menu, wider dialogue and Continue title captures. Evidence: `output/menu-portrait-polish` logs, `output/pause-menu-streamlined.png`, `output/compact-comms/1600.png`, `output/continue-preview-1600.png`. Headless menu recovery failed its display persistence check; the native rerun passes including display recovery and failed-save retention. Existing raw-image warnings remain.

## Next action
Owner visual review. Packaged validation remains pending if a new executable is requested.
