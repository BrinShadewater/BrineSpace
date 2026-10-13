# Project handoff

Updated: October 8, 2026 - Project: BrineSpace - Task: moving-water topology preparation

## Objective and acceptance

Continue the complete PC/Mac performance/release-readiness plan. Reduce active
water rendering overhead while preserving selected pixels, timing, simulation and
owner saves. No release gate or original-report closure is established here.

## Accepted decisions and constraints

Keep these changes private pending actual-runtime CPU/GPU comparison and full-room
visual/lifecycle coverage. No engine upgrade, native dependency, downscaling or
frame removal introduced. Normal source remains unchanged.

## Current state

The fresh dynamic GDScript batch previously cost 4.46-4.82 ms per large bay against
1.12-1.17 ms direct drawing. Three controlled prototype revisions were exercised:

1. Cache immutable triangle-strip indices by (base vertex offset, strip size).
   Cache is owned by the canvas, FIFO bounded to 1,024 entries; appended arrays
   preserve native triangle order without mutating cached indices. Each frame
   still constructs current animated geometry/colors. Large-bay candidate medians
   2.60-2.94 ms against direct reference 1.14-1.18 ms in this run.
2. Replace transient PackedFloat32Array scalar casts with Vector2(value,0).x in
   the private stroke builder. Native single-precision conversion is verified by
   byte comparisons and raster checks. Candidate 1.99-2.25 ms; same-run reference
   1.22-1.48 ms. This run's higher reference costs limit cross-run speed claims.
3. Fill core/fringe color arrays natively, then set only differing vertices.
   Candidate 1.94-2.14 ms; same-run reference 1.16-1.25 ms. Incremental color-fill
   benefit is not established by these separate runs; the combined prototype is
   still more expensive in CPU than the existing direct path.

No native batch GPU measurements have been taken here. Recorded API command count
remains 10 for the batch; do not call that a GPU draw-call count. Potential renderer
CPU/GPU savings need actual workload measurement before selecting this approach.

Evidence folders under D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
water-topology-cache/, water-topology-scalar/, water-topology-colors/ and
water-topology-summary.json. Earlier rejected paths retained. Checkout changes:
this handoff and CURRENT_STATUS.md only.

## Verification

Each revision: native QA/debug=true, 25 checks, 24 final advancing-clock raster pairs,
zero failures. CPU samples alternate queue order and exclude initial sample.

Final combined revision: 6,592 native checks, zero failures, 216 exact raster pairs
across 3 floor footprints, 6 water levels, 3 clocks, pump states, 2 scales,
asymmetric transforms and modulation. Exact index order across 1,030 distinct
base offsets exercises 1,024-entry bound, eviction and reconstruction. 4,096 scalar
conversions compare float32 bytes. Canvas owner releases. Pixel cases are broad
water coverage, not whole-room layering/motion/rotation acceptance.

All four isolated runs clean, all 2,936 non-log owner files unchanged, every process
terminal. No test/probe used the owner's data directory.

## Next action

Compare the combined batch against direct water in an actual debug=false large
station, collecting renderer CPU/GPU time and native draw calls as well as frame
p95/p99 and script cost. Preserve source identity guards. First establish full-room
rotation/layer/filter/motion correctness. Accept only a net matched workload gain;
otherwise pursue a cheaper bulk geometry path rather than ship a CPU regression.
Full release scope remains active, including Mac certification and original bugs.
