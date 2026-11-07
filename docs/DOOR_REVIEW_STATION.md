# Interactive door-review station

Run `tools/launch_door_review.ps1` (optional `-GodotPath`), or run Godot with
`--path . --script res://tests/door_review_station.gd`.

This is an isolated four-room review fixture, not a normal economy run. The normal
simulation remains paused and its processing/input is disabled; the fixture drives
the existing character route and renderer clocks. Saves, if triggered during
initialization, go to `user://brine_door_review_fixture.json`, never the player save.

The character automatically crosses all four connections. Buttons select Bio,
Life Support, Engineering or mixed departments; reverse the circuit; skip to the
next door; rotate the layout; darken one room; or pause/resume the review. Closed
outer boundaries demonstrate unused-socket infill. Real connection rules determine
door finish: mixed boundaries use generic, and the mixed layout also has a Bio
boundary. Separate same-department presets expose all four finish choices without
adding test-only paint overrides to game code.

The character follows the real game's test-walker path; this is not WASD movement
or a replacement population system. Normal build/inspect controls are shielded to
keep the fixture stable. Close the window to finish. The main game is unchanged.

Automated mode adds `-- --capture-dir=res://output/door-redesign/review-station-v2`.
It refuses to overwrite evidence and exits after 32 crossing captures, four
mixed-power views and pause comparisons. Review the rendered crossings for art
quality; successful assertions do not constitute owner visual approval.
