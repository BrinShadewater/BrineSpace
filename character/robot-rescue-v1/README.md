# Josh and River rescue artwork

Selected source-game replacement for the old two-state encounter containers.
River retains the sage salvage-bin identity and gains a front unloading ramp;
Josh retains the slate shipping crate and double doors. These fixed south-facing
recovery props use the same painted detail and robot body art as robot-polish-v1.

Run `python character/robot-rescue-v1/build.py` to reproduce 26 selected alpha frames.
The preserved generated sources and exact prompts are in `sources/`. Eight authored
hinge poses per container are registered to stationary chassis contacts, rather
than recentered around moving doors. The first four-pose revision is retained for
provenance. Opening holds are 100, 110, 110, 120, 130, 150, 180 and 300 ms, so the
motion settles into the open position instead of jumping every 400 ms.
Export: 320×440, pivot (160,280), standing
reference 148, 2.267 source pixels per world unit. Neither robot is rescaled or
recoloured for the container; reboot frames composite the selected existing poses.

The robots are present behind the opening panels from the beginning. Registered
interior aperture masks reveal their unchanged resting poses as hinges move.
The last opening and first reboot frames are pixel-identical. Separate empty
container exports are used only during rollout and after recovery.

The saved eight-second powered clock drives opening (0–1.2s), reboot (1.2–6.4s)
and rollout (6.4–8s). The runtime composites the existing walk frames toward the
same clear navigation point used by spawn. After recovery only the empty prop
remains and the ordinary NPC draws the robot. A blocked exit holds the reboot
pose. No new recovery payment, duration, reward or save fields.

Preview: http://127.0.0.1:8775/character/robot-rescue-v1/ . Its repeated demonstration
adds a one-second closed lead-in and a one-second recovered hold. The runtime
uses actual room navigation; the standalone preview uses an illustrative exit.

Native test: `python tools/run_margot_check.py robot-rescue-native -s tests/test_robot_rescue_art.gd`.
Source-game integration only; the existing Windows export has not been rebuilt
with these new assets. Owner visual acceptance remains pending.
