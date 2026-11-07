# Expedition report interface design handoff

Updated: 2026-10-23 / Project: BrineSpace

## Objective and acceptance
Owner requested a well-designed expedition ending that matches the existing interface.
Build on the accepted reflective report and existing terminal/archive visual language.

## Accepted decisions and constraints
Reuse terminal frames, hull action buttons, Barlow fonts, inset surfaces and status
badges. Keep existing room art/portraits, rewards, hidden recipes and timing.

## Current state
- scripts/main.gd: regular terminal frame for all summaries, larger two-column
  layout, persistent earnings/figures column, fixed closing and single action row.
  Pixel-frame preference continues to use the existing large terminal art.
- scripts/expedition_report.gd: large reward amount and compact breakdown; grouped
  pattern and roster inset cards with shared UI badges. BRINE closing sits outside
  scrolling content. Shop returns update balance and ownership in place; rebuilding
  rows temporarily reset the scroll range in the new layout and is now avoided.
- tests/test_expedition_report_native.gd: adapted to the new earnings location and
  verifies scroll position within updated content bounds after an actual purchase.

## Verification
Final native fixture PASS: output/test-runs/20261023-132408-native (clean final log).
Normal 1600x900 and compact 1280x720 at 130% text captured and reviewed, along with
scrolled details and empty failure: output/expedition-report-design-20261023/.
Purchase/balance/ownership, unchanged earnings, known-pattern filtering, artwork,
zero earnings and panel bounds remain covered. Focused whitespace check passed.
An earlier run caught an incorrectly inserted heading during editing (fixed before
visual review); subsequent runs isolated a genuine scroll-reset issue after purchase.
Final return updates existing rows and passes the scroll assertion.

Runner isolated APPDATA throughout. Protection receipts in
D:/bs-tutorial-20261021/ending-design-before.json and ending-design-after.json:
2,971 owner profile files unchanged; signed ZIP unchanged. No export produced.

## Next action
Owner visual review in a naturally completed expedition. The fixed terminal frame
remains spacious for short or empty records; long accomplishment lists scroll.
