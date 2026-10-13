# Split-prop retention verification

Updated: October 5, 2026 · BrineSpace · R3 investigation

## Objective and acceptance

Determine whether split prop wrappers cause repeated static command rebuilds in
normal gameplay. Preserve pixels, animation, ordering and layout invalidation.

## Accepted decisions and constraints

R3 is closed as already handled in the default rendering path. Do not ship the
proposed identity workaround or claim a new performance gain. Runtime source was
restored to its pre-investigation behavior; prior R1/R2 optimizations remain.

## Current state

The earlier source hypothesis missed `nursery_whole_view._sorted_content_queue`:
it pre-expands and caches split wrappers, then merges live actors into that queue.
Normal retained shell pass 2 uses this cache with `reuse_prop_queue` enabled by
default. Direct raw-prop calls to `submit` bypass it; the diagnostic
`--uncached-prop-queue` path intentionally does extra work.

The initial native direct-call reproduction produced 35 redundant static rebuilds
over five unchanged submissions in each of 12 renderer/rotation cases. A proposed
identity fix passed that fixture, but that fixture did not represent the default
caller. The fix was removed after tracing the caller. Archived experiment files
are under `output/prop-retention-2026-10-05/`.

Retained changes: `tests/test_split_prop_retention.gd` and its UID, native
registration in `tests/index.json`, this handoff and the status/research register
corrections. The test exercises the existing cached queue using actual life
support, hydroponics and BRINE renderers. Synthetic opaque crew textures exercise
depth ordering; they do not certify selected character art or movement.

## Verification

- Default source: **181 checks, zero failures**, including 144 exact retained/fresh
  pixel comparisons across three renderers and four rotations. Covers unchanged
  submission, advancing clock, power, moved props plus layout serial, a distinct
  prop dictionary with the same ID, replacement, zoom, culling/reappearance,
  deletion and crew ordering. Existing retention avoids 168 static command
  rebuilds versus the forced-redraw reference in unchanged/clock cases.
- BRINE capture visually inspected. Not a full Studio editing/save lifecycle test.
- Native 40-room inventory: selected life support/hydroponics/crew hab use library
  layers; BRINE has six split pass slots. Its cumulative static count was only 13
  in this short idle diagnostic. This inventory is not a release performance gate.
- Candidate/reference benchmark stopped after discovering the caller mismatch:
  two runs completed, third deliberately terminated. Partial benchmark data is
  invalid for accepting an optimization; no timing comparison claimed.
- Isolated profiles guarded before writes; every run group, including the stopped
  benchmark, confirms **2,936 owner non-log files unchanged**. Final test has no
  engine errors. Scoped diff whitespace check passes.

## Next action

R4: reproduce repeated failed drone routes through the production caller, then
evaluate a bounded failure cache with origin, destination and topology invalidation.
Memory budgets, long stalls, packaged Windows/Mac acceptance and endurance remain
open. This investigation changes no gameplay, textures, packages or release status.
