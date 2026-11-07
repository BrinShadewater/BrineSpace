# Project handoff

Updated: October 9, 2026 - Project: BrineSpace - Task: normal-source water integration

## Objective and acceptance

Continue the full PC/Mac performance and release-readiness plan. Integrate the
measured water optimization while preserving selected pixels/timing,normal
simulation,owner layouts and saves. Packaged performance certification remains
separate; all original release gates stay active.

## Accepted decisions and constraints

Retain full/stationary cache reuse and existing reduced-motion behavior. Animated
or partial water batches ordered native-equivalent strokes without removing
frames or reducing quality. Keep caches canvas-owned and bounded; no global
texture/cache retention or native dependency/renderer upgrade introduced.
This source integration passes native regressions, but current-source actual
packaged timing is still required before full optimization admission.

## Current state

Normal source now contains the equivalent guarded optimization:

- rooms/large-rooms/moonbay.gd: dynamic command batching only for nonzero-clock or
  partial water; stationary command cache remains unchanged. Diagnostic-only
  --reference-dynamic-water-strokes restores direct dynamic drawing. Canvas-owned
  index topology lookup is capped1,024 entries; positions/colors rebuild each draw.
- scripts/water_stroke_triangles.gd: reuse immutable strip indices by base/count,
  scalar float32 conversion via Vector2, native color fills. Appended packed arrays
  preserve original index order; caller edits do not corrupt cached storage.
- tests/test_water_stroke_triangles.gd: persistent per-paint topology reuse,
  eviction/reconstruction/caller mutation and exact rounded-scalar validation.
- tests/test_moonbay_water_commands.gd: activity/pause reuse and bounded dynamic
  lookup checks added to existing exact native pixel matrix.
- tests/test_moonbay_water_batch.gd: reference explicitly disables dynamic batch,
  ensuring old immediate drawing is compared with new retained candidate drawing.

No private beacon/navigation changes were added by this integration. Existing
UIDs remain paired/unchanged; art,timing,layout and gameplay data untouched.
Pre-edit physical snapshots and source hashes retained outside checkout under
D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/water-normal-integration/.

## Verification

Current normal-source native QA results,isolated profiles with copied owner layouts:

- Stroke geometry:180 visible exact raster pairs,6,159 cache/scalar checks,zero
  failures. Scalar check compares float64 representations of expected rounded
  float32 and actual value,avoiding an extra float32 cast masking a wrong result.
- Water commands:493checks/244exactrasterpairs,zero failures,stationary cache
  eviction/reconstruction/activity/pause and owner release.
- Whole-room composition:135checks/80exactrasterpairs,zero failures,filter/material/
  overlapping room/motion/layout changes/hide/show/replacement/removal/culling/
  retained-parent release. Reference uses old dynamic-water rendering.
- Headless cache-independence probe: separate default helper calls and separate
  WaterCommands instances receive independent dictionaries; passed.

Logs clean/all processes terminal. Real owner2,936 non-log files unchanged.
A runner looked for result.json after the already-passed water test wrote context.json;
result was harvested from the resolved scratch profile and runner corrected without
repeating that successful test. Later changed coverage was rerun as required.
Existing private actual-runtime evidence(October8) remains supporting evidence:
2run-order idle pairs and guarded12interaction phases show net gains. Do not relabel
those private-script timings as a packaged measurement of these edited normal files.
Source-hashed integration-summary.json preserves current checks and identities.

## Next action

Freeze these exact normal Moon/stroke files in a private actual debug=false release
override and compare old direct vs new batch with compiled-source/branch guards.
Separate normal integration timing from earlier private beacon/navigation trials.
Then continue measured rendering/stall fixes,loading/endurance/original-nine closure
and actual Windows/Mac certification. No public package/update/upload occurred.
