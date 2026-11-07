# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: floor attribution and row-upload feasibility

## Objective and acceptance

Identify larger remaining rendering costs without changing selected pixels or
quality. Full PC/Mac performance/release goal remains open. No optimization admitted.

## Accepted decisions and constraints

Private bounded profiling only. Do not add overlapping parent/substage times.
Live floor-detail placement is disabled (`details.draw` requires Studio preview),
so optimizing its resolver would not address gameplay. Reuse physical QA runtime;
muted secondary display, guarded scratch profiles and20GiB storage floor.

## Current state

Normal source/packages unchanged. Private Grid connection timer and RoomFloor
floor/dressing timers in `floor-preparation-probe/` under
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/.
Driver `output/renderdoc-tools-2026-10-08/run-floor-preparation-attribution.py`.
New row-region sampling test under `drone-row-region-trial/` in that evidence root.

## Verification

Actual debug=false saved40-room lighting diagnostic, one run540frames/1×/2×/4×.
Not a matched performance acceptance run; private timer overhead is present.

| Mean per measured frame | 1× | 2× | 4× |
| --- | --- | --- | --- |
| RoomFloor base floor call |0.205ms|0.200ms|0.185ms|
| RoomFloor dressing call |0.197ms|0.192ms|0.176ms|
| Connected-neighbor checks |0.742ms|0.756ms|0.723ms|
| All configure stages |0.922ms|0.883ms|0.860ms|
| Full floor setup |0.631ms|0.611ms|0.565ms|

Floor setup contains nested base/dressing work. There are ~37k connected-neighbor
calls per180-frame phase; duplicate render topology checks are a candidate, but
their cost alone cannot recover the whole budget. Existing draw profiling shows
live-room callbacks~3.6ms, floor/rest callbacks~3.0–3.25ms, render CPU~7.6–7.85ms,
render GPU~6.17–7.71ms and ~3,400 draw calls. Render/frame intervals are not additive.
This changes priority toward render-pass/draw-call attribution rather than an
unmeasured floor-decoration resolver rewrite.

Row-strip experiment differs from the rejected single-frame crop: preserve atlas
width and all cells in the selected row, plus2pixel neighboring-row gutters. Same
draw_texture_rect_region, source frame size, tint, mirrored cases; synthetic and
actual mining-West sheet,6cells each,4scales (including .0476), nearest/linear.
Native GPU feasibility uses GodotQA engine, not debug=false release gameplay.
192comparisons/52mismatches: actual10nearest and42linear; synthetic all exact.
Largest nearest mismatch107pixels/128channel levels. Reject row-strip path.

Whole sheet144,506,880bytes uploads16.601ms; first row4,838,400bytes uploads0.578ms
with1.297ms crop. These are isolated call timings, not usable game improvement:
the candidate fails exact visual acceptance. Normal drone storage stays unchanged.
Texture-size/source-coordinate representation remains suspect; precise renderer
mechanism not established by this test. Do not repeat this crop unchanged or loosen
the pixel gate. First probe had mixed tab/space indentation; normalized private
script, successful V2 records expected raster rejection. Failed logs retained.

All owner guards2,938 unchanged, jobs terminal/config restored; no full copies or
cleanup retries. New evidence4.45MiB plus4.66MiB scratch/4profiles. C126.97GiB /
D79.06GiB free. Evidence: `floor-preparation-attribution/{attribution.json,
pair1-candidate.json,owner.json,storage.json}` and `drone-row-region-trial/
{probe.gd,results.json,native-v2.log,owner-v2.json}`.

## Next action

Measure draw-call/render CPU/GPU contributions of individual passes with reversible
diagnostic controls and fixed matched state. Optimize the largest demonstrated
contribution while preserving quality; no unchanged per-room floor-node/crop/indexed
or larger-drone-cache reruns. Original bug/save/UI/endurance, standard workload,
GTX1650/M1, latest-source packaging and Mac signing/certification remain outstanding.
