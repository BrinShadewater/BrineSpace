# Gameplay bug and optimization pass

Updated: October 21, 2026 · BrineSpace

## Objective and acceptance
Inspect gameplay for concrete bugs and avoidable work, preserving costs, discovery,
physical access, current artwork and exact animation timing.

## Accepted decisions and constraints
Keep the current architecture. Apply the existing construction-dependent scrapping
rule consistently; do not add new menus or change building costs. Source only.

## Current state
- `scripts/room_scrap.gd`: construction protection covers the full queued footprint,
  rather than just its anchor, and includes orders assigned to drones. The existing
  disabled Scrap control and reason now apply to those cases.
- Connectivity checks reuse door-neighbor results between their before/after walks
  within one call. Nothing is cached between queries, so topology changes are read
  immediately. Temporary storage scales with reachable cells.
- `tests/test_room_scrap.gd`: added large-edge, distant-order, assigned-drone,
  connectivity work-count, bridge, and changed-topology checks.

## Verification
The large-edge regression failed before the fix:
`output/test-runs/20261021-182727-headless/`.
Afterward, scrap and inspector-refresh fixtures both pass:
`output/test-runs/20261021-182817-headless/`. Scoped whitespace check passes.
The 100-cell chain leaf check asserts 100 neighbor evaluations; the previous two
independent walks visit 100 + 99 cells. This is work-count evidence, not measured
gameplay FPS or frame-time improvement. No visual layout/art changes were made;
no new native visual or packaged acceptance is claimed.

The new test's temporary graph initially remained referenced at shutdown. Releasing
it before the game fixture removes the warnings. Final scrap rerun passes cleanly:
`output/test-runs/20261021-182948-headless/`.

Tests used isolated APPDATA. All 2,971 owner files and signed ZIP stat are unchanged:
`D:/bs-tutorial-20261021/scrap-before.json` and `scrap-after.json`.

## Next action
Include supporting-room scrapping around an active large build in the next ordinary
playthrough. Broader performance claims still require a representative native run.
