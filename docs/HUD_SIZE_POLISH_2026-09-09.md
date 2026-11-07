# HUD size polish handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: larger navigation icons and compact cycle controls

## Objective and acceptance
Enlarge the four top-right navigation icons and reduce the time/cycle controls panel height.

## Accepted decisions and constraints
Navigation badges increase from 44 to 60 design units, using their existing source art. The header gains room for the icons and captions. Pause and speed share a row; cycle controls retain their meter and expandable view details with tighter padding.

## Current state
Changed `scripts/navigation_badge.gd`, `scripts/main.gd`, and native capture coverage in `tests/test_navigation_badges.gd`. Existing UID files retained. Local source only.

## Verification
Native Godot 4.6.1 navigation fixture passes, including badge redraw behavior, journal/diagnostics actions, and 1600/960 HUD captures. Reviewed both HUD sizes and scrolled cycle panel. Evidence: `output/navigation-1600.png`, `output/navigation-960.png`, `output/hud-size-polish/cycle-panel.png`, and native log in `output/hud-size-polish`. Existing raw-image loading warnings remain.

## Next action
Owner visual review. New export not built.
