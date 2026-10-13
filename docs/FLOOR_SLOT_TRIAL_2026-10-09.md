# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: private per-room floor caching

## Objective and acceptance
Reduce broad floor repaint work without changing pixels, layering, simulation or immediate interactive-room completeness. Require matched packaged performance and state comparisons before admission; complete release gates remain open.

## Accepted decisions and constraints
Private overlay only, based on the frozen accepted crew-cache candidate. Normal source and delivery packages remain unchanged. Preserve connectors, legacy rooms and both ordered layered-floor passes. Use isolated profiles and owner fingerprints. Do not combine wall/terrain trials with this measurement.

## Current state
Acceptance decision: do not install this version. The full matched benchmark
completes eight runs/34,560 samples with96 identical gameplay states and no engine
or missing-art failures. Owner2,938 files remain unchanged. Large means regress
28.8321->28.8693ms forward and27.7619->28.1325ms reverse; worst frames improve
153.448->139.740ms and145.722->138.243ms, but five >100ms frames remain in each
candidate order and all24 large phase gates fail. Results: workloads/analysis.json.
The small-station improvement does not justify the large-station regression.

Prototype and exact two-file overlay live in D:/bs-release-crew-cache-20261009/floor-slot-trial/. Per-room floor nodes use neighborhood dependency snapshots, preserve original child order and compensate for parent zoom scaling. Existing retained parent painter remains the visual reference. The first raw-script compile probe failed because its duplicate global class name hid GridCanvas; the corrected compilation harness and actual packaged overlay load pass.

## Verification
Timing-only preparation diagnostic completes in prepare-diagnostic/workloads-v2:
actual debug=false40-room lighting at1/2/4x,540 samples, zero errors/missing art,
owner2,938 unchanged. Nested preparation means446.82/424.78/403.20us per frame;
parent callbacks510.36/484.03/460.01us include that preparation. Floor-slot draw
callbacks3268.56/3070.71/2942.44us are separate; room setup1754.68/1615.15/1622.84us
is nested across relevant draw callbacks, not an additive whole-frame interval.
This is attribution, not a matched optimization acceptance. The measured~0.4ms
preparation cannot alone explain the remaining~12ms gap to the60FPS frame budget.

First diagnostic launch fails with WinError112 while copying the test runtime;
failed workloads/ evidence and unchanged-owner guard retained. The completed
full benchmark's disposable runtime/BrineSpace.pck is removed only after matching
its accepted SHA256, reclaiming3,623,046,249 bytes. cleanup.json records exact
target/hash; delivery PCK, reports, profiles, captures and source remain intact.

Visible-room correction completes in release-parity-visible-v2: all visibility
assertions pass;23 of25 exact image pairs pass. Placement/removal first-frame
pairs differ by up to39 channels. Normal construction completion replaces free
fixture placement because free placement intentionally schedules station centering.
Zoom visibility is checked after deferred camera restoration. Both failed runs
are retained with unchanged owner guards.

Control release-parity-visible-baseline disables floor slots throughout, retaining
the original combined painter. It reproduces the same two first-frame failures
and maximum39 difference; removal difference maps are exactly equal, placement
maps differ by at most4. Thus the failures do not establish a floor-slot-specific
defect. Their underlying cause remains unresolved; do not claim full immediate
pixel acceptance. Images reviewed and differences.json/baseline-attribution.json
preserve attribution. Owner2,938 unchanged for both runs.

Visual review of q0 confirms the station is visible and its floors/props render.
Review of first-frame-place reveals the affected placement is offscreen after the
fixture's close-view camera move. Consequently the 25 exact comparisons alone
are insufficient evidence for immediate-frame mutation coverage. Correct camera
targeting and require affected-room visibility before trusting those checks.

Actual debug=false packaged parity passes 15 settled and 10 immediate-frame exact RGBA comparisons. Coverage includes rotation, power, lighting fade, raised walls, placement, removal, culling, pan and zoom. No engine errors; owner 2,938 files unchanged. These snapshot checks do not establish full motion, all room types or endurance acceptance.

The eight-run matched performance driver is confirmed live (Python PID720112, packaged child PID719728 at this handoff). First forward 12-room pair averages 14.3291 to 14.2606 ms/frame; this small preliminary difference is not an accepted gain. Full 12/40-room, 24-phase, both-order results and owner guard remain pending in workloads/.

## Next action
Next decision: retain this as an unadmitted experiment. Lighting p95 regresses
at all three speeds in both large-station orders. Attribute preparation overhead
and continuing live-render costs before choosing another variant; do not repeat
the full benchmark without a measured change. Resolve baseline first-frame
environment/reference differences separately. Full release gates remain open.

Corrected fixture parity-visible.gd and runner
output/renderdoc-tools-2026-10-08/run-floor-visible-parity.py are staged, unrun.
They focus the camera before each mutation and assert the affected cell remains
inside the visible viewport. Run after the current GPU workload ends. Both
12-room benchmark orders now complete:48 gameplay state pairs match; means
14.3291->14.2606ms forward and15.1974->14.5438ms reverse. Large comparisons pending.

Finish the existing benchmark, compare all gameplay states, frame distributions, stalls and rebuild counts. Review large-room, flood/ward and zoom/motion dependencies before any production admission. Reject or adjust the prototype if measured performance or visual behavior regresses. Target hardware and Mac certification remain open.
