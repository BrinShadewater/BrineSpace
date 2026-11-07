# Absent crew preparation experiment

Updated: October 5, 2026 · BrineSpace · Diagnostic only

## Objective and acceptance

Measure whether an unrecovered actor can retain cryopod output while its other
images remain unallocated. Preserve frame identities, selected pixels, metadata,
filtering and gameplay deadlines. Do not enable missing-art fallbacks or delay
recovery to hide preparation time.

## Accepted decisions and constraints

Veld is the first measured actor, not a policy for the complete roster. Continue
must have required banks ready before checkpoint validation/restore. Legacy saves
treat the three human actors as present. Current startup builds the grid before
initializing the architect run, so checking `Architects.present` inside the grid
loader is insufficient to select required banks.

Unrecovered humans still use `idle-south` and `walk-south` in
`Architects.pod_for_display`. Separate fall/rise recovery art sometimes overrides
the returned texture, but these underlying calls still execute. Recovery art and
other UI/Studio consumers are outside this bank measurement.

## Current state

Output-only fixture in `output/absent-crew-preparation-2026-10-05/`: source-hashed
complete selected Veld loader, native probe, guarded runner, analysis, full logs
and two JSON results. No runtime or frozen-package changes this pass.

The optional branch retains all bank/frame objects and pending weak records,
materializes the two cryopod clips, then prepares remaining images in work slices
targeting 2 ms, separated by render boundaries with a 60 FPS cap. It uses the
existing raw-PNG loader and immutable texture pool. A single image operation is
indivisible, so 2 ms is a scheduling target, not a hard upper bound.

| Isolated Veld loader | Full | Pod-first |
|---|---:|---:|
| Initial unique images | 1,800 | 63 |
| Initial decoded storage | 365.35 MiB | 8.14 MiB |
| Initial engine texture-counter delta | 487.06 MiB | 11.09 MiB |
| Loader wall time | 2,734.839 ms | 252.684 ms |

These are single local runs, not cold/warm release loading benchmarks. The
475.97 MiB engine-counter difference is not a physical-VRAM measurement.
Final prepared banks return to exactly the same 1,800 images / 365.35 MiB and
engine counter as the full loader. Deferral does not solve full-roster memory.

Preparation requires **18,669.691 ms across 1,069 render slices**, including
2,531.629 ms of measured loader work. Slice p95/p99/max are
2.839/2.988/3.857 ms; maximum single operation is 2.735 ms. These are preparation
work times, not full gameplay frame times. The native fixture has no station work.

Human thawing lasts 7 simulation seconds; 4x speed with the 1.3x Warm Thaw upgrade
leaves about **1,346 ms**. Starting this scheduler when thawing begins is therefore
rejected. Repair start is not yet a proven alternative: repair progress can already
be near completion, and restored checkpoints can be arbitrarily close to release.
Neither a loading pause nor delayed recovery is authorized by this experiment.

## Verification

Two native runs, zero engine errors; all 2,936 owner non-log files unchanged in
both scratch-profile runs. In each run all 3,186 frame identities survive and
every final frame has storage and alpha bounds. All 42 sampled idle/walk source
pixel hashes, dimensions, metadata and filtering match between runs and before/
after deferred preparation. This is source-pixel/readback verification, not
cryopod compositing, moving visual review or actual Continue acceptance.

## Next action

Test bounded worker decoding plus small-image uploads using this same selected
bank and timing budget. Measure outstanding decoded bytes, main-thread work and
completion deadline, preserving source pixels and wrapper identities. Determine
required roster from startup/checkpoint data before admitting any runtime policy;
recovery and preview consumers need explicit coverage. If the deadline still
fails, retain full startup preparation rather than changing simulation timing.
Continue full-roster memory and packaged performance work separately.
