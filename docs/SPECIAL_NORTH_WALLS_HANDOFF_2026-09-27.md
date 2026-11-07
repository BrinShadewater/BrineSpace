# Special north walls

Updated: September 27, 2026 · Project: BrineSpace

## Objective and acceptance
Create machinery-matched north walls for Diving Airlock and Survey Probe Bay.
Owner clarified that the probe windows flank its launcher on the north wall.
Owner visual acceptance remains pending.

## Accepted decisions and constraints
Preserve the functional hatch, launcher, launch route and all owner layouts.
Use matte steel and subdued accents. Windows remain separate registered inserts.
Special backdrops apply at quarter zero, when equipment faces north. Existing
backdrops remain in other rotations; explicit Studio material overrides still win.

## Current state
`assets/special-north-walls-v1` holds unchanged generated masters, exact prompts,
prior registrations, native views and backed-up/refreshed cards.
`walls.json` adds `north_special` to two records without replacing their base art.
`painted_shell.gd` selects those north backgrounds and overlaps the fixed probe
launcher above its matching surround. `ocean_windows.gd` supports side-only windows.
The existing native riser fixture has a `--special` mode and orientation assertions.
Gallery: http://127.0.0.1:8812/special-north/ (build_gallery.py reproduces it).

## Verification
Both sources passed alpha/registration inspection and byte-preservation checks.
Eight native orientation captures passed, all reviewed in a contact sheet.
Quarter-zero selection and other-rotation fallback assertions pass. Two cards baked
using maintained baker with scratch-copied owner layouts. All Godot runs isolated
APPDATA; live session changed last_session.json during profile fingerprint checks.
No claim of byte-identical owner profile. No gameplay or release-export acceptance.

## Next action
Owner review of assembled north views. No release export, commit or push performed.
