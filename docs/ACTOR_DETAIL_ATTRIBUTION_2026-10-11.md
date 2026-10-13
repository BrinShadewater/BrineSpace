# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: separate drawing from preparation

## Objective and acceptance

Improve pacing and memory without changing selected pixels, animation, layering
or default effects. Full release gates remain open.

## Accepted decisions and constraints

Do not add synergy membership caching: measured scans are only 25–29 us/frame.
Preserve existing accepted production optimizations; this pass changes no live
scripts. Keep muted secondary-display tests isolated and output bounded.

## Current state

Private runner/analyzer are `output/renderdoc-tools-2026-10-08/run-actor-detail-attribution.py`
and `analyze-actor-detail-attribution.py`. Artifacts under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/actor-detail-attribution/`.
`analysis.json`, `uploads.json`, and `upload-paths.json` retain the evidence.

## Verification

Two actual debug=false native runs, 3,240 measured frames, large40 map; lighting,
placement and demolition at 1×/2×/4×. Nine full states/cameras and 15 successful
paired actions exact. No runtime image failures. Timing wrappers preserve call
order/results; ring holds at most eight frames. Attribution is not FPS acceptance.

| Mean CPU us/frame | Lighting | Placement | Demolition |
|---|---:|---:|---:|
| Drone animation drawing | 888.343 | 1321.737 | 1084.887 |
| Upload API intervals, all sampled drone uploads | 583.267 | 990.565 | 877.659 |
| Drone drawing on frames without uploads | 139.559 | 149.425 | 140.532 |
| Scrap effects | — | — | 440.039 |
| Functioning synergy drawing | 592.126 | 603.850 | 618.196 |
| Functioning synergy membership scans | 25.246 | 27.604 | 28.996 |

Each action has 540 measured frames; 48/76/81 frames have uploads, with
3,128.457/4,926.958/4,241.043 MiB cumulative raw upload payload respectively.
These are repeated traffic, not resident memory. API times are synchronous wall
intervals, not GPU completion. Rows overlap; do not sum them as a total budget.
Construction-order drawing has no sampled calls in this fixture, so this pass
does not establish its cost. Anchors average only 9.335–9.783 us/frame.

Most costly repeated measured paths include steer-right-west tyres (16 uploads,
76.924 ms total), mine-south effects (4, 61.058 ms), mine-south body (4, 59.382 ms),
unload-south cargo (6, 57.697 ms), wheel-layer-west (10, 56.242 ms). This measured
window does not distinguish first-ever session upload from reload for every path.

This confirms the older aligned upload evidence in
`EXTERIOR_UPLOAD_ATTRIBUTION_AND_ACCOUNTING_2026-10-08.md`; it is not a new
discovery that full-sheet uploads cause stalls. It rules out membership/anchors
as useful targets and locates the recurring synergy cost in geometry submission.
Existing rejected global cache enlargement, cropped UV remedies and indexed
provider outcomes still govern; do not repeat them unchanged.

Owner fingerprint unchanged: 2,938 files. Runs terminal, override restored;
accepted Main/Grid/Bill hashes unchanged. Two terminal trace JSON files compressed
in place, hashes unchanged. No screenshots or runtime/source-tree copies added.

## Next action

Use the ranked repeated upload paths to choose a materially different bounded
storage/lifetime remedy, with matched 12/40-room pacing, memory and exact-pixel
checks. For synergy rendering, evaluate retained geometry with unchanged circle/
arc commands and animation transforms, rather than another membership cache.
Keep unresolved memory/frame gates explicit; no release certification claimed.
