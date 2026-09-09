# Station depth and camera handoff

Updated: 2026-09-08. Project: BrineSpace.

## Objective and accepted direction
Owner approved subfloor slabs, contact/cast shadows, overlapping silhouettes, upper-edge highlights, underwater haze/caustics and gentle camera easing. Preserve room brightness and accurate placement. Partial occlusion by southern rocks supersedes the prior all-or-nothing visibility rule.

## Current state
- scripts/grid_canvas.gd: connected subfloor faces and upper lips, slab/foot contact shadows, weathered derelict bases, true south-contour stone extrusion for basalt. Existing active terrain foundation variants retained. Generated weathered art is in rooms/foundation-v1/ with prompts and immutable source/rejection records. Two opaque checkerboard attempts rejected; fresh third source has verified RGBA.
- rooms/whole-room/room_lighting.gd: narrow perimeter contact shade and clipped southeast cast shadows with length estimated from each prop's visual height above its footprint. Existing power-level pools and fades remain. This is stylized 2D projection, not a full light-occlusion simulation.
- scripts/grid_canvas.gd: low-opacity distance-from-core seabed haze, sparse world-anchored slow caustic curves and exterior rim shimmer. Uses owning visual clock and viewport culling; leaves room sprites crisp. No perspective warp or parallax that would misalign tile placement.
- scripts/main.gd: short keyboard pan acceleration with immediate release stop, exponentially eased wheel/slider zoom around a fixed world center. Direct/programmatic zoom and fit remain immediate. Modal opening cancels pending zoom.

## Verification
Native paid preview passes construction, discovery, crew survival and disk Save/Continue. Focused checks verify intermediate zoom, exact settled target, center preservation, modal cancellation, immediate pan stop, owning clock pause/resume and actual caustic pixels frozen while paused/changing with time. Evidence: output/depth-water-checks-v2.log. Visually reviewed station, derelict and rock captures in output/depth-pass-v2/. Initial rectangular stone extension was replaced with actual boundary geometry after review; slab layering adjusted to reveal damaged art.

The first full-window caustic comparison failed; an isolated SubViewport removed unrelated scene/UI pixels and passed both frozen and animated comparisons.

No fresh packaged build or full catalog performance benchmark. Earlier broad nursery/movement fixture failures recorded in LIGHTING_SHADOWS_2026-09-08.md were not addressed by this visual pass. Owner acceptance remains pending.

## Next action
Owner review of depth and motion strength in the native game. Export verification remains separate. Existing unrelated checkout changes preserved; no commit or push.
