# Bought-prop retention timing

Updated September 21, 2026. Windows, Godot 4.7.2 Compatibility, RTX 4070 Ti.

## Objective and method
Determine whether fewer redraws reduce render work in a larger station. The
output-only probe builds exactly 100 rooms in a compact grid, preserving the current
saved layouts. Synthetic funding/free building are confined to the fixture.
Simulation is paused; only visual time advances. There are no active crew/drone
simulation costs in these timings. Rendering is explicitly forced, so loop times
must not be converted to ordinary gameplay FPS.

Within the same process, compare baseline/retained/retained/baseline classification
of ordinary library slots, preserving the copied-prop animation fix and all other
production code. Each block has 15 warmup and 30 measured iterations. This isolates
classification without editing production files. Native screenshots confirm all
100 overview room centers and three close-view centers are visible.

## Corrected results
Averages of the two blocks for each mode:

| View | Retained-content redraws/sample, before -> after | Content paint ms, before -> after | Render CPU ms, before -> after | GPU ms, before -> after |
| --- | --- | --- | --- | --- |
| overview | 55 -> 28 | 0.951 -> 0.510 | 17.564 -> 17.413 | 15.310 -> 14.964 |
| close | 7 -> 4 | 0.019 -> 0.018 | 5.563 -> 5.345 | 3.503 -> 3.288 |

The consistent overview saving is about .44 ms in script-side content painting.
Close-view painting changes negligibly. Total render CPU/GPU changes are modest
and timing variance/warmup prevent a strong overall frame-rate claim from this one
paired run. Draw commands remain on the GPU even when script submission is retained.
The current optimization is supported by exact visual parity separately; see
COPIED_PROP_ANIMATION_2026-09-21.md.

## Measurement correction and evidence
The initial run aggregated stale draw_usec values from culled canvases in the close
view and had large timing outliers. Its files are retained as profile-initial.*;
do not use its close paint metric. The corrected probe resets each canvas paint
counter before the measured frame and retains raw loop samples. native-corrected.log
completes with exit 0 and no errors; profile.json, summary.json, source-hashes.json,
probe source and native captures are under output/library-retention-profile-2026-09-21.
No production code or assets changed during this measurement turn.

## Next action
Keep broader performance work focused on the remaining render cost, rather than
assuming retained prop submissions solve it. Continue normal expedition and Mac
hardware acceptance separately. Existing exports still predate recent polish.
