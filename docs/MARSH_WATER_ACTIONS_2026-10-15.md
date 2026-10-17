# Marsh water actions handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: remaining water-action gaps

## Objective and acceptance

Owner asked about standing→swimming, airlock drainage and underwater salvaging,
then authorized continuing. These were semantic gaps despite the previous
228-state catalog audit. Implemented in the normal selection and renderer;
[visual review](../character/marsh-water-actions-v1/review/index.html) accepted
by the owner on October 15 ("Those look good"). No export, commit or upload.

## Accepted decisions and constraints

Preserve accepted strokes, locomotion, rest, meals, cargo and density decisions.
Marsh remains a sealed android with anatomical-right temple hardware, ivory boot
tops and a 148-pixel standing ruler. Corner lounge seats remain excluded.
No change to water rules, physical contact/route, work duration, economy, delivery
or saved-state format. Existing loaded cargo drainage remains selected.

## Current state

- `character/marsh-water-actions-v1/manifest.json` is last in the ordered catalog.
  Adds four facings each of lift, settle, underwater braking entry and salvage:
  16 states / 76 holds. Selected library now 244 states / 1,274 holds.
  Existing four pickup slot-zero holds now use the exact shared tread pose.
- `sources/` retains whole-body generated sheets, exact prompts and correction
  attempts. Builder selects 24 complete body keys: one neutral-derived scale
  per direction, whole-pose registration and alpha cleanup, no limb/head grafts
  or opposite-view mirroring. West cell6 kept an incorrect near-side temple mark
  after two sheet edits, so remains unselected; the clean whole West cell3 is
  reused for that brace/pull key. No local head repair was applied.
- `tools/build_marsh_water_actions.py` packages fixed 224×208 frames at pivot
  (112,172); wired into `tools/rebuild_marsh_art.py`. Lift starts/ends at exact
  padded accepted idle/tread; settle reverses it. Braking entry connects exact
  current swim and tread. Salvage ends at pickup's new tread entry; pickup still
  ends at the original loaded swim pose. All 1,198 prior source holds stay intact
  on disk; only those four selected pickup entry slots change.
- `scripts/marsh_water_actions.gd` uses saved chamber water and expedition clocks.
  Rising spans 30–60% water; settling reverses over 60–30%. Empty return first
  brakes while the outer door seals. Underwater work spends 400 ms braking, then
  fits six 900 ms source cycles into the remaining existing 5.48-second service.
  `scripts/grid_canvas.gd` selects it before existing cargo-drain presentation.
  Dry work, cargo drainage, death and injury retain their paths.
- New checks: `tests/test_marsh_water_actions.py`,
  `tests/test_marsh_water_actions.gd` and its crew entry in `tests/index.json`.
  `tools/review_marsh_water_actions.gd` drives actual expeditions.
  New GDScripts have paired UIDs. `tests/crew-art-baseline.json` rebaked narrowly.
- `tools/publish_marsh_water_actions.py` creates 12 source chains and eight native
  sample boards, with pause/play for source previews. Source chains replay with
  authored timing; work shows three loops for review. Native boards are sampled
  stills, not continuous real-time playback. Publication receipts live beside it.

## Verification

Evidence and logs: `output/marsh-water-actions-2026-10-15/`.

- Three Python contract tests pass: all old source hashes, selection scope,
  endpoint joins, reversal, dimensions and clocks.
- Native clock fixture: 6,256 checks / zero failures; four facings across water
  levels and work times, plus dry/cargo/death/injury exclusions.
- Actual native journeys: 36,420 checks / zero failures, eight journeys covering
  delivery and empty recall at all four airlock rotations. All four lift/settle
  facings and every hold reached. Salvage routes reach east, south and west;
  north salvage has source/clock coverage, not an observed native work journey.
  Six work holds and five braking holds reached for each observed facing.
  Sixteen actual mid-lift/work/settle disk restores, plus four loaded return and
  four loaded drain restores; paused source pixels/contact stable. Existing cargo
  drain power-loss checks, resource accounting and one delivery credit per
  delivery journey pass. Normal economy/failure flags retained.
- All four packaged pose boards and native lift/drain views inspected; native
  east/south/west work and published sample boards inspected. Some native crops
  include the existing bottom card UI; actor remains visible. Capture is a
  controlled simulation, not performance/FPS evidence.
- Crew complete packs: 4,880 checks / zero; meals: 8,665 checks / zero.
- Baseline now 4 actors / 2,018 clips / 19,688 frames. Compared with the immediate
  pre-pass freeze: exactly 16 added Marsh clips and four pickup slot-zero changes;
  all other actors, frames and clip metadata exact. Package rebuild byte-exact.
- All exported WebP frames decode; local review asset links resolve; embedded
  JavaScript passes Node syntax checking. Browser interaction was not automated.
- Every Godot invocation used scratch APPDATA. All 2,948 fingerprinted non-log
  owner files unchanged before/after. Existing unrelated editor left running.

This is bounded action integration evidence, not every route/hazard or release
certification. The earlier historical shutdown rebaker mismatch was not changed
or rerun in this pass. Other characters' shared-checkout work remains separate.

## Next action

October15 final follow-up: the owner-authorized integration sweep is complete;
see [final sweep and two runtime fixes](MARSH_FINAL_SWEEP_2026-10-15.md).
North-facing salvage is now observed on an actual route and the historical
shutdown test expectation is corrected. The paragraph below records the scope
remaining at the earlier water-action acceptance milestone.

Owner accepted the new water actions. No known artwork correction remains within
the reviewed animation families. A final combined normal-play sweep can still
check transitions between activities, north-facing salvage on an actual route,
and hazard/injury interruptions. This is remaining integration coverage, not a
known visual defect or missing clip. The historical shutdown rebaker mismatch
remains a separate validation-tool issue. Playable-release certification is
separate work; no new test batch was run for this acceptance-only update.
