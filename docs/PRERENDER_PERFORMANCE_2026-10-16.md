# Pre-render stacks, interrupt accounting and diagnostic I/O

Completed October 16, 2026; captures began October 15 local time.

The earlier 5.24 s and 435 ms primary pre-render stalls did not recur. Their cause
remains open. New captures identify ordinary slow frames overlapping drone texture
creation, and a separate calibration directly measures automatic-report work that
can amplify a following frame. No game-code fix or candidate promotion was made.

## Scope and frozen inputs

Same Windows release reference and private structural-batching candidate as
[the previous scheduler study](SCHEDULER_PERFORMANCE_2026-10-15.md): Godot 4.7.2
`ed1daf0bf`, Compatibility/OpenGL, RTX 4070 Ti, 1920×1080, uncapped and VSync off.
Both 24-source lanes and their PCKs are byte-identical to that study. Native
navigation/water binaries are unchanged. No normal script, UID, test, artwork,
crew logic, renderer setting, priority, affinity or power-plan change was made.

Every game job ran serially with scratch APPDATA and an explicitly checked
`user://`; owner layouts were copied into scratch. Native windows stayed muted,
visible on the secondary display, with external viewport input disabled.
Measured phases use the existing deterministic large-station fixture. This is not
new acceptance of physical input, a Mac build or a complete release playthrough.

Three separate cohorts preserve the distinction between diagnostics and acceptance
timing:

- Two predetermined untraced four-process series: 3,840 frames, 16 exact
  state/camera pairs, 120 frames per phase, idle and placement at normal/4× speed.
  Original lane packs; no new I/O probes, OS sampling, ETW or render-object query.
- Four I/O-only runs: 4,800 frames, four exact pairs, 600 idle frames per speed.
- Four stack/IRQ captures: another 4,800 frames and four exact pairs, same idle
  workload, with sampled stacks, context switches and ISR/DPC records.

All valid benchmark frames remain in the results. The older primary stalls remain
in the previous report; their absence here does not establish a fix.

## Stacks and interrupt integrity

A bounded fixed-purpose elevated WPR helper recorded four ETLs totaling
819.5 MiB, then exited. The game stayed unelevated. WPR is stopped. No service,
policy or persistent privilege change was made. Windows canceled one elevation
attempt; the owner explicitly authorized the successful retry.

| Capture | Target samples | Samples with stack | Stack segments | Valid IRQ records |
|---|---:|---:|---:|---:|
| Forward reference | 23,242 | 23,242 | 24,225 | 230,386 |
| Forward candidate | 21,984 | 21,984 | 22,864 | 226,225 |
| Reverse candidate | 23,054 | 23,053 | 23,982 | 337,620 |
| Reverse reference | 25,043 | 25,043 | 26,083 | 242,978 |

All captures report zero lost events, invalid IRQ records, raw identity
mismatches, unsupported stack records, unmatched stack segments, unresolved cached
references and export overflows. Native TDH verified the actual V2 IRQ prefix
layouts; every exported IRQ resolved to one module/RVA. ISR payloads were 20 or
24 bytes, DPC/TimerDPC payloads 16 bytes. No ThreadedDPC records appeared.

Stack association uses exact original QPC/TID, retaining separate segments. One
sample has no stack, so full-stack coverage is explicitly false: reverse-candidate
normal-idle frame 560, a 19.080 ms frame, `ntoskrnl.exe+0x6c1a38`. It falls in an
8.9 µs scheduler migration gap and overlaps no validated same-CPU IRQ interval.
Its API ISR flag is retained; no interrupt interval or useful CPU work is inferred.

Of 93,323 target-TID samples, 87,223 fall in measured frame windows and 87,222 of
those have stacks. All 698 samples with unknown raw PID lie outside measurement.
Every associated stack segment has the target PID and matching raw identity.
Nine measured point samples fall outside their corresponding same-CPU main-thread
residency intervals; these remain flagged. They do not create unknown scheduler
ownership of measured frame intervals.

Scheduler joins have zero unknown measured ownership, interval overlaps or known
PID mismatches, with one initial boundary orphan per capture. CSwitch V5 state,
wait-reason/mode and priority interpretation remains **unverified**, as documented
in the previous study. These fields are not used to explain a stall.

## Recorded frame evidence

ISR/DPC/TimerDPC spans are unioned per CPU before intersection with that CPU's known
main-thread residency and each frame window. Interrupts from unrelated cores are
not charged to the game. ThreadedDPC would remain separate. These are recorded
handler intervals, not a proof that all interrupt dispatch overhead is covered.

| Capture | Main scheduled residency | Recorded IRQ overlap / frame time | Frames >50 ms | Maximum frame |
|---|---:|---:|---:|---:|
| Forward reference | 99.581% | 0.280% | 6 | 75.260 ms |
| Forward candidate | 99.478% | 0.277% | 6 | 68.234 ms |
| Reverse candidate | 99.580% | 0.300% | 7 | 68.483 ms |
| Reverse reference | 99.591% | 0.282% | 8 | 77.524 ms |

All 27 traced frames over 50 ms overlap actual drone texture-creation stamps.
There are no traced frames over 100 ms. The longest upload-free frame is
46.627 ms. In the slow frames, the largest recorded main-thread IRQ overlap is
0.734 ms and the largest timed diagnostic body union is 6.568 ms.

For example, reverse-reference 4× idle frame 494 takes 77.524 ms, including
69.001 ms before the render signal. It has 38.917 ms inside north/south mining
atlas texture-creation calls, 0.357 ms recorded IRQ overlap and 0.028 ms of timed
diagnostic bodies. Of its 78 instruction samples, 44 are in `nvoglv64.dll`.
This establishes captured contributions, not the cause of the older primary stall.

Across the 87,023 measured instruction samples outside verified IRQ intervals,
56.59% are in `BrineSpace.exe`, 24.98% in `nvoglv64.dll` and 11.84% in
`ntdll.dll`. Pre-render samples excluding recorded texture calls are predominantly
in the game/engine executable. Repeated leaf RVAs include game offsets
`0x2d6a743`/`0x2d6a97e`, driver `0xb80d8f` and `ntdll.dll+0x3baae`.

These are sampled module locations, not exact function durations. Matching Godot
function symbols were unavailable in the inspected binaries/folders. A few stack
addresses remain unresolved. Scheduled time minus recorded IRQ can still include
kernel work, interrupt overhead or spin; it is not demonstrated useful game CPU.
The Godot UTC/tick anchor limits frame joins to roughly millisecond accuracy,
separately from native QPC/UTC arithmetic checks.

## Diagnostic I/O timings

Private wrappers preserve the actual release diagnostic function bodies, buffering
inclusive timestamp scopes in memory. They cover monitor processing, error polling,
breadcrumbs, context/memory queries, screenshot readback, PNG encoding, diagnostic
capture, save/log collection and ZIP/folder writes. All three actual diagnostic
instances are source-hash checked before measurement. No per-event writes occur.

The four I/O-only runs contain 12,011 events, zero dropped events and no natural
automatic reports. Monitor bodies average 0.037–0.039 ms per frame, with a maximum
of 6.909 ms. Error-log polling peaks at 6.862 ms; breadcrumb writes peak at
0.921 ms. Context queries peak at 0.074 ms, bucket finishing at 0.095 ms and
memory queries at 0.027 ms.

All 38 I/O-only frames over 50 ms overlap texture creation. No frame exceeds
100 ms; the longest is 88.450 ms. These observations do not rule out a rare I/O
stall that failed to recur.

A separate calibration supplied a synthetic 500 ms trigger to the unchanged
automatic-report path after station setup, outside every FPS sample. It did not
create or observe an actual 500 ms primary stall. One valid report ZIP was saved.

| Inclusive report-path scope | Observed time |
|---|---:|
| Complete trigger/report path | 362.810 ms |
| Screenshot readback | 4.378 ms |
| Report save body | 358.233 ms |
| Diagnostics capture | 61.984 ms |
| PNG encoding | 264.299 ms |
| ZIP writing | 28.931 ms |
| Log collection | 0.723 ms |
| Save collection | 0.228 ms |

Nested values are inclusive and must not be added together. Frame attribution
uses interval unions. Scope statistics describe observed nonzero timed bodies;
they omit zero-duration calls and do not measure all wrapper/recording overhead
or kernel disk-service duration. The calibration quantifies a mechanism for the
previously observed report-containing follow-up frames, without assigning all of
their time or explaining the preceding 5.24 s/435 ms primary stalls.

Probe `tid=1` is Godot's internal main-thread ID, not a Windows native TID. No
numeric cross-namespace join is made. The pinned engine's
[OS binding](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/core/core_bind.cpp#L530)
and [thread implementation](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/core/os/thread.cpp#L38)
establish that distinction.

## Separate untraced benchmark

FPS is 1,000 divided by pooled mean frame time; each lane has 480 samples per row.

| Phase | Reference FPS | Candidate FPS | p95 reference → candidate | Maximum reference → candidate |
|---|---:|---:|---:|---:|
| Normal idle | 52.24 | 52.71 | 21.603 → 21.587 ms | 38.095 → 31.113 ms |
| Normal placement | 51.31 | 50.75 | 24.148 → 24.859 ms | 47.128 → 52.229 ms |
| 4× idle | 45.54 | 45.21 | 36.794 → 37.894 ms | 68.293 → 71.818 ms |
| 4× placement | 43.15 | 42.61 | 37.237 → 42.350 ms | 62.223 → 70.025 ms |

Four 4× placement actions average **59.207 → 61.503 ms**: candidate worse in
three of four comparisons. Following 60 frames over 50 ms total **4 → 6**;
including each action frame, **8 → 10**. Whole 4× placement phases have **8 → 14**
frames over 50 ms. No fresh benchmark frame exceeds 100 ms. Candidate passes
**0/16** phase gates for 60 FPS. These unchanged-lane repeats do not establish a
performance improvement; the structural candidate remains private.

## Checks, artifacts and next step

Final audit passes: all 26 owner guards and 21+21 native/water binary guards,
2,948 protected non-log owner files equal initial/prior fingerprints, frozen
sources/PCKs/native binaries unchanged, and all exact state/camera pairs. Previous
1,148 focused raster pairs, 38 cache checks, 17 first-paint and 12 repeat station
pairs remain applicable to byte-identical normal lanes. No new visual acceptance
is implied by a headless or diagnostic check. The
[earlier profile incident](TEST_PROFILE_INCIDENT_2026-10-15.md) caveat persists.

Parser validation includes 19 synthetic model checks, actual JSONL round-trip and
11 interval checks for nesting, CPU identity, migration, gaps and frame clipping.
Independent review found no material attribution/accounting error. An end-boundary
reconstruction correction changed none of the I/O attribution totals. Early setup
source-guard failures were a UTF-8 hashing-helper error, corrected and verified
before accepted runs; no stack recording was made by those failed setups.

Evidence: `C:/bs-prerender-20261015/` (`final-audit.json`, `pooled-summary.json`,
`io-summary.json`, `deep-summary.json`, four ETLs/parsed directories, missing-stack
evidence and calibration ZIP). Helpers: `output/prerender-20261015/`. Disk reserve
was restored by hash-verified hard-link deduplication of four explicitly named old
immutable QA EXE/PCK copies, preserving bytes, paths and evidence. Shared frozen
base binaries must not be overwritten in place.

The clearest measured follow-up is to move lossless PNG encoding and report
packaging away from the main frame path while preserving automatic captures and
report contents. This would address report amplification, not ordinary idle FPS
or the unexplained primary stalls. Primary-stall attribution still requires a
recurrence under this recorder; naming the remaining engine hotspots requires
matching symbols or an optimized symbolized diagnostic build.
