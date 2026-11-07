# Fan card sampling review

Updated September 21, 2026.

## Objective and acceptance
Owner note 14 concerns blurry/jagged outer cards in fan mode, not general viewport
or UI font scaling. Review actual native output; full owner acceptance remains open.

## Accepted decisions and constraints
Keep station pixel art and upright card nearest sampling. No blanket scaling change,
source-art edit, or Higgsfield use. Preserve owner rooms and library marks.

## Current state
`scripts/main.gd` now builds mip levels for card thumbnails after the existing safe
raw-image loader. The fan already requested LINEAR_WITH_MIPMAPS but native inspection
found all three 512x512 thumbnails had no mipmaps. The new levels make that filter
functional. Null/fallback behavior is preserved. Other raw art loaders are unchanged.
`scripts/ui_fonts.gd` now provides a cached card-only theme using duplicated
Barlow FontFiles with distance-field rendering at source size 48. The shared
interface fonts and their imports remain unchanged; system fallback fonts are
preserved if a bundled face is unavailable. `scripts/draft_card.gd` uses the theme.
`tests/test_hand_backdrop.gd` checks mip availability, row/fan sampling modes,
shared theme reuse and that the original interface font is unchanged.
The existing release packages predate this change; no re-export was performed.

## Verification
Native Windows Godot 4.7.2/Compatibility, 1600x900: current, plain-linear and
mipmapped comparisons captured in `output/fan-card-review-2026-09-21/`.
Current and plain-linear captures show noisy small art edges; mipmapped art is
calmer but softer. Installed capture keeps the upright center card nearest and
smooths only turned cards. Small tilted lettering remains imperfect.
`installed.log` confirms all three textures have mipmaps and outer/center filters
are 4/1/4. `hand-test.log`: HAND BACKDROP PASS, process exit 0. This exercises
backdrop clicks, fan/row, hover and settings persistence. It is not Mac, export,
owner visual acceptance, or a full expedition test.

## Card font comparison and installed verification
Native captures compare baseline bitmap, 2x/4x oversampling, and distance-field
source sizes 48/96. Oversampling candidates were rejected: small strokes broke up
more. Distance-field 48 improved continuity in tilted titles/resource lines; 96
showed no useful visual gain. Those comparisons live beside the art captures as
`font-*-detail.png`, with probes and logs retained. Original font oversampling
stayed 0 throughout. Font API reference:
https://docs.godotengine.org/en/latest/classes/class_fontfile.html

`font-hand-test.log`: native hand test passes, exit 0. Installed captures at
1600x900 and 960x540 were inspected. Cards retain 200x284 design size. The external
probe checks all 47 loaded card definitions against inherited-font minimum height:
zero new height regressions, exit 0. This is a layout metric, not visual acceptance
of every card. At 960x540 the text fits but remains very small; no claim of full
low-resolution readability is made. Native Apple Silicon and owner acceptance
remain open. All probes use isolated settings/layout/save paths.

## Next action
Gather owner fan readability feedback and treat very small window readability as
a separate layout/accessibility issue. Continue room composition and normal
expedition/motion review. Existing Windows/Mac packages predate both sampling fixes.
