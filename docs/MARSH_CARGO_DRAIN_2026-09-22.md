# Marsh cargo-preserving drainage transition

Updated: September 22, 2026. Project: BrineSpace. Task: loaded water-to-dry repair.

## Objective and acceptance

Replace Marsh's abrupt prone-to-standing switch at the airlock's dry boundary.
Four-facing art and renderer integration are installed. Native south-facing
delivery/recall review passes; owner motion acceptance and complete journeys
through the other airlock orientations remain open.

## Accepted decisions and constraints

No Higgsfield, mirrored directions, changed airlock timings or cargo economy.
Keep both hands on cargo; rear torso may occlude it. Preserve owner layouts and
existing art. Stand with planted feet while waiting, not a frozen carry stride.

## Current state

- `character/marsh-cargo-drain-v1/`: four independent raw source sheets, corrected
  north source02, exact prompts, frozen loaded/carry endpoints and review media.
  North source02 last two cells lower the grip, hiding cargo behind the torso;
  source01 remains selected for its first two cells. Side sheets use measured
  cell boundaries because the first prone figure exceeds an equal-width cell.
- `tools/build_marsh_cargo_drain.py`: four six-slot clips,24 registered frames,
 224x208,pivot112,172,standingHeight148. Exact loaded frame0 at the start; four
  authored rising poses; registered existing carry frame0 stored as exit reference.
  Runtime folders: `character/marsh-v2/supplemental/cargo-drain-*`.
- `scripts/grid_canvas.gd`: drainage presentation applies only to living Marsh
  with cargo in the expedition drain phase. Rise follows saved interlock elapsed
  time1.6-2.8s of the existing4s drain (60%-30% water). Hold authored frame4 with
  planted feet through depressurizing/opening_inner; existing carry playback
  selects its first moving stride on exit. No new mutable animation clock/save field.
- Last authored standing pose and exit reference have dry metadata; earlier poses
  retain water metadata. Supplemental pack validation now reads per-frame water
  flags when supplied, preserving uniform defaults for older supplements.
- Catalog, supplemental source contract, clearance and canonical rebuild updated.
  Existing PNG hashes unchanged. `tests/test_marsh_cargo_drain.py` covers exact
  source reproduction, registered endpoints, binary alpha and borders.
- `tests/test_marsh_expedition_presentation.gd` additionally exercises drainage
  frames, all four facing selections, planted holds, pause, loss of power, disk
  restore and death precedence. Full journeys remain south-facing in this fixture.

## Verification

- All24 frames reproduce exactly. Validator:200 body states/1026 frame references,
  no errors/border touches;211 original source frames and one manifest unchanged.
- Complete pack:21,399 checks, zero failures. Existing fixture image-loading
  warnings do not establish export compatibility.
- Native expedition:3 journeys, zero failures. Delivery and loaded recall render
  five drainage poses; empty recall does not display cargo. Cargo credit, six
  pickup poses, four unload poses and loaded return turns retain their checks.
- Final native rerun after death guard:3 journeys, zero failures. Pause and power
  loss freeze interlock and pose; disk restore preserves exact drainage pixels.
- Existing native Marsh battery/route regression:PASS,93 route samples with the
  updated clearance envelope.
- Agent inspected four source contact strips and cropped gameplay rising sequence.
  `output/marsh-cargo-drain-2026-09-22/drain-gameplay.gif` holds its first/last frames
  for readability; it is an excerpt, not an uninterrupted realtime recording.
- Evidence/logs: `output/marsh-cargo-drain-2026-09-22/`.
- No full canonical rebuild, executable export, commit or publication this pass.

## Next action

Finish complete rotated-airlock journeys and check gameplay-scale motion with the
owner. Then prepare current Windows/Mac test builds through the release workflow;
native Apple Silicon release validation remains separate.
