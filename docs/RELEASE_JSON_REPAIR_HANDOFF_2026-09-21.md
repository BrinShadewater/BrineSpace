# Release JSON dependency repair

Updated: 2026-09-21 - BrineSpace

## Objective and acceptance
Ship the current room and animation work with all runtime artwork available.
Windows actual-release validation precedes the matching Mac candidate.

## Accepted decisions and constraints
Preserve owner layouts and older deliverables. No Higgsfield or publication.

## Current state
Candidate brinespace-4035ce07d72e861f passed exact-PCK integrity and fixture
assertions but logs two empty-image errors during New Game; it is not accepted.
A diagnostic Logger with debug/settings/gdscript/always_track_call_stacks=true
in the isolated external override traced both to room_asset_library.template,
called by Storage Bay during derelict rendering. This override is not a deliverable.
The rack and hand-truck source sheets were absent from the expected manifest.
The manifest's generic quote regex misreads apostrophes in JSON prop labels.
Changed tools/build_release_manifest.py to walk parsed JSON strings; added a
regression in tests/test_release_manifest.py. No runtime error suppression.

## Verification
Six focused manifest tests pass. Full read-only dependency collection now includes
61 additional assets and every registered tileset source (zero missing).
Evidence: output/layout-turns-release-validation-2026-09-21/
logger-stacks-release.log and manifest-repair-audit.json.
Exact-PCK integrity alone cannot detect omissions shared by package and manifest.

## Next action
Export a distinct repaired Windows candidate with the maintained exporter; audit
its PCK and run the actual release smoke without diagnostic flags. Inspect captured
screenshots and engine errors before accepting it. Then refresh Mac. Ordinary Bill
gait, owner visual acceptance and broader polish remain open.

## Repaired Windows candidate verified
Build brinespace-e7c1ea935b573fd2 is in
builds/BrineSpace-layout-turns-fixed-2026-09-21. Maintained export exits zero.
Exact-PCK audit: 15,146 checked, zero missing/changed/remapped/unexpected.
Actual release New Game, simulation and F8 fixture exits zero with zero errors;
gameplay and report PNGs visually inspected. EXE/PCK SHA256SUMS saved with build.
Evidence: output/layout-turns-fixed-validation-2026-09-21/.

The external tests/release_new_game_smoke.gd now captures engine/script/shader
errors with Logger and fails if any occur (warnings remain in logs for review).
Negative control: the previous package exits 1 with both known empty-image errors;
repaired candidate exits 0. No diagnostic backtrace setting is enabled in either
playable package. The fixture uses an isolated app name; owner profile unchanged.
This establishes the scoped Windows startup gate, not broad gameplay/gait acceptance.
Next: export matching Mac candidate via maintained wrapper, inspect bundle and PCK;
native Apple Silicon gameplay remains owner-hardware work.
