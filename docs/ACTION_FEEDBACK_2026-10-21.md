# Workplace feedback and cancellation pass

Updated: October 21, 2026 · BrineSpace

## Objective and acceptance
Find actionable control-state bugs and unnecessary interface work without changing
gameplay, costs, artwork or animation timing.

## Accepted decisions and constraints
Expose the existing primary-work restriction for crew assigned to Moonbay. Keep
the model guard intact. Cancellation is a presentation-only action; no full station
refresh is required. No export or real-profile writes.

## Current state
- `scripts/crew_work_panel.gd`: Moonbay assignment disables the primary-work action,
  labels it ASSIGNED TO MOONBAY and explains releasing the Moonbay assignment first.
  Previously the enabled button called a correctly rejecting model method silently.
- `scripts/main.gd`: cancelling scrap calls `_refresh_inspector` instead of
  `_refresh_all`, avoiding unrelated resource/card/log/routing/menu refreshes.
- Extended `test_crew_primary_work`, `test_inspector_refresh` and native worksite
  controls coverage. No gameplay methods or mission behavior changed.

## Verification
Both new assertions fail before the changes:
`output/test-runs/20261021-232731-headless/`.
Primary work, inspector and room scrap fixtures pass afterward:
`output/test-runs/20261021-232937-headless/`.
Cancellation instrumentation asserts zero full refreshes and exactly one inspector
refresh, unchanged resources/room and restored Scrap label. This is work-scope
evidence, not an FPS or measured frame-time claim.

Native fixture passes: `output/test-runs/20261021-233027-native/`. Normal and compact
Moonbay workplace captures are in `output/worksite-controls-20261021/`; compact
capture visually reviewed. Assignment release restores the enabled action. The
fixture injects assignment state; this is not a complete Moonbay mission playthrough.
Scoped whitespace check passes.

Room-scrap assertions pass but its headless run emitted four ObjectDB/two resource
shutdown warnings. An isolated verbose follow-up exited zero without those warnings
(`D:/bs-tutorial-20261021/scrap-verbose.log`; one orphan StringName notice). Cause is
unresolved; prior successful cleanup does not establish absence of intermittent
shutdown warnings. No runtime leak fix is claimed. Other final test logs are clean.

Protection receipts: `D:/bs-tutorial-20261021/actions-before.json` and
`actions-after.json`; all runs use scratch APPDATA.

## Next action
Use the assignment explanation during an ordinary Moonbay session. Investigate the
intermittent scrap-fixture shutdown warnings if they reproduce with verbose output;
do not treat them as a demonstrated gameplay leak.
