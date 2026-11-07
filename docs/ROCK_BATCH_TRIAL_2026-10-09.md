# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: private rock rendering trial

## Objective and acceptance
Reduce rendering cost and stutters while preserving pixels, gameplay and default quality. Admit only after matched packaged comparisons and relevant motion checks. Full release gates remain open.

## Accepted decisions and constraints
Private trials only. Normal terrain source and frozen delivery packages unchanged. Preserve original ridge geometry, floating-point colors, per-cell layer order, progress marks and simulation. Verified scratch profiles and owner fingerprints on every probe. Known idle editor retained/recorded; these trials are not final uncontested hardware certification.

## Current state
Artifacts: D:/bs-release-crew-cache-20261009/rock-batch-trial/. batch.gd groups rock surfaces/faces. terrain.gd separates static body from progress marks, culls settled views and uses full-map fallback during unsettled zoom. terrain-buffered.gd additionally retains six cells beyond the existing two-cell margin until required coverage changes.

The first remap overlay failed Grid preload despite direct script loads succeeding. Direct original-path replacement fixes resolution. overlay-v2.pck contains original batching; overlay-v3.pck contains buffered batching. Native debug=false resolvers05/06 verify Grid/terrain/main instantiation, trial identity and no errors. Headless resolver04 dummy texture error is not native acceptance. All failed evidence preserved.

## Verification
Original geometry: corrected864 exact pixel pairs,8 clipped views and12 scene checks pass. Expanded motion fixture initially used stale viewport dimensions after resize; visual review of saved red pair63 exposed the fixture mistake. Corrected fixture uses actual viewport dimensions. Final buffered-red-viewport-fixed:95 image pairs,12 intended small-pan rebuild assertion failures; buffered-green-viewport-fixed:95 exact pairs,zero failures/engine errors. Covers24-step pans per view, coverage crossing, resize, empty-region camera jumps, clearance, progress, scale and zoom settling. Owner guards2,938 unchanged.

Packaged v2 comparison session66244 exits0: eight runs/34,560 frames,96 phase-end state pairs match, zero engine/safe-image errors, owner2,938 unchanged. Both-order12-room means15.2244->13.9404 and15.0743->13.8873ms (~8%). Both-order40-room means28.7993->28.6450 and28.6742->28.3632ms (~0.5-1.1%). Pan p95 worsens at every speed in both12-room orders. Candidate fails11/24 phase gates in each12-room order and24/24 in each40-room order. Worst large frames154.233/153.220ms. No optimization admitted. Evidence workloads-v2/analysis.json.

Fresh large-control attribution records six >100ms frames; worst demolition151.578ms includes59.381ms recorded drawing and12.031ms action work. Wall/floor/exterior callbacks contribute. Engine wait79.431ms is not a GPU-duration proof; overlapping timings must not be summed. _sync_wall_slots currently keys every shell/crown on a station-wide surface snapshot. Narrower invalidation must preserve neighboring doors, exterior hatches, ward state, power, layout and raised-wall joins. No wall change installed.

## Next action
Fresh full v3 comparison started in workloads-v3, session61831:12/40 rooms,24 phases/all speeds,both orders. Constructor guard additionally requires coverage_reuses field. Poll existing handle; compare state, mean/p95/p99, stalls, memory and body rebuilds before admission. Then prioritize broad redraw costs for the large scene. Actual release bugs/endurance/target hardware/Mac certification remain open.

V3 first forward12-room pair: mean15.0676->14.6528ms (~2.8%),24 states match. Buffered body builds during pan phases0/2/2 instead of original v2 dozens. Pan p95 control/candidate17.130/17.106,18.933/17.479,17.128/18.334ms;4x still regresses, so no admission or smooth-panning claim. Evidence workloads-v3/forward-12room-preliminary.json.

Separate wall-key-trial prepared only: key.gd plus one-line frozen Grid integration grid.gd and synthetic test-local-wall-key.gd. Projects retained wall dependencies to3x3 neighboring structural/power state and own port/ward entry while preserving global hardware/layout/raised-wall/selection/core/legacy flags and corridor shade. Normal source and live v3 input unchanged. No engine/unit/visual/performance tests run; dependency review remains unproven until actual scene comparisons.

Wall validation prepared: run-local-wall-key.py guards completion of workloads-v3 and isolates profiles; synthetic baseline expects only three distant-state over-invalidation failures. test-local-wall-parity.gd adapts maintained surface parity coverage to12 selected room types, waits for startup and observable rebuild settling, writes captures only to user://, and mounts a future private wall overlay before Main loading. Tests have not run; overlay and native runner still need preparation after dependency checks pass.

V3 large forward pair completes: mean28.7132->28.6084ms (~0.36%), worst155.502ms. Reverse candidate27.8182ms completed; final reverse control running in session61831. Prepared actual debug=false wall parity adapter (explicit checks replace debug-only assertions), private overlay builder and15-pair whole-scene runner with constructor-source identity check, copied owner layouts into scratch, preserved output evidence and owner fingerprints. No wall tests have run yet.

Final V3 session61831 exits0:96 state pairs match, zero engine/safe-image failures, owner2,938 unchanged.12-room means improve2-3%; large forward0.1048ms benefit, reverse0.0047ms regression (effectively unchanged); all24 large gates fail, max155.502ms. Neither rock trial admitted. Active next experiment is local wall invalidation; see LOCAL_WALL_CACHE_TRIAL_2026-10-09.md.
