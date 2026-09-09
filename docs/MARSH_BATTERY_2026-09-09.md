# Marsh battery and breathing

Updated: September 9, 2026 · BrineSpace · local source implementation

## Objective and accepted direction

Owner adds an android tradeoff: Marsh wears no helmet and does not breathe, but periodically returns to his pod to recharge using Power. Approved appearance and original charging-pod recovery retained.

## Current behavior

- No helmet fitting, tank refill, breath depletion, air distress, drowning or unprotected-exterior death for Marsh. Oxygen crew upkeep and forecasts exclude him. Human breathing rules remain active. The explicit exemption is breathing; existing food/hunger behavior remains in this prototype.
- Initial tuning: 100% battery lasts 300 simulation seconds. At 35%, Marsh relinquishes construction/hull work, navigates to his original pod and docks. Empty battery permits only quarter-speed emergency return. Blocked routes/doors stop travel with visible status.
- Charging requires a powered, active pod room and stored Power. It restores 5% per second; each 1 Power buys 25%. Unused credit persists through interruptions and saves. Empty-to-full costs 4 Power and takes 20 powered seconds, in addition to the host's existing upkeep. Pause, power loss and suspension hold progress.
- Docking shows Marsh in the existing cradle with white-fluid motion, hides his floor actor and returns him to work at 100%. Rescued Marsh uses his derelict pod; starting Marsh uses the core pod. Current geometry determines the approach.
- Expeditions use battery rather than helmet/Oxygen requirements. Range is battery-limited; low reserve triggers recall and blocks redispatch. Normal powered airlock interlocks remain required.
- Battery, returning/docked flags, charge credit and effect time persist in his crew snapshot. Older Marsh saves initialize a full battery and discard obsolete helmet state.

## Changed files

Behavior: `scripts/marsh_npc.gd`, `bill_npc.gd`, `room_flooding.gd`, `flood_safety.gd`, `crew_life.gd`, `hull_repair.gd`, `crew_expedition.gd`, `airlock_service.gd`, `run_save.gd`. Display/economy: `main.gd`, `grid_canvas.gd`, `architects.gd`, `architect_selection.gd`, `airlock_panel.gd`, `marsh_charging_art.gd`. Tests: new `test_marsh_battery.gd`/UID, expanded `test_marsh_unlock.gd`, fourth actor added to flooding fixture. Existing raster assets reused.

## Verification

- Battery fixture passes: 87 collision-checked route samples; flooded/exterior survival without gear; human breath drain; legacy normalization; Oxygen accounting; reserve/outage/suspension/pause holds; charge credit across Save/Continue; full release; malformed battery rejection; emergency return.
- Full zero-Oxygen salvage trip covers every expedition/interlock phase, exterior checkpoint restore, finite cargo and dry return. Second trip confirms battery recall and blocked redispatch.
- Final native run has no script/error entries. Reviewed 1600 and 960 docking captures under `assets/marsh-charging-v1/review/recharge-*.png`. Initial null floor-texture renderer error fixed by excluding docked Marsh from floor actor lists.
- Dedicated derelict return and original unlock/persistence/coexistence suite pass. Human station systems and flooding pass. Marsh paid construction passes all four directions. Intermediate headless construction/unlock runs reported shutdown resource warnings; final native and dedicated-return logs do not.
- Godot import and scoped diff whitespace checks pass. No export or commit.

## Next action

Owner play review of interval, cost and return behavior. Numbers are initial tuning, not owner-specified balance. Executable packaging remains separate.
