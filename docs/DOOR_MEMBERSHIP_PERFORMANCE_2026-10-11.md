# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: live-room attribution and door membership allocation cleanup

## Objective and acceptance

Continue full performance/release plan with exact behavior and selected quality.
Reduce measured unnecessary allocations, then pursue larger recurring draw costs.
Prior turn was progress: full callback accounting redirected work away from the
unhelpful Research trial. Full PC/Mac release gates remain open.

## Accepted decisions and constraints

Muted secondary native debug=false, isolated APPDATA/profile, owner fingerprints,
20GiB storage floor. Reuse runtime; no screenshots/full copies. Preserve public
mutable door-list ownership, ports/branches/rotations, animation and owner layouts.
No actor-presence or rendering-connection cache admitted in this pass.

## Current state

Installed scripts/main.gd _room_has_door boolean helper. Membership callers in
_ports_connect and the sentinel-cell fallback of _placed_rooms_connected no longer
request a copied door list just to call has(). Existing room_door_cache and keys
remain unchanged. Cold queries use original _room_doors; public get_room_doors and
_room_doors still return owned copies. No new cache/resources/invalidation policy.
Installed canonical SHA256:
6e2a013f1cd85cf2a5adb82b9454207e8ae437ee611144d9242896961832bbca.
Existing Main UID preserved; grid/Bill/Solar source unchanged.

Added tests/test_door_membership.gd plus engine-generated paired UID
uid://dmmaf8l5tjgyp and tests/index.json registration beside test_room_footprint.
Checks cover cold/warm results, unchanged cache values, caller list mutation,
all room definitions, rotations including aliases/negative values, invalid sides,
unknown room fallback, branch separation and multi-cell ports against the original
connection implementation. The maintained test counts failures explicitly.

## Verification

Live-room private profile: two native large traces/3240frames, nine full phase
states/cameras and fifteen successful paired events exact. Nested eligibility
includes actor presence; counters are not additive with total surface/frame time.

| Recurring scope | Mean ms range |
|---|---:|
| Actor presence |.147–.149|
| Eligibility including actor presence |.297–.303|
| Frame key construction |.180–.183|
| Retained animation advance |.362–.371|
| Large room sync |.008–.009|
| Wet equipment hide |.002|

Actor checks run~37–38 times/frame but are not large enough to justify a new
actor-room lookup yet. Uninstrumented door preparation averages1.076–1.082ms
during placement/demolition and1.408ms lighting, motivating allocation inspection.
Frozen replay Main differs from canonical only by two existing test-only paused
toast tweens. The candidate preserves those pauses; no unrelated source drift.

Native debug=false/headless membership oracle passed20256checks/zero failures.
Initial oracle failed type inference for two strings called through untyped game;
corrected explicit types, retained failed log and excluded it. Fresh installed
maintained-source adapter passed20256/zero; no render or full-game certification
is implied by headless checks.

Eighteen native gameplay runs/29160frames, three alternating pairs each on large40,
current10 and reported12. All81 full phase states/cameras and135 successful paired
lighting/connected placement/demolition events exact at1x/2x/4x. Runtime source,
deterministic warning-clock, mute/display/input and missing-art guards pass.
Tested RTX4070Ti1080p, not target GTX1650/M1. Fixture builds/failure rules remain
fixture-only. No cold/warm, normal title/Continue or physical-input certification.

| Metric | Large before→installed | Current before→installed | Reported before→installed |
|---|---:|---:|---:|
| Whole mean ms |25.413→25.243|11.996→11.999|12.674→12.622|
| p95 ms |42.592→42.649|17.415→17.561|18.382→18.556|
| p99 ms |54.018→53.774|28.641→28.866|21.550→21.443|
| Maximum ms |94.092→93.562|49.826→49.736|53.649→55.555|
| >50 frames |78→69|0→0|6→8|
| >100 frames |0→0|0→0|0→0|
| Door setup sampled mean us |1186.106→1128.274|354.693→347.509|390.118→380.428|

Local door preparation improves4.88% large/2.03% current/2.48% reported; all nine
pair means improve. Whole means large improve0.67% and reported0.41%, every pair
better; current effectively neutral+0.027%, mixed pairs. Slower-frame results mixed:
all p95 slightly worse, current p99 worse, reported max/>50 worse. Accept a small
equivalent allocation cleanup, not a stutter cure or broad FPS certification.
All maps still fail p95; large/current fail p99. Texture peaks unchanged
3028.476/1940.818/1559.522MiB. No new retained metadata or GPU storage.

Owner2938 files unchanged in all guards. All jobs terminal/runtime override restored.
Completed live traces11919858→5464064bytes allocated; eighteen gameplay traces
59965921→22839296bytes. Every content hash verified before/after compression.
No owner/runtime compression/deletion, captures or full runtime copies.
FreeC134.82/D68.56GiB. git diff whitespace/index JSON checks pass.

Evidence under D:/bs-release-crew-cache-20261009/benchmark-input-isolation/
live-room-attribution/analysis.json; door-membership-trial/{parity.gd,
installed-maintained.log,installed-owner.json,candidate-main.gd};
door-membership-pilot/comparison.json, eighteen traces, identities and owner.json.
Runners/analyzers under output/renderdoc-tools-2026-10-08:
*live-room-attribution.py, *door-membership*.py.

## Next action

Investigate repeated render connection queries as the next larger door/live-surface
cost. Any reuse must be paint-local, bypass preview/noncanonical rooms and keep
physics/input querying current data. Prove reciprocal connection semantics and
scope cleanup/invalidation before implementing; do not introduce a permanent
topology cache or combine it with this admitted cleanup without separate evidence.
Continue larger grid/exterior/foreground costs and all original release gates.
