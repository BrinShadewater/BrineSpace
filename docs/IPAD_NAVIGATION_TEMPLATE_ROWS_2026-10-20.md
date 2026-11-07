# iPad navigation template row filtering — October 20, 2026

Installed **brinespace-b770c48284d81479**, unchanged VM1 sampler, on the physical
A14 iPad13,18 / 4 GB. HEAD remains `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted
uncommitted work. Scoped validation; memory headroom and initial redraw remain open.

## Change and exactness

Profiling identified crew navigation-template construction as a remaining restore
cost. Each short authored lattice link previously visited every blocker in its room.
Staged authored templates now use temporary blocker lists for the current row and
the next row reached by these links. The original half-open narrow sweep still makes
every collision decision. Lists do not enter the room cache. Graph point/link order,
weights, routes, actor-local AStar graphs, cancellation and four-millisecond yield
budgets remain unchanged. Corridor/legacy templates and live route policy retain
their existing paths. No artwork or gameplay policy changed.
`--reference-navigation-template-rows` disables only this broad phase.

Red/green regression: 2,647 checks, 13,225→1,265 candidate blocker visits in the
focused case; exact half-open results. Expanded graph regression: 324 checks,
29,152 ordered records and 312 exact routes across rotations/locks/room types.
All **15 actual-PCK suites**, asset/source audits and strict signing pass, including
boundary/segment/prefix parity, staged restoration and lifetime checks. Native tests
used isolated profiles and owner fingerprints. Export configs restored byte-exact.
The initial native candidate timing overlapped export startup and is excluded;
the accepted native pair ran after complete restoration. Native graph CPU
713.000→654.973ms is separate evidence from the physical results below.

The first owner-reentry attempt hit an XCTest snapshot failure; fresh devicectl
confirmed the same app PID alive and the five original files exact. One replacement
helper authorization expired. After the owner-ready retry acknowledged a fresh
screenshot, the remaining card/SaveContinue/restoration gates completed. Interruption
and resumed logs remain distinct; this is not evidence of a game crash.

## Physical comparison

Same package, separate fresh processes, same paused 56-room/four-crew fixture,
normal rules with seeded initial reserves, row filter disabled → enabled:

| Measure | Reference | Candidate |
|---|---:|---:|
| Station setup ms | 8424 | 7918 |
| Restore ms | 3447.731 | 2935.006 |
| Crew restore ms | 3370.122 | 2875.867 |
| Process footprint MB, decimal | 2082.426 | 2076.348 |
| Engine texture MiB | 893.462 | 893.462 |

One ordered pair is not a fixed improvement guarantee. First installed-baseline
setup 8572ms, candidate first
9018ms, same-process repeat
6116ms: other stages vary.
There is **no demonstrated meaningful whole-process RAM reduction** in this pass.
Build timing also excludes later first redraw; that pause remains open.

## Longer run and restoration

Normal 1× 56-room/four-crew test: **20.174
endpoint-counted active minutes**, 22.600 wall minutes,
cycle 69→134. All four active/alive,
errors 0. Sampled process peak 2237.894MB,
end 2229.506MB; first/last-minute median difference
25.788MB. Sparse active bucket median
18.03FPS, max sampled frame
183.328ms. Dialogue pauses were handled through
actual UI and excluded from conservative active duration. One-second memory samples
and sparse frame buckets are not continuous frame capture or long-term leak clearance.
Later active-play texture residency/crew-presentation and drone cache changes are
retained in `later-texture-change.json`; warming coincided with a brief higher
footprint, without proving its complete cause. The row filter changes neither cache.
VM tag100 is IOAccelerator per the local SDK; mapped pages may alias and are not
additive to process footprint. End-run VM evidence is retained separately. GPU-driver mapped residency rose
726.450→757.858MB and malloc-small residency80.871→188.465MB between paused
load and post-run samples. Segment memo entries also grew from4 total to113,886;
this correlation does not establish that they explain the allocator growth.
Investigate allocation churn and bounded runtime geometry memoization alongside
remaining texture residency before assigning the growth to one subsystem.

Actual card return and Save/title/Continue/Save pass. Complete saved gameplay state
and exact timer match across Continue; the existing 1× reset was corrected through
the speed control while paused. All five pre-install owner files, backed up after
the pretest UI Save, are SHA-exact after final launch. Owner cycle64/seven rooms,
paused4×, menu closed. No new paid-construction/multitouch/lifecycle acceptance or
release clearance is claimed. Loading, sustained rendering performance and memory
headroom still need work.

## Identity and rollback

- Source SHA-256: `b770c48284d81479bf467d3f86225cf4aea71b96068c4b826169cc4e789519fb`
- PCK SHA-256: `4dcf79d775713ca069851bba1898101ead7252bfe3b8a4f610cbf1224d9e97f4`
- Signed executable SHA-256: `7b8db23b83f3f9e88595d2002656dd6b20a5878e7041053664df505ff8e195ac`
- Sampler SHA-256: `29b09ee6881320efa445452d84597c5186b0f44d568989d948d0505f76783b66`
- Complete current candidate: `/Users/Shared/BrineSpace-ipad-optimization-20261020/navigation-template-rows/candidate`.
- Immediate **d651** rollback: `/Users/Shared/BrineSpace-ipad-optimization-20261020/staged-navigation-boundaries/candidate`.
  Executable/PCK hashes and strict signature rechecked.
- Five-file owner backup: `/Users/Shared/BrineSpace-ipad-optimization-20261020/navigation-template-rows/candidate/immediately-before-install`.
- Portable evidence: `docs/ipad-memory-placement-evidence-2026-10-20/navigation-template-rows`.

Frozen public Mac/Windows deliveries, prior rollback/recovery donors and original
source artwork unchanged.
