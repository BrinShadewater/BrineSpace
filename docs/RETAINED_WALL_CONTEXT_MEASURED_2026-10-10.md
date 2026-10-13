# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: private wall-context native validation

## Objective and acceptance

Reduce broad wall redraw bursts while preserving selected visuals and gameplay.
The complete PC/Mac release plan remains open. Keep this experiment private until
the remaining immediate-frame/neighbor/motion checks establish visual acceptance.

## Accepted decisions and constraints

Current accepted navigation/preparation/galley/shadow changes are present in both
timing lanes. Compare normal global wall-slot keys against retained local context.
Existing slots/order/filtering preserved; no extra draw nodes or quality changes.
All native work is muted on secondary landscape display, with verified scratch
profiles and copied owner layouts. Shared physical QA package reused, no full copies.

## Current state

Normal source and frozen PC/Mac packages unchanged. Small current-source overlays,
guarded parity/performance drivers and focused analyzer retained under
`output/renderdoc-tools-2026-10-08/`. Private helper and Grid remain unadmitted.
One adapter failed before game launch because a generated driver filename differed
from the expected name; corrected path and retained initial staging output.

## Verification

Actual debug=false native cached-versus-forced repaint:15/15 exact RGBA pairs,
four rotations, close view, rotation, power, light fade, raised walls, placement/
removal, culling, pan/zoom. Static surface retention and mesh bounds pass; selected
q0 image visually reviewed. Frozen-clock settled snapshots, not motion or complete
immediate interactive-room certification. The targeted native outside-snapshot
neighbor case remains pending; pure8,004key checks cover its metadata invalidation.

Current-source actual debug=false station comparisons: three pairs per saved12 and
deterministic40 extension, alternating order, lighting/selection/connected direct
placement/demolition1x/2x/4x.12runs/19,440frames, all54phase-end gameplay states equal.
RTX4070Ti/1080p; not GTX1650/M1 or plain new-package certification.

| Metric | Reported12 reference / context | Large40 reference / context |
| --- | --- | --- |
| All-frame mean |15.757 /15.772ms|28.800 /28.692ms|
| P95 |22.860 /22.749ms|48.485 /47.681ms|
| P99 |29.449 /28.900ms|67.032 /66.155ms|
| Maximum |88.382 /88.307ms|130.715 /111.475ms|
| Frames >50ms |13 /10|174 /144|
| Frames >100ms |0 /0|18 /14|
| Construction-frame mean |52.915 /50.426ms|112.769 /102.469ms|
| Construction grid-draw mean |23.778 /21.579ms|46.433 /37.639ms|

Large construction frames shorten10.30ms; large draw callbacks shorten8.79ms.
Whole-frame improvement only0.37% large; reported12 mean is0.095% worse. Individual
pair means mixed. Useful targeted burst reduction, not a general60FPS or stall fix.
Both scenes fail this lighting-inclusive p95/p99 workload budget; small-scene results
from earlier placement-only tests do not certify the broader workload matrix.
All>50ms frames retained with overlapping action/step/draw/upload metrics; no summing
these intervals as independent costs. No acceptance based on synthetic preparation.

All full owner guards2,938 unchanged; source hashes unchanged. Jobs terminal and
shared runtime configuration restored. This turn117.73MiB evidence plus15scratch
profiles63.78MiB; retained after earlier deletion rejection, no new attempt.
C124.23GiB/D80.46GiB free;20GiB storage floor checked, no large duplicates.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`retained-wall-native-parity/` (15pairs/source/owner/storage),
`retained-wall-large-performance/`, `retained-wall-reported-performance/` (paired
analyses/traces/slow-frame census), and corresponding small inputs/runtime packs.

## Next action

Finish targeted native neighboring-input and visible first-frame checks with a
matched normal control if the existing renderer also differs during first-frame
settling; then dynamic crew/light/fog/layering and scene-exit lifetime validation.
Only then decide whether targeted savings justify admission. Do not repeat unchanged
full timing batches merely to chase a cleaner mean. Continue independent drone
uploads, memory/loading, original bug/UI/save/endurance, target-PC/Mac certification
and release freeze/audits/signing. No release while performance/critical gates fail.
