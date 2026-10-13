# Project handoff

Updated: October 6, 2026 · BrineSpace · Unreachable dry goal searches

## Objective and acceptance
Remove the repeatable ~174 ms James maintenance stall without changing decisions,
route points, needs, movement or art. Full frame-rate/memory/platform gates remain open.

## Accepted decisions and constraints
Retain the narrow negative reachability proof in scripts/bill_npc.gd. After the
first failed ordinary dry AStar query within choose_goal, traverse its directed
component with the currently disabled/fire nodes. Later targets proven unreachable
return empty; reachable routes still use unchanged AStar. Scope keys separate
start nodes and dry proofs from swim-facing proofs; avoidance queries bypass it.
Existing choose_goal lifecycle releases the dictionary on return. No permanent
navigation cache, changed RNG/order/attempt limits, animation or gameplay rules.

## Current state
Normal change: scripts/bill_npc.gd; existing UID retained. Permanent regression:
tests/test_dry_goal_reachability.gd with generated paired UID, admitted to crew in
tests/index.json. Prior unrelated dirty changes retained. Evidence and before-source:
output/dry-reach-2026-10-06/. No export, commit, upload or owner-data changes.

## Verification
Red fixture fails specifically because repeated unreachable queries still perform
AStar work. Final/permanent isolated fixture exits 0: 142 checks, zero failures.
Covers exact reachable paths, disconnected/directed graphs, disabled start/target/
transit, fire blocking/restoration, separate starts, avoidance bypass, outside-choice
calls and fresh topology after scope exit. Diagnostic closure leak fixed before green.

Related tests pass: service reachability 7,402 checks; registered-room walker paths
6,400 pairs/68,850 segments; swim/walk routing; NPC clearance and smoothing. One
initial service test could not parse because the isolation wrapper reused its local
expected variable; corrected wrapper rerun passes, original failed evidence retained.

Three native normal-renderer 1080p 40-room pairs (debug 4.7.2, RTX4070Ti): median
maintenance decision 140.631→31.905 ms (~77% less); repeatable frame
173.651/178.880/174.246→70.516/65.449/65.643 ms. Goal/cell/foot/medium outcomes match
in all pairs. Pairs 2/3 also match 15 phase snapshots of crew paths, positions,
state/stage/direction/timers, needs, visits and RNG, plus zoom/power/drone states.
Native end capture inspected for runtime art; this is not complete visual acceptance.
All runs exit cleanly and preserve 2,936 owner non-log files.

Overall means remain ~36–37 ms. Post-change p95 56.176/56.910/56.556 ms,
p99 69.332/69.411/69.559 ms, max 97.819/105.368/104.240 ms; remaining unrelated
>100 ms frames still block release. Texture memory unchanged at 4,283.22 MiB.
Matched results/hashes: acceptance.json. Not packaged/minimum-hardware/Mac proof.

## Next action
Later attribution and corrected benchmark collection:
`docs/LAYER_UPLOAD_ATTRIBUTION_2026-10-06.md`. Earlier grid totals below were
accumulator readings and are not established exclusive per-frame drawing costs.

Attribute remaining zoom/interface engine-wait/render stalls and sustained frame
cost using existing hitches/stages before another fix. Goal work still takes ~32 ms;
further optimization must preserve ordering, exact paths and RNG. Memory budget,
original report closure, native endurance and Windows/Mac certification remain open.

Latest after-3 evidence: zoom 4x/frame43 is 97.45 ms, ~57.43 ms grid draw across
17 callbacks; interface 1x/frame13 is 94.96 ms with ~72.44 ms grid draw across
8 callbacks. The separate 104.24 ms interface/frame16 has only ~14.00 ms grid
draw and ~101.87 ms engine-wait interval, so redraw work alone does not explain
every hitch. Next distinguish costly layer callbacks from remaining engine/driver
waits; callback counts do not prove duplicate whole-station redraws.
