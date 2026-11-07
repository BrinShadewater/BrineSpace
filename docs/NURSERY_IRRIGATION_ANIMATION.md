# Nursery irrigation follow-up

## Economy-state verification (v4)

The fixture now supplies controlled resources to the real `_apply_room_economy`
calculation instead of only setting working-cell flags. In each of four rotations:
adequate power/biomass animates the rack; missing biomass stops irrigation while
retaining room light; missing power stops irrigation and darkens the room. Local
pixel comparisons and light-target assertions pass. V4 log has no engine errors.
V3 exposed an assertion bug (empty reason checked with String.contains); explicit
empty-string comparison fixes the test, with the failed evidence preserved.

The broader station lighting fixture also passes: four rotations, mixed powered
neighbors, fade/pause, 1,616 circuit samples and a 40-room fit view. Evidence is
`output/underwater-lighting-final*`. Four gameplay regression suites pass in
`output/final-effects-*.log`. No gameplay rules were changed to make them pass.

These checks cover actual economy state propagation, not a complete human run.

The south-facing nursery now draws a restrained staggered irrigation cycle inside
its three growth trays, alongside the existing reservoir bubbles. Source art is
unchanged. Source-pixel anchors translate with the rack's registered art offset;
the droplets do not rotate independently of the stationary-facing machinery.
This is procedural local motion, not newly generated sprite frames.

The animation reads the existing `operating` flag. In the production renderer this
comes from `powered_room_cells`, whose actual contents are the cycle's working
cells, not simply electrical availability. Do not rename or reinterpret that map
casually. Lighting has its own state. No recipe identities, costs, output amounts,
or discovery rules change in this pass.

Verification: `tests/playtest_nursery_irrigation.gd` renders the actual main scene
with an isolated save. Rack-only pixel comparisons verify functioning motion and
inactive stillness in four rotations; paused pairs remain equal. Source-anchor
samples remain inside the rack silhouette across a full cycle. Native v2 captures
and the log are under `output/nursery-irrigation-v2*`; no engine errors occurred.
This fixture toggles the existing working-cell map; it does not independently
prove every simulation reason for a room to stop.

`tools/preview_nursery_irrigation.py` assembles 20 unchanged native room crops into
an approximately 2.22-second GIF. Reservoir motion is also visible and has a
different cycle, so the combined preview is not claimed to be seamlessly looping.
At overview scale the irrigation is a small accent, not a primary state indicator.

Lesson: compare pixels around the specific host machine. Whole-room differences
could pass solely because the already-existing reservoir bubbles animate, hiding
a broken rack effect. Keep motion envelope, operation state, pause, and aesthetic
acceptance as separate checks.
