# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: large-room water preparation concurrency

## Objective and acceptance

Continue the full PC/Mac performance plan. Preserve current-frame pixels, animation,
settings, simulation, room ownership and owner files. This private trial is not a
complete current-checkout export or hardware certification.

## Accepted decisions and constraints

The first pair improved pacing, but the reverse pair regresses it. Do not integrate.
No automatic quality changes, art changes or broad refactor. Default normal source
remains unchanged. Existing private retention1 and low worker priority are common
controls; transparent-atlas deferral is absent from both lanes.

## Current state

A three-moonbay workload exceeds the private water-worker coordinator's two-job
limit: the third room usually builds water synchronously during drawing. Candidate
adds an explicit coordinator limit3 under --water-three-jobs; default2 remains.
No simulation/nav/SceneTree/GPU calls added to worker code. Current inputs and
mandatory join/discard rules are unchanged.

Artifacts: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/
water-worker-three-proof/, water-three-runtime/, water-three-reverse/.
Helpers: output/renderdoc-tools-2026-10-08/test-water-three-jobs.py,
prepare-water-three-runtime.py, analyze-water-three.py, prepare-water-three-reverse.py.
Reverse benchmark completed and analyzed. Crew-stall diagnostic completed separately.

## Verification

Native599checks: reference1 expected failure (only2 concurrent jobs), candidate0;
288 full-room exact raster pairs across rotation, filtering, parent material,
water level/clock; replacement inputs, ancestor hide/show, reduced-motion toggles,
exit joins and weak-owner release. Candidate816 native jobs submitted/joined.

Actual debug=false1080p40room reference-first paired idle runs1000frames at1x/2x/4x:

| Speed | Mean ms 2jobs ->3jobs | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| 1x | 38.630 ->36.339 | 45.509 ->41.326 | 58.115 ->51.814 | 88.741 ->80.660 |
| 2x | 40.199 ->37.459 | 48.436 ->46.126 | 63.085 ->56.253 | 90.446 ->109.124 |
| 4x | 40.305 ->39.267 | 54.295 ->52.642 | 71.545 ->70.831 | 128.357 ->126.103 |

Mean/p95/p99 improve3/3, mean savings1.04-2.74ms; max worse2x. FPS and >100ms
stutter gates still fail. Compiled base SHA b740f61e7c684656de7b1303e09de6cbbdebdf8f3871290f18097edc7f07ecca
matches both lanes; actual coordinator limit/peak2 versus3 validated.
Actual6238 reference and9104 candidate jobs all joined; active0. Unique measured
worker events5879/8566 fully cover expected joins. Typical waitmedian2us/p994us;
maxwait28.778->29.235ms, rare scheduling hitch remains. Texture peak2345.481MiB,
exit228.259MiB and486 drone/4074 crew uploads equal. Ready misses801->798 includes
transparent cells and is not a proof of all visible art availability.
Every compared phase crew/drone/mission endpoint matches. All three missions cross
pressure boundaries, return/unload and recover full navigation; final cleanup drains
pending drone jobs3->0 and releases router. Owner2936 files unchanged/logs clean/
processes terminal/adapters restored.

Mean stage costs (overlapping scopes): live_rooms10.839->9.224ms;
large child base5.552->4.017ms; moonbay base4.773->3.249ms. Extra worker preparation
executes: third room253->3119jobs, prepared hits711->7364. Do not sum overlapping scopes.

## Reverse result and crew-stall attribution

Reverse actual debug=false candidate-first pair, same compiled base hash and all
runtime/branch/cleanup/source guards:

| Speed | Mean ms 2jobs ->3jobs | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| 1x | 35.824 ->36.774 | 38.044 ->42.187 | 49.740 ->52.081 | 77.253 ->102.533 |
| 2x | 36.663 ->37.633 | 42.962 ->46.306 | 53.240 ->58.853 | 75.599 ->105.008 |
| 4x | 37.401 ->39.762 | 49.301 ->53.736 | 67.291 ->70.923 | 126.989 ->123.686 |

Mean/p95/p99 worse3/3 in reverse order. Keep private: overall improvement does not
repeat. Moonbay script draw still decreases in both orders, but reverse reference
also has lower environment/actor costs and render CPU/GPU measurements. Host-state
variation is possible, not proven; do not assign it a cause without direct evidence.
See water-three-components.json and both analysis.json files in artifact root.
Both orders: job/event coverage, endpoints, final missions, texture peaks/exit,
486drone/4074crew uploads, owner2936 unchanged, clean logs, terminal processes and
adapter restoration pass. Broad action/limited-core tests remain unperformed.

A separate repeated non-upload hitch was found at sampled engine frame3086,4x:
94-99ms across four lanes, crew scope61-66ms, no drone GPU upload, worker waits3-6us.
Crew timing alone does not prove which actor/function is responsible.
A further isolated actual-release probe records existing crew_frame_usec only for
frames3078-3094 (17 records) without changing gameplay scripts. It reproduces104.113ms
at3086, crew70709us, ordinary Branforth update523us/rebuilt=false. Adjacent frames
crew1348/1402us. The existing actor timing excludes moonbay/expedition branches and
other crew-pass work, so it does not establish that Branforth causes the hitch.
Other crew/mission/companion work must be timed before a remedy. GPU uploads and
water-worker waits do not explain this particular frame.
Probe artifacts: crew-stall-attribution/reference.json, crew-stall-window.json,
owner-pair.json and clean log. Probe phases35.768/36.719/37.377ms, peak2345.481MiB;
all normal release fixture guards, owner protection and cleanup pass.

## Next action

Narrow the crew-pass hitch with bounded per-operation timing: flooding/fire/safety
reconciliation, mission/expedition advancement, actor topology/rebuild, social,
companions and passage. Preserve deterministic frame identity and existing current
navigation ownership, goals, assignments and simulation. Do not assume a navigation
rebuild merely from the aggregate crew timer. Continue source-matched release proof
and relevant behavior tests for any remedy. Three-job workers remain private;
if revisited, control/measure host variability and limited CPU-pool behavior first.
Full original release requirements remain open; normal gameplay source unchanged.
