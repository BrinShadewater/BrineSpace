# Current floor decoration replacements

The live room detail renderer and shared door thresholds now use floor-dressing-style-v2
and floor-utilities-style-v2 instead of floor-kit-v6 PNG exports. Fifteen stable legacy
keys map to current hatches, plates, markings, mats, drains, cable runs and threshold
strips in rooms/floor-profiles-v1/modern-details.json. Placement IDs are preserved so
saved Studio edits remain usable. Aspect-fit bounds retain the previous mount envelopes;
no source images were modified. Old files remain available for historical fixtures.

Straight corridors, bends and T-junctions now use the selected corridor-deck source from
floors-and-details-v5, clipped to their existing geometry. Wall panels and fittings already
use riser-wall-kit-style-v2 / wall-dressing-style-v2 and remain active. The owner-preferred
Pressure Control and Listening Post installations remain intact. Listening Post floor
briefs now resolve against its actual baked/native equipment when no full-wall prop exists.

Validation: 40 furnished rooms rendered at four orientations; 320 floor detail placements,
zero missing hosts; corridor geometry/native rendering passes at four orientations; full
Studio suite passes including persistence, sizing, mirroring, duplication and deletion.
Reviewed native Crew Hab and bend captures. Logs: output/layout-editor/modern-*.log.
Static room cards were not rebaked by this floor-only runtime change. No broad deletion
of historical art and no change to paid construction, doors or collision geometry.
