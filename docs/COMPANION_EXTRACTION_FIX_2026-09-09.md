# Companion extraction repair

Updated: September 9, 2026 · BrineSpace · River, Josh and Margot white cutouts

## Objective and decisions
Owner rejected the companion animation quality and white cutouts in sprite-polish-v2. Rebuild from original authored sources, preserve character identity, scale, animation timing and behavior. No new generated art or gameplay changes.

## Current state
Installed six `character/companion-cleanup-v3` manifests through `scripts/companion_npc.gd`. `tools/build_companion_cleanup.py` rebuilds all 84 clips / 232 frame references from original robot, cat and personality sources. White robot backgrounds are removed only where neutral background connects to the tile border; interior bright panels are retained. Source images are area-downsampled before binary alpha and the shared 64-color palette, replacing noisy nearest-neighbor reduction. GIF reviews use full-frame disposal. Original V1/V2 art remains intact.

Before/after GIFs and PNGs for every base/action loop, exact source hashes and packaging counts are in `character/companion-cleanup-v3/review.html` and `build-report.json`. Entry/exit clips reuse the corrected endpoints. Existing pose counts and source-motion limitations remain; this is extraction/packaging repair, not newly drawn in-betweens.

## Verification
All six sprite validators pass; builder asserts dimensions, unclipped nonempty bounds, binary alpha, <=64 colors and matching durations. `tests/test_companion_extraction.py` passes: enclosed white subject pixels survive while connected exterior white is removed. Updated `tests/test_sprite_polish.gd` passes native production-player rendering and exact robot transition endpoints. Agent inspected enlarged before/after frames for all three companions, Margot grooming and the native four-direction walking lineup.

Full `test_companion_personality.gd` run did NOT pass on this working tree: concurrent room scripts fail to resolve/compile, including a Vector2i/Vector2 comparison in radio_lab_view.gd, followed by room-renderer errors and Josh action/restore assertions. Do not claim these new assets passed full gameplay/save regression based on the previous V2 pass. Log: `output/sprite-polish/companion-cleanup-native.log`. Native isolated board passes in `cleanup-board.log`. These checks do not establish continuous visual acceptance of every loop.

## Next action
Owner review of the before/after gallery. Re-run full companion personality integration after the ongoing room-script edits compile. No executable rebuild or commit.
