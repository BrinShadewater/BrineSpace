# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: avoid light-anchor layout copies

## Objective and acceptance

Reduce repeated preparation during floor/light redraws, preserving appearance and
owner layouts. Full PC/Mac performance/release goal remains open; budgets still fail.

## Accepted decisions and constraints

Use the existing read-only merged layout lookup in `_layout_light_anchors`, rather
than constructing an owned copy on every call. `anchors_for` reads edits and copies
its settings before adding `at`; shared input remains untouched. Existing layout
cache revision/identity invalidation applies. No new cache, geometry, images, nodes,
art scaling or drawing-order change. Muted/secondary QA, isolated saves, bounded
outputs and the shared physical QA package throughout.

## Current state

Normal `scripts/grid_canvas.gd`: exactly one method-name change, `positions` to
`shared_positions` in the light-anchor lookup. Original bytes/line endings otherwise
preserved, UID unchanged, no trial flag installed. Frozen PC/Mac packages unchanged.
Private probe/drivers under output/renderdoc-tools-2026-10-08:
`probe-shared-light-layouts.gd`, `run-light-layout-copy-native.py`,
`run-light-layout-copy-performance.py`, `run-light-layout-installed-native.py`.

## Verification

316 saved/authored layout cases: owned/shared light anchors identical and shared
layouts unmodified. Microbenchmark3,160calls/lane:79.746→22.102ms total (~72% less
lookup CPU); not FPS evidence. Copies include legacy offsets, hidden lights and
saved settings present in the actual layouts.

Matched actual debug=false RTX4070Ti/1080p saved40-room lighting1×/2×/4×:
three alternating pairs/six runs/3,240frames, all9phase-end game states equal.

| Metric | Owned lookup → shared lookup |
| --- | --- |
| Mean frame |30.787 →30.556ms|
| P95 |50.854 →48.906ms|
| P99 |63.542 →61.956ms|
| Maximum |86.209 →79.679ms|
| Frames >50ms |92 →69|
| Frames >100ms |0 →0|

All three pair means favor shared lookup; aggregate improvement0.75%, modest.
Light-pool setup mean across phases ~416→206µs (~50% less). Texture peaks identical
2,658.987MiB in all lanes. Wall-slot counts vary; this change does not claim wall
rebuild suppression. Lighting-only results do not certify the standard workloads.

Private and installed normal-source actual debug=false visual checks:23 exact RGBA
edge/settled pairs,16 exact RGB scripted crew/light pairs,8 exact RGB interior-switch
rotation pairs. Actor controls, cache reuse and scene/context release pass. Selected
installed light-on image reviewed. Frozen scripted snapshots are not animation-rate
or physical-input certification. Focused source diff check passes.

Initial integration write incorrectly doubled CRLF line endings and prevented Grid
parsing. Confirmed owned failed native PID14368/runtime/scratch identity, stopped
that failed job, then restored original formatting and applied the byte-level
one-name edit. Installed V2 native validation passes; failed logs retained. No owner
files changed on any attempt (2,938 fingerprinted), jobs terminal/configs restored.
New evidence18.68MiB plus238.75MiB scratch/11profiles including failed attempt;
no full copies or deletion retries. C127.00GiB/D79.07GiB free;20GiB storage floor.

Evidence D:/bs-release-crew-cache-20261009/benchmark-input-isolation/:
`light-layout-copy-trial/` (original source, unit results, hashes/storage/owner),
`light-layout-copy-performance/` (reports, paired analysis/source/owner),
`light-layout-copy-native/`, `light-layout-installed-native-v2/` (pixel checks).

## Next action

Continue larger floor/floor-rest preparation and command-generation hotspots;
avoid the rejected per-room floor-node approach. Keep drone upload remedy separate.
Full standard workload/endurance/original bug/UI/save coverage, GTX1650/M1 testing,
latest-source packages and Mac signing/certification remain outstanding.
