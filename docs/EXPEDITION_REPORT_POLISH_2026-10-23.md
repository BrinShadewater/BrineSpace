# Expedition report polish handoff

Updated: 2026-10-23 / Project: BrineSpace

## Objective and acceptance
Polish the accepted reflective ending, especially purchase feedback and clarity.

## Accepted decisions and constraints
Keep existing art, exact animation timing, rewards and discovery rules. Make the
report agree with actual shop state. Existing reversible-work authorization applies.

## Current state
- scripts/expedition_report.gd: available Data comes from MetaShop.balance, which
  subtracts research and purchases; report refresh restores scroll after rebuilding
  ownership entries. Shorter reward explanation, WHAT CARRIES FORWARD, consistent
  Upgrades & Unlocks wording, zero earnings without a plus sign.
- scripts/main.gd: overlay return refreshes the report; no-cascade figure is --.
- tests/test_expedition_report_native.gd: actual isolated Josh purchase validates
  balance, ownership refresh, preserved scroll, unchanged expedition earnings;
  empty failure checks zero earnings. Existing art/layout/accounting checks remain.

## Verification
- Reproduced both stale ownership and incorrect spendable balance before fixing:
  output/test-runs/20261023-131608-native, two expected failures.
- Final native fixture PASS, clean log:
  output/test-runs/20261023-131651-native.
- Captures: output/expedition-report-polish-20261023; reviewed compact 130% text
  and empty failure. Normal and scrolled details captured too.
- Runner isolated APPDATA. Protection receipts in
  D:/bs-tutorial-20261021/ending-polish-before.json and ending-polish-after.json:
  2,971 owner profile files unchanged; signed ZIP unchanged.
- Focused diff whitespace check passed. No additional broad suite required for
  these changes; previous report regression results retain their original scope.

## Next action
Owner review during a naturally completed expedition. Source changes only.
