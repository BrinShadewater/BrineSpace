# Project handoff — drone storage sharing on station maps

Updated: October 10, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance
Verify the proposed identical-sheet sharing on the owner's saved 12-room station
and the deterministic 40-room expansion. Accept only a measured benefit with
unchanged art/gameplay and bounded session ownership; release gates still apply.

## Accepted decisions and constraints
Muted native window on secondary landscape display, isolated APPDATA with resolved
user-directory guards. Reuse debug=false Windows runtime and small source-overlay
PCKs; no full package copies. Preserve all existing accepted source optimizations.

## Current state
Private candidate maps six whole PNG paths to byte-equal canonical sources, checking
current bytes once per pair/session. Logical manifests/frame records remain unchanged;
cache and worker keys count unique storage. Final session release clears six decisions.
**Not installed:** no useful peak-memory or average frame-time improvement here.
Runtime source files remain unchanged by this experiment. Added three focused runner
scripts under output/renderdoc-tools-2026-10-08; evidence lives in
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/drone-storage-sharing-*.

## Verification
Windows RTX 4070 Ti, 1080p, actual debug=false runtime, uncapped. Three alternating
reference/candidate pairs per station; idle, continuous pan, lighting at 1x/2x/4x.
810 measured frames per run, 9,720 total. Reference includes all accepted prior fixes.
This compares this candidate, not total improvement over the original game.

| Map / lane | Mean ms | p95 ms | p99 ms | Max ms | >50 / >100 ms | Texture peak MiB |
|---|---:|---:|---:|---:|---:|---:|
| Saved 12 reference | 15.024 | 20.646 | 22.448 | 25.404 | 0 / 0 | 1558.411 |
| Saved 12 candidate | 14.985 | 21.042 | 23.680 | 28.998 | 0 / 0 | 1558.411 |
| Expanded 40 reference | 27.739 | 44.340 | 53.957 | 115.115 | 45 / 3 | 3027.507 |
| Expanded 40 candidate | 27.833 | 44.055 | 53.009 | 105.547 | 38 / 3 | 3027.507 |

Saved mean difference 0.26%, mixed pairs; large mean 0.34% worse, two of three pairs
worse. Tail improvements insufficient: three >100 ms frames in each large lane.
No peak-memory headroom gained. Observed unique upload events in large trace fall
410 to 399 (18,938,491,644 to 18,408,633,084 bytes). These deduplicate events exposed
by sampled diagnostics, including latest prior events; not a complete session decode
or GPU-residency inventory. Sharing engaged but does not address concurrent peak.

All 54 phase pairs match gameplay state outside historical cached playback observations.
52 full snapshots exact; two large final-4x-lighting snapshots differ only in Branforth
cached last_time/phase/last_position/motion.started. Same category as previous controls;
not silently normalized and not a new certification of all animation timing.

Native equivalence/lifetime V2: 40 checks, zero failures. All six real GPU sheets match
source pixels, dimensions, format and mipmaps exactly; alias texture identity and unique
bookkeeping preserved, no redundant upload, changed counterpart falls back, final-owner
release clears lookups/resources. Initial fixture attempted to mutate a read-only const
map (39 checks passed, one invalid fixture failure); corrected using a separate scratch
script with a different counterpart, without altering assets or measured candidate.

All jobs terminal and override.cfg restored. All three owner guards: 2,938 files
unchanged. Evidence 43.66 MiB plus 37.14 MiB scratch = 80.80 MiB, no full PCK copies.
C:126.92 / D:78.63 GiB free, 20 GiB refusal threshold enforced. No cleanup-policy retry.

## Next action
Do not assume equal sheets coexist at the memory peak. Attribute peak ownership by
current drone layers and retained canvas pins, then test a bounded lifecycle or upload
ordering remedy against the same maps. Preserve complete visible drones, clocks and
quality; do not repeat rejected prewarm, grace, larger-cache or crop trials unchanged.
Large-station redraw/upload bursts remain the useful frame-pacing target.
Both maps fail p95 <=16.7 ms; large also fails p99 <=25 ms and stall gates.
Loading/endurance/original bugs/new final PC/Mac freeze and native M1 certification,
signing/notarization remain open. No itch.io publication.
