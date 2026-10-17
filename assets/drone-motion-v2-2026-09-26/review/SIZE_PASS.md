# Directional size pass — September 26, 2026

Agent visual review; owner acceptance pending. See `size-pass.png`: the upper
rows show eight travel headings at their actual export scale and .34 game-scale
insets. Lower rows compare travel and all four actions at the same .65 review
scale. No sprite was fitted independently to its opaque bounds.

The northwest nozzle was oversized and splayed outward. The selected v4 source
bends it up/right and reduces its barrel/forearm thickness. All eight headings
retain two arms, two large propeller casings and two smaller rear thrusters.
Arm segments and casings are now broadly consistent in projected size; perspective
and arm articulation still change apparent lengths. This is a visual proportional
check, not a claim of exact 3D dimensional equality.

New north/east/west contact sources use a fixed per-heading scale and chassis
landmark registration across all four actions. Rotor centers and local joint
polygons are recorded in `cardinal-registration.json`. North .344, east .300,
west .312 source-to-export scales compensate for different master drawing sizes;
every export retains .34 world units/pixel. South sources retain their existing
recipe. Original sources and accepted v10 remain preserved.

Compared the eight headings, all sixteen work contacts, and active phase boards
at enlarged/native size. No arm swaps, missing limbs or abrupt casing-size change
was observed. The east collection ore is retained as a separate connected alpha
component rather than discarded during speckle cleanup. Chassis/casing dimensions
stay fixed within each loop; local arm articulation and blade rotation supply motion.

Final physical world size, clearance, runtime transitions and Godot integration
remain separate work. Existing 69.12-world-unit nominal width is still provisional.
