# Tutorial bug, performance and polish pass

Updated: October 21, 2026 · BrineSpace

## Objective and acceptance
Review the tutorial/Settings for bugs, unnecessary startup work and presentation issues. Preserve mechanics, artwork and exact animation timing.

## Accepted decisions and constraints
Focus on the current illustrated-guide work. No broad renderer refactor, export or player-save edits. Native timings are diagnostic observations, not a frame-rate claim or flaky timing gate.

## Current state
- Found that Settings built every guide section while visible, decoded/uploaded all five pictures, then hid the page. `settings_panel.gd` now constructs the guide only on first selection. It still opens directly if it was the current category, and uses the existing text-scaling/key-hint rules.
- `tutorial_picture.gd` gives the enlargement dialog the Settings panel colours. Existing captions, Escape, focus/scroll restoration and duplicate protection remain.
- Added `tests/test_tutorial_cost.gd` with paired UID and registered it in the native tutorial subsystem. The regression gate asserts no guide UI or textures for an unopened guide. Timing is logged without a threshold.

## Verification
Five consecutive native Settings builds per version, one before/after order on this machine. Before: 232.143, 173.425, 170.422, 166.962, 167.307 ms; five tutorial textures in every sample. After: 80.256, 32.574, 33.252, 32.359, 32.953 ms; zero tutorial textures in every sample. This measures synchronous archive construction, not total time-to-visible, cold disk performance or gameplay FPS. Opening the tutorial still pays for its images.

Baseline receipt: `output/test-runs/20261021-121835-native/`. Final native cost, guide and gameplay fixtures all pass: `output/test-runs/20261021-121856-native/`. Compact 130% enlarged-picture capture reviewed; scoped diff whitespace check passes. No additional behavioral regression found in this scope.

All runs used isolated APPDATA. Owner fingerprints: `D:/bs-tutorial-20261021/perf-before.json` and `perf-after.json`. No export or signed delivery changed.

## Next action
Use the guide in a fresh-player opening session. Future optimization should measure first-use tutorial cost only if it proves disruptive; do not infer that gameplay upload hitches are fixed by this menu improvement.

## Follow-up: Settings lifecycle
Objective: check reopening, live text scaling and Settings rebuilds after reading the guide. Preserve the existing image lifetime rather than introducing a persistent texture cache.

Extended `tests/test_tutorial_guide.gd` to exercise repeated 100/130% slider changes, the actual controls-default reset path, category focus restoration, lazy rebuilding with refreshed key hints, and reopening the remembered Tutorial category with text scaled once. Both normal and compact window cases pass. No new runtime defect found; the only source adjustment corrects the Settings construction comment.

Verification: native guide fixture passes with zero failures in `output/test-runs/20261021-133606-native/`; scoped whitespace check passes. APPDATA was isolated. Protection receipts: `D:/bs-tutorial-20261021/lifecycle-before.json` and `lifecycle-after.json`. No gameplay behavior, artwork, export or signed delivery changed. The fresh-player opening session remains the next useful acceptance step.
