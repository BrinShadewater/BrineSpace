# Project handoff

Updated: September 30, 2026 · Project: Brine Space · Task: James compact console exit and staged route composition

## Objective and acceptance
Continue the full James animation set and consistency/polish goal. Match masters,
matte materials, viewpoint and anatomical density. This is a staged milestone,
not full-set, controller, owner or release acceptance.

## Accepted decisions and constraints
Preserve existing dry station facing, safe routing, authored furniture and36-unit
service radius. No source mirroring, limb splicing or pose-height normalization.
All native work uses scratch APPDATA; owner files unchanged. No agents or export.

## Current state
New character/james-console-water-exit-turn-v1 contains immutable generated source,
prompt/origin/SHA/reference hashes, connected-alpha crops, fixed25/50 registration,
paired bare/helmet West/North quarter and exact reverse,12 unique frames/24refs,
canonical bounded helmet heads,52-check package verifier, native contact and staged
journey fixtures, captures and review.gif. Runtime/controller/registry unchanged.
Incoming East/North staged pack remains character/james-console-water-turn-v1.
Both candidate packs together supply the arrival and departure quarter pairs.

## Verification
52 package and522 clean native contact checks PASS (16 cases/96 slots). Exact swim
endpoints/finite520ms clock, unchanged body outside helmet ownership, full rear
reach28.22919. Twelve PNG hashes unchanged on deterministic rebuild; source LFS.
52738 clean native staged-journey checks PASS:8 South-storage approach/console/
return cases,4 rotations×2gear, sampled120Hz. Actual graph, heading-preserving
smoothing, move and normal grid player; every selected body/pose clear and route
turn animates. Entry East-to-North held stationary, North swim dwell6s, exit
North-to-West held stationary before translating. Native six journey views and
source/paired boards reviewed. Holds and exact clip gates supplied by fixture,
not normal controller update/safety or restore. Real profile unchanged.

Diagnostic route-probe-evidence.json under incoming pack:32 approaches/8 usable
South routes clear,32 reverse-East departures/14 usable but14 canceled halfturns.
egress-probe-evidence.json replaces departure with a West-facing left-lane join:
14 usable,6 other-route cancellations. Exploratory egress log contains unrelated
Bill artwork warnings; do not call it clean acceptance. Current normal contact/
journey runs are clean. Other directions with no path were not counted as passes.

## Next action
Wire James-only wet-console route/contact hooks and two explicit stationary holds
into normal controller, preserving shared safety processing. Proved approach:
South storage centerNorth → graph gate(16,128) arrivingEast → lane(36.7,147.5015)
→ fine contact(117.0498,147.5015) East. Smoothing reduces this to(0,128),lane,contact.
Hold East-to-North520ms, then6s console; hold North-to-West520ms before departure.
West egress joins graph(32,144) via lane; proved South return uses(32,144),(16,128),
(0,144),(0,384). Do not force these points for arbitrary unreachable goals.
Normal grid currently checks broad legacy transition envelope for quarter turns;
use contextual selected candidate clip geometry. Add hold snapshot/restore and
safe interruption/death/gear cleanup; current restore console validation insists
raw contact within.1, so fine contact also needs conditional validation. Explicit
frame_at_elapsed does not synchronize cosmetic player.motion: prevent duplicate
turn after hold. Then normal update/safety native journeys, traffic, other goals
and full cross-family consistency. Original full goal remains active.
