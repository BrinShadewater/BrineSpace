# Project handoff

Updated: September 9, 2026 - Project: Brine Space - Task: River and Josh companions

## Objective and acceptance
Build the selected robots as playable companions. Local integration complete;
owner full-body/motion and normal-play pacing review remain. No executable rebuilt.

## Accepted decisions and constraints
River is the small green R2-D2-like wheeled droid. Josh is the larger muted blue-
lavender Johnny 5-like robot; the owner explicitly corrected his locomotion to
treads. Unlocked companions are optional selections before new expeditions.
River retains the garbage-room trash container and Josh the derelict storage crate.
Companions are not architects. Margot awaits a photo reference and future integration.

## Current state
New scripts/companions.gd and companion_npc.gd (paired UIDs) implement finite
recovery, roster, independent movement/playback and checkpoint validation. Narrow
hooks in main, grid_canvas, meta_state, architect_selection, run_save, bill_npc,
wreck_field, drone_fleet and the wreck renderer integrate them without refactoring.

character/river-v1 and josh-v1 each contain 8 clips / 24 frames, raw sources,
prompts, manifest and motion GIF. Josh's discarded biped source is archived only.
character/companions/encounters contains four container states and their source.
Selected portraits remain unchanged. Builders are tools/build_companion_sprites.py
and build_companion_containers.py. Review: character/companions/review.html.

Found room shells/economies reuse salvage_workshop and storage_bay. Only the found
rooms reserve a container footprint and omit intersecting furniture. Eight-Metal,
18-second repair and eight-second powered restart are prototype tuning. Companions
follow/wander near crew; no personal battery costs, damage or special jobs yet.

## Verification
- tests/test_companions.gd: PASS, including paid repair, missing access/supplies,
  explicit opening, power interruption, partial repair/restart Continue, once-only
  recovery, separate berths, independent RNG, disk saves, malformed data rejection,
  legacy round-trip, selected River on a fresh loop, cancel and room suspension.
- tests/playtest_companions.gd: native PASS; both recover, travel through the
  station with prop clearance, pause and show selection at 1600x900 and 960x540.
- Existing test_run_save, test_architect_recovery, test_crew_construction and
  test_wreck_clearance: PASS. The wreck fixture was updated to provide an actual
  construction bay; it previously expected the retired bootstrap builder while
  advancing drone-only work. No production construction behavior changed.
- Generic sprite validator: zero errors/warnings for both manifests. New PNGs use
  LFS attributes. Editor import/parse returned zero. Paired script UIDs retained.
- Agent visually reviewed generated sheets, opened/recovered native rooms,
  relative actor scale, core travel captures and the small-window picker. Native
  travel checks use 0.1-second simulation ticks and captures every 2.5 seconds;
  sparse captures do not certify continuous full-speed motion. GIFs support review.

Logs are output/companion-{test,native,run-save,architect,construction,wreck}.log
and companion-final-import.log; captures in output/companions-native. Native and
headless logs include existing raw-image/export warnings. Some headless fixtures
report two resources retained at shutdown despite successful assertions; native
companion completion is clean. No packaged-build claim or performance benchmark.

## Next action
Owner review of River/Josh motion and recovery pacing in normal paid play. Open
project.godot in Godot and use New Loop to find the new encounters; old EXEs are
unchanged snapshots. Margot requires her photo before portrait production.