# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: separate lighting redraw and drone costs

## Objective and acceptance

Reduce lighting-workload stalls using measured causes and exact visual checks.
Full PC/Mac release goal remains open; this turn does not claim a new FPS gain.

## Accepted decisions and constraints

Reuse the three paired large-map runs already recorded; no new benchmark just to
rediscover stage costs. Draw, substage, setup and upload intervals overlap, so do
not sum parent/child timings. Never interpret conditional >50ms samples as all-frame
costs. Normal installed wall cache and default effects remain unchanged this turn.

## Current state

New focused analyzer `output/renderdoc-tools-2026-10-08/analyze-lighting-hitches.py`
reads existing current-source candidate reports. Attribution stored at
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/lighting-hitch-attribution/attribution.json`.
Private candidate removes only `interior` from retained wall-context hardware keys:
`interior-wall-key-trial/retained_wall_context.gd` under that evidence root.
Corridor shade remains a separate key dependency; every other hardware field stays.
No production or frozen-package changes.

## Verification

71 lighting hitches across three large-map candidate runs:44 with sampled drone
uploads,27 without. Upload records explicitly match sampled_process_frame.

| Conditional mean | With upload | Without upload |
| --- | --- | --- |
| Whole frame |58.249ms|61.646ms|
| Grid draw |37.966ms|38.485ms|
| Simulation step |2.917ms|2.838ms|
| Floor pass |7.608ms|7.750ms|
| Floor-rest pass |5.429ms|5.614ms|
| Wall slots |0.999ms|9.287ms|
| Exterior actors |9.868ms|0.520ms|
| Drone upload |7.407ms|0ms|

This corrects attribution of the earlier75.648ms frame: sampled drone uploads took
19.589ms and exterior rendering26.101ms, while floors8.693ms/rest6.500ms and step
2.053ms. Another79.742ms frame uploads137.81MiB mining sheet in30.639ms. These
confirm the already established drone issue, not a new cache-budget remedy.
Without-upload hitches show distinct wall invalidation and floor redraw work.
Interior toggle changes the broad hardware key, while normal room shells do not
read interior lighting; corridor risers explicitly read their shade.

Private native check: actual debug=false executable with current accepted modules
and candidate helper overlay.23 exact RGBA edge/settled comparisons,16 exact RGB
scripted crew/light comparisons,8 exact RGB interior-switch comparisons across
four room rotations. Non-corridor shell keys stay equal on interior toggle; forced
wall repaint matches cached pixels. Cache reuse and Grid/context release pass.
Frozen/scripted snapshot evidence, not timing or complete physical-input acceptance.
Fixture/driver: `interior-wall-key-native.gd`, `run-interior-wall-key-native.py` in
the focused output tools folder. Evidence: `interior-wall-key-native/` under the
shared evidence root. Owner2,938 unchanged, jobs terminal/config restored.
Small overlay/captures only; no full copies, no deletion retries. C126.97GiB /
D79.47GiB free,20GiB floor remains enforced. Normal-source focused diff check passes.

## Next action

Matched current-normal versus candidate interior projection, three alternating-order
lighting-only pairs on the saved40-room workload, with state equality and wall/draw/
upload counters. Admit only if measured savings and maintained invalidation tests
support it. Continue floor-pass packet reuse separately; prior per-room floor-node
approach regressed large maps and must not be repeated unchanged. Drone uploads
need a different remedy than the rejected larger-cache/cropped/indexed trials.
Performance, endurance, original bugs, target hardware/Mac and packaging gates open.
