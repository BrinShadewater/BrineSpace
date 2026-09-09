# Sidebar readability handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: quieter sidebar and readable inspector

## Objective and acceptance
Remove Construction and Flood/Clear sidebar buttons, compact controls and reduce inspector scrolling with more readable text.

## Accepted decisions and constraints
Removed visible status buttons, retaining their internal references. Construction and flooding mechanics remain. Compact both hardware and cycle controls. Inspector uses Segoe UI with system fallbacks, brighter text, 300-unit reading area instead of 210, tighter panel margins, fewer blank lines and no duplicated class row.

## Current state
Changed `scripts/main.gd` and `scripts/hardware_panel.gd`. Existing UIDs retained. No export built.

## Verification
Native navigation fixture passes on final source (explicit PASS, exit 0); reviewed current screenshot and two-size captures. Native hardware fixture passes including eight controls, state capture, lever drag and two-size bounds. Evidence: `output/sidebar-readability` logs and current `output/navigation-1600.png`. Initial navigation invocation exited before its PASS marker and was rerun; final text-spacing edit had an indentation error corrected before the passing final run. Existing raw-image warnings remain.

## Next action
Owner visual review; long room-specific reports still scroll. No new executable.
