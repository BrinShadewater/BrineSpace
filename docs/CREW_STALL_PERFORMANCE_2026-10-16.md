# Focused crew-stall investigation — October 16, 2026

The focused pass ends without a production patch. The earlier 393.261 ms frame
(370.994 ms crew wall scope) did not recur. Repeatable detour and passage costs
were identified, but this pass did not prove a safe shortcut or establish the
cause of that rare stall. Keep it open; proceed toward release QA rather than
start another broad optimization experiment.

## Scope and identities

All runs use isolated Windows release processes. Native runs use Godot 4.7.2
`ed1daf0bf`, Compatibility / OpenGL, RTX 4070 Ti, 1920×1080, VSync off and uncapped,
with the secondary display visible, muted and physical viewport input disabled.
The mixed-large fixture starts with
40 rooms and three active actors (Branforth, River and Margot), copied owner
layouts, seeded reserves, free building and disabled failures. These fixture-only
settings do not certify normal progression or real controls.

Use the previous unbatched 24-source reference plus the accepted async-report
fix. Untouched crew/hazard leaves were extracted from its actual base PCK.
The reference override has 35 sources.
Private diagnostic wrappers are separate packs. No production code, art, crew
behavior or test registration changed. Structural batching remains private.
This reused Windows runtime is not a full-current-source export or Mac build.

Evidence: `C:/bs-crew-stall-20261016/`; helpers:
`output/crew-stall-20261016/`. `summary.json`, `final-audit.json`, source manifests,
exact fixtures, per-run logs and owner/process guards preserve the selection.
The copied legacy `runtime/identity.json` describes its original build; current
fixture identities are in `final-audit.json`, not its old fixture field.

## What the private scopes showed

| Diagnostic | Frames | Crew mean / max ms | Whole-frame max ms |
|---|---:|---:|---:|
| Headless CPU replay | 26,000 | 2.149 / 81.354 | 82.326 |
| Headless detailed replay | 25,000 | 2.123 / 60.293 | 61.747 |
| Visible native diagnostic | 24,000 | 1.790 / 58.247 | 106.765 |

Native diagnostic frame 8,988 contains four detour attempts: 54.617 ms inside
detour scopes, including 38.509 ms in reachability scans. Passage resolution
accounts for 36.117 ms of the same work. These nested wall scopes overlap and
must not be added. The CPU replay also identifies frame 8,988 as expensive.

The 81.354 ms CPU case includes 37 native AStar paths. Native nonempty paths do
not establish that their smoothed detour candidates survive. A proposed early
exit after a fixed dry endpoint rejection was not confirmed in the detailed
replay's retained costly cases. Counters reset every frame and only bounded
costly snapshots remain; absence there is not proof it never happens.
`test_fixed_endpoint.gd` remains an unrun conditional oracle draft in output,
not a registered or validated regression test. No speculative shortcut shipped.

These private timers and event capture can perturb timings. Headless accelerated
replays are CPU diagnosis, not FPS or visual acceptance. The native 106.765 ms
whole-frame maximum is retained; the original detail collector sorted by crew
cost, so it cannot attribute every whole-frame outlier. Do not turn wall time
into useful CPU time or infer an original-stall cause from module/RVA samples.
One initial headless smoke failed a display-only startup guard; that fixture was
corrected and rerun. It is excluded from measurements, with its raw log retained.

## Fresh uninstrumented placement baseline

Two unchanged-source runs, 120 frames per phase: 960 frames total, four exact
phase pairs. Captured state sections, camera start/end/path, drone phases and
minimum room visibility match. The state oracle covers its named RunSave
sections, not every transient actor field. All guard-valid samples are retained.
These short repeats quantify variability; they are not before/after improvement.

| Phase | FPS A / B | p95 ms A / B | Max ms A / B |
|---|---:|---:|---:|
| 1× idle | 52.45 / 47.17 | 22.224 / 27.548 | 30.123 / 30.445 |
| 1× placement | 48.45 / 45.14 | 26.320 / 27.917 | 50.753 / 55.442 |
| 4× idle | 38.54 / 38.27 | 44.554 / 47.188 | 83.604 / 71.227 |
| 4× placement | 37.66 / 35.22 | 41.277 / 45.490 | 67.880 / 74.075 |

At 4×, frame-30 placement calls take 2.933 / 2.373 ms; their whole frames take
67.880 / 59.043 ms. Following frames 31–90 each contain two frames >50 ms,
none >100 ms, with maxima 65.612 / 74.075 ms. Whole 4× placement phases have
four / six frames >50 ms. Direct placement-call cost and whole-frame pacing
are different measurements. No phase meets the existing 60 FPS gates.
Both benchmark texture peaks are 2,776.907 MiB in Godot accounting.

## Final uninstrumented 4× soak

26,000 frames over 582.489 wall seconds. All individual
frame durations are retained in order: mean 22.290 ms
(44.86 FPS), p95 33.980, p99 47.809, max
88.411 ms. Frames >50 / >100 / ≥400 ms:
215 / 0 / 0. Crew mean / max:
1.472 / 38.566 ms.

Automatic reports: 0. Error summary: `{"distinct": 0, "groups": [], "log": "user://logs/godot.log", "total": 0}`.
No SafeImage failures. The full durations permit p95/p99 independently of
the bounded 1,024-frame recent detail and 64 largest whole-frame / crew lists.
Recent detail overwrites 24,976 earlier rows explicitly.
Loop/collection work is outside sampled frame durations: total sampled frames
579.536 s versus wall 582.489 s.
The soak does not reproduce the placement phase or certify long-run normal play.
Its largest frame has only 2.383 ms crew time and 75.676 ms before-render wall
time, so it is not another captured 393 ms crew-scope event. The station evolves
to cycle 411 with seven flooded rooms and two electrical faults; do not compare
its aggregate FPS to the short placement phases as if workload were constant.
Sampled texture maximum (one-second polling) 2783.949 MiB.
The static-memory query returned zero in this release runtime, so RAM usage is
unavailable from that field. Counters are not physical GPU residency or a
memory-leak proof.

## Acceptance and next work

All 13 owner guards pass; 2,948 non-log files match the task
baseline. All 55 protected installed paths are
unchanged. Frozen source manifests and EXE/PCK/native DLL hashes match their
expected bytes. Process guards are clean, game exited, owner editor preserved;
no WPR capture was started in this pass. Final free disk 31.03 GiB.
Benchmark screenshot inspected; final soak screenshot reviewed separately.
No new production test suite is claimed for this diagnostic-only pass.
[Earlier profile incident caveat](TEST_PROFILE_INCIDENT_2026-10-15.md) remains.

Next: inventory and integrate only accepted private changes, freeze one physical
full-source selection, then follow [release workflow](RELEASE_WORKFLOW.md).
Validate the actual Windows package (saves/Continue, placement/demolition,
doors/lights/warnings, UI, loading, transitions and longer soak); keep performance
gate failures visible. Run actual Mac gameplay/performance and distribution
checks on Mac hardware. A passed diagnostic soak is not release acceptance.
