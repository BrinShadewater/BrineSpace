# Scheduler tracing and idle investigation — October 15, 2026

**Bounded scheduler tracing now works. No game-code optimization was applied.**
Captured ordinary hitches overlap expensive mining-drone texture creation, while
new untraced comparisons expose much larger pre-render stalls. Their primary
cause remains unresolved. Keep the structural candidate private and retain every
valid result, including those stalls and automatic-report follow-up frames.

## Getting capture working

The Codex host token is medium integrity, with Administrators marked deny-only
and no `SeSystemProfilePrivilege`. Repeating WPR in that token cannot enable a
privilege absent from it. A small fixed-purpose helper was compiled locally and
launched through normal Windows elevation. Its administrator-role check passed;
the game inherited the original unelevated host context.

The helper only starts/stops the frozen WPR profile for four named captures. It
checks profile SHA-256, preserves conflicting recordings, enforces a 90-second
per-capture watchdog, ten-minute lifetime and 20 GiB free-space reserve plus trace
margin. It never installs a service, changes policy/rights, starts the game or
changes process priority, affinity or power plan. Memory buffers are 64×256 KiB;
the built-in verbose CPU profile's ~3.2 GiB buffer allocation was avoided.

Four serial captures succeeded and saved ~715 MiB total. All stop commands return
zero with `parent-stop`; the broker exited and WPR reports **not recording**.
No elevated helper or recording remains active. No downloads or SDK installation
were required; the existing Visual Studio TraceEvent/FastSerialization assemblies
and compiler were used.

The initial capture code remains in `output/scheduler-20261015/TraceBroker.cs`
and its manifest; generated fixed-profile source/EXE and command logs are preserved
in `C:/bs-scheduler-20261015/`. This broker is finished, not a persistent service.

## Capture workload and integrity

Both 24-source/PCK lanes are byte-identical to the preceding structural study:
private water V2/stable-ID V3/LOD cohort, excluding the waveform trial. Actual
release Godot 4.7.2 `ed1daf0bf`, Compatibility/OpenGL, RTX 4070 Ti, 1920×1080,
muted visible secondary-display QA. Owner editor PID 46624 preserved.

Each process warms for 180 frames, then pauses deterministic fixture stepping at a
handshake while WPR starts. After release it measures **600 normal-idle and 600
4×-idle frames**. Order is reference → candidate → candidate → reference.
**4,800 diagnostic frames / four exact phase-state and camera-path pairs.** These
longer, gated, traced workloads are excluded from the FPS comparison below.

Offline parsing yields 4,557 / 5,075 / 5,595 / 5,579 complete main-thread intervals.
All captures report zero lost events, no interval overlap and no known PID
mismatches. Each has one initial capture-boundary orphan. Initial unknown thread
ownership ends before measurement; **all 4,800 measured frames have known
ownership and complete interior coverage**. Boundary runtime is never invented.

Frame windows use Godot tick/UTC markers and captured PID/main TID. Complete
same-CPU switch-in/out intervals are intersected with each frame; no whole interval
is assigned to a frame merely because it starts there. UTC/relative and external
QPC alignment checks pass. Godot's system-time anchor is roughly millisecond
resolution; printed microsecond-scale arithmetic is not equivalent clock accuracy.

The read-only CPU-set snapshot confirms one processor group: logical indices
0–15 report EfficiencyClass 1; 16–23 report class 0. Higher Windows class indicates
higher performance/lower efficiency, per the
[CPU-set structure documentation](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-system_cpu_set_information).
This is hardware classification sampled after capture, not a clock-frequency log.

## What the captures show

Across individual phases, the main thread is **scheduled on a CPU for about
99.69–99.78%** of elapsed measured time. The lower-performance class accounts for
only **0.16–0.48%** of scheduled time. Gross off-CPU delay or lower-class execution
does not account for the captured large hitches.

This is **scheduled residency**, not an instruction count or proof that all time
executes useful game code. A CSwitch interval can include interrupt/DPC work or
spinning. These profiles contain no stacks, samples or interrupt/DPC accounting,
so those costs remain possible within the resident time. Frequent migration among
higher-class CPUs also remains possible; no affinity fix is justified.

Every captured frame above 50 ms overlaps actual logged mining-drone texture
creation calls. No captured upload-free frame exceeds 50 ms. Normal-idle examples:

| Capture | Frame | Whole frame | Texture creation calls | Grid callbacks |
|---|---:|---:|---:|---:|
| Forward reference | 257 | 62.611 ms | 33.750 ms | 51.980 ms |
| Reverse candidate | 258 | 60.643 ms | 32.332 ms | 51.060 ms |

Both examples create the north/south mining atlases, **144,506,880 bytes each**
(~275.6 MiB combined). The measured calls are `cache_image` →
`make_native_texture`; timestamps bracket texture creation after background image
decode. The outer callback includes additional work, so these times cannot be
added together. Remaining texture preparation/copies/destruction or driver costs
need deeper attribution before a change.

Worst ten-frame windows with no overlapping texture-creation calls average
**19.56–20.28 ms** at normal speed. The original sustained ~30.794 ms upload-free
window does **not** recur in these captures. This does not retroactively establish
its cause or exclude a scheduling issue in that unrecorded original interval.

All new normal-idle runs retain 72 floor slots, 13 grid redraws and no floor/wall
assembly stages. The changed structural CPU callbacks do not execute in those
idle windows. Retained commands still render every frame; downstream costs are
not eliminated by that observation.

## Windows CSwitch V5 decoding limit

The installed TraceEvent 3.1.9 decoder reads legacy auxiliary offsets for these
**Version 5, 28-byte** events. Implausible wait-mode bytes 98/99 persist in measured
interior records. A representative raw audit verifies new/old TIDs agree with
typed identities for all 9,072 target-bearing events, independently of those
auxiliary fields. Native TDH returns **1168 / ERROR_NOT_FOUND**; installed MOF
describes versions 1–4. No guessed V5 masking was applied.

State, wait-mode/reason and priority values are explicitly marked **unverified**.
They are retained for audit and are not used to classify blocking, runnable delay
or priority. ReadyThread records are retained, but no available waker identity
supports attribution to another process. Timing/processor/identity evidence above
is evaluated separately. Further wait-state interpretation needs a decoder with
verified V5 semantics.

The parser passes 25 synthetic model checks, CPU-set layout/error checks,
adapter compilation and actual CSV/JSON report round-trip under fr-FR culture.
Independent review also checks all measured frame joins and clock consistency.

## Fresh untraced release benchmark

Two four-process comparisons were chosen before timing: each reference →
candidate → candidate → reference. Original workload: 180 warm frames, then 120
each normal idle, normal placement, 4× idle and 4× placement. VSync/frame cap off.
**3,840 fresh frames / 16 exact state-camera pairs.** WPR, external CPU collector,
extra render counters and offline parsers are off. Existing benchmark observers
and production automatic diagnostics remain enabled.

**Every valid raw row remains in this table**, including primary long stalls and
the following automatic-report frames. These are measured outcomes, not proof of
an intrinsic candidate cost or an FPS improvement from tracing.

| Fresh pooled phase | Reference FPS | Candidate FPS | Reference p95 | Candidate p95 |
|---|---:|---:|---:|---:|
| Normal idle | 53.17 | 48.82 | 20.403 ms | 20.917 ms |
| Normal placement | 51.53 | 51.91 | 23.623 ms | 23.971 ms |
| 4× idle | 45.84 | 28.93 | 36.252 ms | 40.428 ms |
| 4× placement | 44.05 | 44.46 | 37.403 ms | 36.060 ms |

**0/16** fresh candidate phase gates meet both mean and p95 ≤16.667 ms.
Including all five unchanged-lane untraced studies (9,600 frames), normal idle is
53.83→51.90 FPS, 4× idle 47.02→38.07, 4× placement 44.74→45.15. Original mixed and
negative results remain intact; these new stalls materially worsen idle averages.

### Large new pre-render stalls

The first comparison has six frames above 100 ms; the second has none:

| Run | Phase / frame | Frame time | Evidence |
|---|---|---:|---|
| bench1 forward reference | Normal idle / 37 | 124.514 ms | No sampled upload; ~117 ms before render |
| bench1 forward candidate | Normal idle / 36 | 121.776 ms | No sampled upload; ~111 ms before render |
| bench1 forward candidate | 4× idle / 92 | 5,240.498 ms | ~5,232 ms before render; texture calls only 5.165 ms |
| bench1 forward candidate | 4× idle / 93 | 602.754 ms | Following frame includes automatic report save |
| bench1 reverse candidate | Normal idle / 46 | 434.621 ms | No sampled upload; ~427 ms before render |
| bench1 reverse candidate | Normal idle / 47 | 444.962 ms | Following frame includes automatic report save |

Grid callbacks remain ~8–18 ms and render-signal intervals ~6 ms during these
samples. Most time is outside those measured scopes before rendering. It cannot
be assigned to texture uploads, structural callbacks or a particular process from
these annotations. No scheduler trace exists for these acceptance frames.

The two scratch report ZIPs confirm order: notes record primary frames of 5,241 ms
and 436 ms using the monitor's slightly different boundaries. Their creation-tick
suffixes fall within the following 602.754 / 444.962 ms benchmark frames. The
synchronous screenshot/report path contributes to those following stalls; it
cannot explain the earlier primary stalls, and its whole contribution is not
separately timed. Automatic capture was not disabled to improve the headline.

### 4× placement hitches

Action is frame 30; following window is frames 31–90, excluding action. All
timings below are milliseconds.

| Series / order | Action reference→candidate | Next frame | Following mean | Following p95 | Following >50 ms |
|---|---:|---:|---:|---:|---:|
| bench1 forward | 58.025→59.747 | 22.799→26.128 | 23.441→22.858 | 36.872→37.273 | 2→0 |
| bench1 reverse | 57.080→58.049 | 23.548→24.975 | 22.665→22.881 | 35.797→35.108 | 1→1 |
| bench2 forward | 58.645→56.759 | 24.007→22.697 | 23.021→22.587 | 37.740→33.469 | 1→2 |
| bench2 reverse | 59.952→57.592 | 23.760→23.735 | 22.275→22.267 | 35.348→34.877 | 1→0 |

Mean action **58.426→58.037 ms**, with two orders worse and two better. Following
>50 ms totals **5→3** across 240 frames per lane, or **9→7** including actions.
Whole placement-phase >50 ms count **12→7**. Placement remains far from 60 FPS and
has mixed per-order behavior; no broadly accepted hitch fix is established.

## Protection, files and next action

Both frozen 24-source/PCK lanes and installed source/UID/protected tests are
unchanged. All **13 owner guards** and **12+12 native DLL guards** pass; final
**2,948 protected non-log files** equal initial and prior fingerprints. All report
writes stay in scratch profiles. The existing
[profile-incident caveat](TEST_PROFILE_INCIDENT_2026-10-15.md) remains.

Prior 1,148 focused raster pairs, 38 cache checks, 17 station/first-paint pairs and
12 repeats are reused for byte-identical game bytes, not reported as fresh visual
tests. Existing representative image was reviewed. At least 20 GiB free storage
remains; no game/crew behavior, art, native implementation, export or Mac change.
Final free space is about **20.28 GiB**, leaving little headroom above the enforced
20 GiB reserve. This task's 12 shader caches total only 13.55 MiB, so they and all
raw evidence were retained. Plan storage headroom before another large QA batch;
unrelated evidence was not removed.

Evidence: `C:/bs-scheduler-20261015/` — four ETLs, `parsed/`,
`cpu-topology.json`, `scheduler-summary.json`, raw frame joins,
`bench1/2-analysis.json`, `pooled-summary.json`, raw schema/TDH evidence, capture
logs and `final-audit.json`. Helpers: `output/scheduler-20261015/`;
parser details in `PARSER_README.md` there.

Next: capture a recurrence of the **unscoped primary pre-render stalls**, adding
sampled stacks and interrupt/DPC accounting, plus narrow timings around periodic
diagnostic/log/breadcrumb I/O and report creation. Those are investigative targets,
not established causes. Keep all observers explicit and compare separately from
headline release timing. Texture creation remains a proven repeatable hitch
contributor; the original sustained upload-free burst remains unresolved.
