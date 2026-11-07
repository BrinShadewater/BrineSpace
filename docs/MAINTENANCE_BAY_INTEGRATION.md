# Maintenance Bay registered pass

The existing Maintenance Bay uses four source-registered assemblies in station,
placement preview, draft and inspector consumers. Original 1254-square source
and historical variants remain intact. Native card v1 uses the embedded renderer;
both texture maps, alternate selection and draft aspect-fit use the complete card.

`rooms/production-ten/maintenance_bay_view.gd` records source polygons, ground
pivots, uniform scales, footprints and wall sample regions. The shared hull owns
the west/east/south tee sockets and sealed unused walls. Equipment centers rotate
while artwork remains south-facing. The entire tall panel rack remains inside
the safety bounds in every rotation.

Two operating cues are attached to the repair part and diagnostic screen. The
fixed servicing arm, tool rack and hull-panel storage stay still. These initial
cues do not implement articulated repair-arm motion or a new repair simulation.
No costs, production, discovery, unlock or player-save behavior changed.

## Evidence

`tests/playtest_maintenance_bay.gd` passes at 1280x720, 1600x900 and 2560x1440.
Each run checks four rotations, every host's active/inactive/paused pixels, effect
point containment, full visual bounds, non-overlapping collision footprints,
canonical tee topology, disconnected closed walls and 1092 center-to-port samples.
Native v1 card and the 2560 rotated station/draft/inspector frame were inspected.
Captures/logs: `output/production-ten/maintenance-native-*`, `maintenance-*.log`.

Synergy, discovery progression, polish gameplay and run balance regressions pass.
No ERROR/SCRIPT ERROR entries were found in maintenance stderr logs. Inherited
raw-image export warnings remain. Source/card PNGs have LFS attributes; paired
UID files accompany the renderer and fixture.

## Remaining acceptance

Neighbor crossings with the production actor, incompatible/disconnected pixel
seams, economy-driven power transitions, mature mixed-station zoom, packaging
outside the checkout and owner visual approval remain. Source-floor patches in
concave assembly boundaries and source wear merit closer visual review. Static
source parts plus operating overlays are an initial animation pass, not fully
articulated machinery. Seven other rooms in this batch still await registration.
