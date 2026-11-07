# Clearance status bug and optimization pass

Updated: October 22, 2026 · BrineSpace

## Objective and acceptance
Check job-state feedback for misleading explanations and unnecessary repeated work.
Preserve existing extraction, rewards, access, animation and artwork.

## Accepted decisions and constraints
An unrelated drone type's battery must not explain why this job waits. An assigned
worker's status remains authoritative. No scheduling, charging or save-format edits.

## Current state
- `scripts/drone_fleet.gd`: `clearance_status` accepts a required kind. In one pass it
  records relevant recharging drones while looking for the assigned worker; an
  assigned-worker result takes priority regardless of insertion order. No cache.
- `scripts/main.gd`: rock and wreck inspector calls supply mining and salvage,
  respectively. Existing status strings and layout are unchanged.
- `tests/test_rock_clearance.gd`: reproduces an active excavation incorrectly reporting
  a salvage drone's battery state through the actual inspector.
- Added `tests/test_clearance_status.gd` with paired UID for kind filtering and
  assigned-worker precedence across working, travel and docked states. Registered
  the clearance-status subsystem in `tests/index.json`.

## Verification
Inspector regression fails before the fix:
`output/test-runs/20261022-010728-headless/`.
All three focused fixtures pass afterward:
`output/test-runs/20261022-010925-headless/`.
Rock/wreck tests retain coverage of pause, access, shared jobs, persistence,
once-only rewards and paid rebuilding. Scoped whitespace check passes.

The optimization removes the second fallback fleet scan; it is not a measured
frame-time/FPS improvement. No fresh native visual acceptance is claimed because
the text/layout itself is unchanged. No export or signed-delivery update.

Tests used scratch APPDATA. Protection receipts:
`D:/bs-tutorial-20261021/clearance-before.json` and `clearance-after.json`.

## Next action
Observe clearance explanations during ordinary mixed mining/salvage operation.
Existing upload-hitch and intermittent scrap-test shutdown investigations remain
separate; this pass does not resolve them.
