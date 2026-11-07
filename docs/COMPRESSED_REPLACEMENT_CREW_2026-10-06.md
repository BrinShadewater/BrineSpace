# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: replacement-crew memory prototype

## Objective and acceptance
Reduce retained animation texture storage without changing selected pixels,
timing, frame identity, equipment or gameplay. This advances the approved PC/Mac
release plan; it does not certify a release or enable a new normal backend.

## Accepted decisions and constraints
Use immutable lossless compressed source images and separately owned bounded GPU
presentation leases. Keep James's specialized water/cargo/bridge player inheritance.
Bill and its historical save bindings remain unchanged. Preserve runtime PNG loading,
owner layouts, default visual quality and ordinary gameplay. Tests use isolated profiles.

## Current state
Private prototype/evidence: `output/compressed-crew-2026-10-06/`.
Extends the validated Veld prototype to current James/Branforth and Marsh declarations.
`station-prepare.py` derives physical diagnostic Main/Grid copies from current source;
no normal runtime source or selected artwork changed in this milestone. A single shared
presentation router owns all three replacement banks. The dedicated `busy/` fixture
uses normal architect release at the core to activate James and Marsh alongside Veld,
with fixed decision seeds, 40 rooms, active production and drones. Free construction
and failure suppression remain fixture-only.

## Verification
James: 52,544 native storage/presentation checks, 17,484 exact image pairs plus
33 overflow pairs; 167,285 consumer checks, 970 clips, 11,652 frame references.
Marsh: 5,462 native checks, 1,788 exact image pairs plus 33 overflow pairs;
20,136 consumer checks, 228 clips, 1,190 frame references. Zero failures in the
completed runs. Consumer replay covers 30/60/120 FPS, 1x/2x/4x, pause and snapshot
restore; Veld-specific reading interruption coverage remains in its earlier probe.
Preserve the failed Marsh fixture evidence: it incorrectly assumed helmet equipment;
the corrected fixture enumerates actual equipment banks. No art/bank fix was needed.

One native 1080p combined-bank pair with only Veld active: textures
3,903.21 -> 2,548.41 MiB; all 15 nonempty crew/world phase comparisons match.
One stronger native pair with all three replacement crew active:

| Measurement | Normal reference | Prototype |
|---|---:|---:|
| End texture memory | 3,970.52 MiB | 2,619.40 MiB |
| Peak Windows working set | 1,583.46 MiB | 1,725.30 MiB |
| Peak private commit | 5,851.00 MiB | 4,500.57 MiB |
| Initial gameplay readiness | 12,903.83 ms | 15,921.14 ms |
| Median of 15 phase mean frame times | 36.216 ms | 36.292 ms |
| Maximum measured frame | 88.893 ms | 91.153 ms |

All 15 busy phase comparisons match recorded crew positions/state/direction/stage/
timer, powered rooms, drone phases, action and speed. All three actors remain active
in every recorded phase. This is not a full needs/path/RNG or cargo-interruption proof.
477 distinct private frames, 3,246 route resolutions, zero missing routes, four
base GPU slots and 26 live spills at end. Lossless bank payload is 98,326,303 bytes;
raw-equivalent bytes are not retained decoded RAM. No runtime art errors or engine
errors; clean exits. All 2,936 owner non-log fingerprints unchanged.

The initial 3 GiB large-scene texture budget passes in these two specific fixtures;
three repeated runs, full roster including Bill/companions, 12-room 2 GiB gate,
M1 unified memory, packaged release and endurance remain unverified. Frame and
loading gates fail. Peak working set increases despite lower textures/private commit;
do not add these counters together or infer a Mac memory result.

## Next action
Preferred follow-up prototype: `output/compressed-crew-2026-10-06/bounds-cache/`.
Inspection found the first compressed batch decoded an immutable image to rescan
alpha bounds for every surviving frame reference. This variant keeps the used rect
once per immutable source; wrapper pivot/density/filter metadata remain separate.
Instrumented uncached/cached variants otherwise use identical code and the same busy
fixture; cached ran first in this matched pair.

| Follow-up loading measurement | Uncached | Cached |
|---|---:|---:|
| Bounds scans | 12,434 | 5,834 |
| Bounds work | 1,897.662 ms | 572.163 ms |
| Compression work | 1,257.889 ms | 1,262.461 ms |
| PNG loading work | 6,144.156 ms | 6,265.372 ms |
| Initial gameplay readiness | 15,762.559 ms | 14,541.034 ms |

Both retain exactly 2,619.398 MiB texture memory. Full actor snapshots now compare
equal in all 15 phases, including needs, paths, goals and decision RNG state.
Per-actor presentation coverage: Veld 130, James 286, Marsh 61 distinct frame
objects; zero missing routes. Median phase means 36.973→36.905 ms is not an
established FPS gain. Cached peak working set 1,720.871 MiB versus uncached
1,731.625 MiB; private commit 4,529.855 versus 4,518.516 MiB. One pair is not
a repeatability or release-gate certificate.

Cached variant additionally passes Marsh's 5,462 native presentation checks and
all three complete selected-bank consumer checks: Veld 48,579, James 167,285,
Marsh 20,136; zero failures. These compare every frame's pixels, metadata (including
alpha extent), filtering and boundaries, plus clock/snapshot replay. The Veld count
excludes its previously verified reading-specific actor fixture, unchanged here.
All runs cleanly exit and preserve all 2,936 owner non-log fingerprints.
This fixes verified redundant startup work in the private prototype; normal runtime
remains unchanged. PNG loading (~6.2 s) and compression (~1.26 s) now have explicit
timings to guide the next loading change; do not assume either can disappear safely.

Repeat the preferred busy matched pair with stable selected inputs. Test combined
router ownership across ten title/Continue transitions, including spill plateau/release.
Follow-up ten-transition ownership/save lane is now complete for its four-room
fixture: candidate 826 and normal 296 checks pass; old resources release and settled
title textures match exactly. Simultaneous-spill endurance remains untested there.
Current candidate warns only when Studio is included; this normal control exits
cleanly. See `REPLACEMENT_CREW_LIFETIME_2026-10-06.md`; do not waive the warning using
the earlier Veld-only normal-reference result. Private backend admission stays open.
Resolve startup compression cost before normal admission. Preserve James cargo/water
transition coverage and Bill historical identity checks. The earlier anonymous exit
warning reproduced in ordinary lifecycle reference remains open independently.
Large rover uploads, sustained frame budget, original bug closure, two-hour soak and
actual Windows/Mac packaged certification remain release work.
