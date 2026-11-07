# Layout editor controls

Updated: September 8, 2026 · Project: BrineSpace

## Objective and acceptance
Make layout editing more direct: default free placement, empty-canvas camera dragging,
entryway overlay visibility, and direct floor-decoration movement.

## Accepted decisions and constraints
Explicit saved placement preferences remain respected. Left-drag empty canvas pans;
Shift-drag selects a box. Existing middle-drag, wheel zoom and WASD remain available.
Floor finish stays a finish tool; clicking artwork selects its editing layer automatically.

## Current state
`scripts/room_layout_editor.gd` adds the defaults and canvas gestures. Entryway areas
and Clean preview are in the main toolbar; clean preview hides selection, hover,
alignment and clearance overlays while retaining room artwork and lighting.
`tests/test_layout_workflow.gd` covers camera movement without draft/history changes,
floor-decoration dragging from Objects and undo, default placement, and Shift marquee.
Recovery setup now stages unsaved drafts explicitly because switching rooms saves edits.

## Verification
Native workflow PASS: new controls plus copying, groups, ordering, lights, save/reload,
recovery and live room rendering. Scoped whitespace check passes. Clean preview
visually inspected at 1600x1000 in `output/layout-editor/clean-controls.png`.
Log: `output/layout-editor/controls-check.log`. Existing raw-image import warnings remain.

## Next action
Owner review during normal editing. No gameplay placement costs or expedition rules changed.
