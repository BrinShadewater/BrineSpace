# Gameplay power and selection handoff

Updated: September 12, 2026 · BrineSpace · source only

## Objective and acceptance

Owner assigned gameplay to this session; other sessions handle room art and character
animation. This pass fixes a reproduced bay operation bug, investigates reserve and
turbine reports, and removes initial blueprint selection. No balance change or export.

## Accepted decisions and constraints

Preserve paid construction, finite inputs, failure rules and concurrent changes.
Room operation is funded at cycle boundaries. New/resumed drone bays wait for their
funded cycle; next-cycle affordability must not revoke already funded operation.

## Current state

- `scripts/main.gd`: live fleet and clearance/construction status use funded
  `powered_room_cells`. `_draw_hand` leaves selection empty. Shared turbine blockage
  reasons feed direction/cell/object feedback. Power UI separates generation,
  requested/supplied Power, storage and projected charge/discharge.
- `scripts/crew_construction.gd`: dedicated-builder availability uses the same funded
  state. Only that condition changed here; concurrent route changes are preserved.
- `scripts/station_ui_insights.gd`: power balance and turbine intake descriptions.
- New `tests/test_power_playtest_regressions.gd` and Godot-generated UID; expanded
  `test_power_expansion.gd`, `test_power_demand_ui.gd`, `test_drone_jobs.gd`; registered
  the regression in `tests/index.json`'s gameplay group.

Reproduction: a mining bay consumes the final Power for this cycle. It has prepaid
charging credit, but a fresh next-cycle forecast rejects the bay and stops charging.
The new regression fails before the fix and passes afterward. Pause/master-off and
the next unfunded cycle still stop charging.

Reserves already discharge automatically for room operation. Battery Arrays add
capacity. Drone and Marsh charging draw storage between cycles. All four turbine
intake directions generate 4 with clearance and stop for obstructions; no directional
generation defect was reproduced and no generator output/bonus was changed.

## Verification

- Expected pre-fix failure: `output/test-runs/20260912-164243-headless`.
- Station operations and power regressions pass: `20260912-164324-headless`.
- Expanded reserve/pause/master-off, turbine, drone battery and lifecycle pass:
  `20260912-164500-headless`. Drone-jobs initially failed because the fixture installed
  a bay without paying its operating cycle. It now pays via the real economy and
  waits for observed drilling; final pass: `20260912-164738-headless` (paid building,
  clearance, pause, checkpoint and old-save compatibility).
- Native power UI and hardware pass: `20260912-164821-native`, including unselected
  click/no spending, reserve 3 -> 1, west intake blocked by rock then clear, controls,
  saved state and two viewport sizes. Earlier priority-foundations checks also pass.
- Reviewed `output/power-demand-ui.png`, `output/power-discharge-ui.png` and
  `output/turbine-intake-feedback-ui.png`. Code diff whitespace check passes.

Bounded fixtures/native UI checks do not establish owner balance acceptance or
packaged gameplay. No player save modified, no commit/push or EXE created.

## Next action

Reproduce the original low-power/west-turbine case when its build/save is identified
(asked; not yet supplied). Current fixtures establish the separate bay bug, not the
original report's cause. Review a normal paid expedition. BRINE startup, cryopod
effects, exterior hatch presentation and Studio scale preview remain in the main
playtest queue and need coordination with the art/animation sessions.
