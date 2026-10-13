# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: current mixed-footprint performance coverage

## Objective and acceptance

Add explicit current multi-cell room coverage alongside the existing reported,
current-save and single-cell40-room workloads. Require real powered rooms, a safe
natural Moonbay dispatch, crew/drone activity, isolated muted native execution.
Full performance/release acceptance remains open.

## Accepted decisions and constraints

Original benchmark defaults unchanged. Optional `mixed_large` creates four2×2
rooms plus ordinary rooms to total40. Normal placement/door/ocean rules apply.
Dedicated free-build/reserve/failure flags remain fixture-only. One clean fixture
Bill pilot is introduced before prewarming, declared in output; no owner saves,
layouts or gameplay rules altered. Production renderer unchanged.

## Current state

Maintained `tools/release_benchmark.gd` supports mixed fixture, composition report,
natural mission dispatch/diagnostics and open-intake checks. CLI wrapper exposes
`mixed_large` as optional choice. Native runner
`output/renderdoc-tools-2026-10-08/run-mixed-large-workload.py` reuses existing
debug=false runtime, current accepted Grid/Main/Bill overrides and bounded reports.
Artifacts: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/mixed-large-workload/`.

## Verification

Initial dispatch failure: saved source has Branforth aboard and already busy;
other architect crew absent. Diagnostic confirmed this, then dedicated fixture
pilot added before warm-up and dispatched through normal Mission API. No mission
state injected and no job/route/power requirement bypassed.

Successful native run1,080 measured frames, idle/pan/zoom/lighting at1×/2×/4×.
Actual composition field:40 rooms/52 occupied cells, one each Moonbay, Tidal,
Hydroponics Farm, Storage Depot. Ocean faces checked clear; active crew/drones and
at least20 powered cells verified. Bill mission advances naturally from approach
to flood (water0.05556,clock54s); Tidal powered with no offline reason at final
snapshot. No missing runtime-art errors or engine errors in successful run.

Mean30.631ms,p9545.459,p9953.177,max110.070;19 frames>50ms,one>100ms.
Peak texture2928.086MiB. Single baseline, no optimization comparison or certification.
Visual motion/join review and full mission cycle still pending.

110.070ms zoom1× sample: sampled process frame476 records THREE uploads,
433,520,640 decoded bytes (413.44MiB),49,969us total upload work. Sources:
mine-north-effects,mine-south,mine-south-effects. Next process-frame477 upload list
empty; latest-upload record matches the sampled frame, so this is not attribution
to an unrelated stale event. About50ms is accounted for; remaining stall time
unassigned. GPU query timings delayed, not aligned costs. Trace collection210us,
action2us, simulation step3120us. Other slow samples include uploads and CPU steps;
do not label every slow frame a room-art or upload defect.

Owner2,938 files unchanged, processes terminal, runtime override restored. No
screenshots/art/runtime copies. Room-composition reporting now exercised in actual
gameplay, not only parser-checked. Existing PC/Mac/FPS/loading/endurance/save/UI/
original-nine-bug gates remain open.

## Next action

Investigate bounded live texture working-set/request scheduling around that
three-upload burst. Reuse rejected global-cache/preparation/indexed provider
evidence; do not repeat unchanged trials. A selective lossless effect-only storage
trial may differ materially from the rejected21-source renderer, but first inspect
prior subset evidence and compare the actual needed working set. Preserve selected
pixels/filters/timing, fallback and session lifetime. Separately profile current
mixed-room CPU drawing, extend natural mission phases and repeated workload runs.
