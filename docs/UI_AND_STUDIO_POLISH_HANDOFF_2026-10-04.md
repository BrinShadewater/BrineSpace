# Project handoff

Updated: October 4, 2026 · Project: BrineSpace · Task: Owner UI and large-room polish

## Objective and acceptance
Fix the owner's large-room editing/character-preview issues, tidal waterline and pipe,
unequal hand cards, obsolete live salvage props, and add colored expanded/compact crew
meters with brighter card/resource accents. Source implementation and native review complete.

## Accepted decisions and constraints
- Surrounding large-room equipment is editable; central machinery and pressure enclosures
  remain fixed. No owner layouts were rewritten. Moonbay's three formerly fixed peripheral
  props now use the same saved-layout system; locker service follows its moved position.
- Health represents existing remaining starvation/survival reserve, with zero on death.
  Oxygen uses the equipped tank or breath reserve. Hunger/Fatigue show increasing need.
  Non-breathing characters show unavailable Hunger/Oxygen. No new damage economy was added.
- Existing unrelated edits were preserved. No commit, export or publication requested.

## Current state
- `scripts/room_layout_editor.gd`, `scripts/room_scale_preview.gd`,
  `rooms/large-rooms/studio_view.gd`: visible character controls, full large-room walking
  area and fixed-equipment avoidance, actors drawn at gameplay scale and sorted with props.
- `rooms/large-rooms/moonbay.gd`, `scripts/airlock_service.gd`, `scripts/grid_canvas.gd`:
  movable default support props, saved locker interaction, hidden/deleted locker handling.
- `rooms/large-rooms/tidal_power_plant.gd`: removes shallow prop-waterline treatment from
  the chamber turbine/rotor; chamber fill remains. Pipe/grate starts at -300, clear of north wall.
- `scripts/james_cargo_workshop.gd`: explicit salvage room identity lets the cargo subclass
  load the current four props instead of bypassing layout/retired-art filtering.
- `scripts/draft_card.gd`: equal hand size based on tallest content; deferred layout resolves
  live instance IDs safely when cards are replaced. Brighter department frame accents.
- `scripts/resource_icons.gd`, `scripts/crew_portrait_panel.gd`: brighter resource palette;
  amber Hunger, lavender Fatigue, green Health, blue Oxygen; compact bars beside every portrait.
- `tests/test_owner_polish.gd` and paired UID, `tests/test_large_room_props.gd`,
  `tests/index.json`: regression coverage and registration.

## Verification
- Godot 4.7.2 native: owner polish **727 checks / 0 failures**, responsive UI **148 / 0**.
- Large-room props, large-room revisions, Moonbay missions/assignment/save, and UI workspace
  suites all pass. Final logs contain zero engine errors. Large-room Studio headless check passes.
- Reviewed native large-room character/selection captures, full tidal chamber at 0°/90°,
  actual live Salvage Workshop, equal fan/row cards, expanded/compact crew and 960×540 UI.
- The first regression run caught a deferred-card callback receiving a freed object. Fixed
  with instance-ID resolution and reran affected transitions; first logs retained. A run that
  loaded during that edit had a transient parse failure; its final rerun passes.
- Every Godot run used scratch APPDATA. Final fingerprint: **2,936 owner non-log files,
  zero changes**. Source whitespace check passes (only normal Git line-ending notices).
- Logs, source-before snapshots, focused diffs, captures, `verification.json` and owner
  fingerprint evidence: `output/polish-2026-10-04/`. `tidal-filled-q0.png` and
  `tidal-filled-q1.png` show the final shorter pipe; the final owner fixture also uses it.

## Next action
Owner playtest/visual acceptance in the editor. Source work is complete; packaged-release
acceptance remains separate. If the owner intended movable central machinery or an independent
health system, that expands the present interpretation and needs a follow-up gameplay pass.
