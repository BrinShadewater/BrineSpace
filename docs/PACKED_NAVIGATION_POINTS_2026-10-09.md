# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: cheaper navigation point assembly

## Objective and acceptance

Continue full PC/Mac performance/release plan. Reduce measured graph reconstruction
work while preserving graph semantics, crew ownership and mission movement/timing.
Private comparisons do not certify a full current-checkout release or target devices.

## Accepted decisions and constraints

Test simpler point assembly before adding parked full-graph lifecycle complexity.
The graph-retention/incremental update idea remains unimplemented; no acceptance claim.
Point helper is retained in normal source after repeatable target-hitch improvement
and relevant normal regressions. Overall FPS/tails remain mixed; no full release
acceptance. Shared private worker/nav/storage controls remain unintegrated; no upload.

## Current state

Private helper packs read-only template offsets (PackedVector2Array) and original
weights (PackedFloat64Array) on existing room-cache entries. It fills known contiguous
IDs after a cleared graph, uses pre-sized local IDs and appends room-node IDs in one
batch. Native graphs remain separately owned; local links and seam validation unchanged.
Geometry revision/cache replacement naturally discards these derived fields. No global
cache, reduced node count, reduced collision margin or changed search algorithm.
A read-only assertion verifies ID contiguity; no required release side effects in it.

Artifacts D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
packed-navigation-points/{candidate.gd,test.gd,native-result.json,native-summary.json,
owner.json}, packed-nav-runtime/{bill.gd,reference.json,candidate.json,analysis.json,
packed-summary.json,owner-pair.json}, packed-nav-reverse/ (completed opposite-order pair).
Helpers output/renderdoc-tools-2026-10-08/write-packed-navigation-points.py,
test-packed-navigation-points.py, prepare-packed-nav-runtime.py,
analyze-packed-nav-runtime.py, prepare-packed-nav-reverse.py.
Actual compiled Bill source d86d7ec587e599e12d68397394a0ec3f64ac57057f2fa2a23c013ef0db3ebaa1
is the same in both lanes; --packed-nav-points selects candidate only.
Common private controls: semantic drone retention1, two low-priority water workers,
existing navigation ownership/indexed assembly and crew presentation. This limits
full-release certification scope.

## Verification

Native6460checks/0: ordered point IDs, positions, native weight values, per-room and
global lookup maps, connections and sampled routes match; temporary node disabling
is independent. Includes negative/large grid coordinates and repeated19677point builds.
First fixture parse failed on an inferred Variant key; explicit Vector2i fixes fixture.
No gameplay-source change was made to pass it.

Native point-only alternating-order benchmark14iterations, first4warm excluded:
reference median14.506ms vs packed3.439ms; ref-first14.362/3.453ms,
candidate-first14.742/3.425ms. This isolated wrapper includes dispatch/bookkeeping
and does not measure the actual full rebuild or game FPS. Its gain must not be
substituted for measured actual-release improvement.

First actual debug=false1080p40room reference-first pair,1000idle frames per1x/2x/4x:

| Speed | Mean ms ref ->packed | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| 1x | 38.770 ->37.976 | 44.626 ->43.899 | 53.455 ->53.733 | 86.276 ->97.429 |
| 2x | 39.583 ->39.314 | 47.022 ->47.477 | 59.109 ->61.054 | 120.815 ->86.600 |
| 4x | 40.574 ->40.321 | 53.857 ->53.604 | 71.425 ->72.102 | 137.654 ->127.523 |

Target engine3086/4x crew62.597->56.657ms; frame95.343->91.459ms.
A modest real scope gain, not the native microbenchmark ratio. Mean improves3/3,
p99 worse3/3. No admission or universal pacing claim; FPS/stutter gates still fail.
Compiled source/branch proofs pass; candidate packed calls Bill76/Branforth616/
Marsh388/Veld389, reference0. Phase crew/drone/mission endpoints and final histories
match. Texture peak2345.481MiB/exit228.259MiB,486drone/4074crew uploads equal.
Pending jobs3->0 on exit/router release; owners2936unchanged/logs clean/processes
terminal/adapters restored. CPU memory added by packed template arrays was not
fully inventoried; equal texture memory does not establish equal total memory.

## Reverse proof, lifecycle and normal integration

Actual candidate-first reverse pair, all existing source/branch/endpoint/cleanup guards:

| Speed | Mean ms ref ->packed | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| 1x | 38.104 ->38.858 | 43.235 ->45.051 | 53.988 ->51.973 | 86.095 ->89.585 |
| 2x | 39.209 ->38.868 | 47.667 ->46.128 | 59.067 ->58.770 | 113.378 ->109.237 |
| 4x | 40.316 ->40.039 | 54.610 ->54.379 | 73.666 ->70.854 | 131.705 ->130.758 |

Target engine3086 crew64.740->56.439ms; frame98.911->88.993ms. Target CPU gain
repeats5.94/8.30ms across both orders. Overall means/tails mixed: a targeted hitch
optimization, not a consistent general FPS gain. Texturepeak/exit, drone486/crew4074,
phase/final endpoints, worker accounting/scene cleanup and owners2936unchanged pass.

Additional16 lifecycle checks pass: two actors share template buffers without sharing
mutable graphs; graph building leaves cached positions/weights unchanged; replacement
and cache clearing discard old derived data; graph weak references die on actor release.
Packed payload16bytes/cached point in tested runtime. This is buffer payload, not total
CPU process memory. Packed arrays are references in GDScript: initial copy-on-write
test assumption failed; corrected test takes explicit duplicate snapshots and checks
actual helper read-only behavior. No helper mutation was hidden by that correction.
Buffers are read-only by convention, not protected by implicit copy-on-write.

Normal scripts/bill_npc.gd now retains this helper and diagnostic fallback
--reference-nav-point-assembly. UID untouched. No local-link, seam, template geometry,
route search, movement or mission-state change. The normal legacy link path still
uses its original connectivity lookup; common private indexed/worker controls are
not ported by this change. Before bytes frozen at packed-navigation-points/
normal-reference.gd; normal-source.diff records just this turn's edit independently
of pre-existing dirty checkout changes.

Normal-source validation:6460 kernel checks/0; room ownership90checks/0 in optimized
and reference modes; navigation rebuild-stagger0failures. Exact profile isolation
verified before each invocation; owners2936unchanged/logs clean/processes terminal.
The first normal kernel attempt timed out while mounting a release pack over the
live checkout. Removing that test-only overlay lets the same kernel pass against
the checkout; timeout is not accepted validation evidence. Saved normal source hashes
and logs: normal-validation.json, normal-owner-preservation.json and normal-*.log.
Helpers: integrate-packed-navigation-points.py, validate-normal-packed-navigation.py,
test-packed-point-lifetime.py under output/renderdoc-tools-2026-10-08/.

## Next action

Measure exact normal Bill/helper bytes in actual packaged gameplay separately from
the common private indexed/nav/storage/worker bundle. Confirm cache payload and actual
layout/staged/save lifecycle as further changes require; do not equate equal texture
memory with total-memory acceptance. Larger local-link and boundary assembly costs
remain; consider owned full-graph retention/validated changed-cell updates with
complete geometry/policy/ownership invalidation, preserving same-frame mission exit.
No broad graph refactor or shifted completion hitch. Original bug/workload/loading/
memory/endurance and Windows/Mac certification gates remain open.
