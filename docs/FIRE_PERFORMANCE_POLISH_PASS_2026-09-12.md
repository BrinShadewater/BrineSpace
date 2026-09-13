# Fire performance and paid-operation handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: another performance, polish, bug and optimization pass

## Objective and acceptance

Find reproducible gameplay faults and reduce measured update costs while preserving concurrent art and animation work. This bounded pass addresses fire simulation and power-status refresh; it does not claim overall frame-rate improvement or completion of the original power-balance/turbine investigation.

## Accepted decisions and constraints

Normal cycles remain paid. A fire interrupts its own compartment immediately. Other rooms retain service already paid for in the current cycle. Extinguished compartments retain the existing forecast-based recovery check, including suspension and resource restrictions. No rates, recipes, assets or animations changed; no export or commit made by this task.

## Current state

- `scripts/room_fire.gd`: fire refresh previously replaced the entire paid operation map with a next-cycle forecast. This reproduced loss of an unrelated mining bay after its final reserve unit had been spent. Refresh now changes burning/formerly burning compartments only, and calculates a recovery forecast only when needed.
- Fire advancement gathers burning room references once per call, returns immediately for safe stations, and avoids checking emergency power when sprinklers are off. The original substep, shared water ordering, damage and suppression calculations remain.
- `scripts/main.gd`: removed retired directive rewards from reroll tooltip text.
- `tests/test_power_playtest_regressions.gd`: ignition and extinction regressions protect unrelated paid operation; suspension remains enforced on the extinguished room.
- `tests/test_fire_gameplay.gd`, `tests/test_hazard_chain.gd`: newly constructed fixture stations establish operation using `_apply_room_economy()`. Their former use of fire refresh to bootstrap all power no longer matched that function's compartment-specific responsibility.

## Verification

The new power regression failed twice before the fix and passes afterward. Final focused tests: `output/test-runs/20260912-215552-headless` (power regressions plus 45 fire checks). The end-to-end hazard chain passes in `output/test-runs/20260912-215504-headless`; native fire gameplay passes all 36 checks in `output/test-runs/20260912-215454-native`. These cover fire shutdown, suppression, finite water sharing, pause, save/restore, crew escape, repair and drainage. Native suppression and extinguished-room captures were visually reviewed. Existing runtime image-import warnings remain; this is not exported-build validation.

The initial integration run failed because fixture rooms had no paid operation after their bootstrap shortcut was removed. The native assertions identified absent ignition; the chain then lacked fire damage. Establishing a real economy cycle corrected the setup, without weakening assertions or enabling free building.

Controlled headless comparison: same 300-room fixture, 2,000 calls per case, original fire script preserved alongside the benchmark. Final measurements:

| Scenario | Delta per call | Before | After |
| --- | --- | --- | --- |
| No fires | 1/60 second | 310 us | 91 us |
| No fires | 0.4 second catch-up | 1,264 us | 90 us |
| One fire, sprinklers off | 1/60 second | 310 us | 93 us |
| One fire, sprinklers off | 0.4 second catch-up | 1,231 us | 97 us |

All four cases produced identical room dictionaries, resources and logs. Additional eight-second suppression comparisons passed including operation maps. Benchmark exited zero with zero parity failures. Evidence: `output/fire-pass-20260912/benchmark.gd`, `fire_baseline.gd`, `measurements.json`, `benchmark-godot.log`. These are CPU microbenchmarks of fire advancement, not a whole-game or GPU benchmark. No rendering cache was changed.

## Next action

Use the new F7/F8 diagnostics during a normal paid expedition to investigate the original power/reserve experience and west-facing turbine report. Combined art/animation acceptance and exported-build validation remain separate work.
