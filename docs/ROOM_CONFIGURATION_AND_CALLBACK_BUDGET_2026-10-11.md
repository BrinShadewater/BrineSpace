# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: configuration attribution and broader draw budget

## Objective and acceptance

Continue full PC/Mac performance/release plan. Pursue material frame savings while
preserving selected art, owner layouts, animation, gameplay and cache ownership.
Previous turn was progress: shadow stage attribution narrowed costs and prevented
repeating a rejected shortcut. No new production change accepted here.

## Accepted decisions and constraints

Muted secondary native debug=false executable; isolated profiles and owner
fingerprints; shared runtime and small overlays. No screenshot batches/runtime
copies. Existing accepted crew/zoom/Solar changes preserved. Original full release
gates remain open; no target hardware or Mac certification.

## Current state

Private grid times configure_embedded separately from strip_retired by room type.
Private Research variant tests Solar's existing mutation-checked, owned rotation
working-copy approach. **Do not install the Research variant:** pilot benefit is
too small to justify another retained working set or broader repeated benchmarks.
Production Research source unchanged; no maintained tests/UIDs changed.

Private whole-grid callback probe measures all callbacks already included in
take_draw_timing: grid, surface, walls, doors, seabed, life and environment passes.
Eight-frame bounded metadata ring; drawing inputs/commands unchanged.
Runners under output/renderdoc-tools-2026-10-08:
run-room-configuration-attribution.py, verify-research-working-copies.py,
run-research-working-copy-pilot.py, analyze-research-working-copy-pilot.py,
run-grid-callback-attribution.py.

## Verification

Configuration profile: two large native traces/3240frames, nine full states/cameras
and fifteen successful paired lighting/placement/demolition events exact at1x/2x/4x.
Structural floor configuration1.378–1.821ms, first filtering.517–.576ms. Solar
configure.589–.889ms, Research.332–.429ms aggregate across their rooms. Existing
rotation/edge caches observed in source; no broad replacement justified.

Research native visual/state fixture: reference and candidate each440checks/zero
failures with defaults, then each440/zero with copied owner layouts. Four rotations,
four render passes, power/clock, five layout edit modes, mutation recovery and
same-quarter deletion; exact pixels/props/profile/edges, four-entry bound and Studio
invalidation. Original no-retention oracle retained. First fixture attempt failed
on missing packaged test helper and incorrect static Script API; corrected copied
mute/display helper and explicit Script cast. Failed log retained and excluded.
Images compared in memory; no screenshot files.

Six native pilot runs/9720frames across large/current/reported, one matched pair
per map. All27 full phase states/cameras and45 successful paired events exact.
Runtime source guards verified ordinary/trial source. No errors/missing art.

| Metric | Large before→trial | Current before→trial | Reported before→trial |
|---|---:|---:|---:|
| Mean ms |24.480→24.546|11.759→11.731|12.366→12.375|
| p95 ms |40.431→40.628|16.843→16.941|17.735→17.766|
| p99 ms |50.546→51.140|26.930→28.261|20.630→20.761|
| >50 frames |19→20|0→0|2→2|
| >100 frames |0→0|0→0|0→0|
| Research configure sampled mean us |39.895→36.115|0→0|25.376→25.107|

Texture peaks unchanged3028.476/1940.818/1559.522MiB. Large local saving only
3.780us/sample; reported.269us. Current does not exercise this path. No useful
whole-frame benefit proven; p95/p99 worse on every map in this pilot. One pair is
not evidence of a reproducible regression, but insufficient to justify admission
or expanding this small trial. Keep private and move to larger measured costs.

Uninstrumented large pilot frame scopes: lighting mean27.232ms, placement22.997,
demolition23.212. Placement/demolition grid draw~9.7–9.8ms, simulation~2.4ms,
render-signal interval~6.6ms. Viewport timings and script/child counters have
different/overlapping scopes: do not add them into a claimed complete frame budget.

Whole-grid probe: two native large runs/3240frames; nine full states/cameras and
fifteen successful events exact. **Every frame's callback sum equals the original
grid_draw_usec counter exactly (maximum difference0us)**, validating attribution.

| Callback average ms | Lighting | Placement | Demolition |
|---|---:|---:|---:|
| Live surface |3.206|3.298|3.202|
| Grid |2.750|2.647|2.607|
| Exterior actors |1.231|1.593|1.631|
| Foreground surface |1.287|1.251|1.283|
| Floor + floor-rest |3.190|.088|.062|

Foreground includes selection, legacy door foregrounds, Moonbay exterior and
human rendering. Exterior actor layer includes environment foreground and survey
probe art. Live surface includes room setup, retained-content updates and large
room synchronization. Callback totals are attribution, not FPS gains. Source
inspection identifies those entry points; no quality/rendering branches changed.

All owner guards2938 unchanged; all jobs terminal/override restored. Completed
JSON reports NTFS-compressed with exact before/after hashes; no owner/runtime
compression/deletion. No large copies or capture batches. Evidence under
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/{
room-configuration-attribution,research-working-copy-trial,
research-working-copy-pilot,grid-callback-attribution}/.

## Next action

Target recurring live-surface3.2ms: separate actor/room eligibility checks, frame-key
construction, room submission and large-room synchronization. A paint-local actor
room lookup may avoid repeated actor projections, but measure its cost first and
preserve visibility/animation state. Prioritize recurring costs over further tiny
rotation/filter changes. Full performance, memory/loading, endurance, bugs/UI,
packaged Windows/M1 and signing gates remain open.
