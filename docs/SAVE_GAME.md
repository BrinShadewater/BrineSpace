# Loop checkpoints and menus

The title screen offers **New Loop**, **Continue Loop** when a valid checkpoint
exists, and **Quit**. Codex and Meta Progression remain read-only views of the
existing progression save. New Loop stages doctrine selection without deleting
the previous checkpoint; the next successful save replaces that slot.

During a loop, Menu / Escape offers **Save Game**, **Save & Return to Title**,
and **Save & Quit**, alongside resume and display controls. Closing the game
window also saves an active loop before exiting. A failed save keeps the game
open and reports the error. Restart also saves first. Doctrine selection and
the run summary have a Return to Title action.

One checkpoint lives at `user://brine_loop.save`, separate from the existing
`user://brine_save.json` progression file. On Windows with the default Godot user
directory this is `%APPDATA%/Godot/app_userdata/BRINE/`. No cloud sync or multiple
slots are implemented. Manual saves and save-on-exit are supported; this is not
an automatic per-cycle crash recovery system.

The version-1 checkpoint preserves station rooms and room state, resources,
decks, doctrines, directives, discovery/stabilization progress, reward flags,
orbit state, random-generator states, view position, speed, and remaining cycle
time. Continue opens paused. Occupancy is rebuilt from saved rooms without
replaying placement costs or rewards. Draft shuffles use the saved game RNG.
Finished loops remove their own checkpoint and backup before summary rewards;
they cannot be continued to repeatedly claim those rewards. Extended expeditions
can be saved again with their existing reward flags.

The file uses Godot's object-disabled Variant serialization, with a version,
checksum, temporary write, and previous-save backup. A damaged primary falls
back to its backup. Unknown versions and invalid state are rejected. Checkpoint
compatibility across future room/schema changes is not promised; the existing
unversioned progression format remains unchanged. Test fixtures with free
building or disabled failures cannot write a loop checkpoint.

Verification: `tests/test_run_save.gd` uses isolated paths, paid placement,
round-trip restoration, exact RNG state, backup recovery, write failure,
fixture rejection, title Continue, and checkpoint cleanup. Run it with native
Godot for screenshots in ignored `output/`, or headless for data checks.
`tests/test_title_screen.gd` covers the other title controls. Release export
is still unverified because this checkout has no release export preset.
