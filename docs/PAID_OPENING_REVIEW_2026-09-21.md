# Paid opening review

Updated: September 21, 2026 · Project: BrineSpace

## Objective and acceptance
Check current paid opening viability before further balance or visual changes.

## Accepted decisions and constraints
Normal room costs and failure rules remain enabled. Blueprint choices are controlled
by the existing fixture; this is not a human expedition or native visual acceptance.
Owner layouts and library marks were not modified.

## Current state
No gameplay or art edits. Ran `tests/playtest_paid_opening.gd` headless for mining
and salvage, each with one and two solar rooms, on the current working tree.

## Verification
Both processes exited zero with no logged engine errors. All four stations completed
paid setup and survived 300 simulated observation seconds with Bill awake and one
crew member. Free building and disabled failures were false in every result.

| Bay | Solar rooms | Metal delivered | Charging wait seconds | Final power |
| --- | ---: | ---: | ---: | ---: |
| Mining | 1 | 18 | 30.6 | 3 |
| Mining | 2 | 18 | 0 | 12 |
| Salvage | 1 | 10 | 19.3 | 2 |
| Salvage | 2 | 6 | 0 | 12 |

Evidence: `output/paid-opening-current-mining-2026-09-21.{json,log}` and
`output/paid-opening-current-salvage-2026-09-21.{json,log}`. These are independent,
unseeded runs, with manual 0.1-second simulation updates and controlled building.
Differences do not isolate power as a cause of delivered cargo or prove balance.

Reviewed existing native Life Support and Data Archive focused captures. Equipment
is readable; Life Support's detached compressor remains a composition question.
No new capture or owner visual acceptance is claimed.

## Next action
The follow-up trace below resolves the apparent salvage difference without a gameplay
change. Continue rendered expedition/action
review and present room captures for owner feedback. Apple Silicon execution remains
an independent open lane.

## Salvage trace follow-up
`output/paid-salvage-trace-2026-09-21.gd` extends the same fixture and records phase,
target, cargo deliveries and discovered site stock through setup and observation.
Its JSONL and log sit alongside it. Both runs passed with zero logged errors.

| Solar rooms | Observation starts | Setup metal | Observation metal | Lifetime metal | Last delivery |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 85.6 s | 1 | 11 | 12 | 310.2 s |
| 2 | 148.6 s | 6 | 6 | 12 | 238.8 s |

Both harvested the same surveyed scrap pile at (22,19), which ended at zero of its
12 units. The second generator collected more during setup and exhausted the finite
pile sooner. The post-setup metric excluded those early deliveries, explaining the
apparently lower output. Exact timing differs from the earlier unseeded run; neither
comparison is a general throughput benchmark. No salvage or balance change is warranted
by this finding. Future comparisons must include setup deliveries and remaining stock.
