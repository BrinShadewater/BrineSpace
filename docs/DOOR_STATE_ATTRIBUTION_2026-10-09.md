# Door/light state attribution and known-port trial

Updated: October 9, 2026 · Project: BrineSpace · Task: performance improvements

## Objective and acceptance
Reduce measured door/light preparation without stale connectivity, lighting or door poses. Full PC/Mac performance and release gates remain open.

## Accepted decisions and constraints
Frozen debug=false runtime with isolated user data; 64-frame bounded detailed capture. Nested scopes and instrumentation overhead prevent treating all timings as additive. Attribution instrumentation remains private; normal integration is limited to the verified known-port shortcut below.

## Current state
Door-state-probe completed 64 frames. Median total 1,554.5 us includes added instrumentation (prior coarser total about 1,382 us). Components: geometry/connectivity 425.5 us, variant/width 216 us, port generation 175.5 us, frame/center 160.5 us, lighting/hatch 157 us, exclusions 114 us, parts/depth 107 us, entry/light append 53 us, nearest crew foot 14 us, invalidation/snapshot 10 us. Representative frame: 126 ports, 94 connection calls, 28 accepted edges. Enclosing door_edge_state is 1,185.5 us and overlaps its detailed components.

Helper: output/renderdoc-tools-2026-10-08/prepare-door-state-probe.py. Artifacts: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/door-state-probe/ (candidate.json, component-summary.json, candidate.log, owner-pair.json).

## Verification
Source/branch/exposure guards pass, clean log, adapter restored, 2,936 owner files unchanged. Full workload means 37.455/38.067/37.250 ms, p95 42.543/45.396/49.779 ms, maximum 149.113 ms. Texture peak 2,345.481 MiB. This is attribution, not a matched optimization gain or release certification.

## Next action
Private known-port-trial first pair completed. It skips redundant source-port validation only for ports immediately enumerated by _render_ports, preserving neighbor validation, branch-owner checks, same-room behavior and sentinel/invalid-offset fallback. Both lanes retain the accepted local legacy-door plan. Each lane passed 6,016 actual connection comparisons over 64 frames, excluding proof duration from the detailed connectivity scope. Median geometry/connectivity 379 -> 257 us, a 122 us component saving. Whole-frame means/p95/p99 mixed, so this is not an accepted gameplay improvement. Source/branch/exposure guards pass, logs clean, owners unchanged and adapter restored. Phase/final cross-lane endpoint comparison remains pending.

Wider isolated geometry test passed 1,201,232 comparisons, zero failures, 316 current room/rotation variants, neighbor port alignments/misalignments, branch-owner mutations, same-room/missing-neighbor and sentinel cases. It runs extracted current main reference functions with the actual room database/footprint and proposed helper. No whole scene or native rendering acceptance is claimed. Evidence in known-port-trial/geometry.log and geometry-owner.json; owner 2,936 files unchanged. Helper: output/renderdoc-tools-2026-10-08/test-known-port-geometry.py.

Reverse comparison completed: connectivity 375 -> 258 us, repeating the first 122 us component saving at 117 us. Each lane passes 6,016 actual reference comparisons, no failures. Phase crew/drone/mission/power/door/light state and final missions/texture exit/pending jobs/upload counts match in both pairs. Source/branch/exposure guards pass, clean logs, all 2,936 owner files unchanged, adapters restored. Summary: sibling known-port-summary.json. Overall frame means and tails remain mixed; no repeatable FPS gain or release-gate acceptance claimed.

Retained in scripts/grid_canvas.gd only at the synchronous door/light validator's immediately enumerated ports. Existing main topology helper and all other callers unchanged. Diagnostic --reference-known-port-connections preserves original query. No cross-frame cache introduced. Existing grid UID preserved. New tests/test_render_known_port_connections.gd and paired UID registered in performance-diagnostics. Normal actual Main/Grid geometry regression passes the same 1,201,232 checks, zero failures; connected-door 1,686/0 and crew-feet 9/0, logs clean, owner files unchanged. Evidence: known-port-trial/normal-integration.json, normal-geometry.log, normal-geometry-owner.json and normal-related-checks.json. Helper: output/renderdoc-tools-2026-10-08/integrate-known-port.py.

Next larger target: inspect exact Moonbay drawing order and state dependencies for retained shell/wall commands, previously measured around 1.48 ms per frame across three rooms. Preserve interleaving with water, doors, crew/props, material inheritance, filtering and all live layout/settings changes; require native pixel parity and matched workload results before normal integration. Full original release scope remains open.
