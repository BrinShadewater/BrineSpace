# Static bought-prop retention

Updated September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Reduce unnecessary bought-art drawing while preserving active effects, state
changes and rendered appearance. This is a bounded rendering improvement, not a
claim of overall FPS gain or completion of the broader performance work.

## Accepted decisions and constraints
Preserve source pixels, owner layouts, gameplay and custom/portable animation.
No exports, broad refactoring or tolerance relaxation.

## Current state
scripts/room_content_canvas.gd now classifies ordinary library props according
to the draw path it actually uses: fixed polygons are retained; registered
operating_screens remain live only while the room operates. Custom-library and
portable-view props retain their source renderer's classification. Existing
state/transform invalidation still redraws static content when required.
When adding future clock-driven behavior to RoomAssetLibrary.draw, update this
classification alongside it. No library JSON or source image changed in this pass.
New native test: tests/test_library_prop_retention.gd, paired UID and index entry.

## Verification
Focused native Command Center test fails before the rule (8 expected-count
failures) and passes after. Four views, on/off states, 12 advancing frames each:
36 prop redraws become 24 while operating and zero while off. Static furniture
has no repeated redraws. All eight retained/direct captures match exact bytes.
The native retained q0 image was inspected. Evidence is under
output/library-retention-2026-09-21.

The broader existing content-parity test exercises 49 rooms/44 views, four
rotations, state/camera changes, active crew/drone work and construction. Its
reuse/live-motion and busy-fixture assertions pass, but pixel parity fails in ten
of 31 pairs, each at one pixel. The same test without this change fails identically.
All 31 current pair discrepancy masks and RGB deltas match the baseline exactly.
The optimization was restored only after that comparison. The two archived
old door-open/door-close captures copied from output are excluded from the current
31-pair comparison report. Full native logs, before/after source snapshots and
captures remain with the evidence. No failing test was weakened or labelled passed.

## Follow-up resolution
The subsequent copy-source classification fix resolves the baseline discrepancy;
the full station test now passes with all 31 pairs exactly equal in RGB. See
COPIED_PROP_ANIMATION_2026-09-21.md. The failures above remain historical evidence
for the optimization's original before/after comparison.

## Next action
The resolved discrepancy occurred at: motion captures
at (667,246), busy captures at (590,246). Keep overall render/FPS improvement
unproven until measured in a relevant station. Existing Windows/Mac exports
predate this optimization and the preceding room/card/diagnostic polish.
