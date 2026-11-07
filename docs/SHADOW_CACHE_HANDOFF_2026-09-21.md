# Project handoff

Updated: 2026-09-21 · Project: BrineSpace · Task: Projected shadow geometry cache

## Objective and acceptance
Reduce repeated room draw work while preserving furniture appearance. Broad art,
animation and release work remains active.

## Accepted decisions and constraints
Preserve owner layouts, contact-band styling and translucent drawing order.
No art files, room layouts or player data changed.

## Current state
rooms/whole-room/room_lighting.gd caches the three clipped/triangulated projected
shadow bands by exact effective footprint and rise. Color remains dynamic. Entries
are bounded at 2,048; reaching that limit clears the cache before inserting another.
Reference unbatched path remains available. Per-prop composition order is unchanged.
tests/test_projected_shadow_batch.gd now changes positions and visual heights and
checks changed-input geometry, bounded retention and rebuilding evicted entries.

## Verification
output/shadow-cache-2026-09-21/: final.log native parity 9 cases, zero failures;
input/bound guards pass. Isolated 20,000-call geometry measurement: recomputation
191,587 us; cached 7,634 us. This is about 25x for that operation, not station FPS.
Whitespace check passed. No new release package was built.

## Next action
Measure full station rendering when next assessing performance; the existing
historical draw-call reduction is separate evidence. Continue Bill gait and room
polish; do not treat the geometry optimization as completion of those tasks.

## Full station comparison
Two native profile_large_station runs, with identical paid-operation fixture:
output/game-pass/2026-09-21-shadow-cache-reference/ and
output/game-pass/2026-09-21-shadow-cache-enabled/. Both exited zero, reached 50/100
rooms, kept overview centers visible and at least three close centers, and recorded
90 active-drone frames per scenario. Reference overview screenshot inspected.
100-fit render CPU: 22.122 vs 22.085 ms; calls identical at 11,467.889 average.
50-fit CPU: 13.815 vs 13.906 ms. No demonstrated overall rendering improvement.
Instrumented loop means vary in both directions (100-fit 75.84 vs 72.06 ms;
100-close 21.55 vs 28.89 ms); these do not isolate the cache or establish FPS.
station-comparison.json preserves the scoped numbers. Existing retained room
rendering limits how much repeated geometry work this optimization can remove;
grid_canvas draws these shadows in preview/floor passes, not every prop sprite draw.
Keep the claim limited to repeated geometry construction. Added
--reference-shadow-geometry to disable only geometry reuse while preserving batching
for future controlled comparisons. No further benchmark repetitions are justified
without a more specific live redraw-cost question.
