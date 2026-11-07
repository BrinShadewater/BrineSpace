# Companion rescue animation workflow

Use the character and room pipelines together for an occupant and its container.
Start from current bindings and the owner-selected body pack, not a newly generated
robot inside a prop sheet. Keep the robot's palette, source density, proportions
and floor registration identical across reveal, reboot and roaming.

## Author and register
Generate empty container hinge poses with fixed camera and stationary chassis.
Check aspect ratio against both closed and open endpoints: a plausible sheet can
quietly shorten the crate. Preserve rejected studies and exact prompts.
Register to fixed feet/chassis, never the changing lid/door bounding box.
Use intermediate authored poses and deliberate holds; four poses at 400 ms reads
as a sequence of jumps. Eight poses with shorter movement holds and an open settle
is the selected rescue revision, not a universal frame-count guarantee.

## Occupancy and occlusion
The companion exists inside before opening. Composite its existing resting pose
through registered interior apertures; the closed doors, front panel, rim and lid
occlude it. Do not draw the whole robot over a still-closed door or add it only
after the empty crate has opened. Check partial reveals at several hinge angles.
Make the final opening and first reboot frame identical where the pose is held.
Keep an explicit empty-open asset for rollout and recovered state so the baked
occupant cannot duplicate the live actor.

## Runtime and review
Sample the saved powered recovery clock, preserving pause, power interruption,
duration and reward rules. Use the same navigation exit for rollout and actor spawn.
Review true native framing after layout settles. Filter loading clearance after
saved layouts are applied as well as in navigation; earlier filters can be undone
during rendering. Reset recovery metadata on shared views for ordinary rooms.
Do not rewrite owner layouts to hide an encounter-specific obstruction.

Verify alpha, bounds, reveal masks, joins, empty terminal state, checkpoint restore
and a single actor at handoff. Distinguish native assertions from profile integrity:
fingerprint changes during an isolated test remain an unresolved audit, not a pass
or proof of the cause. Never restore the owner's active files speculatively.
Cache-bust the preview module, manifest and images together; a reloaded page can
otherwise show an earlier animation. Confirm the displayed intermediate pose.

The current example and evidence are in character/robot-rescue-v1/ and
docs/ROBOT_RESCUE_HANDOFF_2026-09-27.md in the active checkout. Source installation
does not update an existing executable. Closeout records the selected revision,
owner feedback, scope of checks and remaining package/acceptance work.
