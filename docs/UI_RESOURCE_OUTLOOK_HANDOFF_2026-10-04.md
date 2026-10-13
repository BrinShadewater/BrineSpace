# Project handoff

Updated: October 4, 2026 · Project: BrineSpace · Task: resource readability

## Objective and acceptance
Continue live UI/UX polish by distinguishing comfortable declines from near depletion, describing empty/recovering/full stores in words, and preserving access to supply explanations.

## Accepted decisions and constraints
Keep the muted palette, accepted hull/panel/card art and two-line resource bar. Estimates use the existing displayed next-cycle forecast, including its existing delivery averaging; no resource allocation, costs, failure rules or save changes. Integrity retains structural percentage and damage/flood warnings, rather than storage labels.

## Current state
- `scripts/main.gd`: shared presentation outlook gives steady/rising/falling/low/empty/refilling/full state and next reserve. HUD adds words only for relevant states; comfortable declines have a neutral border, two-cycle depletion uses muted amber, one-cycle depletion muted red. Empty improving essential supplies read REFILLING, while unused empty Water remains factual without urgent tint.
- Forecast hints round depletion up and avoid a zero-cycle countdown for already empty stores. Zero-change supply hints include forecasts and contribution navigation. Full stores explain delivery limits; vented Power note retained. Integrity forecasts use percentages and explain structure/flood distinction.
- Existing click/Enter resource details navigation retained.
- `tests/test_ui_resource_outlook.gd` and paired `.uid`, registered in `tests/index.json` hull-ui group.
- Backups, incremental review and two final native captures in `output/ui-resource-outlook-2026-10-04/`.

## Verification
Final native Godot4.7.2 resource fixture36 checks/0 failures: real forecast wiring for all stored-resource chips, depletion/refill/full states, longest caption geometry, keyboard supply-detail navigation and no resource spending when reading. Final decision UI suite PASS, including existing rounded depletion expectation. Two native captures reviewed at1600×900 with1920×1080 design scale. Incremental added-line whitespace check passes. Engine errors0; scratch APPDATA, all2931 owner non-log files unchanged.

Final logs/guards: `output/ui-integration-2026-09-30/resource-outlook-native-final` and `resource-outlook-decision-final`. Earlier35-check native fixture and decision suite passed before the explicit Integrity-specific treatment. Captures use controlled presentation reserves/rates; they demonstrate visual states, not a balance playtest.

## Next action
Source pass complete. Owner normal-play review remains visual acceptance. No export or commit requested; unrelated character work preserved.
