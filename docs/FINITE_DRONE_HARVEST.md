# Finite drone harvesting

Current implementation, 2026-09-06. This supersedes the renewable harvest-site
and direct-flight limitations in the first drone pass.

## Play loop

New loops contain 16 authored potential resource sites. Sites conflicting with
existing rooms, wrecks or paid queued construction are omitted when migrating an
older checkpoint. They are surveyed when a station room comes within five cells.
Surveyed contacts have small corner marks, a selectable inspector, remaining
loads and a pause/resume action. Ordinary decorative seabed scatter stays decorative.

Each mineral deposit contains 12 loads of 2 Metal (24 total). Each service scrap
pile contains 12 loads of 1 Metal and 1 Data (12 of each total). Drones select the
nearest reachable unclaimed site, perform six seconds of work per load, and
deliver cargo on docking. Stock is removed when collected, not when sold or
unloaded; storage limits cannot make it regenerate. A depleted site loses its
visible pieces and permits normal paid construction.

The 12-second extraction battery, paid bay charging, basalt's 4 Metal reward,
and existing wreck rewards remain. Cycle forecasts no longer invent automatic
drone income. Bay inspectors label output per extraction load. Pausing retains
partial extraction, and Continue retains stock, survey flags, routes, cargo,
battery and prepaid charge. Old pending cycle credit is delivered once with a
subsequent load; new cycle credit is never accrued.

## Routes

Cardinal waypoint routes avoid rooms, occupied rock/wreck cells, other deposits
and construction reservations. Exterior routes are preferred. If there is no
exterior route, matching room ports provide a service passage; sealed sides and
mismatched rotations remain impassable. Door art opens as the drone approaches.
Blocked routes are recalculated; a newly blocked segment is backed out of without
teleporting. If no route exists, the worker waits. Core construction uses the same
rules, so an enclosed Core can use connected service passages instead of stalling
all expansion. This is cell-level routing, not physics-based avoidance of moving
drones or room furnishings. Harvest sites are fixed, not procedurally generated.

## Art and source evidence

No new generated raster was needed. The resource renderer reuses three unchanged,
previously generated sprites: manganese nodule cluster, collapsed support and
torn cable harness. Four unequal grounded pieces form a site. One piece disappears
per quarter of the stock; an empty contact keeps a subtle ground mark.

The immutable source ledgers and generation prompts remain with the original
`sub-biomes-v1` and `service-wreckage-v1` packs. Their source audits are
`output/harvest-subbiome-source-audit-v2.json` and
`output/harvest-scrap-source-audit.json`. The initial attempt to audit the derived
biome manifest used the wrong schema; the successful run uses its source ledger.
Source reuse hashes and dimensions are recorded beside this document.

Native review covers dark/light backgrounds, full/75%/50%/25%/empty states,
1280×720, 1600×900 and 2560×1440 station views, launch through an open port,
working/paused state, inspector pause/resume, and paid building over a depleted
site. Captures: `output/finite-harvest-native-final/`.

## Verification and pacing

Passing focused suites cover finite stock conservation, competing bays, survey,
depletion, partial-work pause, save/load, malformed charge/stock, dynamic detours,
matching ports, battery depletion, recharge budget and one-time delivery.
The main-scene job, rock/wreck clearance, save, discovery and gameplay-polish
regressions also pass. Relevant logs are `output/*-finite-final.log`,
`output/finite-harvest-final-unit.log` and `output/finite-native-final.log`.

The legacy combined synergy/run suite still has 13 failures asserting that
directives advance, award victory, or expire. Those expectations conflict with
the separately retired directive system; none is a drone assertion. Its log is
`output/test_synergy_manager-finite.log`. Do not describe the entire legacy suite
as passing or restore retired gameplay to satisfy it.

Four controlled paid stations ran for 300 seconds each with normal costs,
resource failures and cycle upkeep. No free-building or disabled-failure flags
were used for these economy comparisons (the separate art fixture places rooms).

| Drone | Power rooms | Metal delivered | Recharge Power | Waiting for Power | Survived |
|---|---:|---:|---:|---:|---|
| Mining | 1 | 26 | 13 | 0 seconds | Yes |
| Mining | 2 | 34 | 17 | 0 seconds | Yes |
| Salvage | 1 | 16 | 16 | 0 seconds | Yes |
| Salvage | 2 | 17 | 17 | 0 seconds | Yes |

Reports: `output/finite-drone-economy-mining.json` and
`output/finite-drone-economy-salvage.json`. The second power room also changes
available routes, so throughput differences are not solely an energy effect.
Travel consumed roughly 129–170 of the 300 seconds. The current charge price
is viable for these openings; no further battery buff was justified. This is
automated scenario playtesting, not evidence of human enjoyment or full-game
balance. Larger fleets, longer expeditions and route congestion remain tuning
work. A rounding defect that could purchase Power for a nearly full battery was
fixed and covered by exact charging-cost assertions.

`output/finite-harvest-v1.pck` passed the same native fixture from an empty
temporary directory outside the checkout, without a checkout resource fallback.
`output/finite-package-runtime-v1.log` has the completion marker and no engine
errors. All three raw sprites load with alpha; the fixture also performs paid
construction over exhausted ground and restores its checkpoint. Captures are
in `output/finite-harvest-packaged-v1/`. Runtime script and selected-source hashes
match the package sidecar. This is a local isolated PCK smoke, not a release export
or a published build. Earlier drone packages predate these changes.
