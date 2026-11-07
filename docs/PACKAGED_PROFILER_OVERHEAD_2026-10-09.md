# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: profiling overhead attribution

## Objective and acceptance

Determine whether benchmark draw profiling or viewport timing queries explain
large-station frame time before selecting the next rendering optimization.

## Accepted decisions and constraints

Same actual debug=false cab0dd6874401f88 Windows candidate and unchanged PCK.
Diagnostic-only test with known idle editor667496 recorded, no other engine/game
activity accepted. No final target-hardware, full-workload or release certification.
Do not change benchmark defaults or game quality based on an unproven overhead.

## Current state

Session34751 exits0: four modes (neither/draw/viewport/both), forward and reverse,
40 rooms, idle+lighting, 180 frames/phase at1/2/4 speed:8,640 measured frames.
All48 selected phase-end gameplay state comparisons equal, zero logged errors/
safe-image failures. Owner2,938 unchanged. Every mode uses180 warm-up frames.
Captured state covers state/crew/drone_fleet/companions/hardware/resource_flow/
architects, not every field of the full save schema. Same two-action texture
endpoint1,952.067MiB; broader zoom/placement workload peak remains unverified here.

## Verification

Evidence D:/bs-release-crew-cache-20261009/profiler-overhead/{completed,analysis,
identity,owner}.json and eight per-run JSON/log/capture sets. Analysis exits0.
Mean frame ms forward/reverse: neither34.192/32.005; draw33.974/31.758;
viewport31.547/32.042; both31.529/31.725. Forward viewport apparent gain2.645ms
does not reproduce in reverse (+0.037ms). No consistent large profiling penalty
proven; ordinary rendering workload still exceeds budget. Neither-mode max
154.675/93.428ms; worst phase p9568.385/61.280ms. All results remain diagnostic.

Historical traced original-package sanity check (different build) examines4,073
same-phase consecutive boundaries: reported mean31.098ms vs inclusive31.221ms;
excluded collector gap mean0.123ms/max0.429ms. This does not measure collector
overhead in the new cache package or explain its full frame-time cost.

## Next action

Inspect current packaged draw/profile breakdown and take targeted native rendering
captures to locate submission/fill/layer costs before edits. Preserve quality and
test any change against matched workloads and pixels/behavior. Final standard
benchmark requires no competing engine activity; native Mac/signing, original
nine bugs, save/relaunch, endurance and all original release gates remain open.
