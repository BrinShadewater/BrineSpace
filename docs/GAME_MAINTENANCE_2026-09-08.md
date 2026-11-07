# Game maintenance handoff

Updated: September 8, 2026 (Vancouver) · Project: BrineSpace · Branch: `main`, local and uncommitted.

## Objective and acceptance

Owner requested a game-wide cleanup, optimization, bug-fix and polish round.
This pass reviewed the current source, corrected concrete findings and exercised
26 targeted checks across the title, menus, saves, navigation, construction,
crew/recovery, expedition, flooding/repair, economy, audio, rendering and Studio.
It is a bounded source maintenance pass, not exhaustive gameplay or release acceptance.

## Accepted decisions and constraints

Preserved paid construction, resource failures, hidden discovery and three consecutive
functioning cycles, open-ended expeditions and the current art direction. No architecture
split, art regeneration, save deletion, commit or binary rebuild. Existing uncommitted
work remains in place; the index and HEAD both contained 7,476 paths at intake.

## Current state

- `scripts/run_save.gd`: captured and synchronously restored checkpoints no longer
  share mutable dictionaries/arrays with the live station. Both aliasing failures
  were reproduced before the fix; the new regression and Save/Continue pass afterward.
- `scripts/main.gd`: cache fixed blueprint door layouts instead of copying complete
  room definitions for every connection check. Each caller still receives its own
  array; all 188 room/rotation combinations match authored ports. Selected work-site
  inspectors refresh at the existing half-second HUD cadence; hovering a different
  site no longer rebuilds them. Completion and resource events still refresh immediately.
- `scripts/grid_canvas.gd`: cached light levels no longer eagerly evaluate the fallback
  target. `scripts/navigation_badge.gd`: unchanged badges retain their draw commands;
  disabled, pressed and hover state changes still trigger redraws.
- `scripts/station_ui_insights.gd`: guide copy fits the three-line HUD area and removes
  the obsolete fabrication-drone instruction. README now points to current status,
  lists 47 room identities and describes the implemented expedition/flooding systems.
- Updated tests: `test_menu_recovery.gd` and `test_station_operations.gd` now advance
  the actual architect thaw/walk/weld flow; `test_navigation_badges.gd` checks retained
  idle drawing and disabled tint updates. `profile_flood_station.gd` records draw stages.
  Added `test_checkpoint_isolation.gd`, `test_inspector_refresh.gd`, and
  `test_room_door_lookup.gd`, each paired with a generated `.gd.uid`.

## Verification

[Evidence and full logs](../output/game-maintenance-20260909/verification-summary.json)
record the 26 checks. Tests ran with Godot 4.6.1 and isolated APPDATA/LOCALAPPDATA.
All latest fixture invocations returned zero; construction and paid-opening fixtures
also emitted intermittent resource-at-exit warnings. A native Save & Quit check passed
without those errors; a verbose recovery rerun also passed. These warnings are not
counted as clean shutdown acceptance for the affected fixtures.

| Same 49-room native fixture | Before median | After median | Reduction |
| --- | ---: | ---: | ---: |
| Dry | 33.943 ms | 25.221 ms | 25.7% |
| Flooded | 44.885 ms | 34.120 ms | 24.0% |

Door/light validation fell from about 6.8–7.0 to 3.1–3.2 ms per frame. This fixture
measures rendering and water steps, not all gameplay systems running at large scale.
Both dense views still exceed the 16.7 ms budget for 60 fps. The selected cryo inspector
dropped from 240 rebuilds to 4 over 120 manually advanced frames/two simulation seconds.

Reviewed native [1600 HUD](../output/game-maintenance-20260909/hud-1600.png),
[960 HUD](../output/game-maintenance-20260909/hud-960.png) and
[flooded station](../output/game-maintenance-20260909/flood-after.png) captures.
Native title/menu, badge, Studio, riser-light and wet-door fixtures pass. Headless
display assertions were not used as display evidence; two rendering-only invocations
were rerun natively. One native menu process terminated without a diagnostic before
passing on rerun. No pixel-identity claim or exhaustive art acceptance is made.

The paid mining opening comparison survived five simulated minutes with one and two
generators, costs/failures enabled. One generator spent 278.3 seconds waiting for stored
Power; two spent 1.9 seconds. This reveals ongoing resource pressure, not a reason to
disable costs or silently change balance. The fixture supplies controlled blueprints;
it does not establish normal draft pacing or cover every economy configuration.

## Next action

The maintenance round is complete. Next acceptance work is a fresh integrated package
and a sustained normal-play session covering draft pacing, multi-crew traffic and
construction/repair under shortages. Dense render cost and intermittent fixture shutdown
warnings remain follow-ups. Owner visual and pacing acceptance remains pending.
