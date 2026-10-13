# Drone integration cold-loading attribution

Updated: October 7, 2026 · Project: BrineSpace · Task: performance/release readiness

## Objective and acceptance

Resolve exit warnings before admitting the lossless drone provider. Preserve responsive loading, normal crew/flood behavior, selected art and owner saves. The full original PC/Mac release gates remain open.

## Accepted decisions and constraints

Do not force-free reference-counted objects, hide warnings, upgrade the engine or replace normal gameplay with reduced test scope. Main-thread scene preparation below is diagnostic evidence; a ~3-second synchronous cold preparation is not accepted as responsive production loading.

## Current state

Private audit at `output/drone-ownership-2026-10-07/` records IDs and weak references for 280 objects: two sessions, two banks, 264 transient dust adapters, four crew/room texture pools and six crew players, plus callback script owners. All tracked runtime objects expire at settled title; two loaded callback **GDScript resources** remain alive as expected from preloads. None of four leaked RefCounted IDs matches the tracked runtime objects, including after normalizing signed IDs to unsigned engine log IDs. 140 functional lifetime checks pass, but four leaks/one warning remain. No direct provider-bank ownership leak established.

The 32-frame provider's otherwise identical two-cycle/no-Studio test with synchronous scene preparation passes **141 checks, zero leaks/warnings**. Preparation happens before title; this changes loading scope and is not a loading-performance acceptance result.

Native **load-only**, no scene instantiation/crew/drone texture jobs/gameplay:

| Preparation | Exit leaks | Warnings | Total diagnostic load time |
|---|---:|---:|---:|
| Cold threaded scene request | 17 | 1 | 2.910 s |
| Synchronous scene load | 0 | 0 | 2.917 s |
| Session/group/room-content scripts first, then threaded scene | 28 | 1 | 3.014 s |
| Grid script first, then threaded scene | 19 | 1 | 3.027 s |
| Main script first, then threaded scene | 0 | 0 | 2.941 s |

Evidence: `output/drone-combined-grace-2026-10-07/load-only.gd`, separate `*-load.log`, `load-only-results.json` and `load-preparation-results.json`. Cold provider helpers or grid preparation alone do not fix it. Preparing Main before the threaded boundary does. This reproduces the defect without running any gameplay and materially narrows it to cold script/scene loading. Counts depend on loading graph/order; no stable per-cycle growth or physical VRAM leak inferred.

An official [Godot issue](https://github.com/godotengine/godot/issues/122001) reports a similar zero-reference-count warning with threaded loading of inherited **C# resources**. That is a different language/backend case and does not establish our GDScript cause. No engine defect/fix-version claim or upgrade decision follows from it.

## Verification

All native subprocesses use isolated resolved user data and preserve all 2936 owner files. The previous 1516 exact dock/room pairs and matched cache comparisons retain their original scope; this attribution does not replace packaged gameplay, responsive loading measurements, animation/memory gates or endurance.

The synchronous-preparation version **with Studio** passes **143 checks, zero failures/leaks/warnings**, including New Game, Studio ownership, save/title/Continue, complete fleet/crew restoration and last-owner release. It uses normal crew and flood code. All subprocesses are terminal and owner fingerprints unchanged. Two small-fixture cycles are not the required large-station endurance test.

## Next action

Narrow cold Main loading further with a minimal script/load reproduction or verify compiled candidate scripts in an actual debug=false package before selecting a remedy. Preserve the responsive loading display; do not admit whole-scene synchronous preparation solely because exit warnings disappear. Finish provider/build/source verification and refresh packaged measurements, then optimize remaining sustained room/rendering cost. Original bug/UI/endurance/hardware/Mac gates remain open; no upload.
