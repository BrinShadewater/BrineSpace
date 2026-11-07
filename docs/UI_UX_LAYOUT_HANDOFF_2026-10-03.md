# Project handoff

Updated: October 3, 2026 · Project: BrineSpace · Task: Pinned controls, inspector hierarchy and readability

## Objective and acceptance
Implement the three prioritized improvements accepted by the owner: essential
controls stay visible, inspector actions lead secondary information, and small
resource/card text becomes easier to read. Native compact/tall-panel evidence
reviewed; final owner visual acceptance remains theirs.

## Accepted decisions and constraints
Keep the original right-side card, original art/portraits, previous panel frames,
muted palette, hull action buttons and plain speed/utility controls. Preserve all
gameplay, costs, mission handlers and save behavior. No export or commit requested.

## Current state
- `scripts/main.gd`: new anchored SideDock holds scrolling inspector/hardware above
  a fixed Time/Cycle panel. Pause, speed and View controls use their original
  handlers and remain accessible at every sidebar scroll position.
- Summary contains one state badge plus contextual remedy/location; redundant
  status label and CURRENT STATUS heading removed. Room actions precede the
  collapsed Forecast & Room Details disclosure. Existing forecast, resource,
  special-property, synergy and link text retained in the detail pane.
- Details stay expanded across refreshes of the same selection and collapse for a
  newly selected room/card. Non-card selections keep their existing information
  immediately visible. Expanded reading viewport is 180 design pixels, providing
  at least six text lines; existing inner scroll/focus behavior retained.
- `scripts/crew_work_panel.gd`: assignment notes use a separate collapsed disclosure
  without changing the primary job action or data. `airlock_panel.gd` and
  `moonbay_panel.gd`: secondary status text increased from 12 to 14 design pixels.
- `scripts/draft_card.gd`: title sizes 16/14/13, rule/build/cost/note text 14;
  cost icons match 14px text, notes retain their two-line layout with 40px space.
  Existing adaptive card sizing and all card art/frame/layering retained.
  HUD resource labels increase from 12 to 14; inspector summary from 16 to 18.
- `tests/test_ui_ux_layout.gd` and paired UID plus hull-ui group entry. Existing hull
  tests now check badges and fixed control ownership, replacing retired heading
  and sibling-order assumptions. Existing script UID pairs retained.
- Backups, review diff and five native captures:
  `output/ui-ux-pass-2026-10-03/`. Unrelated dirty-checkout character work preserved.

## Verification
50 final native UX checks pass, covering collapsed/expanded context, retained
refresh state, six-line reading area, action order, pinned geometry at1600x900 and
1280x720, scrolling, Pause/speed handlers, resource text bounds and captures.
Existing hull UI175, live components64 and mission UI32 checks pass (321 total
across the pass). Final workspace suite passes after the reader-height adjustment.
Five final UX captures reviewed, plus existing live screen captures.
All runs use scratch APPDATA; all2,931 owner non-log files remain unchanged.
Final engine errors0. Logs/guards: `output/ui-integration-2026-09-30/ux-layout-*`.

Initial failures retained: moving the reader changed its parent; the control lookup
was corrected to the preview container. Old CURRENT STATUS expectation updated
for the accepted one-badge hierarchy. New test's incorrect speed-button field name
corrected to the existing API. Failed native runs stopped after their errors;
no failed or stopped run counted as passing evidence.

## Next action
Source implementation complete. Owner review in the editor is next. Continue
with disabled-action explanations or tooltip/focus polish if requested; this pass
implements the three explicitly prioritized layout/readability improvements.
