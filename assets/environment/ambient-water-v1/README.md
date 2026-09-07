# Ambient water

Three original transparent sources: current ribbon, drifting silt fan and fine
microbubble wake. Exact built-in image_gen prompts are in `generation-record.json`;
`manifest.json` records original hashes and explicit selections. Older seabed
water studies remain intact. No local image edits changed these source pixels.

These are static sprites animated in Godot through short translations and two
staggered sine-squared fades, not a frame atlas or fluid simulation. Each copy
becomes invisible before its path wraps. Periods are 18, 23 and 11 simulation
seconds. The renderer receives `main.get_visual_time_seconds()`: pause freezes
motion and the selected simulation speed changes its rate. No wall-clock timer
or separately persisted water state is introduced.

The current is near exterior debris at (24.7,22.8), silt near basalt at
(16.3,21.8), and bubbles in the sulfur region at (14.8,17.6). Full-canvas widths
are 1.8, 1.15 and 0.9 cells. The bubble wake occupies only part of its canvas.
Combined opacity caps are 0.35, 0.30 and 0.65 before source alpha and color tint.
The first settings were too faint in station review; final values improve
readability while preserving a subdued background. Distant bubbles remain tiny.

Water draws after seabed scenery and before rocks, wrecks and station geometry.
Rooms cover it. Fixed ambient cues do not indicate gameplay leaks or hazards;
there is no flooding, pressure loss, resource yield or collision behavior.

`tests/playtest_ambient_water.gd` passes real-alpha and deterministic-sampling
checks, bounded crossfades, invisible wraps, rendered motion and pixel-identical
freeze, authoritative pause/speed, three effects at three verified resolutions,
and unchanged occupancy/resources. It isolates saves/settings and captures a
room over the water separately. See `output/ambient-water-native.log` and
`review.json`. Owner approval and packaged export remain separate.

Audit using `python tools/audit_environment_pack.py assets/environment/ambient-water-v1/manifest.json output/ambient-water-v1/source-audit-new.json`
with a new report filename. `kind: effect` requires partial alpha as well as
visible content and transparent pixels; it does not prove good motion.
Rebuild the catalogue using `python tools/build_environment_catalogue.py assets/environment/ambient-water-v1/manifest.json`.
PNGs inherit Git LFS and the environment export bridge. NOTICE.md governs rights.
