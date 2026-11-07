# Startup alpha-bound measurement

Updated: October 5, 2026 · BrineSpace · Candidate rejected

## Objective and acceptance

Measure the earlier worker-bounds idea in the actual title/loading/prefetch path.
Accept only a reduction in matched loading work with preserved source pixels,
frame bounds, filtering and startup readiness. Do not infer startup gains from
the earlier isolated Veld loader, which did not use normal startup prefetch.

## Accepted decisions and constraints

Retain synchronous alpha-bound calculation in the crew texture pool. The tested
worker implementation makes warm startup slower, despite removing almost all
main-thread scan time. It has been removed from runtime source and tests.
No animation, graphics, gameplay or save behavior changes are accepted here.

## Current state

The only retained runtime change from this pass is additive
`crew_texture_pool.stats.alpha_bounds_usec`, timing the existing `get_used_rect`
call once per new shared upload. The existing performance-report stats copy
includes this field automatically. No permanent image cache or new worker path.

Evidence: `output/startup-alpha-bounds-2026-10-05/` contains the native title-flow
probe, guarded runners, ten loading logs/results, inventory comparison, profile
checks and pool regression. `candidate-source/` retains the rejected implementation
and proposed tests for inspection; those proposed tests were not run and are not
acceptance evidence. Candidate mode in the current probe rejects execution until
that archived implementation is explicitly restored in a diagnostic checkout.

Three warm baseline processes, three candidate processes and three control
processes used the same isolated profile and startup manifest. A first process
populated the manifest. OS disk cache was uncontrolled; none is certified cold.
The normal title, loading overlay, scene transition and startup prefetch execute.
Dialogue typing was skipped for later runs; all comparisons below use the same
existing startup-stage timers, which exclude it. Normal effects remained enabled.

| Median across three runs | Baseline | Worker candidate | Fresh control |
|---|---:|---:|---:|
| Sum of measured startup stages | 4,117.971 ms | 4,917.275 ms | 3,990.986 ms |
| Interface/grid construction | 3,773.183 ms | 4,604.826 ms | 3,709.819 ms |
| Pool alpha-bound work | 860.982 ms | 4.727 ms | 866.104 ms |
| Pool image-loading calls, including waits | 319.805 ms | 1,832.315 ms | 299.358 ms |

These are editor native startup-stage measurements on the owner's RTX 4070 Ti,
not total launch-to-ready time or packaged Windows/Mac release acceptance. The
candidate is approximately 23% slower than the follow-up control by the sum of
stages. No sustained gameplay FPS conclusion is drawn.

The candidate computes alpha bounds on decoded worker images, carries the rectangle
through independent cached image copies, and lets the pool consume it. This scans
worker images even when another consumer does not need bounds or an equivalent
image is already shared. In candidate run 2 the aggregate worker scan cost is
1,715.626 ms, versus baseline run 2's 860.982 ms of unique-upload pool scans.
The increased measured image-loading time includes waits/copies; this experiment
does not isolate all scheduling or memory-bandwidth causes. It does demonstrate
that this particular relocation is a net regression.

## Verification

All nine warm inventories match exactly across **8,188 live storage records**:
source signatures, dimensions, formats, mipmap state, decoded bytes, filters and
alpha bounds. Upload count remains 8,188. This metadata/signature comparison is
not a moving-scene visual review or full GPU pixel comparison.

All ten loading runs finish without engine errors. Each emits one ObjectDB
instance-leak warning at fixture shutdown, in baseline and candidate alike; this
remains unassigned and is not treated as a clean release-exit certification.
The retained implementation then passes the native crew-texture-pool regression:
**46 checks, zero failures**, including exact uploaded pixels, frame identities,
metadata independence, bounds and resource release. No warning in that test.
Owner fingerprints remain **2,936 files unchanged** across each runner batch and
the final validation. No package rebuild or upload.

## Next action

Return to the action register's R1 contact-shadow batching candidate, then R2
zero-alpha terrain draws. Integrate each narrowly with reference fallback where
needed, full-room visual checks and matched workload measurement. Do not continue
expanding this rejected worker-bounds path. Memory-budget, long-stall and native
Mac gates remain open; the new timer supports future measured loading work.
