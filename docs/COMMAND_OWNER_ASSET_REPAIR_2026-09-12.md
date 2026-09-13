# Command Center owner asset repair — native review complete

Final checkpoint: matching charcoal/red architecture, inward overhead independent
table/systems/comms and corrected wall antenna camera are installed. Native
`wall-alpha-native` confirms white edging removed. Latest source checks
`20260912-205605-headless`:20 side variants/47 cards pass. Existing176-layout
pass covers unchanged registration frames. Final actual station pause captures
in `final-station-pause` record zero failures across four rotations; powered
clock advances and then renderer clock/native room pixels freeze on pause.
Full q0 station capture visually reviewed with aligned displays and unobstructed room.
Independent direct/retained parity covers36 samples. Card refreshed from final q0.
No export or owner acceptance. Earlier pending notes below preserve work history;
the next room in this task is Observation.

Owner request: matching wall variant and top-down/inward equipment. Gameplay and
character animation are handled separately.

Fresh native baseline q0–q3: `output/command-owner-repair-2026-09-12/before`.
The room already selected a room-specific architectural wall from
`assets/room-risers-v2/command_center.png`. Its teal bands differ from charcoal,
red and bronze consoles. Wall console controls face inward in current variants;
independent table and comms equipment keep their original facing through rotation.

`assets/command-owner-v2/riser.png` repaints the existing architecture in matte
charcoal and muted red, preserving intercom, blue underwater glazing and registered
face/cap geometry. Exact prompt and original registration retained. Installer
updates the existing Command v2 entry. A first v3 override was ineffective because
Godot Dictionary.merge defaults to preserving existing keys. Native review caught
the unchanged teal wall; duplicate removed and original v2 registration preserved.
Corrected selection reviewed in all four native views at
`output/command-owner-repair-2026-09-12/riser-corrected`: muted red trim now visible,
cap and doorway joins intact. Stderr empty. Selected q0 card refreshed; source/card
hashes recorded in `assets/command-owner-v2/riser-review.json`. Card binding
check `20260912-203533-headless` passed but did not catch source-selection precedence.

Next: review the new riser, then correct independent table/comms camera and facing
with source-local operating effects. Recheck wall console camera at source scale.
No new owner acceptance or export.

Independent console study: `equipment-v1.png` retains tall antenna/joystick and
cup side profiles; unselected. `equipment-v2.png` corrects these to overhead
geometry but bakes an RGB checkerboard. `equipment-v3.png` replaces that background
with magenta, preserving blank displays, keyboard, printer, cup, handles and secured
hoses. Exact prompts retained. `tools/build_command_overhead_equipment.py` prepares
transparent four-facing table/comms variants with hashes and crop records.
Table and comms are now selected in the base Command view with inward turns,
matching visual bounds and source-local effects. Native table q0–q3 reviewed at
`output/command-owner-repair-2026-09-12/table-native`; stderr empty. All 176 layouts
pass in `20260912-204302-headless`. Operating and retained review remain open.

Consumer correction: `split-command-wall.json` replaces `command_ops` and
`command_comms`, preserving `command_table` and `command_systems`. The small live
terminal is systems, not comms. The comms candidate is therefore integrated only
for its original base consumer; it must not substitute for the systems inventory.
`systems-raw.png` and exact prompt preserve a separate overhead systems candidate
with single screen, four-switch bank and circular canister lid. RGBA 1428×1102,
alpha range 0–255. `build_command_systems.py` preserves alpha (haze below16
removed), crops and turns the sprite. Systems now integrated with matching bounds
and inward screen traces. Native q0–q3 in `systems-native` reviewed; stderr empty.
Run `20260912-204558-headless`:176 layouts,20 side variants,47 cards pass.
`capture_command_equipment_states.gd` reviews all three props × four facings ×
offline/two operating clocks:36 samples, displays remain aligned. Direct and
production retained RGB output are identical. Selected q0 card refreshed.
Actual station pause and wall-bank source camera review remain open.

Station pause checkpoint: `verify_command_station_pause.gd` runs the actual station
process using isolated saves and the established comms-dismissal fixture. All four
rotations advance the running clock then freeze renderer clock and native room
pixels while powered/paused. `station-pause/result.json` records zero failures.

Wall source review: south controls and low camera retained. North and side comms
banks retain upright antenna stalks. `wall-sides.png` corrects those to overhead
bases; candidate not yet registered. `wall-north.png` corrects antenna bases but
introduces a new white notch under the right keyboard where the old atlas had a
solid base. Do not select it under the unchanged clipping polygon: repair the notch
or explicitly update transparency. Exact prompts and raw edits preserved.

Wall camera integration: `wall-north-v2.png` restores a shallow base rail; both
north and side sources are now selected through six registrations, with original
frames retained. `install_command_wall_camera.py` preserves raw sources and
registration backups. First native review found remaining white edging under
north console feet after border-connected cleanup. Cleanup now also removes
isolated neutral-white pockets (these sources contain no authored white equipment
surfaces). The revised cleanup still needs native verification. Earlier check
`20260912-205334-headless` passes20 side variants/47 cards but does not prove alpha
quality. Native evidence: `wall-camera-native`.
