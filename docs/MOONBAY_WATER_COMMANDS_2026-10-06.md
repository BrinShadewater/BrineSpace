# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: large-room rendering performance

## Objective and acceptance

Continue the PC/Mac performance plan without changing selected visuals, animation timing or gameplay. Whole-frame and packaged release gates remain open.

## Accepted decisions and constraints

Cache CPU water geometry only for fully filled water at clock zero. Animated or partially filled water retains the original typed drawing path. Replay the same native commands in the same order; no batching or quality reduction. Cache belongs to the drawing canvas, bounded to 16 entries, with no texture or scene references. Normal scene destruction releases it.

## Current state

Changed `rooms/large-rooms/moonbay.gd`, added `tests/test_moonbay_water_commands.gd` and paired UID, registered native/render-perf lane in `tests/index.json`.

Private mixed 40-room attribution identified Moonbay base drawing at ~6.64–6.68 ms/frame across three bays, and large-room Studio props at ~4.3 ms combined. This is CPU preparation attribution, not GPU time. Different station areas/content prevent a pure comparison against the earlier single-cell fixture.

## Verification

Actual normal-source native test: 481 checks, zero failures, 239 exact raster pairs. Covers three water bounds, six levels, three clocks, pumping, fractional/nonuniform transforms, modulation and scales; bounded eviction reconstructs identical output, and canvas destruction is observed before the lifetime assertion. Initial test parse warning corrected; initial one-frame deletion assertion was premature, confirmed by observing owner destruction two subsequent frames later. No runtime ownership leak established.

Private matched mixed-station baseline/candidate: six idle/pan phases at 1/2/4x. Moonbay preparation lower by ~0.443–0.558 ms/frame; whole live-room preparation lower by ~0.479–0.852 ms. Candidate execution confirmed through cache counters (two builds, repeated hits). Full crew/drone, door/light and scene controls equal; texture counters equal in every phase. Both still fail whole-frame gates; p95 approximately 61–75 ms. No aggregate FPS or memory saving claim. Fixtures use private crew/drone experiments and are not release certification.

All successful runs preserve 2,936 owner files. Evidence: `output/moonbay-water-commands-2026-10-06/{stable/station,bounded,normal-final}` and `output/large-room-attribution-2026-10-06`. Failed fixture attempts retained: surface-pass Array mistakenly queried as Dictionary before the corrected station run; lifecycle test failures above are not accepted evidence.

## Next action

Most Moonbay base cost remains (~6.2 ms across three bays). Native antialiased water polylines still rebuild/tessellate on redraw despite reused input geometry. Profile command submission versus geometry preparation and investigate retaining complete stationary water commands within correctly ordered large-room layers. Preserve fill/mission/door transitions, transforms, effects choices and scene lifetime. Also address ~4.3 ms large-room props with measured, ordering-preserving work. Do not treat this local saving as closure of the release performance gap.
