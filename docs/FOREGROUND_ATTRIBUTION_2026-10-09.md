# Foreground and door/light attribution

Updated: October 9, 2026 · Project: BrineSpace · Task: sustained rendering cost

## Objective and acceptance
Identify avoidable drawing work before a matched optimization trial. The complete PC/Mac release gates remain open.

## Accepted decisions and constraints
Use actual frozen debug=false runtime sources, isolated profiles and bounded instrumentation. Preserve drawing pixels, layers and gameplay. Nested scopes are not additive with parent timings.

## Current state
Private foreground-probe grid attributes 64 frames (1400–1463) of foreground drawing and door/light validation. Normal source unchanged in this attribution pass. Helper: output/renderdoc-tools-2026-10-08/prepare-foreground-probe.py.

Median foreground scope 2.284 ms: legacy door under/over walks 0.477/0.420 ms, humans 0.389 ms, synergy links 0.398 ms, station effects 0.203 ms, hardware 0.185 ms, flooding 0.116 ms. Other measured components each below 0.016 ms. Door/light validation 1.382 ms: door edge state 1.202 ms, room lighting/hatch 0.154 ms, invalidation/snapshot 0.008 ms.

## Verification
Actual candidate completed, source guards and both 64-frame exposure checks passed; log clean, adapter restored, 2,936 owner files unchanged. Workload means 38.268/39.382/39.884 ms, p95 43.690/47.468/52.758 ms, maximum 141.080 ms. Texture peak 2,345.481 MiB. No accepted FPS improvement or release certification from attribution.

Evidence: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/foreground-probe/ (candidate.json, component-summary.json, candidate.log, owner-pair.json).

## Next action
Private legacy-door-skip trial moves the existing layered-room exclusion before port generation. All per-port reference guards remain; this only omits traversal of rooms whose every legacy door is already skipped. Both matched lanes completed under session 80621. Median under/over costs 483/421.5 us reference versus 376/316 us candidate: combined saving 212.5 us. Broader frame means improved 0.355/1.571/3.553 ms in this single pair, exceeding the attributed saving; do not claim those as a repeatable optimization gain. Maximum remains 145.928 ms.

Phase crew/drone/mission/power/door/light endpoints match; final missions, texture exit and pending jobs match. Decode totals differ only in measured sync_usec (16,862 versus 17,546), not counts or sources. All source/branch/exposure guards passed, owners unchanged, adapter restored. Helper: output/renderdoc-tools-2026-10-08/prepare-legacy-door-skip.py; artifacts in sibling legacy-door-skip/.

Next test reuse of remaining legacy door data within one foreground paint, avoiding the duplicate underlay/overlay traversal while preserving command order and same-frame state. Require reverse-order confirmation and relevant drawing parity before normal integration. No normal change accepted yet.
