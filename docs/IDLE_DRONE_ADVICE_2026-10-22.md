# Idle-drone advice pass

Updated: October 22, 2026 · BrineSpace

## Objective and acceptance
Correct misleading idle/finished-job feedback and remove duplicate route-planning
work without changing extraction, delivery, physical access or discovery.

## Accepted decisions and constraints
Use current site state. Paused stock is not depletion. Preserve existing directional
advice and survey mechanics; explain current lighting instead of a retired distance
rule. Reuse results within a single alert only, with no persistent plan cache.

## Current state
- `scripts/drone_fleet.gd`: route advice returns a distinct paused state when all
  remaining surveyed stock of the bay's type is inactive. Active goals still take
  precedence; zero-stock and other-kind sites do not count as paused supply.
- Route hint formatting accepts an already sampled plan; `scripts/drone_idle_alert.gd`
  passes its plan, reducing blocked-alert planning from two calls to one.
- Depletion advice replaces "build a room within 5 cells" with bringing survey
  lighting closer, matching `underwater_visibility.gd`'s light/ray-based survey.
- Extended `tests/test_drone_idle_alert.gd` and native worksite controls coverage.

## Verification
Baseline reproduces four new assertion failures:
`output/test-runs/20261022-003313-headless/`.
Finite-harvest tests pass for conservation, survey, depletion, pause, save validation
and obstacle detours: `output/test-runs/20261022-003408-headless/`.
Final alert checks pass including mixed targets and revised lighting copy:
`output/test-runs/20261022-003634-headless/`.
Counting-fleet instrumentation verifies exactly one plan query for a blocked alert;
this is work-count evidence, not an FPS measurement.

Native inspector fixture passes: `output/test-runs/20261022-003702-native/`.
Reviewed `output/worksite-controls-20261021/paused-deposit-advice.png`: paused-stock
reason and RESUME EXTRACTION instruction fit the expanded details. The fixture
sets up a docked waiting drone; it is not a complete fresh-opening playthrough.
Final logs contain no errors/warnings. Scoped whitespace check passes.

Runs used scratch APPDATA. Protection receipts:
`D:/bs-tutorial-20261021/idle-before.json` and `idle-after.json`.
No export or signed delivery update.

## Next action
Check the advice during ordinary pause/resume and deposit exhaustion. Known texture
upload hitches and the prior intermittent scrap-test shutdown warning remain outside
this pass; neither is claimed fixed.
