# Project handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: fitted crew helmet clips

## Objective and acceptance

Continue the complete Veld, Branforth and Marsh replacement following Bill.
Address the owner's oversized-helmet feedback while preserving identity, motion,
gameplay and complete state coverage. The overall goal remains active.

## Accepted decisions and constraints

Use character-specific precomposed equipped clips, sharing the helmet design.
Generate corrected poses where the oversized helmet is painted into the source.
Preserve original sheets/contracts and body scale. Bill remains unchanged and
Marsh remains an android without helmet/Oxygen requirements. No export requested.

## Current state

Four edited sheets in `character/crew-helmet-fit-v2/sources` cover Veld/Branforth
pickup and donning. Prompts/references are preserved with the sheets. LFS applies
to their PNGs. `tools/fitted_crew_helmets.py` extracts the new interiors at original
body scale, anchored at the soles, and resolves reversed aliases.

`tools/rebuild_human_crew_art.py` now selects these interiors and inserts exact
bare/equipped idle endpoints with the correct foot-pivot translation. Timings,
handoff events, 170 body/164 equipped states per human, and frame counts remain
unchanged. Removal uses the reverse of the same sequence.

`tools/review_crew_locker_motion.py` generates a portable playback/scrub page from
selected catalogs: `character/crew-helmet-fit-v2/review/motion.html`. It shows both
characters at source density and 65.28-unit standing height. Interior poses and
idle joins were inspected. The temporary Veld-only extraction helper was replaced
by the shared extractor. The general crew reviewer now supports state glob filters
and portable embedded images for focused gait/action review.

Maintained and installed character skills and the visual bible record the new
source, endpoint, scale and capture lessons.

## Verification

- `python tests/test_fitted_crew_helmets.py`: pass for both humans; world-registered
  idle joins, reverse sequence equality and retained distinct-pose coverage.
- Human validators: zero errors or canvas-border touches; 670/669 original frames
  and 108 source manifests per actor unchanged. 1,104 body/1,056 equipped refs each.
- Binding audit: zero errors; 68 packs, 1,366 clips, 8,022 references, 8 portraits.
- Actual selected crew and Bill pack tests pass:
  `output/test-runs/20260912-095320-headless`.
- Focused native locker runs for both humans execute 252 travel samples and
  equipment/removal, handoff, pause, power-loss, chamber and disk-save checks.
  The full suites FAIL on authored suit-locker containment and three sidebar
  viewport assertions, not on those animation/state checks. Logs:
  `output/crew-replacement-2026-09-12/integration-native/*-fitted-locker.log`.
- Native captures initially showed the core instead of the locker. The fixture
  now flushes deferred station centering before focusing each evidence room.
  Corrected captures are under each actor's `locker-native-fitted` directory;
  Veld fitting/equipped and Branforth equipped room images have been inspected.

## Next action

Latest motion findings and candidate work are in
[the gait repair handoff](CREW_GAIT_REPAIR_2026-09-12.md).

Review and repair the remaining locomotion and action motion across Veld,
Branforth and Marsh. Do not equate source coverage or endpoint tests with complete
gait acceptance. Focused portable walk/run reviews are prepared under each actor's
`output/crew-replacement-2026-09-12/<actor>/focused/review.html`.
The airlock's authored rotated locker placement and sidebar assertions remain
open integration issues. Navigation now applies the same authored geometry as
drawing, exposing the quarter-one approach failure before rendering; do not relax
reachability checks to hide it. Full goal acceptance remains unproven.
