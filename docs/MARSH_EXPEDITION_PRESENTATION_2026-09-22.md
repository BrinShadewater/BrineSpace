# Marsh expedition integration review

Updated: September 22, 2026. Project: BrineSpace. Task: review pickup through unloading.

## Objective and acceptance

Exercise real dispatch, airlock, crew and renderer paths through delivery and recall.
Three controlled journeys pass after two integration fixes. Visual review found a
remaining abrupt prone-to-standing change when the airlock becomes dry.

## Accepted decisions and constraints

No new art generation or Higgsfield. Preserve action durations, cargo rewards,
normal costs/failures, existing sprites and owner room layouts. The regression
fixture places its own airlock for free and supplies power explicitly; it does not
claim normal-loop balance, pacing, performance or owner visual approval.

## Current state

- `scripts/grid_canvas.gd`: map Marsh expedition pickup/unload action time from
  the existing0.52s controller slot to the authored clip duration. Pickup lasts
  0.9s in its manifest; unload already lasts0.52s and retains its timing.
  Before correction the real renderer selected pickup frame3 of6 at0.50s.
  Earlier isolated native fixtures applied this mapping themselves, so their
  passing endpoint checks did not establish correct game integration. Earlier
  handoff statements implying the real renderer already mapped pickup are superseded.
- `scripts/marsh_npc.gd`: allow exterior action poses without station-floor
  clearance, matching human crew. Keep interior checks. Previously missing sea
  floor suppressed all loaded turns in the actual renderer despite valid clips.
- `tests/test_marsh_expedition_presentation.gd` and paired UID: three complete
  journeys on the actual main scene, real dispatch/routes and airlock/controller,
  sampled at1/30s simulation steps. Registered in the crew subsystem.
  Delivery traverses all12 phases; return renders east-west and west-south turns.
  Empty recall skips pickup/unload art; loaded recall retains and delivers cargo.

## Verification

- New native regression:3 journeys, zero failures. Loaded journeys play all6
  pickup poses and all4 unload poses. Exact site depletion and metal/data delivery
  checks reject early or duplicate rewards. Loaded disk restore preserves pixels,
  and the production paused process leaves actor position fixed.
- Initial test also had two fixture mistakes: expecting6 rather than4 unload
  poses, and calling an internal stepping helper directly while checking pause.
  Corrected using actual manifest evidence and the production `_process` entry.
- Existing native Marsh battery/route regression:PASS,93 route samples.
- Agent inspected real pickup, turning return, wet drain and dry exit captures,
  including enlarged case detail. Case remains in both hands after drying.
- Evidence: `output/marsh-expedition-review-2026-09-22/`; original probe and failed
  report retained. Corrected captures/report in `fixed/`. `expedition-excerpts.gif`
  crops gameplay captures with labelled phase excerpts; long journeys are omitted
  and drain/exit stills held, so this is not an uninterrupted realtime recording.
- This fixture uses one airlock orientation and one corner route, manual simulation
  stepping, supplied resources/power and a prebuilt station. UI may retain its
  paused label after a checkpoint test; the trace records actual controller state.
- No source artwork changed, executable rebuilt, commit or publication.

## Next action

Author a cargo-preserving transition from loaded swimming to standing during
airlock drainage, retaining controller timing. Current phase boundary changes the
silhouette directly, so smooth water-to-dry acceptance remains open. Then review
normal gameplay timing and other airlock orientations before fresh test builds.
