# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: targeted topology CPU optimization integrated

## Objective and acceptance

Retain measured navigation CPU savings without signature, locked-cell, route,
rebuild, save or visual changes. Accepted as a targeted CPU improvement, not a
universal frame-pacing fix or PC/Mac release certification. Full goal remains open.

## Accepted decisions and constraints

Every query reads complete original inputs; immutable actor-owned key caches only
the sorted/formatted signature. Locked-room updates run even on hits. Final layout
revision/hardware reads preserve original query order. Public door lists already
owned; redundant second copies and payload lists removed. No quality, gameplay,
art, monolith refactor, source UID regeneration or permanent resource retention.

## Current state

Changed `scripts/bill_npc.gd` only at topology implementation/adjacent primitive
cache fields. Source before/after prefix and suffix exact against tested private
full actor. Current SHA256:
`b0ee1a9b316f12fdf936e222c6e18bd9e59e55d6407601e51c51573b0e732e2a`.
Existing `bill_npc.gd.uid` preserved. Pre-edit bytes retained in
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/topology-normal-integration/bill-before.gd`.

Added `tests/test_crew_topology_signature.gd` and paired new UID
`uid://chxf6d1vn0uab`; registered in crew group. Test compares actual normal actor
against original signature semantics across same-tick mutations, ownership/type,
Moon phases, query-time invalidation and locked-cell/world lifetime.

## Verification

Prior native mixed three-pair comparison: mean30.513→29.963ms, all3pair means
improve1.488–2.296%; topology1394.160→777.169us (-44.25%). Native plain-source
18run real-map comparison108full states/cameras exact; reported/large mean improve,
current pooled mean/tails worse. See [full results and limits](TOPOLOGY_REAL_MAP_REGRESSIONS_2026-10-11.md).

Focused current station native pair resolves local-cost concern: topology278.681→
159.127us/frame (-42.90%), simulation step1255.664→1119.105us, mean12.475→12.269ms.
6480hits/3misses; max topology call187→130us.12states/cameras exact, no>50ms frames,
peak1940.747MiB same. p9517.828→18.142/p9926.443→27.787/max41.948→44.251 remain
mixed; no claim that earlier upload/simulation stalls are fixed. Earlier four>50ms
frames and unknown extra simulation work remain explicit release pacing issues.
Evidence: sibling `topology-current-attribution/comparison.json` and traces.

Six direct normal-project headless tests pass, zero engine errors: signature14567,
room ownership90, prefix1262 (127892point records/984routes/126528sorted targets),
rebuild stagger, Moonbay save, RunSave/Continue. Five corresponding native adapted
tests passed before integration. Headless checks do not substitute for rendered
acceptance; native same-source comparison already recorded. New test initially
triggered strict Variant-inference warning; explicit WeakRef annotation corrected,
subsequent full selected group clean. UID preserved on repeat.

Normal test artifacts: `topology-normal-integration/` results/logs/owner in the
benchmark parent above. All2,938 owner files unchanged after every terminal run;
jobs terminal. Muted isolated profiles; no captures/runtime copies; disk floor held.
Normal runner: `output/renderdoc-tools-2026-10-08/run-topology-normal-checks.py`.

## Next action

Continue actual drone-sheet upload/retention remedy without repeating rejected
larger global caches or shader providers unchanged. Revised native effects storage
needs immutable loaded-source/API review and updated timing before integration.
Record and investigate unresolved current simulation stall. Full-source native
candidate, loading/endurance/original bugs/UI/GTX1650/M1/Mac signing and certification
still required; no itch.io upload/visibility change authorized by this milestone.
