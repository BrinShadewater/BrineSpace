# BRINE room renewal

Updated: September 8, 2026 · BrineSpace · Room art and initial thaw

## Objective and accepted direction

Add distinct northeast corner machinery matching the northwest console; give BRINE a pearl ceramic riser; remove the tube's projecting floor decoration; fit its label to the collar. New loops begin with the selected architect inside one core cryopod and release them after ten simulation seconds. This supersedes the earlier awake-start decision.

## Current state

- `assets/brine-corner-analysis-v1`: centrifuge, cartridges, diagnostics and oxygenation bank, registered at 128 units wide. Available in BRINE's Room Default tray. The illustrated NE fit replaces the existing dual workstation in an isolated review layout; no personal layout or authored workstation placement was changed.
- `assets/brine-riser-v1`: generated ceramic service wall, with source regions sampled by `north_wall.gd` and `room_door.gd`; sliding leaves retain the shared animation. BRINE card refreshed and both card consumers updated.
- `brine_core_view.gd`: removed specimen alignment floor patch under the collar; smaller label on a curved enamel area. Tube source and floating occupant retained.
- `architects.gd`, `architect_cryo_art.gd`, `main.gd`, `run_save.gd`: ten-second core thaw, matching animation duration, no forced awakening on startup/Continue. Version-two records retain partial progress; old version-one awake records remain awake. Other recovered wards retain their seven-second sequence.

## Verification

Architect recovery regression passes: no early actor/population, release at ten seconds, pause, partial-thaw Save/Continue, old awake-save compatibility, one release only and all three selections. Native tray/fit/export check passes. Default room traversal passes four rotations, sixteen doorway entries and returns, 3,827 movement samples. Native room, collar, wall, card and four thaw states visually reviewed. New NE machinery fit has static clearance only; occupied traversal evidence applies to the default room.

Evidence: `output/brine-thaw-tests-final.log`, `output/brine-routes-renewal.log`, `output/brine-room-renewal-2026-09-08/`. Personal layout SHA256 remains CD5D395B06EA2A06617B47C96FA73E3727C9DEFD050DA538DEC14379EBF2BD0D. Existing PNG loader warnings remain; no test/script errors. Owner visual acceptance and further corner orientations remain pending.

## Next action

Review the NE bank and themed room together before replacing the authored workstation layout. The previous northwest asset remains available.
