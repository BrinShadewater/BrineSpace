# Project handoff

Updated: October 6, 2026 · BrineSpace · Palette ownership and combined-budget fix

## Objective and acceptance
Remove the station integration's duplicate storage/idle retention without changing
pixels, clocks, reference identity or live commands. Whole release acceptance open.

## Accepted decisions and constraints
Private copies only; normal source/art unchanged. Every run verifies scratch user
path and fingerprints owner non-log files: 2,936 unchanged. No release/admission.

## Current state
Generator `output/drone-coordinate-2026-10-06/prepare-ownership.py` retains separate
`ownership`, `ownership-eviction`, `ownership-budget` and matching station evidence.
Ordinary request/finish/texture access delegates to the existing normal drone cache.
Palette bank lookup is weak; cache entries, live commands and pins own resources.
Ordered group clears stale frame pins even with no drone draws. Idle indexed entries
older than two frames participate in pressure from the combined ordinary/private
budget. Recent entries survive; held consumer objects survive cache eviction.
Reinserting a live display records its actual indexed-plus-fallback metadata bytes.

## Verification
Initial weak/delegated version: 140 checks / 120 exact native complete-drone image
pairs pass, but paired station final memory still +91.933 MiB. Independent indexed
cache was below its own budget and retained unused South atlas. Preserved evidence.

Combined-budget version: 144 checks / 120 exact image pairs, zero failures/errors,
clean exit. Covers dry/current flooding/unknown materials, nearest/linear, cargo/
effects, transformed overlapping drones, weak-bank release, ordinary texture identity,
recent survival, idle eviction, held-reference survival and full fallback accounting
on reinsertion. Initial private type-inference parse failure retained with owner
fingerprint; fixed before successful evaluation.

One new matched 40-room station pair, same frozen fixture as preceding comparisons:
60 frames each idle/pan at 1/2/4x; 180 warm-up frames; 1080p, VSync disabled, native
Godot 4.7.2 Compatibility on RTX 4070 Ti. Six complete crew and drone state comparisons
equal, empty SafeImage failures, zero engine errors, clean exits.

Texture deltas candidate minus baseline: first four phases 0.000 MiB; South mining
idle/4x -91.817 MiB; final pan/4x +0.058 MiB. Final indexed cache empty, demonstrating
idle eviction under actual station pressure. End memory 3167.000 vs 3167.058 MiB.
First integration's +214.388 MiB regression removed; this is one selected-atlas
saving during active use, not a constant or all-station 92 MiB reduction.
Both final states exceed the provisional large-scene 3072 MiB budget.

p95 baseline 38.736–47.938 ms, candidate 38.530–49.447 ms; both fail 16.7 ms gate.
No frame-pacing gain proven. First phase render CPU means 10.417/10.412 ms, GPU
8.662/9.022 ms, draw-call means identical 4831.95. These counters overlap and are
not an additive breakdown. Slot callback CPU attribution remains incomplete.
Ready times 12.115/12.174 s do not establish cold/warm loading acceptance.

Artifacts: `station-ownership-budget/{reference,candidate,comparison,source-hashes,
owner}.json`, logs and retained screenshots; provider checks in `ownership-budget/`.
Screenshots from the earlier ownership run were inspected: frozen Main has mojibake
labels absent in current normal Main, and a synergy notification overlays part of
the station. Do not use this historical fixture as current UI/visual certification.
Matched snapshots support scoped behavior, not complete station raster equivalence.

## Next action
Refresh physical fixture from current normal source with explicit UTF-8 and audited
private crew/provider substitutions before broad visual or release acceptance.
Verify full exterior order with actual surrounding art and native scene lifetime;
measure additional atlas candidates and indexed upload/preparation attribution.
No admission until matched performance/appearance checks establish net benefit.
Other atlases, linear residency policy, lossless release encoding/hash validation,
three-run workloads, Windows/Mac packages and full original release gates remain.
