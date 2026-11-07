# Marsh final in-game sweep handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: final integration sweep

## Objective and acceptance

Owner accepted the new water actions and requested the remaining in-game sweep,
with fixes for anything found. Completed north-facing salvage, activity handoffs,
power interruptions, deferred injury and shutdown checks. Two runtime defects
fixed; selected artwork unchanged. [Native review](../character/marsh-final-sweep-2026-10-15/review/index.html).

## Accepted decisions and constraints

Retain all accepted art, clocks, standing ruler, android rules and corner-lounge
exclusion. Normal resource/failure flags remain enabled. All native/test runs use
scratch APPDATA; owner saves and layouts are inputs to neither fixture. No export,
commit or upload. Other work in the shared checkout stays separate.

## Current state

- `scripts/main.gd::has_marsh`: exterior shutdown cleared the expedition, then
  failed the station-floor visibility gate. Frame selection still passed while
  the actual body vanished. Admit an active dead exterior actor, matching the
  established Branforth rule. Inactive actors and live off-floor actors without
  expeditions stay hidden. No source or death-clock change.
- `scripts/marsh_npc.gd::die`: clear bunk/berth presentation contacts when death
  clears the live rest stage. Previously those contacts violated Marsh's own
  dead-snapshot validation rules. No new save fields or changes to survival.
- `tests/test_marsh_exterior_shutdown_visibility.gd` and paired UID cover both
  defects; registered in the crew group in `tests/index.json`.
- `tests/test_marsh_shutdown_injury_match.py`: historical shutdown interiors were
  compared with later master-repair rebaker output. Compare the rebaker with its
  declared master-repair stage. Historical installation/source hash checks remain;
  the final native sweep separately checks current catalog shutdown sources.
- `tools/review_marsh_water_actions.gd`: optional fixture obstacle creates a real
  northward final sea-route leg; observation hook records mid-action checkpoints.
  Default existing review behavior retained. No production pathfinder/facing edit.
- `tools/review_marsh_final_sweep.gd` and paired UID run the integrated matrix.
  `tools/publish_marsh_final_sweep.py` publishes the bounded native evidence.
  Review gallery has 320 native pose crops plus a north-facing journey sample.

## Verification

Evidence: `output/marsh-final-sweep-2026-10-15/`; final logs named below.

- `native-fixed.log`: 24,028 checks / zero failures and script errors. Two real
  dispatch journeys (delivery and empty recall) reach north salvage through the
  production route finder, all work/braking holds, pickup, return, drainage,
  unloading and exact resource/delivery accounting.
- Same run: 16 room lifecycles across four rotations of galley, crew habitat,
  observation and salvage workshop. Complete meal→drink, bunk→sleep→exit,
  seat→read→rise and inspect→work→pickup→carry→unload cycles reached. One rotation
  each injects power loss or physical damage 0.5 simulated seconds into service.
  All 16 current disk checkpoints restore source pixels. Four default corner-only
  lounges have no compatible Marsh station and are explicitly recorded as excluded.
- Three actual mid-water checkpoints branch into six damage/shutdown cases.
  Damage defers until dry return, then falls/recovers; death relinquishes the water
  helper and renders all six shutdown holds. Four dry facings each reach all
  12 injury fall/rise holds and six ground shutdown holds.
- Native inspection caught the invisible exterior body missed by frame-selection
  checks. Failing regression before fix: 8 checks / 2 failures. Fixed visibility
  native captures now show the body in open water and in the airlock.
- Further regression before rest cleanup: 12 checks / 2 failures. After cleanup:
  `visibility-cleanup-after.log`, 12 checks / zero; `rest-joins.log`, 69 / zero.
  `rest-shutdown-native.log`: 105 checks / zero and no script errors. Actual default
  bunk arrival advances to mid-climb, shuts down, writes a current checkpoint,
  reads/restores it and renders all six ground collapse holds. Both live rest
  contact types have unit coverage; the native save branch uses the default bunk.
- Total native matrix: 24,133 checks / zero. The broad run precedes the final
  rest-contact cleanup; the affected cleanup path is verified by the subsequent
  native rest branch and regression checks. No unrelated broad rerun claimed.
- Saved water/work clock regression: 6,256 checks / zero. Historical shutdown
  Python test: two tests pass after correcting the stale expectation.
- Full-size native north salvage, exterior shutdown, room-contact overview,
  recovery, ground shutdown and mid-climb shutdown samples inspected. Review
  images decode and local image links resolve. These are sampled pose changes,
  not continuous watched gameplay, measured FPS or automated browser interaction.
- All 2,948 fingerprinted non-log owner files unchanged before/after. Pre-existing
  Godot editor left running. Before/after exterior-body images and failing logs
  retained with evidence; earlier fixture setup/typing failures are not game defects.

## Next action

Review the two small runtime fixes in the native gallery. No further confirmed
animation defect remains from this sweep. This covers prescribed default-room
approaches and production actor/route updates with controlled damage/death entry
points; it does not certify every procedural station, autonomous choice, owner
layout, hazard propagation chain or exported build.
