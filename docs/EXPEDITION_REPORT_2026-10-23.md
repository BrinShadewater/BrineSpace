# Reflective expedition report

Updated: 2026-10-23 / Project: BrineSpace

## Objective and acceptance
Make ending an expedition more satisfying through its accomplishments and lasting
progress. Owner chose the recommended reflective treatment.

## Accepted decisions and constraints
Keep the station visible, reuse existing room art and portraits, emphasize known
patterns and encountered characters, clearly separate expedition earnings from the
spendable balance, and offer progression/next-expedition actions. Preserve reward
math, hidden recipes, ownership rules, animation timing and artwork. No new rewards.

## Current state
`scripts/main.gd` builds the scrollable report with fixed action rows and a lighter
backdrop. `scripts/expedition_report.gd` (+ UID) renders illustrated highlights,
score/pattern reward breakdown, ownership-specific text and BRINE's closing.
Pattern earnings are already banked during play, not granted again by the report.
The existing overlay route opens progression; returning refreshes available Data.
Statistics and resource earnings remain accessible below the highlights.

`tests/test_expedition_report_native.gd` (+ UID), tests/index.json, and existing
learning/character-discovery UI assertions cover the revised presentation.

## Verification
- Native report: PASS, `output/test-runs/20261023-131111-native`.
  Checks score-only payment at ending, no presentation-side awards, known-pattern
  filtering, character ownership copy, existing art, compact bounds at 130% text,
  progression return/balance refresh, and a failure with no discoveries.
- Learning UI, menu recovery and overlay text: 3 PASS,
  `output/test-runs/20261023-131037-headless`.
- Reviewed normal, compact, scrolled details and failure captures in
  `output/expedition-report-20261023/`.
- Earlier native run passed assertions but logged a test teardown music error;
  fixture now stops the music processor before audio shutdown. Final log is clean.
- All Godot runs used runner-isolated APPDATA. Protection receipts:
  `D:/bs-tutorial-20261021/ending-before.json` and `ending-after.json`:
  2,971 owner profile files unchanged; signed export unchanged.
- Existing character-discovery fixture assertions were adapted; that older full
  native fixture was not rerun. The new native fixture exercises recap portraits
  and ownership wording directly.

## Next action
Owner review of a naturally completed expedition. No export produced. Long lists
scroll while navigation stays visible; no unskippable reward animation is added.
