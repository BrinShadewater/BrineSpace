# Full-Power drone report

Updated September 24, 2026 · BrineSpace · Diagnose idle mining with 22/22 Power

## Objective and acceptance
Identify the cause in the owner's F8 snapshot, preserve charging's reserve of 3,
and make the actual idle reason visible without changing resource yields.

## Accepted decisions and constraints
Full Power means storage capacity, not drone activity. Finite deposits stay finite;
unrevealed deposits remain unsurveyed. Owner saves/layouts remain untouched.

## Current state
Report brinespace-report-20260924-024141-228784-12570683401.zip captures seed
3862060672 at cycle 457. Both mining bays are operating, unsuspended, docked with
12/12 battery. Power is on and doors unlocked. The discovered mining deposit at
(17,18) has zero units. Other mining deposits are undiscovered; surveyed salvage
piles cannot supply mining drones. The report's 142 errors concern earlier Studio
polygon/pref issues, not a charging exception; those remain separate follow-up.

scripts/main.gd now puts battery/work status above charging totals in the room
inspector. scripts/drone_fleet.gd uses depletion advice even when there are no
wreck entries, rather than falling back to a false generic route-blocked message.
No charging, extraction or economy rules changed. Added a focused assertion to
tests/test_drone_battery.gd.

## Verification
Evidence: output/drone-power-2026-09-24. Replayed the owner's copied fleet for
120 updates: both batteries stay full, spend zero Power and report NO SURVEYED
DEPOSITS LEFT. Battery regressions pass after the change; power-controller
regressions passed during diagnosis. Native copied-checkpoint inspector capture
is in inspector.png. No owner save or profile was edited.

## Next action
Expand survey coverage to find more mining stock, or schedule accessible basalt
excavation. A Salvage Drone Bay can work the discovered scrap piles. Restart to
load the clearer inspector. Do not treat this diagnosis as proof against all
possible charging bugs; this captured session has fully charged drones.
