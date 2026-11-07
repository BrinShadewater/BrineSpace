# Reachable bunk priority

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Keep the shared-bunk fairness fix from reserving a bed for a tired colleague who
cannot reach it. Avoid repeating the new reachability query for every candidate
node in one goal choice. Preserve existing arrival/occupancy claims.

## Accepted decisions and constraints
No owner layout or save-format changes. This remains a local priority rule for
reviewed bought-bunk stations, not a global scheduler.

## Current state
scripts/bill_npc.gd now checks the eligible peer's route between its current room
and the matching bed contact. The normal route helper respects disconnected graph
components and fire exclusions. choose_goal caches station claims by room/contact
for that synchronous decision only, and reuses the resolved target station.
Claims are recomputed on the next choice, so route or need changes do not leave a
persistent reservation. No FPS or wall-clock speed claim is made.

tests/test_bunk_eligibility.gd is indexed in the crew lane with a new engine-generated
UID u13pu8xo7866. It covers disconnected/connected peers, fire, inactive/dead,
charging/distant peers, urgency thresholds, queued arrival, rise and release.

## Verification
Evidence: output/layout-default-audit-2026-09-21/.
- bunk-eligibility-before.log reproduces a disconnected peer blocking the bunk.
- bunk-eligibility-after.log rejects that peer and still accepts the connected peer.
- bunk-eligibility-final.log: 12 checks, zero failures.
- Focused whitespace check passes.
bunk-multi-eligibility.log: the 180-second / 3600-update four-crew regression
passes again. All four sleep and rise, maximum one occupant, 15 centered captures,
zero failures. Sleep counts match the earlier successful sharing scenario.

## Next action
Continue broader paid expedition/room polish and release validation. This test
covers graph eligibility, not every transient traffic obstruction or arbitrary
furniture orientation. Existing exact contact and collision checks still govern
arrival.
