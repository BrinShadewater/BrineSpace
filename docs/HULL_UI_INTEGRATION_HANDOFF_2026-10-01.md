# Project handoff

Updated: 2026-10-01 · Project: Brine Space · Task: install auditioned UI

## Objective and acceptance

Install the new UI family in the live Godot game. Owner authorized integration after auditions and a whole-family polish pass. Native visual review completed; owner review of the installed result remains available. This is a source installation, not a playable export or release claim.

## Accepted decisions and constraints

Thin matte grey hull rails, tiny bolts, dim blue pressed / red disabled lights, petrol interiors, muted highlights/meters, bold readable live text. Preserve original room cards, room art and character portraits. Top-left portrait strip expands details rightward; enlarged inspector card and compact lower actions. Fan without background is the fresh-profile default, with fan/row, frame and hide/show controls retained. Existing explicit saved preferences are preserved. Later owner decisions still govern station hardware controls and no selected-room outline.

## Current state

60 unique 32px transparent icons plus four source atlases in `brineui/hull-ui-v1`; whole-path registry `scripts/ui_icons.gd`. New native skin `ui_hull_style.gd`, crew flyout `crew_portrait_panel.gd`, paired UIDs. Shared menu/title/HUD styling, resource colors/icons, inspector actions, crew workplace row, draft preferences and terminal frame updated. Existing hardware controls retain their authored tactile artwork; other panels use the new shared chrome. Native icon imports were prepared in a minimal project to avoid a full repository import sweep. `output/.gdignore` prevents editor recursion into generated snapshots. `draft_card.gd` now checks optional art metadata before reading it, avoiding errors from the workspace fixture's bare card. Test registered as the `hull-ui` subsystem in `tests/index.json`.

Pre-existing changes were preserved. Backups of touched existing sources and full logs: `output/ui-integration-2026-09-30/`. No commit, publish or export performed.

## Verification

Godot 4.7.2 native hull fixture: 145 checks PASS, including icon dimensions/transparency, shared button skin, title/codex lifecycle, inspector/action bounds, compact portraits and live details, and draft toggle round trips without resource mutation. Reviewed title, codex and gameplay at 1600x900 and gameplay at 1280x720. Shared-menu regression PASS (native); workspace regression PASS with zero errors after the metadata guard. Owner profile fingerprints before/after checks: all 2,914 non-log files unchanged. Shared-menu shutdown emitted small RID/ObjectDB leak warnings; no engine errors. Failed initial import/native/test attempts are retained, including the corrected fixture property typo; no failing attempt is counted as a pass.

Title-screen regression PASS (native, repeated mouse clicks and modal lifecycle). Targeted whitespace check passed.

## Next action

Owner can run F5 and review the installed style. Integration and targeted checks are complete. Release validation is required only when a playable export is requested.
