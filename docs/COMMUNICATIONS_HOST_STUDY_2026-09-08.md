# Communications bank host study

Updated September 8, 2026. Read-only Radio Lab layout study.

## Objective and constraints

Check whether the new full-length communications banks can be added to the current
Radio Lab while retaining its furniture. Default layout has east/west doors.
Do not treat native asset review or a successful screenshot as placement approval.

## Current state

`tools/review_communications_host.gd` and its UID produce a four-case native overlay
and overlap report in `output/communications-host-study.png` and `.json`. Room data,
authoring layouts and saves were not edited. Personal layout overrides are isolated;
authored defaults remain active. JSON hashes selected host and asset dependencies,
not the complete transitive renderer/raster graph.

## Verification and result

Graphical capture completed with no script/error lines. All four images reviewed at
one pixel per world unit. None of the tested placements is accepted:

| Candidate | Existing visual bounds intersected | Door bay crossed |
| --- | --- | --- |
| North | Installed radio signal wall | No |
| South | Electronics bench | No |
| West | Receiver, operator chair, installed signal wall | Yes |
| East | Acoustic bench, installed signal wall | Yes |

The report uses visual rectangles and schematic 72-unit doorway bays. These are
overlap diagnostics, not physics, mount-plane or occupied-route verification.
The images corroborate the conflicts; no fixture was hidden to manufacture a fit.

## Next action

Author shorter communications service sections around measured free areas, or
evaluate a distinct preparation layout. A full bank replacing the existing focal
installation is a separate composition decision, not an automatic additive upgrade.
Keep these full-length candidates available for suitable hosts; runtime placement
and owner acceptance remain pending.
