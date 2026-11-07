# Project handoff

Updated: October 4, 2026 · Project: BrineSpace · Task: control explanations and focus feedback

## Objective and acceptance
Continue the accepted UI/UX improvements with readable, current explanations for unavailable actions and clearer keyboard focus. Implemented in the live interface and checked with native rendering.

## Accepted decisions and constraints
Retain matte hull action buttons, understated panel frames, original cards/portraits and plain draft/cycle utility controls. No persistent last-click outline on the menu. This pass changes presentation and explanations; existing availability predicates, costs and action handlers remain unchanged. Preserve concurrent character work and owner saves.

## Current state
- `scripts/title_button_style.gd`: disabled buttons now support styled hover hints; keyboard focus also reveals hints. Unavailable heading, Barlow text, live `set_hint` updates and safe text restoration. Hints measure after layout, shrink with changing text, stay inside the viewport and sit above bottom-edge controls. Plain controls have a muted focus underline.
- `scripts/airlock_panel.gd`: chamber/locker/expedition explanations identify suspended rooms, power, active cycles, obstructions, ongoing locker work and crew conditions; suspended status no longer says only Power Off.
- `scripts/moonbay_panel.gd`: launch, repair, locker and recall hints explain mission/contact/crew/power/pause conditions and the actual Metal shortfall.
- `scripts/crew_work_panel.gd`: assignment hints identify unavailable crew or the current workplace owner and how to free the assignment.
- `scripts/main.gd`: inspector hints use live updates; room operation/doors/scrap/repair explain concluded expeditions, intact hulls, queued repairs and missing Metal.
- `tests/test_ui_feedback.gd` and paired `.uid`, registered in `tests/index.json` hull-ui group.
- Before-edit backups, reviewed incremental diff and three reviewed native captures: `output/ui-feedback-2026-10-04/`.

## Verification
Native Godot 4.7.2 at 1600×900 with 1920×1080 design scale: feedback fixture 24 checks, mission UI 32 checks, hull UI 175 checks; all 231 passed with zero logged errors. Shared menu also passed earlier in this pass; existing exit-only CanvasItem/ObjectDB leak warnings remain. Scoped whitespace check passed. Reviewed disabled hint, keyboard underline and gameplay inspector captures.

Each test used scratch APPDATA and verified all 2931 owner non-log files unchanged. Logs and guards are in `output/ui-integration-2026-09-30/` (`feedback-native-reviewed`, `feedback-missions`, `feedback-hull`, `feedback-shared-menu`). Initial feedback fixture incorrectly retained an eligible survey contact; clearing that fixture contact resolved its one failed assertion. No gameplay change was made to satisfy it.

## Next action
This pass is complete. Owner play review can assess hint timing and wording during normal play; no remaining required implementation or checks for this pass. No commit or playable export created.
