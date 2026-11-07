# Empty-effect gameplay comparison and nested memory audit

Updated: October 5, 2026 · BrineSpace release readiness

## Objective and acceptance

Measure the accepted transparent mining-effect draw omission in gameplay and
finish the bounded audit of nested seabed and room-wall texture storage. Preserve
selected visuals and report failed gates without implying release certification.

## Accepted decisions and constraints

Three alternating developer-native runs per path, 40 rooms, 1080p, 180 measured
idle frames at each of 1×/2×/4×. Reference removes only `emptyFrameRanges` from the
in-memory mining catalog; it does not edit the manifest or selected art on disk.
Run order: reference, candidate, candidate, reference, reference, candidate.
No overlapping native tests. Scratch profiles, copied checkpoint and owner layouts.
This is current source, not an actual packaged release or fully frozen source set.

## Current state

Median p95 across three runs per path:

| Speed | Reference ms | Candidate ms | Change | Mean draw calls, reference → candidate |
|---|---:|---:|---:|---:|
| 1× | 40.861 | 44.473 | +8.8% | 5,502.8 → 5,502.3 |
| 2× | 53.371 | 50.013 | −6.3% | 5,490.4 → 5,489.7 |
| 4× | 53.226 | 55.657 | +4.6% | 5,539.1 → 5,537.3 |

**No consistent frame-time improvement.** The change remains a pixel-verified
removal of invisible draw work, not an established gameplay FPS optimization.
Differences are not sufficient to attribute the slower runs to this small change.
All nine candidate phases fail the frame gate. Candidate worst frame reaches
967.872 ms. Median engine texture totals match between paths at every phase:
4,465.61 / 4,771.86 / 4,098.26 MiB. These phase-dependent totals must not be compared
as savings against the earlier shorter inventory ending at 5,139.36 MiB.

The nested audit adds 52 seabed images totaling 111.03 MiB base storage and three
foundation images totaling 18 MiB. Cached format metadata distinguishes RGB8 from
RGBA8, avoiding earlier RGBA-only overestimates for library/floor assets. Base
storage excludes mipmaps/driver overhead and is not certified GPU residency.

An initial room-tree scan hit its 512-node cap and is incomplete. Replacing it with
the four existing room-view registries visits 14 views without creating new ones
or calling lazy getters. Nine own full-wall pools; all nine have audit enabled,
**zero requests and zero upload records** in this fixture. They add no observed
wall-pool storage here. This is not a claim about every room/layout in the game.
Explicit collection covers ~49,254 values in ~40 ms after measured phases, with
no value/registry cap reached. No unbounded reflective scan or GPU readback.

Evidence/helpers remain under `output/pool-inventory-2026-10-05/`:
`empty-pairs/comparison.json`, `nested-registry-summary.json`, and
`wall-coverage/large-1920x1080-1.json`. This milestone changes no production runtime
or art beyond the already accepted empty-frame change; no new export or upload.

## Verification

All six timing runs and the audit runs complete without engine errors. Every run
preserves 2,936 owner non-log files. Compared fixture/runtime diagnostic files,
mining manifest, checkpoint and four effect sheets retain their hashes. This
scoped input check does not certify unrelated working-source art as frozen.
Earlier 720-cell alpha and 48/48 native exact-pixel checks retain their original
scope; no new visual behavior was introduced in this measurement turn.

## Next action

Stop treating transparent draws as a solution to the frame budget. Profile the
larger render batches/passes: this workload still submits roughly 5,500 draws per
frame, and the first reference's 1× sample reports ~11.7 ms render CPU and ~10 ms
render GPU. Those timings can overlap and must not simply be added. Use controlled
diagnostic isolation to attribute work before changing rendering or selected quality.
Active drone storage and exact sampling-compatible reuse remain unresolved. Windows
kernel scheduling trace still requires elevation; Mac native testing/signing and
all remaining release gates stay open. Release remains blocked.
