# Drone residency and reload trace

Updated: October 5, 2026 · BrineSpace · Diagnostic only

## Objective and acceptance

Distinguish acquired/pinned drone storage from submitted atlas draws, then measure
the cost of reloading unchanged images. Do not enable eviction that creates missing
art, changes timing or substitutes memory savings for new stalls.

## Accepted decisions and constraints

Use an output-only copy of the current drone renderer, with per-path notes added
at texture acquisition and atlas submission after invisible-frame checks. Preserve
original images, UVs and behavior. Three mining directions plus a south collection
animation approximate the major layers found in the earlier station inventory;
this is an isolated fixture, not a replay or certification of that station.

## Current state

Evidence in `output/drone-residency-trace-2026-10-05/`: generator, source hash,
instrumented renderer, native fixture/runners, trace JSON, synchronous and worker
reload results, release counters and owner checks.

Across 180 authored animation samples (30 Hz animation time, 60 FPS render cap):

| Measure | Result |
|---|---:|
| Decoded cache storage | 1,148.438 MiB |
| Acquired storage each sample | 1,148.438 MiB |
| Storage referenced by submitted atlas commands, samples 0–44 and 135–179 | 735 MiB |
| Storage referenced by submitted atlas commands, samples 45–134 | 1,148.438 MiB |
| Canvas-pinned paths | 12 |
| Uploads during traced animation | 0 |

These are sums of unique referenced texture storage, not bytes transferred or
pixels drawn per frame. The 413.438 MiB difference is three effect sheets with
temporarily empty cells. A wholly transparent one-pixel placeholder is also
acquired but never submitted. The actual renderer pins sheets before skipping
empty cells, preserving readiness when visible effects resume.

Destroying the fixture canvas (thereby releasing retained commands/pins) and
detaching those three sheets expires all three texture objects. Engine texture
accounting drops by 578,026,932 bytes (~551.25 MiB), versus 413.438 MiB decoded
storage. Do not conflate these measures or call the engine counter physical VRAM.

### Original-sheet reload cost

Warm-file results, one reload per direction; no gameplay work in the fixture:

| Direction | Synchronous decode/scan/upload | Worker wait wall time | Main-thread finish after worker | Finish call to render boundary |
|---|---:|---:|---:|---:|
| North | 110.876 ms | 99.995 ms | 19.592 ms | 24.239 ms |
| East | 106.353 ms | 92.348 ms | 15.282 ms | 20.509 ms |
| South | 105.466 ms | 96.124 ms | 12.610 ms | 20.701 ms |

The worker path uses the actual request_texture/finish_texture functions. Upload
calls account for almost all its measured main-thread finish time. Worker wait
includes scheduling and render-frame observation; it is not isolated decode CPU
time. Render-boundary intervals include pacing and are not isolated GPU timings.
Unrelated resident textures were marked used in this diagnostic to prevent the
soft cache limit from changing the tested set during uploads.

Decision: **do not ship active effect-sheet eviction**. The normal async path still
has a full-image main-thread operation comparable to or exceeding a 60 FPS frame
budget before other game work. The synchronous fallback exceeds the 100 ms stall
gate here. These runs disprove the assumption that worker decoding alone makes
reloading the original huge sheets harmless; they do not prove every possible
storage mechanism impossible. Earlier pixel-failing atlas remaps remain rejected.

## Verification

Three successful native runs: acquisition/submission trace, synchronous release/
reload, and worker-decode release/reload. Zero engine errors. All 2,936 owner
non-log files unchanged in each run. No runtime or frozen-package changes this
pass; the previous transparent pending-job cleanup fix remains intact.
No new visual-parity claim: source instrumentation only observes path use; these
are memory/timing diagnostics, not replacement-renderer acceptance tests.

## Next action

Investigate startup ownership of animation banks for absent/unrecovered crew.
`_load_replacement_crew_animations` currently loops all replacement actors. Establish
first-use requirements and recovery/restore preparation windows before deferring
any bank; required crew must still be complete before gameplay. This may avoid
loading unused storage without cycling huge active drone images, but its real
scope and saving are unmeasured. Full-roster large scenes will still require a
separate memory remedy. Continue pixel-preserving draw optimizations independently.
