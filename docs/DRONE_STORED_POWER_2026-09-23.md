# Stored Power for drone charging

Updated: September 23, 2026 · Project: BrineSpace

## Objective and acceptance

Owner reported a mining drone refusing to charge with 16 Power stored. Charging
must use stored Power, automatically stop spending at a reserve of 3, and resume
when more becomes available. “Spot automatically” was interpreted as “stop
automatically.”

## Accepted decisions and constraints

Mining and salvage share battery charging. Their charger now uses stored Power
independently of the bay's operating-power allocation for the current cycle.
New charges preserve 3 Power across the entire fleet. Already purchased charge
can finish without spending again, including after Continue. Manual suspension,
global pause and master Power off still hold charging. Launching new work still
requires an operational bay. Charge rate and price remain unchanged.

## Current state

`scripts/drone_fleet.gd` separates charging from launch eligibility and applies the
shared reserve. `scripts/main.gd` passes bay suspension into status text;
`scripts/station_ui_insights.gd` explains the reserve and automatic resumption.
Battery, power-controller and priority-feedback tests cover the new behavior.
No save migration, asset change, commit or release package.

## Verification

Passing logs in `output/`: `test_drone_battery-stored-reserve.log`,
`test_power_playtest_regressions-stored-reserve.log`,
`test_priority_foundations-stored-reserve.log`, and
`test_finite_harvest-stored-reserve.log`.
Coverage includes 16 stored Power with no bay allocation, stopping at 3,
resuming at 4, shared-bay budgets, suspension, pause/master-off, prepaid charge
through saves, unchanged extraction yields and depleted deposits.
The native scene fixture also passes all three cases (16 → 14 Power/full battery,
3 → 3/no charge, 4 → 3/half battery), with zero errors in
`output/drone-stored-power-native.log`. The inspector text in
`output/drone-stored-power-reserve.png` was inspected and clearly explains the
reserve and automatic resumption. This is a controlled fixture, not the owner's
original playthrough.

## Next action

Ready for the owner's next playthrough. The original session was not available
for diagnosis; no changes were made to owner saves.
