# Improved rear loop extraction

## Objective and acceptance
Owner liked rear v6 video and authorized extracting a natural-speed loop and comparison with accepted sides. Source accepted as foundation; extracted-loop approval pending.

## Accepted decisions and constraints
No new generation or credit spend. Preserve original timing, RGB, anatomy and shared side scale. No per-frame rescaling or interpolation; no runtime installation.

## Current state
character/veld-video-north-v6/build_loop.py extracts source frames 54-81: 28 frames at 24fps, 1167ms. Writes transparent 184-square frames, strip, manifest, audit and north-loop-review.gif beside approved rear idle master. compare_sides.py writes rear-and-sides.gif and readable full-cycle contact sheet. Comparison preserves each clip's original cadence; its 3.5-second overall restart resets side loops and must not be mistaken for their native seams. Rear repeats exactly three times.

## Verification
Manifest validation: zero errors/warnings. Zero clipped frames. Seam pixel difference .01316 vs internal median .01353 and max .01570. Full-cycle contact sheet inspected: both left/right swing phases occur. Pixel measurements and still inspection do not certify temporal smoothness. Owner can review dedicated rear-loop GIF without comparison restart artifact.

## Next action
Review extracted rear loop at natural speed against accepted side loops. Rear cadence is faster (1167ms vs east1667/west1708); preserved as requested rather than silently matched. Decide final timing only after visual review. Front candidate remains separately pending.
