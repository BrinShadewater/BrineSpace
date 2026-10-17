# Live-object lifetime investigation — October 16, 2026

The preserved release is `brinespace-b0b5d1b031c6ec29` under
`D:/bs-release-qa-20261016/`. Its two-hour normal 4× soak showed continued
ObjectDB growth with stable textures and Node counts. Current investigation and
private validation artifacts live under `D:/bs-object-growth-20261016/`;
reproducible external helpers are `output/object-growth-20261016/`.

## Baseline lifetime evidence

Two fresh-process observer modes each ran two 180-second episodes from the same
12-room checkpoint, using actual Continue, 4× speed, Resume, Return and Quit
handlers. All measured flags were zero, both old gameplay Nodes were freed, no
engine/script errors or placeholder images, all 2,948 owner files unchanged.

| Observer | Episode live objects | Returned title objects |
|---|---|---|
| Minimal; no frame arrays/deep soak history | 32,145→32,740; 32,150→32,745 | 2,353 both |
| Full recorder plus read-only router census | 32,147→32,760; 32,151→32,764 | 2,354 both |

Minimal/full modes pass 47/49 checks. Full mode adds a diagnostic script, so its absolute
title baseline differs. The first title warms 1,972→2,354; subsequent returns are
identical. No accumulating station-scene retention across these entries.
Cached resources stay 465 during play; processed Tweens stay zero. Cached-resource
count does **not** include every procedural Resource. Release orphan/static-memory
counter zeros are unavailable, not acceptance evidence.

The active crew texture router subscribes to every CanvasItem addition and stores
a WeakRef indexed by canvas RID. It originally removed none until station exit.
Spatial AudioStreamPlayer2D voices and replaced UI therefore left live WeakRef
Objects after their targets were freed. The full-observer census confirms expired
canvas references 89→363 and 89→365; from 60–180 seconds this grows 151/152, about
75–76 per minute. Source-frame count remains 16,432, pose cache reaches 128 slots,
spills stay zero. Early total object growth also includes normal cache warmup;
do not attribute every startup allocation to the stale registry.

## Narrow source change and regression evidence

`scripts/crew_storage/router.gd` now subscribes to SceneTree.node_removed, removes
the departing canvas's WeakRef/epoch/draw callback records, and disconnects the
subscription on session close. Re-entry registers and tracks the canvas again.
The presenter's existing tree_exited lease cleanup remains unchanged. Three
fixed-size registry counts join its existing diagnostic snapshot. No art,
animation, actor simulation, texture pixels, cache budgets or renderer changes.

- New lifetime regression failed as expected before the fix: 12 checks, 5 failures.
  Afterward: 13 checks, zero failures, including 128 retired spatial voices and
  live owner removal/re-entry/closure.
- Native router pixel regression: 12 checks, zero failures. Exact viewport bytes
  survive keep-global reparenting between scaled parents and removal/re-entry;
  another owner's existing lease and pixels survive without redrawing it.
- Existing native pose-cache regression: 18 checks, zero failures.
- Existing performance-monitor and normal/detached crew-loader tests pass.
- New pixel fixture needed an explicit native-lane override and correction of a
  fixture-only Viewport property (`world_2d`); the corrected real-display run passes.
- Independent read-only review found no source correctness issue. Its retained-peer
  fixture coverage concern was addressed before the successful native run.

Both new scripts have engine-generated paired UIDs; tests/index.json includes them
in performance diagnostics and classifies the pixel test as native. Existing
unrelated dirty workspace changes are preserved.

## Private release validation

Build **brinespace-e54e8a0eb8d58f65** exported successfully with the maintained
Windows exporter from a physical copy of the preserved selection plus the router
delta. All 36,430 runtime paths remain identical; only router.gd changes bytes.
Exact asset audit: 35,942 entries, zero missing/changed/unexpected. Packed-source
audit: 431 selected +421 frozen extra scripts, zero unexpected/failures; build
metadata exact. Original Windows/Mac deliveries remain the preserved b0b5 build.

- EXE SHA256: `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`
- PCK SHA256: `880bac9f98d153ad583217ad2fb9ae41c937711d9297fcfb3280426371b3ea4c`
- Source SHA256: `e54e8a0eb8d58f6578cca3d4753e72405cd93edc4af93e55261893bbd992de97`

The unchanged full observer plus read-only router census ran **600.014705 seconds /
35,975 frames / 36 checks pass** on the actual release, normal 12-room station at
4×. Its additional progress print reports counters every30 seconds; no pruning,
reset, actor edit, manual simulation, free building or disabled failures.

**Zero expired canvas or tracked-owner references across all 121 censuses.** Total
objects warm 32,057→32,535. During the last three minutes they fluctuate
**32,527–32,547**, median 32,537 (first 32,527, last 32,535), replacing the sustained
stale-reference growth. Source frames remain 16,432, presenter cache 128 slots /
17,334,272 bytes, zero spills and zero missing texture routes. The old gameplay
Node is freed; title returns to 2,354 objects, matching the warmed baseline.

All 35,975 interval flags zero. Mean 16.679 ms / 59.957 FPS, p95/p99 16.764/17.248 ms,
max 36.998 ms, zero frames ≥50/100/400 ms. This is the VSync-limited **12-room**
workload, not evidence of 60 FPS on the 40-room station. Active Branforth, Margot and
River remain alive, with 118/115/120 moved observations and 83/66/67 goal changes.
No engine/script errors or placeholder images; normal Save/Return/writer-idle/
title Quit succeeds. The OS-memory cost of observer retention was not remeasured;
do not turn stable late ObjectDB counts into a general RAM-leak acceptance.

The narrow stale-registry defect is fixed and validated. A full two-hour re-soak,
40-room performance/placement checks and refreshed matching Mac ZIP/native Mac
validation remain separate release gates. No whole-game behavior equivalence,
whole-game visual acceptance or public release approval is claimed here.

## Final preservation and storage checks

All 2,948 player files match the task's initial fingerprints. Both original
Windows/Mac SHA256SUMS verify all 11 entries; the private candidate's five-file
identity also verifies. The private source index matches all 60,460 HEAD entries.
Only four task-owned duplicate QA EXE/PCK files were removed after normal process
exit and exact canonical hash checks, recovering **6.963 GiB**. Free space:
**C: 103.966 GiB / D: 98.658 GiB**. No source/art/history/owner data removed.

Adapters and identities remain in runtime/ and runtime-fixed/; canonical packages
remain in their candidate directories. `runtime-binary-restoration.json` maps the
four copies. The run helper reconstructs missing physical binaries on demand;
`python output/object-growth-20261016/finalize.py restore` explicitly restores both.
Final evidence: analysis.json, final-verification.json, fixed-manifest-comparison.json,
fixed-packed-sources.json and each run's launch/process/owner guard records.
