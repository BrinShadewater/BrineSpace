# Project handoff

Updated: October 14, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: room-card readability and frame sampling

## Objective and acceptance

Owner requested clearer room-card text, decorative metal over the colored outline,
and solid-looking colored strokes when cards are angled. Preserve card size and fan.

## Accepted decisions and constraints

Existing authorization covers this reversible visual fix. No gameplay or animation work.
Regular menus/HUD fonts remain unchanged; no raster source assets were replaced.
Maintain scratch user-data isolation and preserve other working changes.

## Current state

Uncommitted changes in `scripts/ui_fonts.gd`, `scripts/draft_card.gd`, `scripts/card_art.gd`:
card-only medium-weight hinted font at 2x oversampling, mipmaps, larger titles/rules,
minimum 12-point fitted rules. Colored backing moved outward beneath authored metal;
metal still composites last. Two-pixel interior strokes and mipmapped filtering for
turned cards; straight cards use linear filtering. Original 200x284 card dimensions.
`docs/CURRENT_STATUS.md` records the milestone. No executable rebuilt or published.

## Verification

Native Godot 4.7.2 / Compatibility / RTX 4070 Ti, muted second monitor:
- Temporary all-room layout probe: 79 cards, zero oversized cards or clipped titles.
- `test_card_art`: 34 checks, zero failures, exit 0.
- `test_hand_backdrop`: PASS including card dimensions, fan/row, font isolation,
  art filters and hover behavior, exit 0.
- Reviewed straight and +/-7-degree production card components at 1600x900.
  Detached card probe omits room thumbnails; frame and text are production components.
- Diff check clean. Runner classified these two fixtures as headless and skipped them
  under `--native`; direct native invocations above supplied actual render validation.

Evidence: `output/font-diagnostic-20261014/` (`before-after.png`, `cards-after.png`,
`layout.log`, `card-art-test.log`, `hand-test.log`). Baseline `cards-warm.png` is
byte-identical to the initial capture, as recorded by the preceding investigation.
User data: `C:/bs-font-probe-20261014` and `C:/bs-card-tests-20261014` APPDATA roots.

## Next action

Owner to judge the visual result in source. Release rebuild and native Mac acceptance
remain open. The original Q-like-zero artifact was not reproduced; this change addresses
the demonstrated small-text readability and rotated-line sampling problems.
