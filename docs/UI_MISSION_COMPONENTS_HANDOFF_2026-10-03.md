# Project handoff

Updated: October 3, 2026 · Project: BrineSpace · Task: Continue live UI integration

## Objective and acceptance
Continue wiring the matching UI into remaining live controls. This pass covers
Diving Airlock, Moonbay and the root-owned restoration overlay. Owner visual
review remains theirs; no export or publication requested.

## Accepted decisions and constraints
Preserve original cards/portraits, existing panel frames, matte hull action buttons,
muted petrol/gunmetal surfaces and existing gameplay/save semantics. Real caller
state drives all readings. Reduced Motion removes restoration activity animation.

## Current state
- `scripts/airlock_panel.gd`: helmet/refill share one compact row. Current water
  and pressure use compact badges, derived from `AirlockCycle.pose`; hatch phase,
  actual obstruction feedback and power-held explanation remain visible. Refill,
  hatch and expedition actions receive existing higher-density glyphs.
- `scripts/moonbay_panel.gd`: compact locker controls, matching action glyphs,
  current phase/water/recall/damage badges and phase-duration progress track.
  Existing dispatch, recall and repair handlers/costs retained. Active mission
  pickers now display the actual pilot/order/destination, including an exhausted
  contact during return. Idle no-contact state has explicit disabled text without
  inventing a selectable destination. Eligible idle contacts remain filtered.
- `scripts/restore_overlay.gd`: shared loading card/theme with original BRINE text,
  indeterminate activity and Reduced Motion handling. Root ownership, input block,
  process mode and real checkpoint restoration remain unchanged.
- `tests/test_ui_mission_components.gd` and UID: native integration/geometry/action
  coverage, registered in hull-ui group. Existing script UID pairs retained.
- Backups, review diff and four captures in
  `output/ui-mission-integration-2026-10-03/`. Existing dirty checkout and unrelated
  character work preserved. No monolith refactor, new asset generation or commit.

## Verification
Native Moonbay assignment, staged checkpoint restoration and live airlock surface
retention suites pass, zero failures/errors. Staged restoration used 6 loading
frames and preserved the hidden/disabled station plus final Continue focus.
Final mission UI run: 32 checks pass, zero failures/errors, including real action
callbacks, empty contacts, active pilot/order synchronization, depleted destination
retention, compact horizontal bounds and Reduced Motion. Existing assignment suite
passed before the final picker-display fixes; the final native fixture covers those fixes.
Native restoration, airlock, Moonbay and compact Moonbay captures reviewed.
All completed runs used scratch APPDATA; all 2,931 real non-log owner files unchanged.
Logs/guards: `output/ui-integration-2026-09-30/mission-ui-*`.
The first new test used the wrong settings initialization method and failed parse;
corrected to the existing API. Failed log and profile guard retained.

## Next action
This continuation pass is complete locally; final updated captures reviewed.
Owner review in the editor follows this source integration; no release build requested.
