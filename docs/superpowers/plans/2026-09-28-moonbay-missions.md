# Moonbay Missions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Let assigned crew pilot Moonbay mini subs to survey, recover resources, and access deep sites, with observable launches, hazard returns, repair, and Save/Continue.

**Architecture:** A dedicated Moonbay mission state machine owns the sub and its launch chamber. Existing crew navigation, surveyed sites, resources, and inspector controls provide inputs and receive outcomes. It consumes the 2×2 Moonbay room and ocean hatch delivered by the foundation plan.

**Tech Stack:** Godot 4.7 GDScript, existing crew/site systems, headless/native tests.

**Spec:** `docs/superpowers/specs/2026-09-28-large-rooms-design.md`; prerequisite: `docs/superpowers/plans/2026-09-28-large-rooms-foundation.md` Tasks 1–5.

## Global Constraints

- Player assigns a crew member and destination; no direct steering.
- Hangar stays dry; only the sealed launch chamber floods during departure/return. Ocean hatch and station access never open together.
- Survey reveals distant sites; Recovery brings resources from surveyed sites; Deep Access reaches sites beyond diver range.
- Routine missions are slow and dependable; visibly hazardous sites may damage the sub and force early return. Damaged subs need repair before launch.
- Crew are unavailable for other station work until return. Pause, power loss, and Save/Continue preserve mission progress.
- Never run tests against the owner's real `APPDATA`; keep paired `.gd.uid` files.

## Review Focus

- Assigning a crew member already on an expedition or another job must fail with a clear reason (Task 2).
- Losing power during chamber flooding must hold a safe sealed phase and resume without opening both sides (Task 1).
- A hazardous early return must retain crew and earned cargo correctly, without double-credit after Continue (Task 1).
- A mission target removed or depleted before arrival must return safely with a clear log (Task 1).
- Saving and restoring each launch/sea/return phase must keep crew reservation and hatch state consistent (Task 3).

---

### Task 1: Mission model and outcomes

**Files:** Create `scripts/moonbay_missions.gd` and `.gd.uid`; modify `scripts/site_generator.gd`, `scripts/site_discovery.gd`, `scripts/crew_expedition.gd`, `scripts/main.gd`; create `tests/test_moonbay_missions.gd` and `.gd.uid`; register `moonbay` in `tests/index.json`.

**Interfaces:** `static func dispatch(game, room: Dictionary, crew_id: String, target: Vector2i, order: String) -> String` returns an empty success string or a player-facing rejection; `static func tick(game, delta: float) -> void`; `static func recall(game, room: Dictionary) -> bool`; `static func mission_state(room: Dictionary) -> Dictionary`. Orders are `survey`, `recover`, `deep_access`. Mission state lives on the room and carries crew, target, order, phase, progress, damage, cargo, and credited flag.

- [ ] Test generation of at least one deep-access destination beyond diver range, the three orders, routine duration, visible hazard damage/early return, absent/depleted target, single cargo credit, and repair requirement.
- [ ] Run `python tools/run_tests.py --subsystem moonbay` with scratch `APPDATA`; expect failures before implementation.
- [ ] Implement mission state transitions and site/resource outcomes; make tests pass.
- [ ] Commit state machine, site integration, and tests.

### Task 2: Crew assignment and controls

**Files:** Modify `scripts/main.gd`, `scripts/crew_work_panel.gd`, `scripts/crew_passage.gd`, `scripts/crew_expedition.gd`; create `tests/test_moonbay_assignment.gd` and `.gd.uid`; register it.

**Interfaces:** Consume `MoonbayMissions.dispatch`, `recall`, and `mission_state`. Moonbay inspector shows order, eligible crew, reachable destinations, mission progress, recall, damage, and repair cost. Crew job state reserves the assigned member from boarding through unloading.

- [ ] Test available/busy/injured crew, occupied sub, unreachable target, assignment, pause, power loss, recall, and return-to-station release.
- [ ] Run the focused `moonbay` subsystem with scratch `APPDATA`; expect assignment failures.
- [ ] Connect controls and crew movement/reservation; make tests pass.
- [ ] Commit UI/crew integration and tests.

### Task 3: Launch visuals and persistence

**Files:** Modify `scripts/grid_canvas.gd`, the Moonbay view/layout under `rooms/large-rooms/`, and `scripts/run_save.gd`; create `tests/test_moonbay_save.gd` and `.gd.uid`; register it.

**Interfaces:** Render the room's mission phase from `MoonbayMissions.mission_state`. Persist state on the Moonbay room; restore crew reservation and chamber state once, defaulting missing state to dry/idle.

- [ ] Test save/restore at approach, sealed flood, outbound, work, return, drain, and repair; assert the hatch and station entrance cannot both be open.
- [ ] Run focused `moonbay` tests with scratch `APPDATA`; expect save/visual-state failures.
- [ ] Add launch/return visuals and safe restore defaults; make tests pass.
- [ ] Inspect native departure, at-sea, early return, repair, and resumed-run visuals; correct issues found.
- [ ] Commit visuals, save integration, and tests.

### Task 4: Integrated acceptance and handoff

**Files:** Update `docs/CURRENT_STATUS.md` and `docs/LARGE_ROOMS_HANDOFF_2026-09-28.md` with results.

- [ ] Fingerprint the real save folder; run `python tools/run_tests.py --subsystem moonbay` under scratch `APPDATA`; confirm the real folder is unchanged.
- [ ] Run relevant existing crew expedition, site, save, airlock, flooding, and reliability tests.
- [ ] Perform a native paid-run review of all three orders, routine and hazardous return, repair, and Save/Continue; preserve visual evidence.
- [ ] Record results, known limits, and next gameplay tuning; commit documentation.
