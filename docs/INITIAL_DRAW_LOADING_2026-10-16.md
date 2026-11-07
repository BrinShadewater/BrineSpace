# Initial drawing and deferred UI profile — October 16, 2026

**Most of the post-setup gap is CPU work inside drawing methods.** Four corrected native traces account for **91.5–93.9%** of that interval with instrumented grid drawing. No game code, assets, crew behavior, source snapshot or playable export changed. This is attribution and refreshed loading evidence on frozen **brinespace-53f5bf16534c2cf5**, not an optimization gain or release promotion.

Evidence/helpers: `D:/bs-first-draw-20261016/` and `output/first-draw-20261016/`. Matching d3 Windows/Mac, prior3f/688 and current53f remain frozen. Scope follows [the mixed-loading investigation](LOADING_VARIANCE_2026-10-16.md).

## What the initial drawing costs

Native Windows Compatibility/OpenGL, 1600×900 screen2, silent/Dummy audio, scratch profiles, normal title/buttons and gameplay flags. Four diagnostic visits cover fresh/repeat New and Continue. External observers enable the existing `profile_draw` clocks, trace draw/node/render events, and inspect texture-cache metadata without GPU image readbacks. Diagnostic timings include observer overhead and are separate from headline loading below.

| Post-setup interval | New fresh/repeat | Continue fresh/repeat |
|---|---:|---:|
| Last setup ready → first subsequent render-pre | 932–962ms | 1,596–1,600ms |
| Accounted instrumented grid drawing | 853–888ms | 1,498–1,499ms |
| Remaining wall time | 74–79ms | 98–101ms |
| Root draw's seabed/environment substage | 532ms | 524–529ms |
| Retained terrain-cell painting | 139–176ms | 168–170ms |
| Derelict pass in this first interval | 81–82ms | 137ms |
| Retained still seabed | 58ms | 58–59ms |

Continue also spends **270ms in the first retained floor-slot draws** and **181–182ms in retained wall-shell draws**. These are draw-method totals, not GPU measurements. The seabed substage is part of the root grid draw, so do not add both. Other environment/surface passes make up the remaining accounted time. Terrain cell figures come from their actual child draw intervals/profile labels; the older partially observed trace incorrectly left those child costs under the preceding tracked item.

The sampled seabed/environment texture-cache snapshots gain **66 entries for New/70 for Continue** between setup and the first render-pre. Entries are not a deduplicated image count or a byte-residency measurement. Source paths show first-use environment preparation can load textures, generate biome meshes/placement data and submit retained drawing; this pass does **not** split decoding, upload and geometry costs within each preparation routine.

Relevant source: `scripts/grid_canvas.gd` (`_draw_space_background`, `_draw_environment_layer`, `_draw_cryo_derelicts`, retained floor/wall slots), `assets/environment/seabed-v1/seabed_background.gd`, `assets/environment/sub-biomes-v1/sub_biome_view.gd`, and `scripts/terrain_content_canvas.gd`.

## Deferred UI and the wait after the startup timer

Deferred markers and resize observations establish callback order. The post-setup marker executes about **748–755ms after setup for New /871–875ms for Continue**, while drawing has already consumed much of that time. That waiting interval is **not the marker's CPU cost**. Only 74–101ms of the examined first gap remains outside the measured drawing methods; that residual includes unclocked child drawing, scene/UI work, engine work and observer overhead. Individual UI methods were not timed, and this does not establish that all interface setup is cheap: the earlier `interface_and_grid` phase remains outside this gap.

New has a second important covered draw **after the fixture's startup-complete observation**. In both corrected New traces, startup-complete → uncovered is **1.088–1.189s**, including **798–803ms in the derelict pass**; observed grid-method totals in that window are **1.044–1.047s**. Continue's corresponding extra wait is only **23–25ms** in these traces.

The derelict path can instantiate room views and draw companion/cryo shells on first visibility. The camera-centering path also waits for a process frame and culling depends on the current view. Those source paths are useful targets; this trace does not prove exactly which camera/deferred operation causes the later visibility or split room-view construction from painting. Moving the startup flag or skipping a covered draw would not demonstrate faster visible loading. Keep **both readiness and uncovering endpoints**.

## Unmodified actual-release loading again

Observer disabled and primary QA fixture restored byte-identically. **Eight accepted runs**, two fresh profiles and two repeats per mode, on unchanged53f. Six passed the inherited guard; a seventh launch was rejected and retained, then retried with a new profile before its repeat. Every accepted run uses the normal title/buttons, normal simulation and default gameplay flags.

| Entry | Button → observed startup complete | Button → loading screen gone |
|---|---:|---:|
| First-profile New | **5.571–5.608s** | **6.637–6.691s** |
| Repeat New | **4.960–5.057s** | **6.025–6.230s** |
| First-profile Continue | **7.656–7.679s** | **7.675–7.701s** |
| Repeat Continue | **6.673–6.696s** | **6.695–6.731s** |

No treatment candidate was introduced, so these ranges are **not a measured gain over the preceding cohort**. OS caches are uncontrolled. Normal New Loop randomizes the site; repeat means an existing profile/learned image order, not the same New geography. Post-timing scratch reports confirm four different New seeds; all Continue visits restore **2808620329**. Future New A/B optimization fixtures should explicitly capture/control site seed and final view, with those diagnostic controls separated from normal randomized release acceptance.

Complete crew lossless-source/clip/metadata/timing/filter/historical-bank identities match the previous frozen53f reference within entry mode for all eight primary and four corrected diagnostic visits. Bill's New/Continue binding distinction is retained. Learned request orders match within mode, missing artwork and engine/script error checks pass, normal simulation advances and startup workers/caches release. Max pending decoder96/compression8; repeat decoded peak214.23MiB remains a job-count bound, not a byte cap. Private memory is sampled across the whole process, including post-timing QA: New **2,128–2,140MiB**, Continue **2,642–2,705MiB**; no soak or memory improvement claim.

## Calibration, guard repair and retained failures

- Native calibration confirms the CanvasItem draw signal precedes scripted `_draw`. The first two tiny calibration attempts stopped at their scratch-directory check; the empty-project custom user directory was corrected. No owner data changed.
- One initial fine probe was rejected when the legacy guard saw an empty executable path for PID120800. Its scratch report filename identifies that PID as our own completed game. Four subsequent protocol-valid `fine2` runs are retained but superseded for attribution: `monitor.frames` resets each bucket and is not a unique counter epoch, and terrain children had not all been observed. Do not use their invalid Continue counter differences.
- A diagnostic-only indentation parse failure (`fine3`) stopped before timing. Fixed, headless check-only passed. Corrected `fine4` uses monotonic `monitor.last_usec`, carries consumed `last_draw_timing` across observed resets, observes all grid descendants, and reconciles interval sums with cumulative counters. Continue crosses one reset in each target interval. No production monitor code changed.
- Primary launch `loading-new-2-fresh` was likewise rejected for its own exiting PID129416 with an empty path; original records remain. The task-local guard now retains the actual Popen child/Windows process handle and rejects every other Godot/BrineSpace PID, including another copy inside the QA directory. Four focused guard regressions red→green cover an owned missing-path row, foreign missing-path row, second copy/editor, wrong image and unbound cases. Two subsequent native runs pass; neither reproduced the missing-path race, so exact native race-fix reproduction is not claimed.
- Existing frozen-build exit warnings remain: earlier canonical primary logs already report33 RefCounted ObjectDB instances, and observer runs report34. These warnings are not diagnosed or fixed here; no runtime source changed. Error checks passing are not an overall leak-free claim.

The final analysis cohort is **four corrected diagnostic plus eight primary visits**. Earlier attempts are preserved for audit, not silently substituted into headline timings. Data, fixture/adapter identities and original/final schedules are retained.

## Decision and next work

Keep production unchanged this pass. The next useful prototype is **bounded preparation of the initially visible environment and derelict room art during loading**, with finer clocks separating decode/upload from mesh/material preparation and exact visual controls. Continue's initial floor/wall preparation is another measured target. Retain final camera coverage, draw order, complete assets, normal crew behavior and worker/cache bounds. Measure through uncovering and use controlled New seeds for treatment comparisons. No large refactor, new export or speculative UI change was justified by this profile.

Final verification passes: **124 frozen delivery hashes** and **2,948 protected player files unchanged**, complete crew identities equal within entry mode, and working main/grid/dressing sources match frozen53f. Fresh-context review reports no material findings. Verified task-owned duplicate EXE/PCK cleanup removes **3,738,363,642 bytes (3.482GiB)**; canonical builds, evidence, helpers and restoration identities remain. Final C:/D: free space **115.593/41.150GiB**, no game process. Exact results are in `D:/bs-first-draw-20261016/final-guards.json`. No production edit, export, commit or publication. The owner's matching d3 Mac kit remains the native Mac validation target; large-station60FPS, release endurance and native Mac acceptance remain open.
