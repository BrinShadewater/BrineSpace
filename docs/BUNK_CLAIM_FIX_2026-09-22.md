# Shared bunk destination fix

Updated: September 22, 2026. Project: BrineSpace.

## Objective and acceptance
Prevent two crew choosing the same bought lower bunk while it is empty but already
has an incoming occupant. Preserve physical avoidance and animation behavior.

## Accepted decisions and constraints
No furnishing or save-format changes. Only reviewed bought-bunk stations use this
claim check; existing unrelated activity choices retain their behavior.

## Current state
scripts/bill_npc.gd checks bunk_claimed before searching a candidate route. Active,
living peers claim the same contact through their existing queued destination or
lie/sleep/rise stage. Self is excluded. Abandoning a route releases its claim with
no new persistent registry. tests/test_branforth_bunk.gd includes two-crew choice,
route-abandonment, dead-peer and self-exclusion assertions.

## Verification
Evidence: output/layout-default-audit-2026-09-21/.
- bunk-contention-probe.log reproduced both crew choosing (7997.23, 8603.996).
  The occupied-bed check already avoided the bed: this was an unnecessary travel
  issue, not evidence of two simultaneously rendered sleepers.
- bunk-contention-fixed.log shows a different second destination while queued and
  while occupied.
- bunk-claim-controller.log passes the expanded native test and fourteen equipped/
  bare disk restores, pause, interruption and completion with zero failures.
  Editor-imported PNG reference reads emit raw-image export warnings in this test;
  this is a native source-pixel comparison, not packaged-export validation.
- Focused git diff whitespace check passes.

## Next action
Continue remaining bought-bunk cast profiles and broader autonomous gameplay.
This fixture does not establish a full expedition or multi-room performance result.
