# Legacy door plan trial

Updated: October 9, 2026 · Project: BrineSpace · Task: sustained rendering optimization

## Objective and acceptance
Remove duplicate legacy-door traversal within one foreground paint while preserving drawing commands and same-frame state. Full PC/Mac release gates remain open.

## Accepted decisions and constraints
Retained after matched reverse confirmation and drawing parity. Plan is local to one paint, never retained across frames. Missing/invalid texture fallback and original per-port exclusions remain. The diagnostic --reference-legacy-door-plan path preserves independent traversal. This acceptance covers this optimization, not a complete release candidate.

## Current state
Normal scripts/grid_canvas.gd now builds an ordered array of center/source rectangle/size/rotation once before the underlay, then reuses it for the overlay. The original traversal remains available as reference and for callers without a prepared plan. Added tests/test_legacy_door_plan.gd and its paired UID, registered in performance-diagnostics. Helpers in output/renderdoc-tools-2026-10-08/: prepare-legacy-door-plan.py, test-legacy-door-plan.py, integrate-legacy-door-plan.py and test-native-legacy-plan.py. Pre-change bytes and SHA record retained in the trial artifact directory; no unrelated changes reset.

## Verification
First packaged pair complete: median legacy under/over 436/416 us reference versus 388.5/28 us candidate; combined 852 -> 416.5 us. Full means 38.454/39.554/40.732 -> 37.141/38.884/39.894 ms; larger full-frame differences are not yet a repeatable speedup claim. Maximum candidate 139.047 ms, still over release gate. Both 64-frame live ordered-plan proofs pass with 30 entries per sample. Source and branch guards pass.

Separate isolated headless command-recording test executes extracted original traversal against extracted candidate planner/drawer: 1,442 cases, zero failures, clean log, verified user directory, owner 2,936 files unchanged. Covers ten frames, four sides, connected/unconnected, layered rooms/neighbors, duplicate ports/rooms, special always-draw IDs, three sizes and missing texture fallback. This proves command arguments/order, not standalone native pixel captures or full release visual acceptance.

Evidence: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/legacy-door-plan/ (reference.json, candidate.json, command-parity.log, command-owner.json).

Reverse pair completed: median under/over 443.5/418.5 us reference versus 351.5/26 us candidate, combined 862 -> 377.5 us. Saving repeats at 0.436/0.485 ms across the two orders. Broader reverse means 38.236/38.708/40.256 -> 37.869/38.283/39.496 ms; p95 mixed, maximum candidate 151.580 ms. No release frame-gate acceptance.

Both pairs match phase crew/drone/mission/power/door/light state and final mission, texture-exit, pending-job and decoded/upload counts. Only measured sync decoding duration differs. Both logs/source/branch/exposure guards clean, adapters restored, all 2,936 owner files unchanged. Summary: sibling legacy-door-plan-summary.json.

Normal-source native regression passes 480 exact pixel pairs using actual legacy/default/dooranimated.png, both filtering modes, ten frames, three sizes, connections, duplicate ports and layered room/neighbor exclusions. Accepted sample visually reviewed; logs clean. Related normal tests pass: door frame 1,686 checks; crew feet cache 9; profiler lifecycle 6. Owner 2,936 files unchanged. Evidence: native-plan.log, native-plan-owner.json, normal-checks.json; native sample path printed in the native test output. Existing grid UID preserved.

## Next action
Continue measured rendering work: door/light validation remains about 1.2 ms of edge preparation. Attribute connectivity, port generation, pose/depth preparation and retained-part lookup before changing lifetime or invalidation. Full release rebuild, loading/memory/workload gates, endurance, original bug rechecks and actual Mac certification remain open.
