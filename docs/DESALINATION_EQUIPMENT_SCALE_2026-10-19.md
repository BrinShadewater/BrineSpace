# Desalination equipment scale — October 19, 2026

The owner accepted the INTAKE floor decal and asked that equipment match the rest
of the game's prop scale. Native comparison used five corresponding machines,
three furnished rooms at the same zoom and the production 65.28-world-unit crew
ruler. It exposed two differences hidden by catalog-only comparisons.

| Equipment | Previous width | Current width | Reference and finding |
| --- | ---: | ---: | --- |
| Filter vessels | 107.78 | 107.78 | Water Reclamation vessels; visible width within 0.4% |
| Intake pump | 93.84 | 93.84 | Water Reclamation pump; visible widths equal |
| Quality console | 112.54 | 81.73 | Water Reclamation's authored 0.726269 scale makes its effective width 81.7343 |
| Membrane skid | 140.3 | 130.5 | Tidal Condenser skid; repaint filled more of its source canvas |
| Service cartridges | 76 | 76 | Intentionally smaller service bank, separate from a full purification machine |

Console size decreases 27.4%; skid size decreases 7.0%. Their bottom-center floor
anchors stay fixed in all four authored rotations. Visible alpha bounds above 4/255
put their new widths within 0.02 world units of the references. Pump height differs
slightly with the repainted silhouette; its matching width and physical use remain
appropriate beside crew. No raster resampling or new generation was needed.

Only these two room-specific `display_width` values and their eight default-layout
positions changed. Other prop registrations, other room layouts and original art
remain exact. Normalized collision boxes now follow the smaller machines. Accepted
paint, cap, riser and decal artwork, room doors and gameplay rules are retained.
Only Desalination's card was rebaked.

Verification: **906 native checks /0 failures**, including real paid construction,
Water economy, Save/Continue, all rotated entrances and connected-neighbour routes,
actual Studio, cap and intake direction probes. Route-dependent check counts vary
with geometry; this uses the unchanged native fixture with only its output directory
redirected. Scoped layout lint and preservation receipts are in the handoff below.
Agent visual review covers the equal-scale board, all four orientations, Studio,
card and isolated playable preview. Owner acceptance of the revised sizes remains
separate from the earlier decal acceptance. This is source work; no release export,
signing, upload or new platform/performance acceptance.

[Before comparison](../output/desalination-equipment-scale-20261019/comparison-before.png) ·
[Revised comparison](../output/desalination-equipment-scale-20261019/comparison-after.png) ·
[Measurements, checks and continuation](../output/desalination-equipment-scale-20261019/HANDOFF.md).
