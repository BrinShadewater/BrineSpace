# Intro Continue handoff

Updated: September 8, 2026 · Project: BrineSpace · Task: readable awakening intro

## Objective and acceptance
The owner requested that the intro after Awaken remain until Continue is pressed.

## Accepted decisions and constraints
Show the complete transmission before scene initialization; remove timed dismissal and any-click skipping. Continue becomes available when the station is ready. Reading pauses gameplay. Larger text can scroll. Archive recordings use an explicit Return to Archive button.

## Current state
Changed `scripts/loading_transition.gd` and `tests/test_loading_transition.gd`; existing UIDs retained. No gameplay balance or save-format changes. Local source only; no new export.

## Verification
Native Godot 4.6.1 loading fixture passes (exit 0, no script errors): new awakening, restored checkpoint, early Enter rejection, real GUI Continue click, ready-state Enter, paused reserves, resumed processing, reduced motion and archive dismissal. Reviewed native captures before loading and after readiness; full intro and button fit at 1600×900. Evidence: `output/intro-continue/test_loading_transition-native-1788937070916299700.log` and PNGs. Existing raw-image export warnings remain. The passing fixture isolates external input while exercising its own GUI click in viewport coordinates.

## Next action
Owner normal-play review; packaged validation remains pending if a new executable is required.
