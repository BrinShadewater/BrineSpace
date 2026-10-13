# Project handoff

Updated: October 3, 2026 · Project: BrineSpace · Task: Wire the new UI into live screens

## Objective and acceptance
Integrate the component, navigation and badge auditions with existing game data
and actions. The owner requested implementation after the higher-density icon pass.
Native screen captures establish implementation quality; owner visual acceptance
is still theirs.

## Accepted decisions and constraints
Muted petrol, matte gunmetal, cream typography; existing understated panel frames,
original room cards and character portraits. Action buttons retain their hull
frames; draft utilities, filter chips and cycle speed controls retain plain styling.
No new gameplay rules, unlock semantics, save formats or monolith refactor.

## Current state
- `scripts/title_archive.gd`: shared section chips/tabs and menu breadcrumb,
  Codex filter/sort chips, reversible sort direction and 12-entry pagination;
  matching empty/reset state, discovery badges, actual Archived Data balance,
  blueprint/crew shop state badges and license disclosure. Existing selector API,
  transactions, hidden entries and focus handling retained.
- `scripts/main.gd`, `ui_badges.gd`: live room condition/material readiness badges,
  signature-based updates and assembly meter using the existing fleet progress
  calculation (architect and normal/bootstrap drone durations). Plain notifications
  use the shared notice; special synergy reveals retain their own content.
- `scripts/crew_portrait_panel.gd`, `journal_widgets.gd`: actual alive/assignment
  state and compact need readouts/meters; roster rows use the game's own portraits.
  Reserves use current storage, capacity and forecast tiles, with contribution
  actions, disclosure and existing room location links.
- `scripts/settings_panel.gd`, `ui_widgets.gd`, `synergy_reveal.gd`: matching
  confirmation content, notices, resource flow readouts and single-line pager.
  Existing display Keep/Revert, timeout and keyboard handling remain native.
- `scripts/ui_icons.gd`: 52 distinct 256px redraws now feed shared resource/action
  icons. Seven v2 draft utilities and the v2 Archived Data cartridge retained.
  All artwork references are whole paths; original sources/exports retained.
  59 raster imports built in an isolated minimal project; no unrelated imports.
  `tools/audition_badge_icon_density.gd` keeps an explicit legacy comparison map.
- `tests/test_ui_live_components.gd` plus UID and hull-ui test index entry;
  `test_hull_ui.gd` expects the new source dimensions. Paired script UIDs retained.
- Captures, selective before-script backups and review diff:
  `output/ui-live-integration-2026-10-03/`. Icon README updated for live selection.
  Work remains local in the existing dirty checkout; unrelated character work preserved.

## Verification
Godot 4.7.2 native shared-menu PASS, hull UI 175 checks PASS, workspace PASS.
Final wired live-component run: 64 checks, zero failures, including normal drone
versus architect assembly progress. Together with hull UI, 239 checks pass;
shared-menu and workspace suites pass separately.
Native Codex, shop, gameplay, compact gameplay, assembly, reserves, notification
and display confirmation captures reviewed. Toolbar rows compacted after review;
page counter and notice headings made single-line to avoid stacked text/minimum
height inflation. Bottom hardware remains accessible through existing sidebar
scrolling; hull UI checks that reachability at compact size.

Every completed run used scratch APPDATA: 2,931 real non-log owner files unchanged,
exit 0 and zero engine errors. Shared-menu exit retains the previously observed
1 CanvasItem RID / 2 ObjectDB warnings. Earlier failed custom fixtures (manual
search signal, missing recovered crew, empty focus target) were corrected; original
logs retained. The initial headless rendering test was stopped and is not evidence.
Logs/strict guards: `output/ui-integration-2026-09-30/live-ui-*`.

## Next action
Integration complete locally. Owner review in the editor is the next useful step.
No playable export, commit or publication was requested. Keep the accepted card
and portrait identity while refining the integrated screens.
