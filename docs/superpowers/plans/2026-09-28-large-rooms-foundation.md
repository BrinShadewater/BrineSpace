# Large Rooms Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add four functional 2×2 rare rooms with fixed large props, valid perimeter doors, ocean-facing placement, and one later card per run.

**Architecture:** A focused `RoomFootprint` helper describes occupied cells and perimeter ports for both 1×1 and 2×2 rooms. Existing placement, construction, navigation, environment, renderer, save, and draft call sites consume that helper. Room-specific economy stays data-driven; Moonbay missions are delivered by the companion plan.

**Tech Stack:** Godot 4.7 GDScript, existing headless/native test runner, PNG art under Git LFS.

**Spec:** `docs/superpowers/specs/2026-09-28-large-rooms-design.md`

## Global Constraints

- Preserve existing 1×1 behavior and prototype paid construction/failure rules.
- Four 2×2 rooms with exactly four reachable station doors and fixed large props.
- Farm Green, Depot Yellow, Moonbay Cyan, Tidal Power Plant Yellow.
- Moonbay and Power Plant require an open-ocean face; Moonbay has four station doors on its other three walls.
- Initial costs: Farm 16 Metal + 3 Biomass; Depot 18 Metal; Moonbay 20 Metal + 2 Rare Minerals; Power Plant 18 Metal + 3 Rare Minerals.
- First four new runs offer Farm, Depot, Moonbay, Power Plant in order; later runs choose randomly. Exactly one large-room card appears later in each run.
- Name whole quoted `res://` art paths. Keep `.gd` and `.gd.uid` paired. Never test against the owner's real `APPDATA`.

## Review Focus

- A 2×2 placement at the map edge must reject any covered cell outside the 40×40 grid (Task 2).
- A rotated large room beside a normal room must match the door at its exact perimeter cell, not merely its wall (Task 3).
- An ocean wall blocked by terrain, a deposit, or queued construction must reject placement (Task 2).
- A queued build interrupted or restored must never occupy only part of the 2×2 footprint (Task 2).
- A rerolled large card may return, but a built one must not reappear after discard recycling or Continue (Task 5).

---

### Task 1: Footprint and perimeter port model

**Files:** Create `scripts/room_footprint.gd` and `.gd.uid`; create `tests/test_room_footprint.gd` and `.gd.uid`; register the test in `tests/index.json` under `large-rooms`.

**Interfaces:** `static func cells(anchor: Vector2i, size: Vector2i) -> Array[Vector2i]`; `static func ports(room: Dictionary) -> Array[Dictionary]` where each port has `cell: Vector2i` and `side: String`; `static func exterior_cells(room: Dictionary, side: String) -> Array[Vector2i]`; `static func room_at(occupied: Dictionary, cell: Vector2i) -> Dictionary`. The room dictionary carries `size`, `pos`, `rotation`, and a `ports` list of unrotated edge segments. Default size is `Vector2i.ONE`.

- [ ] Add assertions for 1×1 compatibility, four 2×2 cells, four rotated ports, and absence of ports on internal seams.
- [ ] Run `python tools/run_tests.py --subsystem large-rooms` with scratch `APPDATA`; expect the new test to fail before implementation.
- [ ] Implement the helper and make the focused test pass.
- [ ] Commit the helper, test, UID files, and index entry.

### Task 2: Atomic placement and construction

**Files:** Modify `scripts/main.gd`, `scripts/drone_fleet.gd`, `scripts/crew_expedition.gd`; create `tests/test_large_room_placement.gd` and `.gd.uid`; register in `tests/index.json`.

**Interfaces:** Consume `RoomFootprint.cells` and `exterior_cells`. Add `func get_footprint_placement_problem(id: String, anchor: Vector2i, rotation: int) -> String`; route existing `get_placement_problem` through it. `occupied` maps every covered cell to the same room dictionary; `placed_rooms` contains one entry per room.

- [ ] Test four-cell reservation, full-footprint collision/bounds checks, open-ocean checks under rotation, blocked deposit/wreck/queued order, and no partial occupation after interrupted construction.
- [ ] Run the focused `large-rooms` subsystem with scratch `APPDATA`; expect placement assertions to fail.
- [ ] Implement atomic validation, reservation, construction completion, and occupancy; make the test pass.
- [ ] Commit placement/construction integration and tests.

### Task 3: Doors, paths, environment, and save

**Files:** Modify `scripts/main.gd`, `scripts/grid_canvas.gd`, `scripts/crew_passage.gd`, `scripts/room_flooding.gd`, `scripts/room_fire.gd`, `scripts/run_save.gd`; create `tests/test_large_room_integration.gd` and `.gd.uid`; register in `tests/index.json`.

**Interfaces:** Consume `RoomFootprint.ports` and `room_at`; add `func _ports_connect(room_a: Dictionary, room_b: Dictionary, cell_a: Vector2i, cell_b: Vector2i) -> bool` in `main.gd`. Save one anchored room, reconstruct all occupied cells after load, and default legacy rooms to 1×1. Flood/fire/power remain one state per room.

- [ ] Test exact-cell rotated door matching, crew traversal through the 2×2 interior, door water isolation, single room-wide fire/power state, and old/new Save/Continue round trips.
- [ ] Run the focused subsystem with scratch `APPDATA`; expect integration assertions to fail.
- [ ] Update connection/navigation/environment and restore paths to use footprint/ports; make the test pass.
- [ ] Commit integration and tests.

### Task 4: Four room definitions and fixed visual layouts

**Files:** Modify `scripts/room_database.gd`, `scripts/grid_canvas.gd`, `scripts/room_card_art.gd`; create four room view/layout files under `rooms/large-rooms/` with paired `.uid`; add full-path PNG art under `assets/` through Git LFS; create `tests/test_large_room_art.gd` and `.gd.uid` and register it.

**Interfaces:** Room IDs: `hydroponics_farm`, `storage_depot`, `moonbay`, `tidal_power_plant`. Add all four to `STARTING_UNLOCKS` so run one can offer the Farm. Data includes `size: Vector2i(2,2)`, `ports`, `ocean_side` for Moonbay/Plant, category, cost, production/consumption/storage, and fixed centerpiece layout. Initial economy targets: Farm produces 6 Food and 3 Oxygen for 2 Water and 3 Power per cycle; Depot adds 180 Metal, 80 Food, 80 Oxygen, and 80 Water capacity; Plant produces 14 Power while ocean intake is clear. Moonbay reserves its mission effects for the companion plan.

- [ ] Test IDs, colors, costs, four ports, fixed prop occupancy, whole art paths, and economy/intake behavior.
- [ ] Run the focused subsystem with scratch `APPDATA`; expect the new assertions to fail.
- [ ] Add definitions, rendering, card art, and fixed large props with clear routes; make tests pass.
- [ ] Inspect native screenshots for each room and rotation, including blocked/valid ocean previews; correct visual issues found.
- [ ] Commit room data, art, UIDs, and tests.

### Task 5: One rare card per run

**Files:** Modify `scripts/run_manager.gd`, `scripts/meta_state.gd`, `scripts/main.gd`, `scripts/run_save.gd`; create `tests/test_large_room_draft.gd` and `.gd.uid`; register it.

**Interfaces:** `static func large_room_for_run(run_index: int, rng: RandomNumberGenerator) -> String` in `run_manager.gd`; `MetaState.large_room_run_index: int`; `Main.large_room_selected_id: String` saved in `RunSave.FIELDS`. Increment index only when a new run starts, not on Continue. Keep the chosen card outside the opening hand and requeue it after reroll until built.

- [ ] Test ordered first four runs, random later selection from four, one late card, no duplicate, reroll return, built-card removal, and Continue preserving selection/index.
- [ ] Run the focused subsystem with scratch `APPDATA`; expect draft assertions to fail.
- [ ] Implement selection/profile persistence and draft lifecycle; make tests pass.
- [ ] Commit draft logic and tests.

### Task 6: Integrated acceptance and handoff

**Files:** Update `docs/CURRENT_STATUS.md` and `docs/LARGE_ROOMS_HANDOFF_2026-09-28.md` with actual evidence.

- [ ] Fingerprint the real save folder, run `python tools/run_tests.py --subsystem large-rooms` with scratch `APPDATA`, then confirm the real-folder fingerprint is unchanged.
- [ ] Run relevant existing placement, save, reliability, flood, fire, and paid-run tests; inspect their focused summaries.
- [ ] Review a native paid run showing one late large card, construction, crew passage, each room's function, and Save/Continue. Preserve screenshots or report paths.
- [ ] Record results and limits in the handoff and status; commit documentation.
