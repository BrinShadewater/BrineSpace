# Gameplay follow-up: Studio scale and title preview

Updated September 12, 2026 · source workspace; broad non-art playtest goal remains active.

## Objective and acceptance

Add standing/walking crew to Room Layout Studio for equipment scale review and move
Continue Loop preview content right. Preserve the other sessions' room art and crew
animation replacements. Maintain the bible, skill and workflow with verified lessons.

## Accepted decisions and constraints

The Studio actor is a preview using the selected Bill catalog at gameplay size. It
does not enter furnishing data, undo, recovery, autosave or live crew state. Use the
room's normal actor/prop depth sorting. Character artwork and timings remain owned
by the animation session. Continue stays in the center; its summary/schematic moves
to a separate right-hand panel. Saved game data stays unchanged.

## Current state

- `scripts/room_scale_preview.gd` + UID: lazy selected-pack loading, standing, safe
  local walking and placement. Registered prop boxes use 10-unit clearance, corridor
  hull shape and exact rectangle sweeps. Layout changes rebuild the graph and choose
  the largest connected walking area. Current supported cardinal facings are used.
- `scripts/room_layout_editor.gd`: **Scale: Bill -> Hidden / Standing / Walking**,
  **Place** button and status; external actor inserted into existing depth queue.
  Preview stays visible in Clean preview. Hidden is the default.
- `scripts/title_screen.gd`: right-hand Saved Station panel; central action group
  contains the start/continue actions without checkpoint content.
- `tests/test_studio_character_scale.gd`, `tests/test_title_checkpoint_layout.gd`
  and paired UIDs; registered in `tests/index.json`.
- Added `skills/brinespace-room-pipeline/references/gameplay-preview-contract.md`
  and entry-point link, synchronized only those changes to the installed skill.
  Bible and ROOM_ART_PRODUCTION receive a concise usage/evidence note.

## Verification

- Native Studio: `output/test-runs/20260912-170102-native`: 16 room/orientation cases
  across BRINE, Med Bay, Crew Hab and corner corridor; 2,560 movement steps pass
  clearance; actual pack standing-height metadata, preview placement/no draft
  mutation, Hidden and compact controls pass. Screens reviewed in
  `output/gameplay-studio-20260912/` (standing/walking and 960px controls).
- Early Studio failures found unsupported diagonal idle facings and corner crossing
  between displayed positions; fixed with supported facings, exact sweeps and one
  clear segment per displayed step. Final result supersedes those attempts.
- Native title: `output/test-runs/20260912-165836-native`: valid disposable save,
  no-save path, unchanged saved contents and nonoverlapping right panel at
  960x540/1280x720/1600x900 pass. All three native captures reviewed in
  `output/gameplay-title-20260912/`.
- Existing native layout workflow and full title-screen checks pass in
  `output/test-runs/20260912-170153-native` (editing, undo/recovery and menu/settings).
- New skill reference matches the installed copy. Sync audit checks 26 files; the
  three pre-existing differences in layered-assets, material-and-scale-review and
  check_source_sync remain untouched. UID pairing, JSON and diff checks pass.
- Preview is a local scale/clearance aid, not all-room art acceptance or a live crew
  job journey. No new art, animation sources, save format, EXE, commit or push.

## Next action

Continue the remaining non-art owner queue: BRINE staged dark startup/pod timing,
airlock exterior-door/hatch visibility and runtime motion, and globally remove
decorative cable renderers. Cryopod source-animation replacement remains with the
other sessions; coordinate freezing particles/temporary character tint as runtime
effects. Original power/turbine report remains unconfirmed against the owner's exact
build/save; focused current-source diagnosis and bay fix are in the power handoff.
