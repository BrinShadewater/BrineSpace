# Hull condition art replacement

Updated September 30, 2026. BrineSpace source checkout.

## Objective and acceptance
Continue original asset replacements while preserving station perspective,
matte materials, world size and condition readability. Five hull states installed;
agent source/native visual review completed. Owner review remains separate.

## Accepted decisions and constraints
Keep the 48-world-unit tile footprint and existing leak/drip anchors. Water and
sparks stay separate. Damage rates, paid repair, crew behavior, save state and
hallway geometry are unchanged. Old artwork retained; no commit/export.

## Current state
New `assets/environment/hull-condition-v2`: five independent built-in generated
masters, exact prompts, immutable source ledger, 256px individual exports and
768x512 runtime atlas. Hairline/split/rupture/patch/weld selection. Runtime pixel
density is 5.333px/world unit; actual visible heights 32/34/37/29/32 world units.
`scripts/flood_visuals.gd` loads the explicit whole atlas path through the existing
runtime PNG loader. `tools/build_hull_condition_art.py` verifies master hashes,
crops alpha margins and resamples isotropically without painting/colour grading.
`tests/test_hull_repair.gd` waits for startup, explicitly flushes native rendering,
centres its captures and adds hairline/split capture states. The spare legacy
short weld was never selected in live code; new atlas slot 5 remains transparent.

## Verification
`python tools/verify_hull_condition.py`: physical hull repair PASS and native
room/straight/corner/tee condition review PASS in all four rotations, zero errors.
Final evidence `output/hull-condition-20260930-092117/summary.json`: all 2,924
owner files unchanged. Scratch APPDATA/LOCALAPPDATA with copied layouts only.
Earlier run changed two owner log files; attribution unknown and no restoration.
An intermediate capture edit had a type-inference parse failure, fixed by explicit
Vector2 annotation before the final passing run.
Agent reviewed alpha-composited source contact and native damage/patch/weld
captures. `output/hull-condition-v2/native-details-3x.png` uses 3x nearest display
enlargement for inspection only; original captures retain actual native pixels.
Hull texture loaded, repair/scar/save checks passed, Git LFS attribute confirmed,
source-hash rebuild and scoped diff whitespace check passed.

## Next action
Owner visual review. Next useful asset audit: provisional exterior low-rock/timber
scenery and salvage-site markers, checking current selected sources before replacing
anything. Packaged-release verification remains a separate requested workflow.
