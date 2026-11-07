# Crew action expansion handoff

Updated: September 8, 2026 · Project: Brine Space

## Objective and acceptance

Owner authorized all five animation priorities for Bill, Veld and Branforth:
salvage/work, swim transitions, torch handling, cargo handling, and missing
directional work. Generated, packaged and integrated; owner visual acceptance
is pending in [the moving review](../output/crew-actions-review.html).

## Decisions and current state

- [Pack and source record](../character/crew-actions-v1/README.md): 666 registered
  frames, 168 added runtime clips with helmeted counterparts. Original base
  packs and accepted swimming helmet fitting remain intact.
- `crew_action_pack.gd` loads the expansion and fits equipment; `crew_sprite_player.gd`
  plays and checkpoints swimming transitions. Grid consumers include Bill's legacy
  path. Wider transitions require measured clearance.
- `bill_npc.gd` selects work/cargo actions and furniture-facing interactions.
  `crew_construction.gd` supplies the existing ten-second job clock for draw/stow.
- `crew_expedition.gd` adds a 0.52-second unload phase before cargo credit.
  `run_save.gd` validates the additional Bill water playback checkpoint.
  Workshop carrying uses the authored case instead of its old floating prop.

## Verification

- Godot native pack/export check: zero failures, equipment/timing, transition
  checkpoint, turn selection and simulation-driven draw/stow/unload checks.
- Swimming regression: zero failures. Construction: zero failures.
- Room activity: 36 room/rotation/architect approaches, facing and save cases pass.
- Native station systems: pass, including unload pause/Continue, one-time cargo,
  recall and rotated expeditions. Hull repair: pass.
- 666 PNGs: correct dimensions and transparent corners. Native equipment contact
  renders and station screenshots inspected; generated flaws corrected as recorded
  in the pack README. Full browser motion inspection was blocked by URL policy.
- Some earlier headless station/construction runs emitted existing wreck PNG
  import warnings and shutdown resource warnings; final native station run passed
  without script errors. No unrelated assets were changed to silence them.

## Next action

Owner reviews [the animation gallery](../output/crew-actions-review.html) and
[compact showcase](../output/crew-actions-preview.gif). Tune pose transitions or
equipment anchors against specific feedback. No commit or deployment performed.
Other active room/water/BRINE edits in this shared checkout are outside this change.
