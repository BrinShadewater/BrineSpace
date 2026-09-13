# Helmeted crew mining handoff

Updated: 2026-09-12. Project: BrineSpace.

## Objective and accepted decisions
Owner requested crew members mining outside while wearing diving helmets. Extend existing salvage expeditions and helmet/airlock systems. Mineral trips select the nearest reachable, surveyed, active finite mineral deposit within return range. Ordinary room costs, tank limits and storage caps remain unchanged.

## Current state
scripts/airlock_panel.gd adds a mission selector: Mine Minerals (2 Metal) or Salvage Scrap (1 Metal + 1 Data). Helmet fitting, refill, dispatch and recall remain in the Diving Airlock inspector. Active missions lock/synchronize the selector.
scripts/crew_expedition.gd accepts mining or salvage, retains the mission kind through saves and validates the corresponding cargo. One completed work/pickup consumes one site unit. Cargo is credited only after return and unloading. Human crew require fitted helmet, at least 55 seconds tank reserve and 2 station Oxygen; existing range checks and low-air recall apply. Android behavior remains helmetless and battery limited by design. Existing underwater work/pickup/carry animation is reused; no new mining-specific art was produced. Old salvage saves without a mission kind remain valid.
Tests: tests/test_diver_mining.gd and UID, registered in crew subsystem; tests/index.json. No new EXE was built; the prior hazard release predates this feature.

## Verification
Headless mining test passed. Native final run passed with zero script errors, including real locker fitting, inspector button dispatch, exterior helmet state, complete airlock phases, save/restore during work and carrying mined cargo, one-unit depletion, and delivery of 2 Metal. Bill returned alive and dry with about 29 seconds tank oxygen in this close-deposit fixture. Legacy salvage cargo remains valid; mismatched mining cargo is rejected. Existing test_marsh_battery passed (771 route samples), including the salvage expedition regression. Diff whitespace checks passed.
Evidence: output/diver-mining-native.log and output/diver-mining.png. Native inspector mission/recall controls and exterior view reviewed. Tests use a deliberately nearby surveyed deposit; this does not establish all procedural map layouts or long-distance pacing.

## Next action
Owner playtest and include in the next requested release. Dedicated underwater mining animation/audio could be a later polish pass.
