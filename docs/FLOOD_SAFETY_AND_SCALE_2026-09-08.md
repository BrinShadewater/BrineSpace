# Flood safety, controls, balance and scaling

Updated: September 8, 2026 · Project: BrineSpace

## Objective and acceptance

Owner requested all five follow-ups: crew air safety, repair cancel/reassignment,
station flood alerts, normal-play balance testing and larger-station validation.
Implementation and targeted validation complete; owner visual/pacing review pending.

## Accepted decisions and constraints

- Repair estimates conservatively include travel, critical-water exposure and a
  recovery reserve. Powered pump recovery is considered. Unsafe jobs wait for a
  helmet/refill instead of starting. Real remaining air and hazards still apply.
- Low-air crew suspend work and route to a reachable low-water, unbreached room.
  Escape timing uses route length; unreachable refuge is an explicit urgent warning.
  Crew seek a functioning diving locker, refill physically and retain paid repair
  progress. Locker routes exceeding available air are rejected. No teleportation.
- Cancel refunds unused whole Metal, rounded down; exact amount is shown before
  clicking. Reassign chooses an available named architect without another charge.
- Standard rupture profile tuned from 4%/s and 16s welding to 3.2%/s and 14s after
  startup emergency failures. Cost stays 5 Metal. Hairline remains 0.8%/s, 2 Metal,
  6s; seam 2%/s, 3 Metal, 10s. Accumulated/existing 100% damage still floods at 4%/s.
  Legacy paid 16-second jobs remain valid and keep their purchased work duration.

## Current state

New `scripts/flood_safety.gd`, `scripts/flood_alerts.gd` and UIDs. Updated
`hull_repair.gd`, `bill_npc.gd`, `main.gd`, `room_flooding.gd` implement safe task
selection/retreat, validated saved states, controls and a persistent flood button.
Button locates the most urgent room; severity warnings use hysteresis, while dry
rooms disappear from alert counts. Repair status identifies air/path/access issues.
Water connections cache by room position/type/rotation/branch, while aperture,
water, sources, pumps and isolation remain live.

New tests: `test_flood_retreat.gd`, `playtest_flood_balance.gd`,
`profile_flood_station.gd` with UIDs. Expanded repair and flooding tests. Existing
station-system fixture now waits the accepted 10-second thaw rather than 7 seconds.

## Verification

- Native repair, controls, air refusal, blocked refuge, refund/reassignment,
  hysteresis, disk Save/Continue and existing physical repair assertions pass.
- Real four-compartment swimmer retreats through a doorway, survives and reaches
  the actual locker, refilling to 60 seconds. Saved retreat actor state validates.
- Existing station systems/expedition/locker suite passes after fixture thaw fix.
- 64-room all-open network conserves total water across 60 simulated seconds;
  all depths remain bounded. Rotations invalidate connections correctly.
- Normal starting supplies, paid repair, running economy and active failures are
  exercised for each profile with a five-second response delay. Reports retain
  completion time, peak water, survival, metal and post-repair drainage. No free
  building flag enabled. Final repairs sealed at 11.0/19.2/22.3 seconds after leak
  onset, with peaks 7.2/30.36/60.96%; all crew survived and water declined afterward.
  This is a bounded emergency scenario, not campaign balance.
- Native 49-loaded-room profile at zoom 0.22, 30 warmup/90 measured frames per mode:
  water median 1.425 -> 0.301 ms after connection caching (~79% reduction).
  Final dry frame median 50.941 ms; flooded 65.142 ms, p95 69.477 ms. Earlier flooded
  median was 61.123 ms; overall rendering has NOT been shown faster. Crew updates
  are excluded from this rendering/water benchmark. Visible room subset shown in
  `output/flood-station-49.png`. Large room-rendering cost remains a known limit.
- Native controls reviewed: `output/hull-safety-controls.png`. Scoped whitespace
  check passes. Some test shutdowns retain the existing two-resource warning.

Evidence: `output/flood-safety-native-final.log`, `flood-retreat-final.log`,
`flood-safety-systems-final.log`, `flood-network-unit.log`, `flood-balance.json`,
`flood-balance-verified.log`, `flood-station-profile.json` and
`flood-station-profile-before-cache.json`.

## Next action

Owner review of safety/controls and revised rupture pacing. A separate broader
room-rendering investigation is needed for smooth dense-station overviews. No
export/release performed and no universal safety or frame-rate guarantee claimed.
