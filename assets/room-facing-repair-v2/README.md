# South-wall overhead batch — September 12, 2026

Owner accepted the Tidal top-down pilot and requested more rooms. Engineering
department; matte charcoal/slate with muted brass or burnt-orange accents.
The wall is at image bottom and all working access faces north into the room.

| Room | Selected source | Revision |
| --- | --- | --- |
| Pressure Control | pressure-manifold-wall-south.png | Round vessel lids, ribbed pump tops and small flush gauge/control deck |
| Thermal Power Control (`solar_array`) | thermal-control-wall-south.png | Tank lids, overhead radiator fins, pumps and cabinet top |
| Maintenance Bay | maintenance-repair-wall-south.png | Overhead worktop; tool grips, boxes and vise oriented toward the operator |

`briefs.json` contains exact initial prompts and subject-reference paths. All use
the accepted `assets/room-facing-repair-v1/tidal-south-topdown-v3.png` for camera
and drawing language. The two revision prompt files record self-reference edits:
Pressure V1 retained frontal pumps/standing dial; Maintenance V1 had outward tool
grips. Both rejected images are preserved here. Five generated candidates, three
selected. Biomass was inspected and left unchanged because it already reads overhead.

Three active `rooms/full-wall-v1/registrations/side-*-south.json` bindings point to
these sources. Previous registrations and their original rasters are preserved.
Read-only neutral-exterior polygon extraction uses threshold 228/spread 22 on pure
white source backgrounds. PNG pixels are unchanged; these are RGB sources with
polygon cutouts, not native-alpha sprites. Native floor review found no visible
white exterior. `validation.json` records dimensions, region, SHA verification and
read-only release dependency inclusion. All new PNGs have LFS filter coverage.

Maintenance retains the original placement-frame aspect ratio with blank space
above the new silhouette. Using the smaller detected region alone altered its
collision-driven furnishing fallback and brought an old machine back. Preserving
the frame restores the original composition while keeping the overhead drawing.
No saved positions/scales, runtime code or gameplay settings changed.

Native before/after captures: `output/room-facing-batch-2026-09-12/`. Three south
views visually reviewed; rotations 0/1/3 are RGB pixel-identical for each room.
176 preferred-layout crew-route cases pass after the final frame correction.
Side-wall checks pass; 47 card bindings and 188 layout keys pass. Cards use
unchanged q0 art, so no card rebake was needed. Source-only; owner review pending,
no executable export or publication.
