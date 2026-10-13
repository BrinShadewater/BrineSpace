# Project handoff

Updated: October 8, 2026. Project: BrineSpace. Task: door validation profiling and immutable queries.

## Objective and acceptance
Continue full PC/Mac readiness. Optimize measured work with matched workload/state proof; do not admit tiny private gain as60FPS remedy.

## Accepted decisions and constraints
Keep immutable door-query trial private/deprioritized. Public door lists remain mutable copies; no gameplay/layout decisions change. Main owns cache, no global images/scene retention. Existing normal crew-foot cache fix retained in private grids. No normal source change this turn.

## Current state
Private door-stage-grid.gd/run-door-stage-census.py wraps current cached helpers only while validating doors/lights; original helper called once. Normal crew-foot scale/owner fix copied into existing candidate grid. Single actual40room/fourcrew three60frame idle diagnostic, profileron, traceoff; hooks affect timings.

Private shared-doors-main/grid.gd: separate immutable cached query for connection/render membership, preserves public mutable-copy API, flagfalse/true comparison. shared-doors-test.gd and native runner; actual run-shared-doors-actual.py. Packs/report/comparison evidence under output/renderdoc-tools-2026-10-08/{door-stage-census,shared-doors-native,shared-doors-actual}. Adapter restored after each actual run. Main/Grid are private candidate copies, not new export.

## Verification
Door profile362validations accumulated634068us (~1752us each including wrappers). Connectivity34028calls/134135us; frame10136/72424; ports14480/69604; variant10136/78249; crew_depth20272/39035; lights14480/37002; parts10136/15180. Some helper scopes nest; not additive. Existing same-frame crew gather and part caching already active. No missing art/errors/leaks/unfocus; owners2936same/terminal.

Native shared-query290checks0failures: eight actual roomIDs/four rotations/exact door order, readonly repeated identity, mutable public copies independent, connected-neighbor agreement, cache clear/reconstruction. Actualdebug=false40room short matched pair, same module/PCK onlyflag differs:0 versus132568shared calls confirms executed path. All compared crew/drone/door/light/power/zoom/prop counters equal allthree phases. Validation1386.267to1360.217us,1406.133to1378.283us,1399.783to1383.033us: only16.75-27.85us saved. Means improve14.58-46.87us, p95 worse1x/2x/better4x; noise-limited/no robust whole-frame gain. Peak1734.531MiB/exits228.259MiB/uploads808same; shorter idle chronology is not memory reduction against full9x180. Actual reported means~32-33ms still fail gates. Owners2936same/adapter byte-restored/alljobs terminal.

Current OS read-only snapshot after tests:66894552KiB physical/~63.8GiB total,37054056KiB/~35.3GiB free. Does not support assuming present RAM exhaustion; not historical sampling or per-frame paging proof. No further hardware assumptions. Disk remains constrained; current control EXE restored, obsolete candidate/ordinaryQA recovery contracts remain.

## Next action
Deprioritize further query microcaches: measured absolute saving too small. Return to significant renderer submission/geometry work with actual executed path proof, referencing existing complete draw census and exact primitive trials. Do not repeat private style-query runs merely to obtain favorable p95. Normal cache correctness fix still requires packaged camera/door visual acceptance; full original bug/load/memory/endurance/targetPC/M1/signing/notarization/frozen-package gates open. Preserve archives/art/userdata and default quality.
