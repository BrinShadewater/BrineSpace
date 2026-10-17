# BrineSpace renderer comparison — October 15, 2026

Owner requested Compatibility/OpenGL, Compatibility/ANGLE and Mobile/Vulkan on
the large station, preserving appearance, including zoom/placement frame pacing.

## Scope and identity

This is a Windows experiment on the RTX 4070 Ti, Godot **4.7.2 official release**
(`ed1daf0bf001b61586d9930840f2f1394092c079`), 1920×1080 on the secondary display,
muted Dummy audio, physical viewport input disabled, VSync off and FPS uncapped.
Actual rendering method, driver, adapter and API version are asserted and recorded;
all three requested backends start without fallback.

| Label | Process arguments | Confirmed backend |
| --- | --- | --- |
| Current | `--rendering-method gl_compatibility --rendering-driver opengl3` | NVIDIA OpenGL 3.3, driver 616.92 |
| ANGLE | `--rendering-method gl_compatibility --rendering-driver opengl3_angle` | ANGLE 2.1.1, Direct3D 11 on the same RTX 4070 Ti |
| Mobile | `--rendering-method mobile --rendering-driver vulkan` | Forward Mobile, Vulkan 1.4.351 on the same RTX 4070 Ti |

The frozen performance candidate includes the **private room-image LOD prototype**
and the accepted geometry/submission optimizations through the frond change.
It is the previous QA cohort, not a claim about a newly exported current normal
source tree. Unrelated newer character changes are outside this frozen cohort.
The historical synthetic Bill pilot produced an invalid recovery/carry checkpoint;
this experiment instead clears the existing checkpoint-owned Branforth's job and
uses him for the Moonbay mission. Every backend shares that fixture correction.
Therefore the preceding ~53 FPS figure is context, not this comparison's control.

The eighteen overlay sources are checked after mounting, before measurement.
All source/asset identities, scratch profiles, exact engine command lines, fixtures,
raw samples and owner fingerprints are retained under
`C:/bs-renderer-compare-20261015/`. Driver scripts live in
`output/renderer-compare-20261015/`. Normal-source snapshots are retained only as
context; they are not represented as a tested normal-source release.

No production code, game settings, artwork or Windows delivery changed. This
does not certify Mac, another GPU/driver, real input handling or release acceptance.

## Appearance

All four final image processes restore **one binary station checkpoint** plus
unscaled time, settled light levels and underwater silt state. Crew, drones,
environment, RNG, camera, selection and HUD state are captured. Comms history is
normalized from the checkpoint; transient toasts are cleared and hardware-button
animation is explicitly settled. Current drone image jobs drain before capture.
Simulation and clocks freeze only for these image comparisons, not timed play.

The six cases are fitted zoom **0.1308139535**, **0.25**, **0.5**, each with interior
lights on/off. Each process captures two repeats per case. All saved state,
camera and visual-sidecar comparisons agree. All **24 within-process pairs** are
pixel-exact. Independent OpenGL processes also match in **all six cases**.

| Backend versus OpenGL | Different pixels per 1920×1080 image | Largest channel difference | Exact appearance gate |
| --- | ---: | ---: | --- |
| OpenGL repeat process | 0 | 0 | Pass, 6/6 |
| ANGLE | 615,119–676,774 | 1 / 255 | Fail, 0/6 |
| Mobile | 858,924–980,239 | 95 / 255 fitted; 18 / 255 closer | Fail, 0/6 |

ANGLE's differences are tiny rounding differences, not evidence of visibly broken
art. Mobile has larger differences. The strict unchanged-appearance requirement
is retained; neither alternative is admitted as a renderer change.

![Frozen renderer images and channel-difference maps](C:/bs-renderer-compare-20261015/renderer-visual-comparison.png)

Final evidence: `visual-gl-j`, `visual-angle2`, `visual-mobile2`, `visual-gl-k`;
`visual-analysis.json` and `visual-region-analysis.json`. Earlier fixture debugging,
a minimized-window attempt and unfinished hardware-switch captures are excluded.

## Frame pacing and hitches

The clean six-run series **`pacing3` is complete: 10,080 measured frames**.
The owner confirmed other runs were paused before it started. Its monitor made
723 process samples, with no foreign Godot process, duplicate game or monitor
error; largest sampling gap 0.668 seconds. Every run verified the same source
overlay SHA256, `fa65dc5329ad6e93436e15d448581afd8f341980dfe9e2b9669bffa84df41939`,
and preserved all 2,948 fingerprinted non-log owner files.

The first six-run series (`pacing1`) detected
three foreign Godot processes and is **excluded in full**. `pacing2` was initially
refused while a Krusher repair test was active. It later resumed during a gap,
completed the three forward runs, and stopped when another Godot process appeared
during Mobile. No reverse runs occurred. Its guard records PID 325688 first seen at
18:55:29 UTC in `pacing2-f1-mobile`. The incomplete/contaminated series is also
excluded from accepted three-way performance results. Preliminary timing values
must not be treated as renderer gains.

The comparison uses forward **OpenGL → ANGLE → Mobile**, then reverse
**Mobile → ANGLE → OpenGL**, serially. Each process uses 180 deterministic warm
steps, then 120 frames per action at normal and 4× speed: idle, pan, fitted zoom,
lighting, placement, demolition, and a fitted/0.5 zoom sweep. Measurements retain
mean, median, p95, p99, maximum, counts above 16.67/33.33/50/100 ms, and placement
event plus the following thirty frames. Four zoom targets per sweep cross the
private LOD thresholds. Frame samples are CPU wall intervals around native frames;
delayed viewport render-query values are separate and not added to script costs.

All 56 cross-backend phase pairs match the fixture's recorded station-state
snapshot and start/end camera. All normal-speed paths are exact. Four pairs have
different intermediate paths: both alternate backends, in both orders, for the
**4× wide zoom sweep only**. The real room-cover wait can defer zoom differently;
those four phase comparisons describe interaction pacing, not identical rendered
load. Other paths match exactly. These timed snapshots cover the named station,
crew, companion, drone, hardware and resource-flow fields; the separate appearance
cohort above compares the full frozen checkpoint/visual sidecar.

### Normal speed

Each row pools two 120-frame phases, one in each process order. FPS is 1000 divided
by mean frame milliseconds. Quantiles use the pooled 240 samples, not averages
of the two quantiles. All times are milliseconds; hitch counts are per 240 frames.

| Backend | Action | Mean FPS | p95 | p99 | Worst | Frames >33.33 / >50 ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| OpenGL | Idle | 49.7 | 22.9 | 29.6 | 32.4 | 0 / 0 |
| ANGLE | Idle | 38.8 | 28.2 | 34.2 | 55.4 | 4 / 1 |
| Mobile | Idle | 59.2 | 19.2 | 25.7 | 26.9 | 0 / 0 |
| OpenGL | Fitted-station zoom | 40.9 | 38.6 | 83.7 | 90.4 | 23 / 5 |
| ANGLE | Fitted-station zoom | 31.2 | 50.3 | 110.4 | 120.8 | 49 / 13 |
| Mobile | Fitted-station zoom | 44.9 | 37.0 | 72.6 | 81.4 | 20 / 5 |
| OpenGL | Placement phase | 49.2 | 23.7 | 38.7 | 62.4 | 4 / 2 |
| ANGLE | Placement phase | 39.2 | 28.8 | 52.5 | 67.5 | 5 / 3 |
| Mobile | Placement phase | 59.7 | 18.5 | 29.1 | 59.0 | 2 / 2 |
| OpenGL | Fitted ↔ 0.5 sweep | 45.4 | 33.2 | 36.4 | 37.9 | 10 / 0 |
| ANGLE | Fitted ↔ 0.5 sweep | 34.1 | 44.3 | 49.7 | 50.7 | 47 / 2 |
| Mobile | Fitted ↔ 0.5 sweep | 50.8 | 29.9 | 33.7 | 34.6 | 3 / 0 |

![Normal-speed renderer frame pacing](C:/bs-renderer-compare-20261015/renderer-frame-pacing.png)

### Four-times simulation speed

Same sample count and units. The wide-sweep rows have the intermediate-camera
qualification above. Faster simulation does not imply the same sequence of work
as a normal-speed phase; compare each speed separately.

| Backend | Action | Mean FPS | p95 | p99 | Worst | Frames >33.33 / >50 ms |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| OpenGL | Idle | 41.1 | 38.5 | 48.2 | 69.4 | 21 / 2 |
| ANGLE | Idle | 32.3 | 44.1 | 61.2 | 63.3 | 51 / 8 |
| Mobile | Idle | 48.1 | 32.0 | 43.1 | 46.2 | 10 / 0 |
| OpenGL | Fitted-station zoom | 39.5 | 36.7 | 43.1 | 50.6 | 27 / 1 |
| ANGLE | Fitted-station zoom | 30.7 | 46.8 | 49.7 | 57.2 | 69 / 2 |
| Mobile | Fitted-station zoom | 45.0 | 33.6 | 38.7 | 40.7 | 13 / 0 |
| OpenGL | Placement phase | 44.0 | 36.0 | 56.3 | 66.1 | 17 / 4 |
| ANGLE | Placement phase | 33.9 | 44.2 | 66.1 | 75.7 | 31 / 9 |
| Mobile | Placement phase | 52.1 | 29.5 | 44.5 | 59.9 | 9 / 2 |
| OpenGL | Fitted ↔ 0.5 sweep | 45.1 | 33.5 | 43.7 | 44.0 | 14 / 0 |
| ANGLE | Fitted ↔ 0.5 sweep | 34.3 | 45.4 | 54.8 | 74.4 | 63 / 9 |
| Mobile | Fitted ↔ 0.5 sweep | 51.1 | 30.0 | 34.7 | 36.4 | 5 / 0 |

![Four-times-speed renderer frame pacing](C:/bs-renderer-compare-20261015/renderer-frame-pacing-4x.png)

### What this establishes

Mobile has the best measured mean frame time in every matched action/speed here.
At normal-speed idle its pooled 16.89 ms is about 16% below OpenGL's 20.12 ms;
ANGLE takes 25.80 ms. Both process orders show the same idle ranking. Mobile's
normal-speed zoom p95 varies materially between orders (45.90 versus 33.75 ms),
so the pooled value should not hide that variation.

**No backend passes a 60 FPS pacing gate in any of its 28 phases**: both mean and
p95 must be at most 16.67 ms. Mobile comes close on mean idle/placement, but does
not sustain that frame budget. Its lower average also does not remove structural
stalls. Normal-speed placement event frames are 62.22–62.38 ms on OpenGL,
64.81–67.51 ms on ANGLE and 57.62–58.98 ms on Mobile. In the four-times ANGLE
forward run, another frame fourteen frames after placement reaches 75.71 ms.

The direct placement action measures about 7.8–8.4 ms across all twelve placement
events, separate from the simulation step and the rest of the native frame.
This does not attribute the remaining wall time to a particular subsystem or GPU
operation. Delayed render queries, accumulated draw callbacks and previous-second
engine maxima must not be added into a purported per-frame breakdown.

ANGLE has no demonstrated performance benefit on this Windows GPU. Mobile is
worth investigating for its CPU/render path, but still fails the established
appearance gate and leaves zoom/placement hitches. **Keep OpenGL as production
default.** This short comparison is not endurance testing or Mac evidence, and
the old ~53 FPS cohort is not a direct control for the corrected pilot fixture.

All 42 action/speed/backend summaries, including pan, lighting and demolition,
are retained in `C:/bs-renderer-compare-20261015/pacing3-phase-results.csv`.
`pacing3-analysis.json` retains repeats, all threshold counts and event windows;
the six `pacing3-*-*.json` files retain raw samples and traces. Backend texture
counters are retained as diagnostics, not compared as physical VRAM usage; see
the source-audited GLES accounting/scope caveats below.

## Next action

The [follow-up research](GODOT_FOLLOWUP_RESEARCH_2026-10-15.md) identifies a GLES
texture-counter accounting error, unsupported Compatibility compilation counters,
image-isolation candidates and a private diagnostic journal to bound before endurance.
Those findings remain independent of this clean timing comparison.

No further renderer series is needed without a new change or unresolved concern.
Next useful performance investigation: a short, event-aligned Windows thread/GPU
scheduling trace on current OpenGL during fitted zoom and placement, with game
markers. Attribute the remaining waits before choosing another optimization.
The [methods research](GODOT_PERFORMANCE_VISUAL_METHODS_2026-10-15.md) identifies
specific preparation/rebuild sites to measure. A faster renderer still needs
appearance parity before it can be proposed for delivery.
