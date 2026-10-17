# Riser fitting audit — September 26, 2026

## Findings and changes

- Perspective: reviewed front-facing north-wall fittings against the accepted riser and furnished room props. New fittings keep horizontal/vertical frames, shallow edge depth and restrained upper-edge light. No floor-plane rotation or nonuniform stretching.
- Sizing: individual side/centre size limits replace filling every available rectangle. Clocks, handsets and safety boxes retain smaller physical proportions. Wide machinery occupies more width; centre pieces no longer stretch towards doorway height.
- Centering: visible alpha bounds and opaque-area centroid anchors replace canvas centering. The centre mount is now centred at y=-215.5, matching the yellow bay; side mounts centre at y=-230.5. Aspect ratio and panel containment are preserved in both viewers. The centroid is an optical approximation, verified visually in context.
- Pixel density: the original 28 source assets ranged roughly 6–54 source pixels per world unit at the former 27-unit height. Source resolution alone is not rendered pixel density: some old sources contain enlarged coarse painted pixels. Source rasters were preserved; no artificial pixel-grid normalization or upscaling was applied. Native captures were used to judge detail weight against walls, props and crew. New wide silhouettes remain legible after reduction, though tiny screws and labels are naturally lost.
- Art style: 12 new matte, restrained fittings cover pressure, heat, power, drones, specimens, medicine, botany, galley, crew memories, acoustics, anomalies and BRINE sensors. Assigned across 43 room designs. 27 existing fittings remain in use, including ocean windows. Older pressure gauges, loose tools, oxygen masks and posters retain visibly coarser detail; replacement candidates, not silently marked style-normalized.

## Verification

Three native pilots: Reactor, Research Lab and Crew Lounge. Then all 47 designs captured (44 furnished rooms plus three corridor segment studies), 185 captures across closed/open doors, interior dressing and exposed ocean. All 44 internal walking routes passed; zero failed segments. Fitting containment assertions passed. Save fingerprints unchanged.

Final full-run evidence: `output/riser-room-preview/session-39931ab487f248c38c9d7a8685d387c8`.
Six updated `review/panels-*.png` sheets visually reviewed at native capture scale. Browser Galley checked in closed-interior mode. New assets have real alpha, original masters, exact prompts and source/prompt hashes in `panel-expansion/manifest.json`.

## Scope

Preview-only. Connected north bays stay clear; ocean exposure remains a manual preview mode. Production decoration flag, station neighbour detection and owner room layouts are unchanged. Owner visual acceptance and production integration remain separate steps.
