# Project handoff

Updated: October 1, 2026 · Project: BrineSpace · Task: Matching secondary UI components

## Objective and acceptance
Make additional UI components match the accepted matte gunmetal, muted petrol and
cream typography. Native 1440x1000 audition shows eight component families at real
control sizes. Owner visual acceptance of this new set remains pending.

## Accepted decisions and constraints
Keep original room/card art, portraits and previous understated panel frames.
Illustrated hull fittings stay on action buttons; smaller controls use thin inset
surfaces and restrained state indicators. Preserve existing gameplay and settings
semantics. No generated raster art or external publication needed for native widgets.

## Current state
- `scripts/ui_component_style.gd` plus paired UID: reusable fields, tabs, menu
  surfaces and badges, SVG-rendered at 2x display density with bounded cached art.
- `scripts/ui_widgets.gd` plus UID: theme palette, recessed tracks, check/radio
  glyphs, metal switches, dropdown arrows, scroll rails and reusable status badge
  factory. Online, idle, warning and fault variations use small dim indicators.
- `scripts/title_button_style.gd`: shared menu/game theme applies these styles;
  existing panel frames and action-button hull styles retained.
- `scripts/settings_panel.gd`: existing settings switches use shared matte switches.
  Toggle/check backgrounds are frameless, with quiet hover feedback.
- `tools/audition_ui_components.gd` plus UID: reproducible native audition and nine
  layout/style/interaction/export checks. Saves the full sheet to
  `output/ui-components-2026-10-01/components-audition.png`.
- Eight families: tabs, search/entry, sliders/meters, toggles/checks, dropdown/menu
  rows, status badges, tooltip/notice surfaces and scroll/list rows. Badge/list
  factories are reusable components; this task does not invent new gameplay rows.

## Verification
Nine native audition checks and175 existing UI checks pass. Shared menu regression
passes, including modal focus traversal and settings persistence. Final engine
errors0; shared-menu exit also reports1 CanvasItem RID and2 ObjectDB instances
leaked, retained in the original log without asserting cause. Final runs all use
scratch APPDATA and their strict2931-file real-profile guards pass unchanged.
Native sheet visually reviewed; no oversized hull frames on toggles/checks.
First audition failed on a misindented helper line; corrected before final runs.
All changed/new scripts retain paired UIDs. No commit, export or upload requested.

## Next action
Owner review of the component sheet and live menu controls. Continue using shared
widgets for new screens; retain card/art/portrait identity. Evidence and original
script backups in `output/ui-components-2026-10-01/`.
