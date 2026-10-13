# Project handoff — restored layout templates prepared before gameplay

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Reduce the remaining real-save construction-completion spike without delaying navigation,
altering gameplay or changing selected pixels. Previous turn was progress: installed
pending room-view preparation removed a reproducible101–105ms drawing stall. This turn
installs saved-layout template preparation; complete release/performance goals remain open.

## Accepted decisions and constraints
Actual debug=false Windows RTX4070Ti/1080p, muted secondary display, isolated resolved
APPDATA and input disabled. Frozen current10→11 save and owner layouts copied read-only;
fingerprint original files. Small overlays/reused runtime,20GiB refusal floor. No atlas,
quality, art, simulation scheduling, renderer upgrade or indexed-provider admission.

## Current state and cause
Private timed overlays isolated zoom4x/frame27:
- Branforth completion update~5.6ms; room placement~2.8–3.2ms, UI refresh comparatively
  small. The crew timing includes companion updates; it was not all builder work.
- River navigation rebuild~21–23ms, Margot~3.5–4.4ms,3,012nodes each, retained prefix0.
- New geometry~9–10ms, specifically reactor saved-layout apply~9.073ms; view lookup,
  configuration, retirement filtering and snapshot copy each below0.1ms.
- New BRINE-core and reactor local navigation templates cost~4.6–5.1/~3.1–3.4ms.

Installed changes, existing UIDs preserved:
- scripts/grid_canvas.gd: during station loading, prepare pending orders' layout templates
  once per room type/rotation. Handles queued crew orders and active drone orders.
- scripts/room_asset_library.gd: disposable LayoutPreparation node owns a deep-copied
  prop list and uses the existing apply/copy/variant routines with saved positions.
  The live view's props/rotation/layout stamps remain untouched. Node explicitly freed;
  templates/textures use existing caches and scene cleanup. No new per-frame work/cache.

Source text exactly matches tested private candidate; installation.json records hashes.
scripts/bill_npc.gd remains unchanged; rejected rectangle rewrite was not installed.
All private probe counters remain outside normal source.

## Verification
Three alternating normal/fix pairs on frozen current save,12phases each, idle/pan/zoom/
lighting1x/2x/4x,90frames/phase,6,480measured frames. All36 gameplay snapshots and
phase camera pairs exact. Runtime/safe-image/input/mute/display guards pass.

| Metric | Normal, with preceding room-view fix | Saved-layout preparation |
|---|---:|---:|
| Mean ms |13.051|12.986|
| p95 ms |19.217|19.233|
| p99 ms |29.137|28.929|
| Max ms |63.025|50.685|
| >50 / >100 |3 / 0|1 / 0|
| Peak gameplay texture MiB |1940.831|1940.831|

Completion-frame totals per pair60.455/63.025/62.220ms →50.685/48.548/48.094ms.
Crew portions33.075/36.652/34.169ms →25.473/23.767/23.706ms. Pooled mean~0.50%better,
mixed pair means: admit for consistent event-cost improvement, not a broad FPS claim.
p95/p99 and one remaining >50 frame still fail gates. Instantiation-to-ready9,824–10,095ms
normal and9,903–9,940ms candidate are noisy and exclude earlier startup/scene request;
not cold/warm-loading certification. Do not compare absolute means across prior turns.

Separate native visual/ownership pass (timings discarded): eight exact RGBA reactor pairs
at61.333–64% fitting and immediately before/at/after completion. Same game clocks,
progress, camera rectangles; hand hidden only in fixture, simulation frozen for capture.
169x169 fitting and147x147 completion images inspected,3,156–5,656 distinct colors.
Repeated helper call leaves live props, metadata and rotation unchanged. Final library
texture-source sets exact,59paths each; no extra retained source in this workload.
This is scoped construction/completion coverage, not all rooms/rotations or Mac acceptance.

Rejected independent scalar rectangle trial: removes the explicit axis loop while keeping
slab arithmetic/half-open edges.100,000 valid differential cases pass (28,719hits/71,281
misses). Initial negative-size fixture invoked unsupported Rect2 inputs and logged engine
errors in both versions; normalized fixture reran clean. Native three pairs on privately
warmed layouts:mean13.278->13.282ms, p9520.105->20.137, p9929.955->30.915,
max54.156->72.565,>50count1->2. Completion costs improve somewhat, but overall benefit
unproven; reject rather than admit additional kernel work. All36 states/cameras exact,
memory equal. No production predicate change.

Evidence under D:/bs-release-crew-cache-20261009/benchmark-input-isolation:
current-crew-completion-trace, current-companion-rebuild-trace,
current-navigation-template-trace, current-navigation-geometry-trace,
current-navigation-layout-trace, pending-layout-template-trial,
navigation-scalar-rect-trial, pending-layout-template-pixels.
Trial comparison/identity/installation/storage JSON, source overlays, unit log and native
reports/logs/captures retained. Focused runners in output/renderdoc-tools-2026-10-08.

All jobs terminal; runtime configuration restored; every owner guard2,938 files unchanged.
Focused source diff check clean. This-turn evidence+scratch144.75MiB; C117.96/D81.29GiB
free at final check. No new project imported assets observed in this turn's time window.
Windows currently reports9,728MiB allocated pagefile; previous allocation unknown, so do
not attribute free-space changes to the tests or modify system virtual-memory settings.
No full builds/copies, broad cache deletion or cleanup workaround.

## Next action
Target remaining measured local-template generation (~8ms combined) and larger renderer/
redraw costs, using same frozen real station plus corrected40 fixture. The pure rectangle
rewrite is rejected; do not relaunch it as an accepted fix. Keep navigation immediately
correct, preserve endpoint/graph/path decisions, and accept further changes with matched
workloads and relevant art/behavior checks. Inspect residual >50 frames.
Full frame gates, target hardware, cold/warm loading/startup peak, same-process lifetime/
endurance, original bugs, private provider regression/lifetime, final PC/Mac freeze and
actual M1/signing/notarization remain open. No release or minimum-hardware certification.
