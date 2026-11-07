# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: live-room preparation and instrumentation calibration

## Objective and acceptance

Continue full PC/Mac performance readiness. Identify the larger live-room preparation cost and accept changes only with behavioral parity and a matched useful saving. Verify renderer timing does not explain the reported frame deficit.

## Accepted decisions and constraints

No new normal runtime change admitted in this pass. Keep within-live-pass connection caching and inverse port queries private. Correctness alone does not demonstrate a worthwhile optimization. Preserve all current art, simulation, owner layouts and release gates. The prior wave-culling turn was progress: accepted source plus current native and matched workload evidence.

## Current state

Evidence directories:

- `output/live-preparation-profile-2026-10-07/`: current normal Grid subclass, nested timers active only inside live surface drawing.
- `output/live-connection-pass-2026-10-07/`: private symmetric boolean reuse only inside one live surface call; canonical occupied room dictionaries only, cleared at call end.
- `output/inverse-port-query-2026-10-07/`: private pure port query plus actual Main integration. First algorithm/source/results preserved separately; revised zero-rotation fast path filters unmatched local cells/sides before edge checks.
- `output/render-timer-overhead-2026-10-07/`: both backends load actual normal Main; only renderer timing enabled/disabled differs.

No normal script, artwork, UID, export, owner profile or publication change. All processes terminal.

## Verification

Nested native attribution: all six full gameplay states and texture endpoints match the prior current-source fixture; no missing art/errors/warnings/leaks. At1×: instrumented inclusive live scope6.744ms; connection checks160/0.806ms; actor occupancy24/0.198ms; plain-view checks24/0.038ms; view lookup28/0.221ms. Nested costs overlap; instrumentation adds overhead. Crew scans are not the strongest observed lead.

Within-pass reuse:44,252 actual-Main connection checks pass, covering authored rooms/rotations, reverse/repeat/cardinal/noncardinal/branch queries, substituted preview dictionaries, same-tick rotation/new passes/demolition and cleanup. Native matched40 six states/textures equal, ordinary door setup savings0.081–0.118ms; inclusive live changes0.041–0.277ms, whole-frame p95mixed37–53ms. Limited return; no admission.

Inverse port query:133,320 exact reference checks pass for each revision, including all authored rooms, negative/wrapped rotations, non-square sizes, invalid/outside ports and unknown sides. First native station revision makes preparation slower and is rejected. Revised candidate-only comparison uses unchanged preserved normal control; all six full states/textures equal. Ordinary door setup saves0.010–0.061ms, door validation changes−0.055 to+0.005ms, inclusive live mixed. No decisive station gain; no admission. Earlier candidate source/log/JSON retained.

Renderer timing on/off: fresh native normal pair, six full states/textures equal, no art/errors/warnings/leaks. Disabled lane CPU/GPU timer fields correctly0. p95on/off:39.211/39.393,40.319/39.256,37.078/40.838,39.069/39.029,47.921/51.982,53.756/50.216ms. No consistent substantial reduction; frame gate remains failed. This isolates enabling renderer timing, not all diagnostic overhead or packaged performance.

Primary upstream context: [RenderingServer documentation](https://docs.godotengine.org/en/stable/classes/class_renderingserver.html) describes opt-in viewport measurement; [Compatibility timing source](https://github.com/godotengine/godot/blob/master/drivers/gles3/storage/utilities.cpp) reads buffered GPU queries from earlier frames. Upstream source is context, not certification of the local binary or proof of zero overhead; the native pair tests this local concern directly.

All owner fingerprints2,936 before/after, zero changes. No refreshed debug=false PCK or Windows/Mac gameplay certification. Normal frame/loading/memory budgets and endurance remain open.

## Next action

Freeze the latest accepted normal source/runtime dependencies using the maintained release workflow, build a refreshed Windows QA release executable, audit PCK outside the checkout and measure actual debug=false gameplay in an isolated profile. Keep private crew/drone storage providers and both connection prototypes out of these accepted inputs. Compare packaged results with current source evidence before another small query optimization; continue full original release issue, hardware, memory, endurance and Mac requirements. This candidate is for measurement and certification, not itch publication.
