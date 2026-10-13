# September 27 owner report fixes

Updated: September 27, 2026 · BrineSpace · report follow-through

## Objective and acceptance

Resolve the reports listed in OWNER_REPORT_TRIAGE_2026-09-27.md. Visual reports
need current native replay, not merely proof that assets are registered.

## Accepted decisions and constraints

Use isolated copies of report saves and Studio layouts. Preserve real player
files and owner catalog marks. Paid repairs use existing crew jobs and costs.
Veld animation studies are separate work and remain unpromoted.

## Current state

`scripts/main.gd` now shows signed Power balance including vented surplus at
capacity, and exposes a selected-room repair button. It queues existing hull
work, disables repeat purchases and intact-room repairs, and retains the existing
containment-repair path. `scripts/room_flooding.gd` handles unplaced dictionaries
without reading a nonexistent position. This error occurred seven times in the
00:32:46 and 00:35:41 reports.

Regression fixture: `tests/test_report_controls_sept27.gd`; isolated runner:
`tools/check_report_controls_sept27.py`. Evidence is under
`output/owner-report-fixes-2026-09-27/`.

## Verification

Initial native regression reproduced all three failures. After changes, controls
passed with zero failures and identical real-profile fingerprints. A subsequent
native check found the mining drone prop present in all four rotations; this is
not yet visual acceptance of the missing-drone report.

## Native replay milestone

The report's `saves/brine_loop.save` is an earlier checkpoint; use
`diagnostics/live_station.save` for the actual captured station. The runner copies
that into scratch before restoring and resets the autosave path afterward.

- Mining report: current source renders the drone and integrated launch pad;
  all four orientations retain the machinery. No additional dock fix was needed.
- Construction hatch: `room_asset_library.gd` filters the separate circular
  `construction_hatch` from live rooms; the working dock remains. Owner layout
  entries are preserved. Current native capture reviewed.
- Corridor overlap: `corridor_dressing.gd` clips raised side returns and chamfers
  at a connected north threshold. The reported T corridor now joins cleanly.
- Dark water: `underwater_visibility.gd` and `underwater_fog.gdshader` add fading
  local spill beside powered hallways, which can otherwise have every exterior
  beam suppressed by neighbouring rooms. Exploration/survey state is unchanged.
- North windows: `painted_shell.gd` uses the three existing reviewed ocean-window
  sources in exposed north panels. Doors, BRINE's screens and selected materials
  remain authoritative. `grid_canvas.gd` sets explicit exposed context before
  drawing a shared north-wall view. Life Support native capture reviewed.
- Survey timer: excluded live probe clock/blocking state from static floor/wall
  cache keys. Regression reproduced invalidation before the change and passes
  afterward. This is a separate cache defect; the mining report has no survey bay.

Native run passed, including both live report restores; no script errors.
29-room lag replay, 300 measured frames after 60 warmup frames: p95 23.69 ms,
maximum 32.73 ms, zero floor/wall rebuilds. This stationary sample does not prove
startup, Studio, zoom or intermittent lag resolved. All real-profile fingerprints
match. Replay captures and logs are in the evidence directory above.

Both cyan reports predate the later install of 323 existing clean Desktop prop
exports (`DESKTOP_PROP_INSTALL_2026-09-27.md`). Current bay renders have those
muted sources. Veld's later installed consistency pass has a separate 792-check
native audit (`CHARACTER_CONSISTENCY_HANDOFF_2026-09-27.md`); the new animation pilot
is still separate. No further recolouring or pilot promotion was performed here.

## Next action

Investigate the startup/Studio automatic stalls and camera-driven spikes with
targeted native captures. The large lag reports are not closed by the stationary
sample. Owner visual review remains appropriate for windows, water and the later
installed cyan/Veld corrections. No playable executable has been rebuilt.

## Studio latency continuation — September 27

Reproduced three synchronous loading costs in a fresh native Studio process:
opening 1,499 ms, first Walls category rebuild 390 ms, and first Robotics
thumbnail loading frame 244 ms. Fixed the causes rather than suppressing the
performance reports:

- `room_layout_editor.gd`: wall choices publish immediately; their textures
  decode off-thread and populate one at a time, retaining exact atlas regions.
- `floor_finish_tools.gd`: hidden floor choices no longer decode all finishes
  during Studio startup. Visible previews load progressively through the existing
  background image loader and share the production floor cache.
- `drone_dock.gd`/`drone_animation.gd`: prepare the exact south-facing preview
  layers off-thread before rendering a dock thumbnail. Uploads are spread across
  frames; the same runtime texture cache and eviction policy are retained.
  Synchronous consumers drain an outstanding job instead of decoding it twice.

Final native sample: opening 598 ms, first Walls rebuild 1.54 ms, Robotics maximum
15.78 ms across complete thumbnail loading. All 22 wall choices, all Robotics
previews and all floor previews finish loading. Reviewed Walls, Robotics and floor
captures. Common Props still has a 120 ms first-frame peak; these measurements
do not claim every cold load is eliminated. Drone regression: 252 clips,
144 directional phase samples and dock boundaries, zero failures. Owner-profile
fingerprints match; `git diff --check` passes.

Fixture and runner: `tests/test_studio_report_latency.gd` and
`tools/check_studio_report_latency.py`. Evidence: `studio-latency.log`,
`studio-owner-fingerprints.json`, and `studio-{walls,robotics,floors}.png` in the
existing report-fixes output directory. No owner layouts, art files or save
formats changed in this continuation.


## Camera lag follow-through — September 27

The fixture now exercises the real zoom request path for 270 frames after the
stationary replay. First reveal of the Salvage Drone Bay remains a cold-load
spike (468–481 ms in measured runs). Temporary per-load instrumentation traced
about 352 ms to its blocked-state body/cargo and rotor PNGs; the entire bay draw
was 379 ms. Airlock content added about 60 ms. Station simulation was about 3 ms.
This narrows the remaining issue to newly visible artwork, not stationary ticks.

An idle-dock background warmup did not cover the blocked animation and was
removed. Temporary source instrumentation was also removed. Keep the camera
measurement in the isolated report fixture; do not mark the lag reports closed.
Next: prepare the actual fleet state before first visibility, accounting for the
256 MiB animation cache so offscreen warmups do not continually evict live art.
Common Props' 120 ms first-frame load and general startup remain open too.
No executable rebuilt; source changes require running the current project.


Final verification after removing the unsuccessful warmup: report controls zero
failures, owner fingerprints unchanged. Stationary 29-room replay: p95 28.55 ms,
max 40.48 ms, zero floor/wall rebuilds. Camera: p95 27.20 ms, max 474.73 ms.
The lower typical frame time does not excuse the unresolved cold-reveal spike.


## Camera preparation and corrected Studio attribution - September 27

The earlier idle-only warmup was superseded by preparing the actual dock state
for rooms within the requested camera view. `drone_dock.gd` enumerates the layers
used by the real south-facing dock, including blocked, charging and loaded cargo
states. `grid_canvas.gd` waits before moving the camera while those PNGs decode
in parallel; uploads use a 4 ms scheduling budget (an individual upload may exceed
it). All requested cached layers are touched before uploads, preserving the
existing cache eviction policy. Studio keeps sequential preparation, which avoids
preview churn seen with the parallel camera strategy. No fleet state is mutated.

The native camera fixture now checks that requested zooms finish, preparation
waits stay below one second, and no measured camera frame reaches 250 ms. It also
captures the first wide view for visual inspection. These are scoped regressions
for the reproduced cold-reveal problem, not an all-game performance guarantee.

Studio's original Common Props maximum included the editor's first presentation.
The corrected fixture waits for that observable event before measuring category
changes and uses time-bounded completion polling for asynchronous previews.
Final Studio sample: ready 556 ms, first presentation a further 115 ms; Common
Props build 15.94 ms / subsequent peak 5.95 ms, repeat build 16.00 ms / peak 3.58 ms;
Robotics peak 10.21 ms. All wall, Robotics and floor previews finish; 252 clips /
144 directional phase samples plus blocked/charging/cargo preparation checks pass.
Owner profile fingerprints match. No separate Common Props regression reproduced.


### Final verification and next action

Final isolated report run: zero control failures, all zoom destinations reached,
owner fingerprints unchanged. Cold first reveal: 104.07 ms frame versus the
previous 474.73 ms; salvage child draw 0.253 ms versus roughly 379 ms. Camera
preparation waits were 362.92, 24.18 and 93.71 ms. The longer 540-frame camera
sample had p95 29.59 ms and maximum 220.84 ms; two later 211/221 ms frames remain
unexplained by the recorded simulation and draw timings. Stationary 29-room
sample: p95 22.12 ms, max 30.49 ms, no floor/wall rebuilds. Airlock first draw still
cost about 61 ms. Reviewed `camera-replay-wide.png`; dock art is present.

Changed this continuation: `scripts/drone_dock.gd`, `scripts/grid_canvas.gd`,
`tests/test_report_controls_sept27.gd`, `tests/test_drone_runtime_animation.gd`,
`tests/test_studio_report_latency.gd`, `tools/check_report_controls_sept27.py`,
this handoff and CURRENT_STATUS.md. Existing .uid files preserved.

Next investigation: correlate the later long frames with render/GPU timing and
other unprofiled work before attributing them to a subsystem. Investigate the
61 ms first-visible airlock draw separately. Startup still has a 115 ms first
presentation and the larger original gameplay-startup report remains open.
No executable rebuilt, commit or upload. The broad lag reports remain open.


## Airlock reveal and frame-boundary investigation - September 27

Individual prop timing reproduced 63-81 ms in `pressure_chamber` on its first
visible draw. It synchronously loaded engineering wall material, fittings and
low ocean-hatch layers. Camera preparation now shares those decoded images into
the existing renderer caches before reveal. Fittings can load individual keys;
loading all wall fittings later still completes the remaining keys and reuses
already prepared textures. No chamber geometry, cycle rules or artwork changed.

Changed this continuation: `rooms/underwater/airlock-v1/airlock_view.gd`,
`rooms/underwater/airlock-v4/fittings.gd`, `scripts/grid_canvas.gd`, the isolated
report fixture/runner and status notes. Temporary per-prop and PNG-load prints
were removed. The fixture retains render-boundary timing, first-30-frame peaks,
a first-airlock-draw budget and partial-to-full fittings cache checks.

The larger unexplained frames are not all in game simulation or prop drawing:
one focused-window 236 ms frame spent 200 ms after frame_post_draw, with only
15 ms between frame_pre_draw and frame_post_draw. An isolated VSync-disabled
comparison still had a 196 ms frame, 146 ms after frame_post_draw; disabling VSync
is therefore not a sufficient fix. No player display setting was changed.
The diagnostic run is retained as `camera-no-vsync-diagnostic.log` in the report
output directory. These signal boundaries do not identify the underlying OS,
driver or other main-loop work; keep the broad lag report open rather than
attributing it to GPU work without evidence.


Final native acceptance: report controls and partial/full fittings-cache checks
pass, all three zoom destinations finish, owner fingerprints unchanged.
First 30 camera frames peaked at 45.95 ms for the cold reveal (airlock draw
0.48 ms); the following zooms peaked at 57.00 and 43.32 ms (airlock 0.33 ms).
Preparation waits were 334.40, 21.96 and 108.60 ms. The 540-frame camera sample
was p95 29.57 ms, max 189.30 ms; stationary sample p95 25.58 ms, max 210.89 ms,
with zero floor/wall rebuilds. Reviewed the final wide-view capture. Scoped
`git diff --check` passes. Existing UIDs retained; no executable rebuilt.

Next action: investigate the remaining intermittent main-loop gaps with timing
outside the current render signal boundaries. Do not restore synchronous asset
loads, disable player VSync or claim the broad lag report closed. The specific
cold dock and airlock decode stalls are covered by the native regression.


## Transparent atlas memory and persistent frame boundaries - September 27

The remaining timing investigation found a 193 ms frame with approximately
47 ms of cumulative CPU time across the Godot process, using a read-only Windows
process-time sampler. This supports substantial waiting, but does not identify
its cause. Physics callbacks were below a millisecond. The native renderer
reported about 7.5 GiB of textures; the texture audit is an ownership estimate,
not proof of VRAM pressure. A broad initial audit was stopped after the measured
replay because it traversed cached geometry; the bounded texture-only audit
completes. Real-profile fingerprints matched even after that stopped diagnostic.

One concrete waste was verified from source pixels: mining's `empty-120.png` is
2688 x 8960 and entirely transparent (91.875 MiB decoded RGBA). The drone loader
now detects fully transparent images, using Godot's documented `Image.is_invisible`
check on the decode worker when loading asynchronously. It retains a transparent
1 x 1 texture and skips atlas drawing for that layer. Visible layers retain full
size, including salvage cargo. No source art, manifest, timing, frame count or
fleet behavior changes. The original PNGs remain intact.
API reference: https://docs.godotengine.org/en/4.5/classes/class_image.html#class-image-method-is-invisible

The observed drone cache fell from 546.01 to 454.14 MiB; total engine texture
memory in the replay fell from 7533.78 to 7411.28 MiB. This is a memory saving,
not a claim that it solves the broader frame spikes.

`performance_monitor.gd` now includes before-render-signal, between-render-signal
and after-render-signal intervals in hitch records/F8 JSON. They are explicitly
not GPU timings. Stale, out-of-order and absent/headless render pairs are omitted.
The previous implication that all unaccounted frame time is rendering was removed.

Changed this continuation: `scripts/drone_animation.gd`,
`scripts/performance_monitor.gd`, `tests/test_drone_runtime_animation.gd`,
`tests/test_performance_monitor.gd`, `tests/test_report_controls_sept27.gd`,
`tools/check_report_controls_sept27.py`, status and this handoff. No new scripts
or UID changes. The report runner supports opt-in `BRINE_SAMPLE_CPU=1`; the
fixture supports bounded `BRINE_TEXTURE_AUDIT=1`. Neither diagnostic runs in game.

Verification: performance-monitor unit checks, diagnostics checks, 252 drone
clips / 144 phase samples / transparent-layer memory checks, and native F7/F8
report integration pass. The F8 fixture requires native rendering: an initial
headless attempt timed out at its frame-post-draw wait, then the native run passed.
Owner fingerprints match. No executable rebuilt or upload performed.

Important remaining failure: the final measured camera replay still FAILS the
250 ms whole-frame gate (maximum 280.59 ms, p95 28.30 ms); stationary maximum was
643.69 ms with zero floor/wall rebuilds. First-30-frame camera peaks were 87.46,
68.81 and 71.14 ms; airlock draw remained below 0.4 ms. A 281 ms camera frame
spent 210 ms between render signals; its adjacent 193 ms frame had a 154 ms gap
after rendering. Do not describe the global performance gate as passing.
Next: use the now-persistent frame-boundary records to correlate engine/driver
waits, and finish accounting for texture ownership before changing rendering
backends or asset quality. Keep the broad lag report open.
Evidence remains under `output/owner-report-fixes-2026-09-27`: controls.log,
camera-cpu-samples.json, texture-memory-audit.json, the *-boundary.log checks and
fingerprint JSONs. No player display settings, layouts or saves were modified.


Post-change Studio regression also passes: ready 577 ms, first presentation
119 ms, Robotics peak 10.70 ms, all previews complete. Reviewed the Robotics
capture. The native animation assertions remain green; player hashes match.
This does not override the failed whole-frame camera budget above.
