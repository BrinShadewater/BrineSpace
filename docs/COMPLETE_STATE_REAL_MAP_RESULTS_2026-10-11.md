# Real-map renderer verification

Updated: October 11, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance

Measure the private indexed-image renderer against the current normal renderer on
real station saves, preserving complete checkpoint state and camera state. These
checks support the release plan; they do not certify the release.

## Accepted decisions and constraints

Keep default art and effects quality. No production admission without loader,
filtering, visual and resource-lifetime acceptance. Tests remain muted, on the
secondary display, with isolated user data. Reuse existing runtime/art; keep new
evidence bounded. No owner save or layout changes.

## Current state

18 serial debug=false Windows native runs, three alternating pairs per map, on an
RTX 4070 Ti at 1080p. Reported 12-room save, frozen owner 10-room save and deterministic
40-room fixture. Idle, pan, zoom and lighting at 1x/2x/4x; 90 measured frames per phase,
19,440 total measured frames. Both lanes include installed world-coordinate gait
input and current workshop behavior.

The fixture uses the previously verified deterministic survey clock in both lanes.
Gameplay survey code is unchanged. This prevents wall-clock rendering differences
from changing persistent fog memory in fixed-step comparisons. Compare all
RunSave.capture fields except saved_at, with exact equality and no epsilon.

| Map | Mean ms, normal → indexed | Peak texture MiB, normal → indexed | p95 / p99 ms, indexed |
|---|---|---|---|
| Reported 12 | 12.513 → 12.737 | 1558.872 → 1528.343 | 19.302 / 22.486 |
| Current 10 | 12.002 → 12.196 | 1940.831 → 1911.626 | 17.876 / 23.664 |
| Stress 40 | 25.268 → 25.402 | 3028.007 → 2629.355 | 40.793 / 49.910 |

Average frame time worsened 1.79%, 1.61% and 0.53%. No FPS improvement accepted.
Large-map texture saving is 398.652 MiB (13.17%). Frames over 50 ms: reported 0→0,
current 0→1, large 50→32; none over 100 ms. Large decoded upload volume falls
22108.875→14750.918 MiB; texture-creation CPU time 2033.601→1491.526 ms across runs.
These are cumulative upload measurements, not simultaneously resident memory.

## Verification

All 108 paired complete checkpoints and camera phases exact. Candidate backend scans
complete, with no ordinary duplicate indexed sources or fallback draws in these
workloads. Prior 28/28 scoped pixel comparisons remain separate visual evidence;
this benchmark is not a new visual acceptance pass.

Actual release lifecycle probe: 12 checks, zero failures. Shared display identity,
original dimensions, multi-owner retention, queued worker draining, cache teardown,
weak-reference release, external caller ownership and a fresh session checked.
The first probe failed before execution because its helper was absent from the pack;
fixture now embeds the maintained window helper and the rerun passed.

Actual release malformed-image diagnostic: a 1×1 RGBA8 image was accepted as indexed
storage for a 2688×13440 image expecting format 3. This confirms runtime validation is
missing when debug assertions are disabled. No assets were corrupted or changed.
This is a private-provider admission blocker, not a proven production-game defect.

Owner fingerprint: 2938 files before/after, zero changes. Runtime configuration
restored and all launched jobs exited. New comparison directory 107.38 MiB, lifecycle
directory about 0.01 MiB; C: 124.20 GiB and D: 70.69 GiB free at completion.

Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`
`world-gait-indexed-complete-maps/comparison.json` and
`indexed-session-lifetime/{result.json,invalid-image-result.json,owner.json,invalid-owner.json}`.
Private fixture runners live in `output/renderdoc-tools-2026-10-08/`.

## Next action

Add runtime validation of decoded indexed images and palettes, and a measured,
accounted ordinary-PNG fallback. Verify synchronous and asynchronous failed loads in
debug=false, then filtering and representative pixels before any production admission.
Do not rerun all real-map benchmarks merely for documentation or unchanged source.
For FPS, return to measured floor/lighting rebuild and upload hotspots; memory savings
alone do not solve the large-station frame budget. All target-hardware, endurance,
remaining gameplay, full workload, packaging and Mac certification gates remain open.
