# Expedition continuation and hatch rendering repair

Updated: September 23, 2026 · Project: BrineSpace.

## Objective and acceptance

Continue normal expedition review and repair observed defects. Native Godot 4.7.2
source execution, normal dealt hand, paid construction, failures and comms pauses;
automated legal placement choices, not human pacing or listening acceptance.

## Accepted decisions and constraints

Use isolated process-specific preferences, meta and loop files. Preserve owner
layouts, art, saves and existing packages. No generation, commit or publication.
Resume only disposable copies of the frozen checkpoint.

## Current state

- A 90-second opening and 150-second continuation reached cycle 10/seven rooms
  and Conclude Expedition. Cycle-3 disk restoration matched crew, rooms, resources
  and cycle exactly. Saved construction continued; the starter wake line did not
  repeat. Low-power dialogue appeared, and power shortages produced blackouts.
- This run exposed `Invalid polygon data, triangulation failed` in
  `DroneArt.draw_hatch`: a tiny positive aperture can degenerate at room coordinates
  before its opening fraction reaches zero.
- `scripts/drone_art.gd` now checks triangulation for near-closed apertures and
  retains the closed hatch art if the aperture is not drawable. Other aperture
  geometry and drone motion are unchanged. An initial fixed size cutoff was
  insufficient and was replaced by the actual geometry check.
- Added `tests/test_drone_hatch_polygon.gd` and its UID; registered the regression
  in `tests/index.json` with the native render lane.

## Verification

- New native regression: 66 combinations of hatch width, room position and opening
  fraction; reproduced seven renderer errors before repair, zero afterward.
- Existing native drone handoff regression: six comparisons, zero failures.
- A fresh 100-second continuation from a disposable copy of the same checkpoint
  reached cycle 7/seven rooms and conclusion with zero captured engine errors and
  an empty stderr log. Normal costs/failures remained enabled.
- Inspected opening, paused restore, fixed continuation/low-power warning and
  conclusion screenshots. No room/art change was justified. These still images
  do not establish continuous motion quality, audio quality or whole-game approval.
- Evidence and bounded harnesses: `output/expedition-continuation-2026-09-23/`;
  original `events.json`, `checkpoint-frozen.loop`, `native.log`, `stderr.log`,
  `hatch-before/after.log`, `handoff.log`, `fixed-native.log`, `fixed-stderr.log`
  and `fixed/`. The original run intentionally retains its observed failure.

## Next action

Include this hatch repair and the earlier Continue-dialogue fix in the next
maintained export. Current packages predate both. Continue broader crew/room and
power-management review from specific observations; this bounded opening strategy
does not establish sustained growth, balancing acceptance or native Mac behavior.
