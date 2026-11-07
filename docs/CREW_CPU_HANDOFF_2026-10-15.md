# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: crew CPU / 4× placement

## Objective and acceptance

Investigate remaining crew CPU and 4× placement hitches without changing appearance
or gameplay; benchmark average FPS, action peaks and following-frame pacing.

## Accepted decisions and constraints

Keep prior accepted Bill/Synergy changes installed. No quality, renderer, clock,
crew scheduling, graph/route semantics or art change. Scratch profiles and visible
serial native release runs; private LOD remains separate from normal source.

## Current state

**Trials rejected for admission; normal runtime unchanged.** Private packed-ID
link assembly and flatter topology-key trials are preserved in
`C:/bs-crew-cpu-20261015/`; helpers in `output/crew-cpu-20261015/`.
Only this handoff, the performance report and CURRENT_STATUS are new project edits
from this task. The temporarily expanded navigation test was restored exactly to
the prior frozen oracle after rebinding its private preload paths.

## Verification

Actual-release diagnostics: normal/4× steady whole-crew CPU about 0.9 ms; two
companion graph rebuilds about 24–25 ms on 4× placement, dominated by suffix
removal and point/link assembly. Small trials do not remove that scope.
Topology-only micro saves 6.6 µs/call; refined link micro is essentially flat.
Private combined graph oracle: 1,609 checks / 259,265 ordered records / 2,328
routes exact. Topology: 14,567 checks pass. Restored normal prefix test: 1,488
checks pass. Independent source review complete.

Clean 1,920-frame reference/candidate/candidate/reference comparison: eight exact
state/camera/path pairs. Normal idle 50.69→51.36 FPS, but forward change nearly
zero; 4× placement-phase mean/p95 slightly worse. Action peaks 80.285→79.202 and
72.669→69.076 ms at 4×; following 60-frame >50 ms counts 1→2 in both orders.
No dependable overall pacing improvement; 0/8 60 FPS gates. No fresh pixel
acceptance claimed for rejected code; selected runtime/art retain prior acceptance.

All 23 owner guards clean; final 2,948 files equal prior post-recovery baseline.
Preserve [earlier incident](TEST_PROFILE_INCIDENT_2026-10-15.md) caveat: this does
not restore the two old legacy metadata files. No task-owned game remains.

## Next action

No more unchanged timing needed. Investigate bulk graph construction or proven
retention, separating GDScript dispatch from native AStar work first. Preserve exact
IDs, weights, disabled state, connection order, routes and standalone validation.
Do not install the private trials based on average FPS alone. See
[results](CREW_CPU_PERFORMANCE_2026-10-15.md) for raw evidence and limitations.
