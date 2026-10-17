# Report generation and longer stall soak — October 16, 2026

PNG encoding and report packaging now run on one bounded worker. In the frozen
Windows workload, the manual report request's main-thread duration fell from
367.708 to 65.093 ms (82.3%). A longer soak caught a 393.261 ms frame with 370.994 ms
inside the crew-update wall-time scope. No report was active during that frame.
The earlier unexplained5.24s/435ms pre-render stalls did not recur.

## Change and preservation

`scripts/bug_report.gd` freezes a request on the main thread, duplicates its
screenshot and attachment bytes, then encodes lossless PNG and writes ZIP/folder
output on a detached worker. Live scene/texture access stays on the main thread.
One worker and at most two accepted jobs bound memory/concurrency. Completion
polls while paused; shutdown joins accepted work. A later F8 snapshot survives an
older completion. Overlay generations protect new dialogs, including reopening
F8 during a pending upload. Upload still requires the user's explicit Send.

`scripts/performance_monitor.gd` awaits this path for automatic reports. It logs
save failure truthfully. The synchronous API remains for startup crash recovery
and explicit tools. Gameplay, renderer, art, navigation and crew sources were not
changed by this task. `tests/test_async_bug_report.gd` and its paired UID are new;
`tests/index.json` registers it without removing existing entries.

## Actual Windows calibration

Godot 4.7.2 release `ed1daf0bf`, Compatibility/OpenGL, RTX 4070 Ti,1920×1080,
muted visible secondary display, frozen 40-room mixed station. Previous 24-source
**unbatched reference** plus report-only changes/scopes; the structural candidate
was not promoted. This reused runtime is not a full-current-source release build.

| Separate forced calibration | Main request | PNG worker | Package worker | Total wall | Frames while pending |
|---|---:|---:|---:|---:|---:|
| Original synchronous manual report |367.708 ms|main thread|main thread|367.708 ms|0|
| Async manual report |65.093 ms|285.701 ms|31.479 ms|406.309 ms|18|
| Async automatic-report trigger |64.510 ms|279.190 ms|30.923 ms|394.387 ms|19|

Each saved PNG matched its request-time pixels exactly; live station attachments
were present. These forced inputs are outside soak/FPS measurements and are not
primary stalls. Total completion time has not improved; main-thread blocking has.
Live capture still costs about62–65 ms and can itself exceed a frame budget.

## Soak results

Three accepted blocks total **20 min 23 s /63,327 complete frames** before tracer export.
All raw results remain preserved. Simulation uses the existing deterministic
1/60-step fixture, with normal / 4× speed controls, live room/crew/door/warning code,
fixture-only resource/failure flags, and physical viewport input disabled.
This does not certify real keyboard/mouse interaction or all station configurations.

| Block | Clean duration | Frames | Sample FPS | Whole-wall FPS | >50 ms | >100 ms | Maximum |
|---|---:|---:|---:|---:|---:|---:|---:|
| Normal, untraced |600.006 s|34,212|57.66|57.02|29|0|75.643 ms|
| Normal, Memory trace |120.006 s|6,401|53.95|53.34|5|0|70.178 ms|
|4×, Memory trace, pre-export prefix |503.029 s|22,714|45.63|45.15|168|5|393.261 ms|

Sample FPS excludes the fixture's collection gaps; whole-wall FPS includes them.
Tracing and different simulation duration/state make these diagnostic rows
unsuitable for a before/after FPS claim. Normal untraced p95/p99 are19.756/29.953ms;
normal traced21.800/32.080ms. No accepted frame reached400ms; all three blocks
reported zero logged errors, missing-art failures and automatic reports.

An initial4× attempt was rejected when the Windows administrator prompt minimized
the QA window. Its log/heartbeat remain separate and contribute no accepted frames.
An earlier recorder-handshake setup failure is preserved under `setup1`.

The393 ms observation was below the game's automatic400ms trigger. An external
heartbeat marker requested bounded export to retain its circular native history;
the marker explicitly did not know the exact frame. Offline analysis identified it.
The4× fixture continued collecting through export: raw521.104s/23,442frames,
raw p95/p99=33.862/47.102ms. A conservative UTC/tick cutoff excludes the boundary
frame and727later frames from the clean prefix. Both independent anchors choose
the same boundary (0.165 ms drift). All728suffix rows are retained, allowing exact
count/sum/hitch subtraction. Full individual durations were not saved, so **clean
4× p95/p99 are unavailable**. No outlier was deleted;393 ms remains in the prefix.

## Captured393 ms stall

Soak frame21574 / process frame21836, ticks495950605–496343866:

| Scope | Duration |
|---|---:|
| Entire sampled frame |393.261 ms|
| Fixture simulation step |371.730 ms|
| Crew update wall scope |370.994 ms|
| Before render, after step |14.689 ms|
| Render signal interval |6.630 ms|
| After render |0.190 ms|

Crew scope nests inside the simulation step; these values are not additive.
They locate elapsed time in a call path, not a specific function or useful CPU
instruction count. The last recorded texture creation ended17.684ms before the
frame began and is stale for this frame. No report worker/report capture overlapped
it. Following frames were26.113,25.030 and23.315ms.

The retained native window has392 sample observations, all 392 with exactly associated
stacks. Raw sample PID remains unknown; separate ownership derives from query-only
native handles/creation times held through stop and matching ending Thread/DCStop.
Observed complete scheduler pairs account for392.499ms; validated same-CPU IRQ
overlap accounts for2.079ms. These are retained positive lower bounds, not proof of
complete circular coverage or a full busy/off-CPU decomposition. Reported locations
are mostly BrineSpace.exe module/RVAs; no matching Godot PDB/function attribution.
Other >100 ms frames include before- and after-render intervals and are not all
explained by this crew scope.

## Trace limits and validation

Memory profile:1024×256KiB fixed buffers, SampledProfile stacks, scheduler and
ISR/DPC events. Helper accepts only two fixed labels, holds target identity,
checks storage/time limits, keeps game unelevated/alive through rundown, then exits.
Both stops succeeded; ETLs are283,115,520 and283,901,952bytes. Sampled free-space
minimum stayed above23GiB;20 GiB reserve held. WPR is stopped; owner editor remains.

Unchanged offline parsers read73,566 target samples:72,647 with stacks,919 without,
four unmatched stack segments. StackAssociationComplete=false for both captures.
875,401 validated IRQ records, no reported event loss, overflow or invalid IRQ rows.
Zero event loss does not establish full circular history. Raw unknown scheduler
ownership stays unknown; handle/rundown derivation is separately labelled.
Per-CPU retained buffer/silence boundaries and exact module lifetime history are
unavailable. CSwitch V5 auxiliary state/wait/priority semantics remain unverified.
No full600s native coverage, exact total IRQ, or new primary-cause claim is made.

Final checks: five headless diagnostics/reliability tests pass; native
`test_performance_reporting` passes. New coverage uses real PNG/ZIP, request-time
pixel/metadata detachment, frames during writing, paused completion, queue bounds,
duplicate Save, stale dialogs/uploads, real ZIP-failure folder fallback and shutdown
joins. Regression tests failed before their fixes. Offline prefix tests verify
boundary handling, complete suffix retention, outlier preservation and clock rejection.
Native final station screenshots were inspected; exact screenshot preservation was
tested separately. This task does not redo earlier exhaustive room/door visual audits.

Final audit:26 owner guards,2,948 protected non-log files equal this task's baseline;
36 installed guards differ only in the two authorized report scripts.24 frozen game
sources, base EXE/PCK and native DLLs match the prior reference. Reversing private
diagnostic wrappers reproduces both final production report sources exactly.
The [earlier profile incident caveat](TEST_PROFILE_INCIDENT_2026-10-15.md) persists.

Evidence: `C:/bs-report-soak-20261016/` (`summary.json`, `tail-analysis.json`,
`final-audit.json`, immutable raw JSON/ETLs, scratch reports/logs/identities).
Reproduction helpers: `output/report-soak-20261016/`. No publish, Mac acceptance,
full release acceptance or60FPS achievement is claimed.

Next useful work: instrument the individual crew/companion updates and their path
search/rebuild calls around the captured crew scope, then reproduce it. The earlier
unexplained pre-render stalls remain open; changing crew behavior is not authorized
by this finding.
