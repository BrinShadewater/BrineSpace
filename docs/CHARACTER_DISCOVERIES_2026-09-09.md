# Character selector and recap

Updated: 2026-09-09 - BrineSpace

## Objective and acceptance
Companion portraits match architect portraits; the end-of-loop recap includes character discoveries.

## Accepted decisions and constraints
Both portrait areas are 160x170 design pixels, with aspect preserved and linear filtering. Discoveries mean first-time character unlocks this loop, including architects and companions. Existing unlocked starters are not counted again.

## Current state
Changed architect_selection.gd, main.gd, cryo_recovery.gd, companions.gd and run_save.gd. Recap includes Characters discovered with names or None. Optional checkpoint data preserves discoveries on Continue; old checkpoints default to no recorded character discoveries. New loops clear the list. Character unlock rules remain unchanged.

## Verification
Companion recovery tests pass, including first recovery, Continue and new-loop reset. Native test_character_discovery_ui.gd passes: portrait dimensions and action visibility at 1600x900 and 960x540, recap names, Continue and legacy checkpoints. Selector and recap screenshots reviewed in output/companion-picker-1600.png and output/character-discovery-recap.png. Headless companion run retains the existing two-resource shutdown warning.

## Next action
Ready for owner review. No executable rebuild or commit requested.
