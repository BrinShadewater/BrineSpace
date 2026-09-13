# Gameplay follow-up: startup, cryostasis, exterior hatch and cables

Updated September 12, 2026 · Brine Space source workspace. No export or commit.

## Objective and acceptance

Complete the remaining non-art requests from the owner playtest handoff. Leave
replacement room art and character animation sources to the other sessions.
Earlier power/initial-selection and Studio/menu work is recorded in
[power](GAMEPLAY_POWER_HANDOFF_2026-09-12.md) and
[Studio/menu](GAMEPLAY_STUDIO_MENU_2026-09-12.md) handoffs.

## Accepted decisions and constraints

- BRINE starts dark. Interior light flicker precedes consoles, and pod power/thaw
  starts last. Keep the ten-second total recovery and normal economic rules.
- Cold emergence is a runtime effect, with no character source replacement.
- Exterior hatch closure follows physical departure; reopening precedes reentry.
  Inner/outer interlocks and normal expedition costs remain authoritative.
- Retire decorative floor power cables globally. Keep equipment pipes, functional
  power simulation, salvage scrap, source provenance and saved layout data.

## Current state

- `scripts/brine_startup.gd`, `architects.gd`, `grid_canvas.gd`,
  `architect_cryo_art.gd`, and `brine_core_view.gd`: saved core wake drives dark,
  flickering lights, consoles at two seconds and pod activation after three.
  Reduced motion uses a smooth light rise. Master power off holds recovery.
  Emergency console presentation lasts through cycle zero, then funded room
  operation takes over; it does not add generated power or free machine service.
- `scripts/cryo_release_effect.gd`, `cryo_recovery.gd`, `architects.gd`,
  `grid_canvas.gd`, `flood_visuals.gd`: four-second cold mist and blue-to-normal
  human tint. Optional validated roster time/position fields preserve Continue;
  legacy rosters without them do not replay an effect. Animation textures are
  wrapped with their existing pivot/height metadata, never mutated. Marsh's
  charging release is excluded. Retained and direct room-content drawing preserve
  the effect with the normal station lighting path.
- `scripts/airlock_cycle.gd`, `crew_expedition.gd`, `airlock_panel.gd`,
  `grid_canvas.gd`: departure seals to a flooded, pressurized waiting state;
  returning divers wait for the hatch to open before moving inside. Saves accept
  those states. Pause, suspension and power loss hold the cycle. An unreserved
  sealed chamber can be manually drained. North-facing exterior doors render on
  the raised hull even when closed; the existing rotated low hatch remains.
  Door cache state includes the exterior aperture.
- `rooms/whole-room/decoration_props.gd`, `room_services.gd`,
  `rooms/floor-profiles-v1/details.gd`, `modern_details.gd`: cable-specific draw
  and placement filters also remove orphaned bridge plates. Enabling general
  decoration cannot restore these cables. No assets or layouts were deleted.
- Added startup, exterior-hatch and cable native tests and paired UIDs;
  extended the real diver-mining journey test. Tests are grouped under
  `owner-gameplay-playtest` in `tests/index.json`.

## Verification

- Startup/recovery phase, pause, master power, Continue and reduced-motion checks;
  native captures in `output/gameplay-startup-20260912/` show dark, intermediate,
  powered, cold and warm states. The first failure was incoming comms pausing
  the fixture; a state probe established that cause before isolating comms.
- Airlock native checks cover four orientations, open/closed states, moving hatch
  pause/power loss, half-closed Continue and full return. Screens are in
  `output/gameplay-hatch-20260912/`. Initial first capture was recentered by a
  pending placement callback; corrected evidence settles layout before focusing.
- `20260912-171639-headless`: mining, station salvage and Marsh battery journeys
  pass, including saved cargo and alive return. The miner asserts closed hatch
  while away and all departure/reopening phases.
- `20260912-172126-native`: cable removal passes all 176 furnished room rotations.
  Native pixel comparisons show zero cable/bridge output with decoration enabled
  and nonzero pipe output. Four Data Archive Studio captures are in
  `output/gameplay-cables-20260912/`; north view visually reviewed.
- `20260912-172259-headless`: architect recovery, cryo recovery and full run-save
  tests pass with optional emergence fields.
- `20260912-172619-native`: final startup/cold effect and exterior-hatch checks
  pass. Each rotated airlock connects its interior side to the core and leaves
  its exterior approach open. Retained and direct room-content cold captures
  were reviewed with normal station lighting. North closed/open and all other
  hatch orientations were inspected across the native captures.
- Scoped `git diff --check`, six-fixture index and new UID checks pass. Bible,
  status and production guidance additions preserve existing bytes; the new
  gameplay skill section matches the installed copy.

## Remaining scope and limits

The identified non-art fixes are implemented in source. The owner's original
low-power/west-turbine executable or save remains unidentified; directional and
accounting tests did not reproduce a turbine defect, so no speculative balance
change was made. Art replacement, corner alignment, helmets and animation-source
quality remain with the other sessions. Cold Store particles were explicitly a
later art request. Native source evidence is not packaged-release verification
or owner visual acceptance. No release was built.

## Workflow lessons

Use saved simulation clocks for staged effects; distinguish fixture isolation
from real pause evidence. Track physical hatch phases in simulation and save
validation, then include aperture in retained-render cache keys. Remove decoration
at its actual draw/placement owners, preserving pipes and provenance. Settle
pending scene/layout callbacks before framing native evidence. Inspect actual
captures even when assertions pass. Shared files contain other sessions' work.

Diagnostic limit: disabling all retained surfaces produced a dark lighting view
in an intermediate capture. That broad diagnostic renderer is not the direct
room-content comparison above and has not been established as visually equivalent
to normal station rendering. It was not used as startup acceptance evidence.
