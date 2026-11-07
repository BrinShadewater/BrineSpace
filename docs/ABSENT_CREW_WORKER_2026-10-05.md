# Absent crew worker preparation

Updated: October 5, 2026 · BrineSpace · Diagnostic only

## Objective and acceptance

Test whether bounded background work can make the pod-first Veld bank ready
without missed recovery deadlines, pixel changes or unbounded decoded storage.
Continue the same selected-bank experiment from
[the preceding measurement](ABSENT_CREW_PREPARATION_2026-10-05.md).

## Accepted decisions and constraints

Do not enable recovery-triggered whole-bank deferral: all tested variants exceed
the approximately 1.346-second human thaw window at 4x with Warm Thaw. Preparation
must not delay recovery or consume a larger gameplay frame allowance to hide this.
The experiment does not rule out every earlier preparation or smaller-bank policy.
Full-roster memory and native Windows/Mac release gates remain unresolved.

## Current state

Output fixtures only; no runtime, art or package changes. Evidence:

- `output/absent-crew-worker-2026-10-05/`: scheduler, source-hashed loader, probe,
  guarded runner, comparison script/JSON, native logs and owner checks.
- `output/absent-crew-worker-bounds-2026-10-05/`: generated alternative, copied
  texture pool with source hash, result/log/profile check.

Both schedulers target 2 ms work slices at a 60 FPS cap. Workers decode/hash PNGs;
the first variant supplies completed images through the existing SafeImage/pool
path, with eight pending jobs. The second also computes alpha bounds on workers,
uses completed immutable images directly in the copied pool and allows 32 pending
jobs. These three changes are combined; this comparison does not isolate their
individual gains. No GPU work runs on workers.

| Variant | Preparation wall time | Render slices | Total main-thread slice work | Slice p99 / max |
|---|---:|---:|---:|---:|
| Previous synchronous slices | 18,669.691 ms | 1,069 | 2,531.629 ms | 2.988 / 3.857 ms |
| Worker decode | 14,456.898 ms | 792 | 1,490.680 ms | 2.933 / 4.045 ms |
| Worker decode/bounds/direct image | 10,341.637 ms | 566 | 1,212.695 ms | 2.811 / 3.298 ms |

Each row is one local isolated measurement, not a repeated packaged gameplay
benchmark. Worker decode also had an earlier completed diagnostic at 14,158.595 ms;
the table uses the rerun after shared job-field access was protected. Worker setup
takes another 6.2–6.7 ms and is included in preparation wall time, not slice totals.
These are preparation-work measurements, not whole-game frame percentiles.

Both worker variants submit 2,842 distinct-path jobs; identical storage still merges
through the original pool. Reservation uses PNG dimensions and eight decoded bytes
per pixel, with a hard 16 MiB pending-image reservation cap. The faster variant peaks
at that cap; observed completed image bytes peak at 8 MiB. This is **not** a total
process-memory cap: encoded buffers, decoder workspace, temporary image copies,
metadata and GPU storage are separate. Individual images cannot be preempted.
The faster variant's maximum materialization call is 0.393 ms; scheduling, file
headers, polling and other work remain in the measured slices.

The probe temporarily supplies completed images through the startup prefetch cache;
this is fixture plumbing, not a production API. No incomplete worker job is waited
on in a slice. Completed task IDs are joined once, then a stored completion flag is
used. Worker results are read after completion, and shared job access is locked.

## Verification

The first attempt incorrectly reused already-joined worker task IDs, produced
errors and was stopped. Its log is retained as `task-lifecycle-failed.log`; it is
excluded from performance results. The runner confirmed 2,936 owner files unchanged.
Three subsequent completed runs report zero engine errors and unchanged 2,936
owner non-log files under scratch APPDATA (initial correction, locked-field rerun,
and bounds/direct-image variant).

Final variants preserve all 3,186 frame identities with no unready final frames.
All 42 cryopod sample pixel hashes, metadata, dimensions and filters match the
original full loader, and match before/after preparation. Final storage returns
to 1,800 images / 365.35 MiB. Initial pod-first storage remains 63 images / 8.14 MiB.
This does not verify all body-frame pixels, composited cryopod visuals, cancellation,
scene exit, real Continue, minimum hardware or Mac behavior. No production policy
is admitted from these results.

## Next action

Retain required crew preparation before gameplay. Stop increasing the per-frame
allowance or repeating this whole-bank recovery strategy. Investigate worker alpha
bound calculation in the existing startup prefetch path under a matched normal
loading benchmark; that path already performs background PNG decode, unlike the
direct-loader baseline here, so these gains must not be credited to normal startup.
Continue the already identified draw-work optimizations and full-roster memory
remedy independently. Earlier preparation remains a separate design requiring
startup roster, near-complete checkpoint and every recovery consumer coverage.
