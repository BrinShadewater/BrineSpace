# PC/Mac release readiness — October 4, 2026

October 5 paired-build update: **brinespace-af8b5f00998283ef** exports on Windows
and Universal 2 Mac with byte-identical PCKs, each passing a 35,779-asset exact
audit. Actual Windows New Game/F8 smoke passes. Three packaged runs per Windows
version confirm mixed p95 changes, ~4 GiB texture memory and ~1.04-second stalls;
all new phase runs fail frame gates. No public release. Mac native gameplay,
signing/notarization and the existing exit warning remain open. Current evidence:
[drone experiment and paired candidates](DRONE_UPLOAD_AND_PAIRED_BUILD_2026-10-05.md).

Updated: October 4, 2026 · Project: BrineSpace · Status: **RELEASE BLOCKED**

## Current packaged comparison — October 5

[Twelve accepted visible release runs](PERFORMANCE_PACKAGE_RESULTS_2026-10-05.md)
compare both frozen packages with the corrected driver, and cover the new
candidate at 1080p/1440p plus 12-room idle. Large-scene lighting p95 improves
19–20%, zoom 2–4.5% observationally. All 45 candidate phase runs still fail the
combined performance gate. Median reported memory: 4035 MiB large/1080p,
4048 MiB large/1440p, 3631 MiB reported/1080p. Warm request-to-ready 6.15–6.35 s;
fresh-profile 13.01–14.61 s, disk cache uncontrolled. The 40-room saved-load case
is not certified. A long QA-profile shader-cache error was reproduced and fixed
by short isolated profile placement; all three runner regressions and twelve
final native runs pass without engine/script errors. Original saves unchanged.

## Prior diagnostic/candidate continuation

See [the performance diagnosis](PERFORMANCE_DIAGNOSIS_2026-10-04.md) for the
corrected benchmark, source-mapped image inventory, room storage sharing and new
frozen Windows candidate **brinespace-124c70736fbfb879**. Exact asset audit and
normal-entry/F8 release smoke pass. Reported 12-room memory still exceeds budget;
the 40-room inventory is incomplete. New matched package timings are not accepted
because concurrent jobs and minimization invalidated the attempts. The fixture
now fails these render interruptions clearly. Older signal-driver frame results
below are historical comparisons, not a certification of current gameplay.
Window-availability clarification remains pending; all 2,936 owner files unchanged.

## Objective and acceptance

Implement the owner's PC/Mac performance, bug closure and release-readiness plan.
Public itch.io uploading/visibility changes remain a separate action. Target
hardware is GTX 1650-class 4 GB / 16 GB RAM / SSD and Apple Silicon M1 / 8 GB;
these are test targets, not verified published minimum requirements.

Gates: uncapped p95 <=16.7 ms, p99 <=25 ms; investigate every frame >50 ms,
no reproducible gameplay stall >100 ms; cold loading <=10 s, warm <=6 s;
texture memory <=2 GiB for 12 rooms and <=3 GiB for the large scene; settled
transition growth <=5%. Preserve selected art, timing, scale, filtering, layers,
default effects and explicit user settings. Actual debug=false packaged gameplay
on both platforms is required. Headless tests do not certify rendering.

## Accepted decisions and constraints

No global texture downscale, lossy conversion, removed frames, engine upgrade,
automatic quality changes, broad monolith refactor or art deletion. Preserve
owner saves, layouts, archives and gameplay decisions. Character candidates,
including Krusher V4, remain unselected unless separately accepted. Every native
test uses isolated user data. The workspace contains extensive unrelated changes;
no broad reset, cleanup or commit was performed.

## Current state

Evidence: `output/release-readiness-2026-10-04/` and
`output/release-memory-pass-2026-10-04/`. Full logs, failed experiments, JSON
timings, inventory, source hashes, screenshots and scratch profiles are retained.

### First implementation pass

- Session-owned weak immutable crew-image storage preserves separate frame
  wrappers, identities, metadata and filtering. PNG signatures are prepared by
  bounded image-prefetch workers. Selected-animation loading remains intact.
- Matched warm startup improved **9.070 -> 6.617 seconds**. Startup texture memory
  fell **5,249.95 -> 3,142.75 MiB**. All retained selected animation banks passed
  source-pixel, metadata and timing parity. This is developer-native evidence,
  not packaged certification. Earlier 8.31-second startup and 20.32-ms replay
  measurements also do not certify this candidate.
- Added p99, action labels, startup stages and texture/prefetch counters. Worker
  reporting includes unused results, peak decoded bytes and aggregate work time.
- Fixed stale primary-work room lookup immediately after scrapping. Added bounded
  geometry-keyed full-wall placement reuse; solar placement configuration fell
  from roughly 100 ms to 11 ms in the diagnostic comparison.
- Foundation meshes now belong to the grid instance and release with it.
- Removed required image-loading side effects from assertions in BRINE preview
  loaders so release builds perform the same loads.
- Rejected a wave-mesh experiment: idle p95 worsened from about 22 to 28 ms.
  The experiment was removed; evidence remains.
- Ten native title/Continue/station/title transitions: 808 nodes / 12 orphans
  remained stable; texture counter 3,854.08 -> 3,978.45 MiB (+3.23%). Cycles 2–10
  changed only 0.28 MiB. This passed that earlier transition-growth check, not
  the absolute memory gate or the current candidate's full endurance gate.

### Follow-up: room memory and workplace stalls

- Full-wall/split-wall helpers share identical immutable source images within
  their lifetime and upload them only when drawn. Registrations and geometry
  remain available to Studio. Matched frozen 12-room inventory: settled texture
  usage **3,956.98 -> 3,651.08 MiB**, saving **305.90 MiB**. Eager sharing alone
  saved 121.97 MiB; delaying unused images saves the remainder. Still above 2 GiB.
  Warm startup for the on-demand inventory was 6.15 seconds.
- Inventory after this change: 9,023 texture objects, 9,014 unique RIDs, about
  2,499 MiB decoded image storage. GPU allocation counters are larger than decoded
  base pixels. Exact transparent-border cropping showed potential, especially
  for crew images, but **no cropping is implemented or accepted**. Readback,
  filtering, logical dimensions and frame identity need proof first.
- The original 40-room fixture left drones docked. Those old timings cannot
  certify active-drone operation. The revised fixture places bays on the perimeter,
  seeds explicit QA reserves and requires active crew, >=20 powered rooms and a
  launched drone before sampling. Observed: 38 powered rooms, four outbound drones.
  `ready_ms` measures the initial save, NOT 40-room loading; synthetic fixture
  preparation is now reported separately.
- Active workloads exposed **~650 ms repeated workplace-note route searches**.
  One reachability traversal now replaces searching separately for every meal
  or rest node. The matched 60-frame-per-speed comparison reduced this work to
  about 15 ms while preserving route answers. Collapsed workplace notes skip the
  query and refresh immediately when opened; subsequent panel samples are ~50 us.
  Additive interface diagnostics separate workplace, forecast, scrap and alerts.
- Three subsequent developer-native 1080p idle runs (180 frames per speed): p95
  **44.1–46.5 ms at 1x**, **51.8–57.4 ms at 2x**, **59.3–83.3 ms at 4x**. All
  phases fail the frame gate. Two runs reproduce **~843–845 ms** stalls outside
  the explicit gameplay step, which takes about 2.4 ms there. Engine wait includes
  other node processing and rendering; GPU causation is not yet established.
  Additional bounded drone upload/render timing was added to investigate.
  The follow-up trace found a 484 ms frame with ~482 ms engine process time,
  and a separate 269 ms frame with ~134 ms measured GPU time. Recent drone
  uploads were 46–138 MiB atlases, but occurred 7–15 frames before those stalls;
  the trace does not establish uploads as the cause. Investigate other node
  processing and GPU/resource scheduling separately.
- These are short diagnostic developer-native runs on an RTX 4070 Ti, not target
  hardware or packaged release certification. Large-scene memory remains over
  budget (roughly 4.0–4.1 GiB at the end of these samples).

Changed areas: crew texture pool/batch/prefetch and renderer ownership; full-wall
and split-wall helpers; `bill_npc.gd`, `crew_primary_work.gd`, `crew_work_panel.gd`,
`main.gd`, `drone_animation.gd` upload diagnostics, performance monitor, benchmark tools, assertion
safety fixes, focused tests and `tests/index.json`. Existing unrelated changes
remain untouched.

## Release issue register

| Issue | Current disposition |
|---|---|
| First navigation rebuild after door lock/unlock uses prior lock state | Fixed in normal source October 8: maintained Bill/Marsh regression red90/4 failures, green90/zero; private rotation/scope coverage passes. Current packaged verification pending. See NAVIGATION_LOCK_AND_BAY_SCOPE_2026-10-08.md. |
| Warm large-room navigation cache retains another room owner; Moonbay boarding stalls | Fixed in normal source October 8: 86 regression checks clean; actual private release all three natural missions launch. Combined export delivery pending. Remaining 240 ms transition stall open. See NAVIGATION_ROOM_OWNER_FIX_2026-10-08.md. |
| Apparent station-controls/time-panel overlap at 1440p | Corrected October 5: expected scroll clipping. Actual packaged wheel-input check exposes all eight controls/status labels, time panel stays fixed; screenshot reviewed. No UI fix required for this report; broader scaling matrix remains open. See PRE_RENDER_OPTIMIZATION_2026-10-05.md. |
| Deep Windows QA shader-cache paths | Runner fixed after reproduced long-path error; copied cache at short path and twelve final release runs clean; normal player profile unchanged |
| Large-room default prop editing/placement | Earlier source fixes; current packaged recheck pending |
| Large-room characters in Studio | Earlier source fixes; current packaged recheck pending |
| Tidal mini waterline | Earlier source fix; current packaged motion review pending |
| Tidal north-wall pipe overlap | Earlier source fix; current packaged review pending |
| Middle hand-card sizing | Earlier source fix; current packaged size/alignment matrix pending |
| Salvage Workshop wrong props | Earlier source fix; current packaged selected-art review pending |
| Hunger/fatigue/health/oxygen panel meters | Earlier source implementation; packaged readability review pending |
| Compact portrait needs meters | Earlier source implementation; packaged scaling review pending |
| Brighter hand/resource accents | Earlier source polish; packaged contrast/visual acceptance pending |
| Stale room reference after scrap | Source fixed; focused regression passes; packaged flow pending |
| Repeated workplace reachability pause | Source fixed and matched developer-native improvement; packaged recheck pending |
| Absolute texture memory | **Blocker**, both standard scenes exceed budgets |
| Native frame pacing | **Blocker**, p95/p99 and reproducible stalls fail |
| Loading budgets | **Blocker**, cold/warm and true large-save loading not certified |
| Save/Continue, input and menu ownership | Full current packaged matrix pending |
| Layout/doorway/navigation/construction cancellation | Relevant focused checks exist; current release matrix pending |
| Two-hour native soak / longer headless run | Pending; short transition test is not a substitute |
| 960x540 through 1440p, text scaling, Retina, motion/layering | Full current visual matrix pending |
| Windows clean launch/upgrade/DPI/audio/focus/reports | Frozen candidate audited; packaged workloads run with debug=false. Normal entry/upgrade/DPI/audio/focus acceptance still pending |
| Mac gameplay/Retina/trackpad/Cmd/save/audio | Native Apple Silicon tester required; Intel unverified |
| Developer ID/notarization/Gatekeeper/stapling/offline launch | Local credentials and Mac setup/testing pending |
| Matching physical source freeze / PCK audits / packages | Pending; no candidates certified |

Existing report index: 289 records, clustered into 149 performance, 4 Credits,
4 navigation, 2 nil draw, 2 lazy reentry, 1 card overlap, 2 audio, 2 visual and
123 other historical/fixture reports requiring individual disposition.
`report-clusters.json` preserves that triage. Clustering does not prove resolution;
merge new reports before freeze. Historical tests never close a current issue.

## Verification

First-pass checks passed: crew batch 76, immutable pool 39, placement cache 7,
stale room 3, grid mesh lifetime, image prefetch, performance monitor, release
manifest Python tests 9, Mac exporter Python tests 2, release assertion safety 2.
Monitor observation overhead was 0.18–0.19 us/sample in a synthetic test; this
does not certify screenshot/report/autosave costs.

Follow-up checks passed: wall sharing/on-demand lifetime and exact source pixels
**73**; service reachability **7,402** against existing route answers on deterministic
dry/swimming graphs with disabled nodes and fire (including unchanged graph state);
stale-room regression **3**. Native large-station capture reviewed for populated
room art. This does not close the nine original packaged visual reports.

Known older fixture mismatches: wall-rollout expects one bank where current art
uses split banks. `test_side_wall_variants.gd` also stops at its one-bank assertion
(line 27), before mirror checks. Neither is counted as passing; reconcile with
current selected art before treating it as a production regression. Failed probes
and instrumentation parse errors were corrected; their logs are not acceptance.

Owner profile fingerprint: **2,936 non-log files unchanged**. Every benchmark also
checks its own resolved scratch user directory before writes and records a before/
after owner comparison. No owner saves/layouts/progression were altered. No release
upload, visibility change, notarization, signing or certified package was produced.

## Follow-up milestone: first-use audio synthesis

The 24-callback native profile found five station-audio callbacks taking
11.8–39.1 ms. They included first-use procedural sound synthesis. It did not
reproduce the earlier ~844 ms stall, so this smaller hotspot does not close that
issue. All temporary profiler edits were restored byte-for-byte after each run.

Prepared all **45 original procedural cues** offline as import-free PCM plus
loop metadata. `station_audio_cues.gd` retains the unchanged synthesizer and
cache identity contract; runtime loads the prepared samples. The full set takes
**52.1 ms to load versus 868.5 ms to synthesize** in the focused comparison;
worst single load was **3.76 ms**. The matched callback-instrumented large-station
run reported **zero audio callbacks over 10 ms**, versus five before.

Validation: **406 parity checks passed**, including every PCM byte, duration,
format, rate, channel count, loop settings and cached object identity. Existing
`test_suno_audio.gd` integration passed. Read-only release-manifest collection
includes **45/45** cue files. Native p95 remains **47.4 / 54.9 / 82.6 ms** at
1x/2x/4x, with max **81.9 / 96.7 / 149.8 ms**: this does not pass frame gates or
establish an overall FPS improvement. The assets add about 2 MiB decoded audio
(2.8 MB serialized), with no selected sound-design change.

Changed: `scripts/station_audio_cues.gd`, `assets/audio/procedural-cues-v1/`,
`tools/bake_procedural_audio.gd` (+UID), `tests/test_baked_procedural_audio.gd`
(+UID), and `tests/index.json`. Reproduction instructions are beside the data.
Evidence: `child-profile-fixed/`, `audio-baked-profile/`, and
`audio-pass-summary.json` under the memory-pass evidence directory. Failed
instrumentation attempts are retained separately and not counted as acceptance.
All **2,936 owner non-log files remain unchanged**.

Room-screen/effect code inspection confirms continuous animation curves; simply
skipping those redraws would change motion. Consider retaining static prop bodies
separately from animated overlays only after a matched visual/performance check.
No renderer quality reduction or speculative redraw change was applied here.

## Retained library bodies — continuation

Ordinary library screens/effects now use adjacent body and animation slots. Static
polygons and contact shadows stay retained; screens/effects still redraw on their
original clock, with unchanged draw order, filtering, flood shaders and culling.
Portable/custom props, aquariums and drone docks retain their existing paths.
Expanded entries compare stable prop identity, so repeated submits do not invalidate
the body merely because a new wrapper dictionary was created.

Changed: `scripts/room_content_canvas.gd`, `scripts/room_asset_library.gd`,
`tests/test_library_layers.gd` (+UID), and `tests/index.json` (native lane).
Existing reduced-motion changes in the library predate this pass and were preserved.

Verification: **528 native checks passed** across current Command Center and
Anomaly Lab props, four orientations, power on/off, copied IDs, mirroring, two scales,
dry/flooded states, nearest/linear filters, exact combined/split pixel equality,
continuous live redraws and unchanged-body retention on repeated submit. Existing
bunk-layer parity also passed **17 checks**. The large-station capture was reviewed
for populated room art; this is not packaged visual acceptance.

A focused same-process alternating comparison of 120 animated props measured
**7.97–8.23 ms combined versus 5.44–5.49 ms split** drawing CPU time (about 33% less).
Three matched 40-room/1080p idle runs per revision (180 frames at each speed) reduced
mean room-content draw CPU from **6.29/6.32/6.60 ms to 3.74/3.76/4.03 ms** at 1x/2x/4x.
Median run p95 changed **44.17/54.27/56.09 → 42.30/51.42/56.12 ms**. Thus 4x frame
pacing is effectively unchanged; no 60 FPS gate passes. Texture memory is identical
between matched runs (4,195.77 MiB first profile; 4,131.96 MiB warm repeats).
A separate character preview was running on this host: frame results are diagnostic
and may contain contention, not clean release certification. Focused CPU evidence
supports accepting the bounded redraw optimization without claiming overall readiness.

Historical fixture failures remain explicit: `test_library_prop_retention` expects
two screens but current art draws four (four count failures, exact pixel checks pass).
`test_powered_display_retention` names retired Anomaly props (36 failures). Both fail
identically with splitting disabled. `test_copied_prop_animation` accesses the removed
`mining_tether` before drawing and was stopped after that error. None was weakened or
counted as passing; migrate those fixtures to the accepted current art in the test
cleanup pass. New regression coverage uses actual current props and copied IDs.

Evidence: `output/release-render-pass-2026-10-04/{before,after,comparison.json}`;
focused/parity/legacy fixture logs in `output/release-readiness-2026-10-04/`.
Memory, stutters, broader action/resolution coverage, endurance and packaged checks
remain open. This optimization does not alter simulation or selected artwork.

Follow-up 60-frame pan/zoom/lighting phases at all three speeds completed with no
missing-image reports. The diagnostic `--combined-library-layers` switch allows
comparison without altering source files. Both paths still stall: split zoom p95
100.6–113.7 ms, lighting 93.8–123.7 ms, maximum 189.7 ms. Combined-path maximum is
225.2 ms. These are single runs with shared-host contention, not a certification
matrix or proof of every action's improvement. Detailed paired values are in
`action-comparison.json`; zoom/lighting stalls are the next focused investigation.
All **2,936 owner non-log files remain unchanged**, verified after the final run.


## Wall fade invalidation — continuation

Accepted a limited optimization: the wall pass excludes ordinary-room light-fade
levels from its key. It preserves every other existing surface dependency and
keeps **corridor** fade levels, because their risers are tinted directly. Floor
lighting still redraws continuously. Floor and wall cache sizes settle independently
after zoom; the key is only derived when floor state changes, avoiding a new deep
copy every idle frame. `--rebuild-walls-with-light-fades` provides the reference path.

Changed: `scripts/grid_canvas.gd`, `tests/test_wall_fade_retention.gd` (+UID), and
`tests/index.json` (explicit native lane). Concurrent Bill source-binding guard
changes were preserved. This is not per-room wall retention: when a visible
corridor fades, the combined wall pass still rebuilds.

**104 native checks pass**: exact retained/fresh wall pixels through four orientations
and four ordinary-room light levels, positive nonempty captures, floor redraws,
corridor fade invalidation, and key dependencies. The initial experiment incorrectly
excluded corridor fades; its pixel test caught that before acceptance. Camera limit/
pointer anchoring and the existing six-view/three-transition zoom-shell test pass.
No temporary profiler wrappers remain. A first tracer attempt failed to compile;
all 34 modified files were restored exactly. The layer profiler then preserved a
concurrent edit by removing only its own wrappers (recorded selective-restore diff).

Focused native alternating reference/candidate/candidate/reference runs (80 frames,
first 10 excluded, VSync disabled) change only ordinary-room fade levels while
corridor light stays fixed. Mean elapsed frame time: **17.45/16.74 ms reference vs
15.06/14.37 ms cached** (pooled means about **17.09 → 14.71 ms**, 14% reduction).
P95 ranges **17.73–18.33 → 15.03–15.97 ms**. Wall rebuild counts drop **79 → 0–1**.
An earlier probe's draw-time counters were consumed elsewhere and returned zero;
those timings are invalid and were replaced with elapsed rendered-frame timing.
This focused fixture is not a release performance gate.

Three 40-room/1080p runs per path, with 60-frame pan/zoom/global-lighting phases at
1x/2x/4x, show **no reliable overall gain**. Median p95 (reference → candidate):

| Action | 1x ms | 2x ms | 4x ms |
|---|---:|---:|---:|
| Pan | 41.15 → 42.11 | 41.74 → 40.14 | 56.98 → 55.84 |
| Zoom | 95.08 → 99.46 | 103.87 → 107.16 | 115.75 → 109.69 |
| Global lighting | 97.03 → 96.10 | 97.60 → 94.60 | 94.85 → 97.48 |

All 27 candidate phases still fail the release gates; do not call the global stalls
fixed. Texture memory matches by run: **4,234.49 MiB first profile / 4,170.68 MiB
warm repeats**, above budget. Profiling shows several simultaneous rebuild costs,
including solar-room preparation and floor/wall layers; the earlier ~844 ms
engine-wait stall is not closed by this work.

Evidence: `output/release-zoom-pass-2026-10-04/` (reference/candidate, comparison,
profiler logs/backups, scoped diff and final owner fingerprint), with regression
and focused logs in `output/release-readiness-2026-10-04/`. All **2,936 owner
non-log files remain unchanged**. Native GPU tests remain on the owner's RTX 4070 Ti,
not the target GTX 1650/M1 or frozen release executables.

## Floor and room-setup diagnosis — October 4 continuation

Objective remains the accepted PC/Mac release gates. No new performance optimization
is accepted in this pass; visual quality, owner layouts and source art are unchanged.

**Changed:** `scripts/grid_canvas.gd` adds optional per-room actor preparation,
floor, shell, contents, light-pool and equipment-shadow timings. Existing fields
remain intact. Collection uses the existing `profile_draw` switch, resets with the
existing frame dictionary, and adds no per-frame histories or image storage. The
new fields retain the historical `setup_` prefix for report compatibility; floor,
shell and lighting fields describe drawing, not only setup.

**Verification:** a native 40-room/1080p diagnostic completed zoom and lighting at
1x/2x/4x, 60 frames per phase, without logged engine errors or missing-image reports.
All six phases contain finite, nonnegative values for every new timing group.
Solar configure contributes 0.995/2.222/2.680 ms per frame during zoom, and
1.141/1.211/1.152 ms during lighting. The worst lighting frames contain about
9.7–10.1 ms of solar setup and 64.9–74.5 ms total grid drawing. Simulation stepping
on these frames is only 2.3–3.4 ms; engine wait spans 172.7–187.3 ms. These timings
can overlap and must not be added as independent components. They do not establish
a GPU-upload cause for the remaining stalls.

A focused warm rotation probe narrowed solar configure cost: fixed rotation costs
about 15 microseconds, alternating rotations about 1.28 ms. Separate measurement
attributes approximately 0.23 ms to base geometry rebuilding and 1.22 ms to the
full-wall installation/apply path. A four-rotation base-geometry cache **did not
improve** the matched probe (about 1.45 ms), so it was removed and the original
solar source verified byte-identical to the pre-experiment backup. No cache code
from that experiment ships. The initial probe had a wrong reactor script path;
its partial log is not a passing test. The corrected probe completed both rooms
and all four fixed rotations plus alternating rotation.

This is one developer diagnostic, not a three-run comparison or packaged acceptance.
Zoom p95: **84.95/97.65/118.56 ms**; lighting p95: **98.20/105.43/99.54 ms**.
No phase passes the release gates. Texture memory **4,233.32 MiB** and measured
12-room startup **16.00 seconds** also fail their targets; the 40-room fixture is
prepared afterwards. Startup is a fresh profile with uncontrolled OS disk cache.
All **2,936 owner non-log files remain unchanged** across the complete pass.

Evidence: `output/release-floor-pass-2026-10-04/` contains the scoped diagnostics
diff, probe, rejected experiment, native `stages/` results, `analysis.json`, and
owner fingerprints. Focused probe logs are in `output/release-readiness-2026-10-04/`.
No new art/visual acceptance is claimed for this diagnostics-only change.

Next useful step: isolate full-wall installation/owner-layout application before
attempting another cache; any cache must retain current edits, deletion markers,
rotation-specific dressing, navigation geometry and frame identity. In parallel
with that investigation, the much larger combined surface redraw/engine-wait cost
remains the primary frame-pacing problem. Do not attribute all stalls to solar setup.

## Actual Windows release baseline — October 4 continuation

**Objective/decisions:** continue the accepted release gates without reducing art
quality. Further profiling puts repeated solar full-wall setup near 1.03 ms per
alternating rotation (roughly 0.19 ms placement, 0.28 ms dressing, 0.49 ms layout
application). A filter-before-copy dressing experiment has no reliable gain:
reference 1.2195/1.1594 ms versus candidate 1.1858/1.1829 ms for complete configure.
It was removed; the original runtime file is restored. No runtime optimization is
accepted from this continuation.

**Changed files:** `tools/run_release_benchmark.py` now accepts `--release-exe`
for Windows EXE + adjacent PCK, using physical QA copies and temporary autoload
adapters. It records build/EXE/PCK/fixture/guard identity, rejects debug runtimes,
and guards the resolved profile before BugReport's session-lock writes.
`tools/release_benchmark.gd` adds preliminary scene-load/full-ready timing and
automatic-report counts while preserving existing fields.
`tests/test_release_benchmark_runner.py` covers copy independence, delivery override
preservation, overwrite rejection and missing-PCK rejection (two tests).
`docs/RELEASE_WORKFLOW.md` documents the maintained packaged route and timing scope.
No overrides are placed beside the delivery candidate. Mac bundle launch remains
outside this runner's supported scope.

**Frozen candidate:** `output/release-wall-setup-2026-10-04/candidate-r2/BrineSpace.exe`,
build **brinespace-7cefe63089abd67a**. A physical 55,684-file snapshot (3.55 GiB,
including sidecars/build prerequisites) yielded 36,235 selected manifest inputs.
All copied bytes were stable during capture; post-export source checking found
zero changes apart from permitted export-preset/import-sidecar updates. Both
platforms can use this retained snapshot; no new Mac package was produced here.
EXE/PCK hashes match the tested QA copies and are recorded beside the candidate.
It is labelled internal/not release approved and has not been uploaded.

The first export was rejected: this session's driver set Git's work tree to the
original checkout, so raster-role lookup from the frozen subdirectory missed
three UI atlas dependencies. Correcting the driver to use the frozen work tree
restored all three normal texture import roles. The failed package/logs remain in
`candidate/` as rejected evidence, not a deliverable. The successful retry uses the
maintained exporter and the same source identity. The official release template
also rejected an earlier loose-source `--path` attempt; that is why actual packaged
execution was added rather than relabelling editor results.

**Verification:** nine manifest tests pass; all 392 selected runtime scripts pass
the loading-side-effect assertion scan. The exact-PCK audit ran from an empty
folder outside the checkout: **35,779 checked, missing=0, changed=0, unexpected=0**.
All six packaged workload runs complete with `debug=false`, no logged engine
errors and no missing-image reports. An intentional wrong-profile launch exits
nonzero before creating any non-log user files. All **2,936 owner non-log files
remain unchanged** across the entire continuation.

Three large-station runs (40 rooms, 1080p, 60 frames per phase, 1x/2x/4x):
38 initially powered rooms, four outbound drones plus one docked, Branforth with
River and Margot. Median p95/p99 across runs:

| Action | Speed | p95 ms | p99 ms |
|---|---:|---:|---:|
| Zoom | 1x | 76.65 | 87.59 |
| Lighting | 1x | 82.46 | 163.11 |
| Zoom | 2x | 86.36 | 111.39 |
| Lighting | 2x | 98.05 | 167.14 |
| Zoom | 4x | 100.20 | 121.22 |
| Lighting | 4x | 88.86 | 156.78 |

**All 18 large-station phases fail.** Worst sampled frame 176.37 ms. Texture memory
is 4,215.32 MiB first / 4,213.95 MiB repeats (**about 4.12 GiB**, not 4.22 GiB).
A final native screenshot was inspected: station, selected artwork, cards and
compact meters render. That single far-zoom screenshot does not close the nine
original visual reports or establish animation/motion acceptance.

The first loading numbers (11.76 s first / 4.72–4.94 s warm) measured only the
historical post-resource-load `ready_ms` interval. **Do not count those as a warm
loading gate pass.** Three follow-up packaged 12-room runs validate the added fields:

| Timing | Fresh profile | Warm 1 | Warm 2 |
|---|---:|---:|---:|
| Main scene resource load | 1.235 s | 1.181 s | 1.170 s |
| Historical ready interval | 12.231 s | 4.744 s | 4.824 s |
| Scene request through ready | **13.601 s** | **6.062 s** | **6.131 s** |
| Engine uptime at ready | 15.055 s | 7.378 s | 7.407 s |

First-profile OS disk cache is uncontrolled, so these are not certified cold-disk
measurements. The fixture bypasses normal intro/title/dialogue; normal application
startup and Continue still require separate acceptance. Twelve-room textures are
**3,687.26 MiB** (over the 2 GiB budget). Idle p95 across these nine phases spans
**18.74–19.84 ms**; none meets the frame gates.

Automatic reports are enabled in the packaged fixture, unlike editor `-s` runs.
Each large run saves one report during initial loading of the empty QA entry scene,
before the measured gameplay phases (about 1.24–1.30 s stall at engine uptime 2 s).
These are retained startup evidence, not evidence of a gameplay report-capture stall.
No direct editor-versus-release speedup claim is made across the differing fixtures.

**Evidence/next action:** `output/release-wall-setup-2026-10-04/` retains the freeze,
rejected experiment/export, audit, safety checks, `packaged-benchmark/`,
`packaged-loading/`, `packaged-summary.json`, final owner fingerprint and hashes.
The release runtime confirms that substantial surface redraw and texture-memory
work remains necessary. Prioritize those measured costs; small solar setup tweaks
alone cannot recover this frame budget. Normal entry/save/upgrade, the other actions,
1440p, original bug/visual closure, endurance, target hardware and Mac certification
remain open. This is a real Windows release baseline, not release certification.

## Retained room walls accepted — October 4 continuation

**Objective/accepted decision:** reduce repeated surface drawing while preserving
artwork, layer order, effects and all structural invalidation. A corridor's light
fade formerly repainted every visible wall. Room shells and north crowns now keep
separate retained drawing nodes in the original order (all shells, then crowns).
Only the corridor shell redraws for its continuous fade. All prior non-fade state
remains a shared deep snapshot; structural changes still conservatively invalidate
all wall slots. Slots follow the existing parent zoom transform, release when their
room leaves the retained set, and die with the station. No new images are loaded.
`--combined-wall-slots` selects the prior combined renderer for matched comparisons.

**Changed files:** `scripts/grid_canvas.gd`; `tests/test_wall_slot_retention.gd`
and its `.uid`; native lane/subsystem entry in `tests/index.json`. Existing work
from other sessions was preserved. The scoped source diff is retained with evidence.

**Verification:** 134 native checks pass: exact combined/retained pixels across
four rotations, ordinary and corridor fades, first-rendered-frame slot creation,
wall visibility toggles, room removal and dependency coverage. The initial slot
experiment hid and showed every child on each pass, causing unnecessary redraws;
the redraw-count assertion caught it. Only genuinely hidden/reference paths now
hide slots. The zoom-shell regression passes six room views and three transitions.
The maintained test is byte-identical to the validated fixture, with its UID paired.

Three 40-room/1080p developer-runtime runs per path, 60 frames per zoom/lighting
phase at 1x/2x/4x, complete without engine errors or missing art. Median p95:

| Action | 1x: reference → retained | 2x: reference → retained | 4x: reference → retained |
|---|---:|---:|---:|
| Lighting | 93.34 → **81.74 ms** | 97.94 → **86.50 ms** | 98.18 → **84.53 ms** |
| Zoom | 83.39 → 83.22 ms | 98.48 → 100.31 ms | 115.32 → 115.73 ms |

Lighting p95 improves roughly **12–14%**. Median lighting p99 falls from
188.56/189.17/187.52 to 175.74/173.34/166.51 ms. Measured mean wall work (parent plus
slots) drops from 1.74–1.86 to 0.36 ms/frame during these lighting phases. Zoom has
**no reliable improvement**; do not claim the remaining zoom stalls are fixed.
Texture memory matches exactly by run: 4,233.32 MiB first and 4,231.94 MiB warm.
All 18 candidate phases still fail the release frame gates. This accepted change
is supported by matched native development diagnostics, not a new release package.

**Current state/next action:** `brinespace-7cefe63089abd67a` is still the previously
frozen packaged baseline and **does not include this optimization**. Re-freeze and
recertify a later candidate after the next accepted work. Remaining priorities are
floor/surface preparation during zoom/global lighting and the texture-memory budget;
normal entry/upgrade, other actions/resolutions, bug/visual closure, endurance and
Mac/target-hardware acceptance remain open. No upload or visibility change occurred.
Evidence: `output/release-wall-slots-2026-10-04/` (reference/candidate runs, comparison,
source diff, pixel fixture, owner fingerprints); native test logs are under
`output/release-readiness-2026-10-04/`. All **2,936 owner non-log files are unchanged**.

## Solar rotation preparation accepted — October 4 continuation

**Objective/decision:** reduce the measured solar-array setup hotspot during zoom
without changing art or adding GPU images. A shared view formerly rebuilt full-wall
placement/dressing when alternating room rotations (up to about 6 ms in a slow frame).
It now retains at most four prepared layouts, keyed by selected layout, store and
geometry revisions, and source item registrations. Restores own mutable geometry,
props and dressing copies; the existing view retains its textures. Studio bypasses
and clears snapshots. Runtime door openings, power and clocks still configure on
every call. `--rebuild-solar-rotations` selects the previous path for comparisons.

**Changed files:** `rooms/full-wall-v1/solar_array_view.gd`,
`tests/test_solar_rotation_cache.gd` with paired UID, and native performance test
registration in `tests/index.json`. Other-session work is preserved.

**Verification:** 405 native checks pass: nonempty exact floor/shell/prop pixels,
all four rotations, varied door openings/omissions, power and clocks, deleted and
restored banks, moved/resized/flipped layouts, wholesale store replacement without a
revision bump, same-quarter deletion, four-entry bound and Studio invalidation.
The maintained test is byte-identical to the passing fixture. The existing zoom
regression passes six room views and three transitions. Candidate large-station
screenshot inspected: station, card hand and compact needs meters render; this
far-zoom fixture is not original bug-list or motion acceptance. Its 10000% integrity
is an explicit QA reserve, not normal gameplay.

Three matched 40-room/1080p development-runtime runs per path, 60 frames per action
at 1x/2x/4x, complete without engine errors or missing-art failures. Median p95:

| Action | 1x: reference → cached | 2x: reference → cached | 4x: reference → cached |
|---|---:|---:|---:|
| Zoom | 85.55 → **78.96 ms** | 100.45 → **90.35 ms** | 115.90 → 115.88 ms |
| Lighting | 82.44 → **74.19 ms** | 90.54 → **81.14 ms** | 85.52 → **78.20 ms** |

Solar configure work falls roughly **71–75%**: zoom mean 1.02/2.35/2.64 ms/frame
becomes 0.26/0.58/0.66; lighting 0.86–0.90 becomes 0.24–0.26. Zoom p95 improves
about 8–10% at 1x/2x, with **no meaningful 4x gain**. Lighting p95 improves about
9–10%. Texture memory is identical in both paths: 4233.32 MiB first run and
4231.94 MiB warm. All 18 candidate phases still fail the frame gates. Large stalls
remain: worst reference 1002.68 ms and candidate 951.18 ms. The change does not
resolve engine-wait spikes, memory budgets or overall 60 FPS readiness.

**Current state/next action:** retain this source optimization. Frozen Windows
`brinespace-7cefe63089abd67a` predates both this and retained wall slots; no new
packaged acceptance is claimed. Investigate the remaining engine-wait stalls and
texture budget, then re-freeze/certify the accepted source alongside the outstanding
actions, resolutions, normal entry/upgrade, bug coverage, endurance and Mac testing.
Evidence: `output/release-solar-cache-2026-10-04/` contains reference/candidate runs,
comparison, source diff/hashes, pixel fixture and owner fingerprints. Native logs
are under `output/release-readiness-2026-10-04/`. All **2936 owner non-log files
remain unchanged**. No upload or visibility change occurred.

## Next action

Reduce the remaining combined floor/wall rebuild work during global lighting and
zoom (ordinary-room-only fade retention now passes). Continue isolating the earlier
engine-wait stalls using upload/render timing and lowering texture memory. Finish fresh/reported/large action and resolution
coverage, actual release-template execution, endurance, packaged visual/bug closure,
report disposition and the maintained `RELEASE_WORKFLOW.md` package process.
Mac hardware and Developer ID credentials are external requirements. Failed memory
and frame gates remain blockers even when those requirements become available.
