# Project handoff

Updated: October 1, 2026 · Project: BrineSpace · Task: Matching UI patterns, second set

## Objective and acceptance
Continue the matching UI work with notifications, confirmations, portrait rows,
loading/status, empty/filter states and shortcut hints. Native1440x1100 audition
reviewed. These new patterns are candidates for owner review; creating reusable
patterns does not authorize changing their gameplay semantics.

## Accepted decisions and constraints
Muted gunmetal/petrol and cream text; previous panel chrome and action hull buttons.
Preserve original portraits/card art, existing input bindings and game behavior.
Components receive caller data/actions. No fake progress wired into gameplay,
new confirmation requirements, character artwork replacement or broad UI refactor.

## Current state
- `scripts/ui_widgets.gd`: reusable text labels, notice cards, empty states,
  caller-driven loading meters, confirmation action layouts, keycaps and portrait
  rows. Notices have ordinary Body containers for caller-owned buttons/data.
  Confirmation controls expose CancelAction/ConfirmAction with no implicit action.
  Portrait factory accepts actual caller Texture2D; examples use Architects' own
  selection_portrait for Bill/Veld. Shortcut examples use saved key bindings.
- `scripts/title_archive.gd`: Codex no-match state uses the shared empty card;
  existing ResetCodexSearch caption/callback and filter/search behavior preserved.
- `tools/audition_ui_patterns.gd` and paired UID: second native sheet plus actual
  compact Codex rendering and filter-reset interaction checks. First component
  audition remains available separately; no prior source or artwork replaced.
- Captures: `output/ui-components-extended-2026-10-01/components-audition.png`
  and `codex-empty-state.png`, with original changed-script backups and full logs.

## Verification
12 native checks pass,0 engine errors. Checks include supplied portrait identity,
selected treatment, loading value, caller confirmation connections, sheet bounds,
actual Codex empty-state integration,1280x720 action bounds, successful captures,
and restoration of entries after clearing the filter. Sheet and actual compact
Codex visually reviewed. Final scratch APPDATA run's strict2931-file owner profile
guard passes unchanged. Existing nine/175/shared-menu checks from the first set
remain evidence for that revision; not rerun or falsely counted as new checks.
All runtime/helper UIDs retained, new audition tool paired. No commit/export/upload.

## Next action
Owner review of the second sheet. Reuse these factories for future message/list
views while keeping their existing data and action handlers. Most new patterns
are reusable candidates; only the existing Codex no-match flow was integrated here.
