# Project handoff

Updated: September 29, 2026 · Project: BrineSpace · Task: install large rooms in main project

## Objective and acceptance

Make Hydroponics Farm, Storage Depot, Moonbay and Tidal Power Plant available in the main checkout's Layout Editor and normal game runs.

## Accepted decisions and constraints

Four 2×2 rooms, fixed large equipment, four station ports, muted department colors. One rare large-room card per run; first introductions follow the chosen order, subsequent runs randomize. Normal runs retain room costs and placement/resource rules. Moonbay and Tidal require an ocean face. Owner Studio layouts and ongoing character/UI edits are preserved.

## Current state

Installed the completed large-room branch into `C:/Users/Alex/Documents/Brine Space`, merging overlapping working edits instead of replacing them. The branch includes the latest committed main UI work. Large-room picker entries, per-rotation prop editing/saving, live overlays/navigation, room cards, multi-cell construction, rare drafting and Moonbay crew missions are integrated. Large-room Studio authoring currently supports props; character/floor/wall/light/effect authoring remains unavailable. Installation backups are in the worktree's `output/large-room-install/backup`.

## Verification

Main-checkout tests: six headless large-room checks, three Moonbay checks and the native large-room Studio check all pass. Native main-checkout station review captured 16 rotations with zero errors or warnings; Storage Depot's assembled native view was inspected after installation. Prior full rotation visual review remains recorded in the polish handoff. All Godot launches used scratch APPDATA. Real progression/checkpoint/layout hashes stayed unchanged; `last_session.json` changed while a separate main-checkout game session was running, so the full real-folder fingerprint did not match. No real profile files were restored or edited.

## Next action

Restart the running game or reopen Layout Editor to load the installed code. Owner visual and hands-on acceptance remain open. No export or upload was requested.
