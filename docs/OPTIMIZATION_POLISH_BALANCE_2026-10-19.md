# Station refresh, placement warnings and reroll fairness

October 19, 2026. Owner requested another optimization, polish and balance pass with attention to all three areas. This is a **local source change**, ready for isolated playable review; it is not a new release.

## Changes

- **Less repeated economy work.** A complete interface refresh evaluates the next-cycle economy once and shares that read-only result with the resource bar, guidance, selected room and open diagnostics. The scope ends synchronously with `_refresh_all`; independent reads and actual cycle simulation still use current state. Native evaluation counts changed **2 → 1** for HUD plus selected room and **4 → 1** with diagnostics open. These are operation counts, not an overall FPS or loading-speed claim.
- **Fairer rerolls.** Single-card and whole-hand rerolls prefer different blueprints in the remaining draw stack, including a newly recycled stack. Rejected copies remain in the deck and can return if no alternative exists. Normal building draws retain their previous behavior. One charge per action, recovery after four running cycles below the three-charge cap, room costs and survival rules are unchanged. The button tooltip now explains the action, alternatives and recharge.
- **Complete placement warnings.** A large room now warns if any of its footprint squares covers a Current Turbine intake. Previously only its anchor square was checked. This remains an advance warning; it does not forbid the owner's placement decision or spend materials.

No art, filters, animation timing, room costs, recipes, unlock purchases, save format or release package changed. The screenshot-selected look remains the source default.

## Verification

All **eight focused fixtures pass** on Godot 4.7.2:

| Fixture | Relevant result |
|---|---|
| `test_draft_reroll_fairness` | 197 checks; 64 shuffled seeded stacks have no immediate rejected-card repeats when alternatives exist; charge, card-count, recycle and unavoidable-repeat cases pass |
| `test_power_playtest_regressions` | Existing power checks plus all four large-room squares at four rotations and a nearby non-overlap case pass |
| `test_ui_forecast_scope` (native) | 15 checks; one forecast per refresh; changed reserves, hardware and suspension are reflected; independent inspector/resource reads stay fresh; legal non-anchor intake warning renders without spending materials |
| `test_ui_resource_outlook` (native) | 36 checks; resource forecasts, readability and navigation pass |
| `test_run_balance` | Draft recovery, cap, banked charges, pause, reboot and station-fit checks pass |
| `test_polish_gameplay` | Existing economy/shared-input and gameplay checks pass |
| `test_station_operations` | Construction/operations checks and 500 opening-deck seeds pass; first support card remains draw three |
| `test_synergy_evaluation_parity` | 8,043 checks / 1,188 cases / 112 authored recipes pass |

Initial failing reproductions and subsequent test-fixture corrections are retained. The native fixture was corrected to use the real scene's full-viewport anchors, explicit free-placement rotation and resource-icon whitespace; these were fixture issues. Final captures were visually inspected. The warning fixture uses explicitly placed rooms and supplies for presentation validation, not a paid-run balance result.

Logs, before-source copies, captures, source-only diffs and profile checks: [pass handoff](../output/optimization-polish-balance-20261019/HANDOFF.md). Latest native fixture log: [15 passing checks](../output/test-runs/20261019-130542-native/logs/test_ui_forecast_scope.log).

## Limits and continuation

Tests ran with isolated APPDATA. The native fixture also verifies its resolved `user://` path before creating a station. The owner's already-running game was left open. Only its `last_session.json` changed during the profile comparison; no whole-profile-unchanged claim is made. The signed Windows ZIP's size and modification time remain unchanged.

Human early-loop pacing, larger-station frame times, rare stalls, endurance and memory headroom remain open. Next: review a normal paid opening and large-room placement in isolation, then select these two runtime-file changes alongside the accepted look/settings work for relevant packaged Windows validation. No export, signing, upload, commit or expanded Mac/iPad acceptance occurred in this pass.
