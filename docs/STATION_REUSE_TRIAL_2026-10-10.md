# Project handoff

Updated: October 10, 2026 · Project: BrineSpace · Task: activity station reuse

## Objective and acceptance
Reduce the measured destination-selection cost without changing ordered station
contacts, RNG, routes, crew state or selected visuals. Full release gates remain open.

## Accepted decisions and constraints
Owner requests muted native testing on a secondary monitor. Use isolated profiles;
do not change owner settings. Preserve canonical station order separately from the
observation-room target-sort reversal. Cache only within one synchronous decision.

## Current state
Private output drivers prepare/run-placement-goal-stages.py and
prepare/run/analyze-station-reuse-trial.py under output/renderdoc-tools-2026-10-08.
Original release payload plus one frozen Bill diagnostic override. Same private
source pack in both lanes; BRINE_STATION_REUSE selects off/on before game loading.
Candidate duplicates the canonical station array before optional reversal and
uses the original contact-distance rule instead of repeatedly calling stations().
Normal scoped reuse is now retained for the measured destination CPU reduction
and compatibility checks below. This is not a global frame-rate improvement claim.

Maintained tools/release_benchmark.gd now mutes Master, sets BRINE_SILENT, selects
a suitable non-primary display and reports selection. Measurement guards reject
unmuted audio or a move to the primary display. tools/run_release_benchmark.py
isolated environments now set BRINE_SILENT=1 before launch. Current private drivers
also launch at the observed left secondary position to avoid initial primary placement.

## Verification
Goal stage session94011 terminal0: 540 samples; three states equal control.
Station contact resolution accounts for12.4/19.1ms of20.4/31.6ms goal selection
at2x/4x; target sorting2.9/4.8ms, smoothing0.1/1.9ms. Owner2,938 unchanged.

Station reuse session26972 terminal0: four lanes/2,160 frames, six phase-end states
equal, logs and missing-art checks clean, debug=false and input disabled; owner
2,938 unchanged. Evidence D:/bs-release-crew-cache-20261009/benchmark-input-isolation/
station-reuse-trial/{paired-analysis,completed,owner}.json.

| Order/speed | Goal selection control -> candidate ms | Placement frame control -> candidate ms |
|---|---:|---:|
| Forward2x | 20.461 ->8.206 | 145.028 ->127.564 |
| Reverse2x | 19.456 ->8.281 | 141.595 ->131.964 |
| Forward4x | 32.621 ->14.722 | 150.529 ->133.204 |
| Reverse4x | 31.554 ->13.780 | 145.244 ->135.553 |

Logical Branforth route calls remain23/55 in both lanes; station-resolution time
drops to0.5-0.8ms. All phase means lower but p95/p99 mixed, and every full phase
FPS gate still fails. No goal selection occurs on1x placement; do not credit its
timing differences to reuse. Timings nested/non-additive and bounded instrumented
workload; full action/behavior/visual coverage remains required.

Window setup reports muted=true, selected2/primary1. Windows native rectangle read
for owned process: left-3348, top69, right-1412, bottom1188, entirely on left display.
Native current-tool test-muted-secondary-benchmark.py passes three focus changes,
mute and secondary-screen assertions; owner2,938 unchanged. Python syntax checks
pass. Evidence window-preference-check/{probe.log,owner.json}. Private gameplay
trial predates the new per-frame mute/screen guards; separate helper check verifies
setup/focus behavior, not a replay of those guards throughout the previous batch.

## Next action
Normal implementation now staged in scripts/crew_room_activity.gd (at_stations
resolver; at delegates), scripts/bill_npc.gd (decision-local canonical snapshot
before reversal), tests/test_activity_station_reuse.gd plus Godot-generated UID,
and crew subsystem registration in tests/index.json. No prototype flags/timers.
Existing unrelated working-tree edits preserved; whole Git diff is not this change.

Red check exits1 on missing scoped resolver before implementation. Green checks:
601 new cases/0 failures, galley counter test0, observation sofa90/0. Covers
first contact on overlap, inclusive5/36px threshold edges, reversal isolation,
fresh moved desk geometry and comparison with existing at lookup. Both isolated
owner guards2,938 unchanged. Evidence station-checks-{red,green}/ beside trial.
These lightweight checks do not establish all owner-layout gameplay compatibility.

Broader normal-source four-lane benchmark session44074 is running, observed owned
BrineSpace process39056 and phase progress through2x idle at this handoff. Poll
this session before launching another GPU job. Evidence normal-station-reuse/;
control/candidate each use two hashed scripts in normal-station-reuse-packs/.
All8 standard actions x3speeds x180frames =4,320 samples per lane, both orders.
Driver run-normal-station-reuse.py restores temporary runtime config on exit;
analyze-normal-station-reuse.py requires completed marker before comparing48
phase-end states and phase timings. Do not claim broader acceptance before job
completion, owner guard and comparison. Freeze/delivery packages not rebuilt.

Session44074 subsequently exits1 after a complete clean forward-control run:
driver incorrectly asserted4,320 trace rows, while collector intentionally caps
at4,096. All24 phase aggregates and4,320 measured frames present. This was a
driver validation defect, not gameplay failure. Initial owner guard2,938 unchanged
retained as initial-owner.json; driver-recovery.json records old expectation.
Corrected driver respects existing cap and resumes validated complete lanes only
when both source-member hash maps still match. Existing packs reused; completed
forward-control not rerun. Reused lane additionally checks marker/clean log,
debug=false, empty missing art, input guard,24 phases and4,096 retained trace rows.
Resume20894 observed live owned process51568/forward-candidate startup. No new
performance acceptance yet; temporary config restoration remains exit-finally.

Resume20894 completed terminal0: four complete lanes/17,280 measured frames;
48phase-end states equal, all logs/art/input/audio/display guards clean and owner
2,938 unchanged. Final paired-analysis.json generated. Temporary config restored.
Forward mean29.352->29.168ms; reverse28.878->29.019ms. >50ms frames207->180 /
177->173; >100ms7->7 /6->7. All candidate full phase gates fail. p95 improves10/24
forward,15/24 reverse; p99 improves14/24 forward,5/24 reverse. No consistent global
FPS/p99 benefit. Normal1x placement maxima153.064->139.405 /149.051->133.079ms;
1x demolition159.074->140.228 /144.454->136.828ms improve both orders.

Remaining2x candidate placement frame59 is104.796/104.477ms with192,675,840B
sampled drone uploads taking22.1/23.4ms. Forward control same bytes98.533ms;
reverse control96,337,920B82.704ms. Crew1.6-1.7ms across those cases. Difference
in upload workload/timing means this is not an isolated causal station-reuse
regression or clearance proof. Keep stall-details.json/frame59-comparison.json;
upload/renderer stall remains open. Full48-state match is phase-end, not every
intermediate rendered animation frame. No visual pixel comparison claimed here.

Additional isolated activity session80736 terminal0: crew activity48room/rotation/
actor approaches including facing/save validation, lounge11assertions/0, cold-store
four rotations and blocked-front rejection/0. Owner2,938 unchanged. Evidence
station-checks-activity/{results,owner}.json. Benchmark source explicitly disables
VSync and Engine cap after game settings; focus/driver overrides not measured
and cannot be excluded by that source inspection alone.

Retain the narrow canonical-list reuse, supported by repeated private destination
timing reductions, normal1x placement/demolition maximum reductions and compatibility
checks. Global smoothness, p99 uncertainty and all release gates remain open.
Next profile/optimize synchronous graph emission and static rendering; preserve
ordered routes and independent graph ownership. No further GPU jobs active from
this handoff;20894/44074/80736 terminal. Do not rerun completed lanes without a
new change, failure or specific unresolved concern. Frozen delivery not rebuilt.
