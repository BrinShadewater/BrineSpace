# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: exterior and foreground draw attribution

## Objective and acceptance

Find larger recurring rendering costs without changing animation, pixels,
gameplay or default effects. Full PC/Mac release performance gates remain open.

## Accepted decisions and constraints

Preserve accepted production improvements. This pass adds private timing only;
no production edits or new quality reduction. Native tests stay muted on the
secondary display, with isolated saves and bounded reports.

## Current state

Private trace builder/analyzer:
`output/renderdoc-tools-2026-10-08/run-actor-stage-attribution.py` and
`analyze-actor-stage-attribution.py`.
Artifacts: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/actor-stage-attribution/`.
The diagnostic grid times 17 drawing stages and keeps at most eight frames in
its lookup. Reference uses accepted root grid; both lanes use the latest
door-membership Main fixture (two paused test-only toast tweens), accepted Bill,
and deterministic test-only idle-alert clock. No asset changes.

## Verification

Two actual debug=false native runs on the 40-room station; 3,240 measured frames
across lighting, placement and demolition at 1×/2×/4×. All nine full gameplay
states/cameras and 15 successful paired actions match exactly. No runtime
image failures. This is attribution, not matched FPS optimization acceptance.

Sampled mean CPU submission/preparation time per frame, microseconds:

| Stage | Lighting | Placement | Demolition |
|---|---:|---:|---:|
| Drones, including construction/scrap art | 1184.289 | 1583.044 | 1557.430 |
| Synergy links | 658.028 | 661.287 | 653.883 |
| Station effects | 177.311 | 181.424 | 174.850 |
| Hardware effects | 163.274 | 163.865 | 160.850 |
| Flooding | 121.235 | 124.111 | 119.517 |
| Harvest sites | 116.565 | 117.646 | 112.050 |

Human legacy/foreground drawing is only 27.698 microseconds on lighting phases;
layered room crew rendering is outside this function and is not covered by that
number. Door overlays and Moonbay/probe exterior drawing are also small in this
fixture. Drone cost includes construction, pending orders, pose work, dust,
sampling and sprite submission; it cannot yet be attributed solely to animation.
Timers surround original calls, retain their ordering and do not remove output.
Their totals are CPU timings and must not be treated as GPU cost or added to
overlapping aggregate timers as a total frame budget.

The source explains a promising target: synergy drawing repeatedly scans the
active-link array for each route segment. Drone drawing includes construction
art, which deep-copies a room definition and prepares geometry each draw.
These are candidates for narrower measurement, not established root causes.

Owner fingerprint remains 2,938 files with zero changes. Both runs terminal;
runtime override restored and accepted Main/Grid/Bill hashes unchanged. Two
completed generated reports compressed in place; content hashes unchanged.
C: 134.81 GiB / D: 68.50 GiB free afterward. No screenshot batches, source-tree
or runtime copies added.

## Next action

Split drone construction/scrap preparation from animation sampling/submission,
and split synergy functioning-link scans from animated geometry submission.
Optimize the measured larger component, then use matched real-map runs plus
visual/behavior checks. Do not infer a broad animation slowdown from this pass.
All loading/memory/endurance/Windows/Mac certification and original bugs remain
part of the active release goal.
