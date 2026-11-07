# Project handoff

Updated: October 1, 2026 · Project: BrineSpace · Task: Matching navigation/information components

## Objective and acceptance
Keep making matching UI elements. Third native sheet adds filter chips, resource
readouts, breadcrumb navigation, sorting, pagination and expandable details.
1440x1000 audition reviewed; owner visual acceptance remains pending.

## Accepted decisions and constraints
Same muted petrol/gunmetal/cream palette, thin matte surfaces and readable state.
Preserve original game card/portrait art and shared resource icons. These are
reusable controls and candidates, not new navigation or progression mechanics.
Caller actions/data remain caller-owned; no existing screen behavior replaced.

## Current state
- `scripts/ui_widgets.gd` (existing UID retained): chip factory, exclusive filter
  choices in HFlowContainer, icon/amount/delta resource tiles, breadcrumb controls,
  callback pagination, collapsible caller content and callback sorting. Native
  up/down chevrons replace fullscreen-style expand glyphs for the new disclosure.
- Filters clamp selection and wrap; sort tracks one column and toggles direction;
  page counts clamp to at least one safe disabled page, callbacks fire on movement.
  Breadcrumbs expose path-index actions and a noninteractive current label.
- Resource tiles use original icons plus the current Archived Data badge and1.18
  display brightness; negative deltas remain explicit. Values are caller supplied.
- `tools/audition_ui_navigation.gd` and paired UID: native rendering and27 behavior,
  boundary, identity, geometry and export checks. Caption families fit1440x1000;
  extra320px filter fixture verifies wrapping and every chip stays inside width.
- `output/ui-navigation-2026-10-01/components-audition.png`, before-script backup,
  original first/final logs and strict profile guards preserved. No commit/export.

## Verification
27 native checks,0 failures,0 engine errors. Original portraits/cards untouched.
Final scratch APPDATA run preserves all2931 real non-log profile files. Native
sheet visually reviewed. First audition failed layout bounds: autowrapping a
shrink-width breadcrumb label stacked its letters vertically. Current labels and
separators now explicitly single-line/vertically centered; sheet fits normally.
First failed log's old audition harness printed PASS despite recording an error;
final navigation harness accumulates failures and exits nonzero for any failure.
This third set does not rerun or recount earlier9/12/175 checks as new evidence.

## Next action
Owner review of third sheet. Adopt factory controls in existing screens only with
those screens' current data/handlers, preserving the accepted layout and behavior.
Existing first and second audition tools/captures remain available.
