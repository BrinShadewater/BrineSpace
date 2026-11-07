# Worksite controls: bug, polish and optimization pass

Updated: October 21, 2026 · BrineSpace

## Objective and acceptance
Find concrete gameplay interaction defects and unnecessary work while preserving
normal costs, discovery, physical access, artwork and exact animation timing.

## Accepted decisions and constraints
Restore existing controls rather than add a new interaction. Companion survey checks
remain separate. No renderer/cache changes, exports or player-profile edits.

## Current state
- `scripts/main.gd`: the inspector's control-row visibility now includes selected
  visible unbuilt work sites and discovered finite deposits. Their existing action
  handlers, disabled states and blockers remain authoritative. Previously only built
  rooms and surveyed companions showed the row, hiding the prepared repair,
  clearance and extraction buttons.
- Cryo/charging repair descriptions and buttons share a single repair-blocker query
  per refresh instead of checking doors, active jobs and costs twice.
- Salvage action hint now explains delivery on docking and storage capacity, matching
  the actual cargo flow and inspector paragraph.
- `tests/test_inspector_refresh.gd`: visibility regression plus instrumented door-call
  assertion for a single blocker evaluation.
- `tests/test_worksite_controls_native.gd` and paired UID: native action/layout fixture;
  registered with the worksite-controls subsystem and native override in `tests/index.json`.

## Verification
The new ward-visibility assertion fails before the fix:
`output/test-runs/20261021-225409-headless/`.
Final inspector and cryo recovery tests pass:
`output/test-runs/20261021-225602-headless/`.
Native worksite controls pass:
`output/test-runs/20261021-225745-native/`.
Final logs contain no errors or warnings. Scoped whitespace check passes.

Native checks exercise normal eight-Metal payment, pause/resume without repaying,
salvage and excavation toggles, missing-bay blockers, discovered deposit controls,
undiscovered deposit hiding, and blueprint-hover hiding. An authored fixture supplies
rooms and a production-constructed deposit; this is not a fresh opening/balance test.
1600x900 and 1280x720 captures are in `output/worksite-controls-20261021/`;
normal salvage and compact repair/extraction reviewed. Work-count coverage proves
one blocker evaluation, not a measured FPS improvement. No new charging-specific
native capture or packaged acceptance is claimed.

Tests used isolated APPDATA. Protection receipts are
`D:/bs-tutorial-20261021/worksites-before.json` and `worksites-after.json`.

## Next action
Use the restored controls during an ordinary recovery/mining playthrough. A real
opening remains the useful test of discoverability and pacing; no further UI feature
is implied by these repairs.
