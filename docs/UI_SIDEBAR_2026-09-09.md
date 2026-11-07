# UI sidebar and navigation polish

Updated: 2026-09-09 - BrineSpace

## Objective and acceptance
Center and evenly space the four top-right buttons; enlarge the inspector and station controls; show TIME / CYCLE with a cycle counter.

## Accepted decisions and constraints
Preserve existing station behavior and pause/speed controls. Slightly widen the sidebar (36 design pixels) and increase inspector reading height (30 pixels).

## Current state
Updated scripts/main.gd, scripts/navigation_badge.gd and scripts/hardware_panel.gd. Navigation buttons share equal widths; station switch artwork and hit areas are larger. The lower panel displays TIME / CYCLE, the current cycle number, pause state and countdown. Updated tests/test_navigation_badges.gd with counter and geometry coverage.

## Verification
Native Godot navigation test passes at 1600x900 and 960x540. Screenshots visually reviewed: output/navigation-1600.png and output/navigation-960.png. All three sidebar panels fit without scrolling in the default state. Counter refresh, paused timer, equal button widths and panel bounds checked. No script errors; existing raw-image loading warnings remain.

## Next action
Ready for owner review in game. No export or commit requested.

## Owner follow-up: taller inspector
Removed the visible Locate Room & Connections action, retaining its internal selection anchor for existing focus links. Increased inspector minimum height from 430 to 520 design pixels and let the reading area fill available height. Native navigation and bounds checks pass at 1600x900 and 960x540; reviewed the taller inspector capture. Station and time controls remain visible.

## Owner follow-up: tutorial removal and icon spacing
Sidebar tutorial stays hidden, including on new-player saves. Top navigation retains equal-width buttons, with centered 56-pixel badges, 8-pixel upper inset and extra caption padding. Updated main.gd, navigation_badge.gd and the navigation test. Native checks pass at 1600x900 and 960x540, including new-player tutorial absence, icon centering and bounds; 1600 capture visually reviewed. Evidence: output/ui-layout-spacing.log and output/navigation-*.png. Ready for owner review.
