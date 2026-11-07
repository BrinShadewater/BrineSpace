# iPad card crop demand loading — October 19, 2026

Validation2 candidate `brinespace-58324c425a8fc834`; source SHA-256
`58324c425a8fc834d3423fb2e487e8063b3efef0cb0729da147653051c29e161`.
Active branch `codex/ipad-memory-placement-2026-10-17`, HEAD81b2f9a4 plus accepted
dirty work. Frozen Mac/Windows deliveries unchanged.

## Change and evidence

Grid startup formerly decoded all79 compressed card staging images and scanned
their crop bounds, including unused fallback art. It now postpones those scans
for tablet deferred-card textures until fallback drawing requests them, caches
the exact result and retains the existing eager desktop/supplied-image behavior.
The legacy crop algorithm, raster sources, mipmaps and rendering are unchanged.

Native red test:79 unnecessary CPU image reads,124.307ms in the isolated crop
preparation phase. Green:0reads/.021ms. All79 demanded crop rectangles match the
previous algorithm, repeated demands reuse them, and bounds after prior UI upload
remain identical. No GPU upload is caused by crop-only demand. This reduces
startup/transient pixel work; retained GPU texture bytes remain991.548MiB in the
frozen40-room native comparison. **No steady-state process-RAM saving is claimed.**

Frozen40-room candidate pixels equal the baseline hash exactly. The single native
before/repeat interface-grid observations3.986/2.623s are cache/order sensitive;
they do not establish a controlled whole-load or physical-iPad improvement.

Seven actual-PCK checks passed: tablet card regions/storage, raw texture regions,
shared room floors, hull UI175checks, RunSave and tablet controls. Asset audit:
36197selected,0missing/changed/remapped/unexpected. Source audit437selected/
433extras,0missing/changed/unknown. Export/app packSHA identical and strict native
signature passed. Scoped reviewer found no actionable issue. Full logs and builds:
`/Users/Shared/BrineSpace-ipad-optimization-20261019/card-region-demand`.
[Portable evidence](ipad-memory-placement-evidence-2026-10-19/card-region-demand/native-summary.json).

## Physical validation

Updated Validation2 installed on iPad13,18/A14/4GB/iPadOS27.2. All five original
save/checkpoint files remained SHA-256 identical through installation. The packaged
QA workload completed all nine idle/zoom/placement-request phases at1×/2×/4×:
5,400 sampled frames; phase maxima33.588–49.824ms, no reported artwork failures
or automatic reports. This fixture has40single-cell rooms/one active actor, uses
fixture-only free building/failure bypass and deterministic1/60 simulation.
It does not certify full-port-connected, multi-cell, organic play or actual gestures.

192 native1Hz exact-PID footprint samples: peak1,867,844,912bytes, final
1,820,151,040bytes. Initial3-room fixture setup4.910s (interface/grid3.638s,
interface art.587s); warm-up/40-room fixture preparation are separate. No paired
baseline establishes a RAM reduction, first-load improvement or leak clearance.

The benchmark did not change the five owner files. Afterward they were restored
hash-exact again and the QA opt-in marker was verified absent. Documents-only AFC
cleanup initially failed; root app-container cleanup succeeded and absence was
independently verified. Normal Validation2 relaunched with the original checkpoint.
The initial XCTest authorization attempt timed out; the later authorized UI pass
below dismissed the test-session recovery notice and completed station testing.
Method-driven benchmarks alone do not establish touch acceptance. Initial loading,
memory growth, organic multi-crew play and release readiness remain open.
[Physical summary](ipad-memory-placement-evidence-2026-10-19/card-region-demand/physical-summary.json).

## Authorized touch and Save/Continue follow-up

The owner approved the renewed Apple prompt; fresh helper command acknowledgment
confirmed connection. Actual Continue reached the original cycle64/seven-room
station. Dragging the selected blueprint from invalid water back to the hand
cleared selection; native save inspection confirmed pinch zoom changed
.0708597375174268→.219108316577404, and the rotation button changed Cold Store
orientation to1. Resources/hand/room list/cycle and exact timer remained unchanged.
Codex content visibly scrolled with a touch drag. Home→activate returned paused
and intact. No two-finger rotation gesture or paid placement claim is made here.

After this reversible exercise all five original files were restored byte-exact
before owner launch. Save→title→Continue→Save passed full gameplay-state and exact
1.11834893097652 timer parity. Original speed2/4× restored after the existing
Continue1× reset. Only event history, timestamps, scroll/camera and path metadata
differed after UI use. Final station visibly paused/menu closed at cycle64; helper
93794 remains connected for its two-hour session.

Final Save78.278ms; errors0, final-session automatic reports0.
Owner first/repeat station setup4.316/3.356s; cache-sensitive,
no paired loading gain established. A23.178s frame/report already existed before
the UI checks, coincident with XCTest/TouchID authorization. It is retained,
not erased or presented as proof that application stalls are resolved.
[Actual UI evidence](ipad-memory-placement-evidence-2026-10-19/card-region-demand/actual-ui-summary.json).
