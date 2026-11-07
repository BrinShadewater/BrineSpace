# Material repaint batch — September 8

Implemented source-level matte repaints for Tidal Condenser north, south and both side installations, plus its standalone pump/vessel source. Preserved blue-grey paint, brass fittings, existing footprints and room layout. Updated all four vector registrations; original raster sources remain available.

The shared research accessory repaint is now used by eight active room compositions: Mycelium Nursery, Med Bay, Quarantine Cell, Research Lab, Bio Lab, Cryo Chamber, Med Center and Xeno Lab. The common nursery_supply_trolley tray item uses the same source. Ten placed accessory definitions retain original regions, footprints and pivots; vector pieces exclude the new neutral background. Historical compositions remain unchanged.

## Verification

- Nine affected rooms: 72 native rotation/state renders, exit 0, no ERROR output. All nine powered default views visually inspected.
- Tidal four orientations visually inspected; enclosed neutral patches near gauges identified and removed through vector aperture seeds. Final eight rotation/state renders passed; corrected south and west inspected.
- Nine sealed offline room cards freshly baked and mapped into both card and grid preview consumers. Original cards retained.
- Raster originals were never postprocessed. New PNG paths are covered by Git LFS. Generated source hashes are in assets/material-polish-v1/manifest.json.
- Evidence: output/art-material-polish/shared and output/art-material-polish/tidal-final. Review gallery: output/art-material-polish/shared/index.html.

- Native layout workflow regression passed: copy/duplicate, placement, ordering, light settings, reload and recovery. An initial headless invocation could not capture a viewport; the supported native-rendered rerun exited 0 with no ERROR output.

## Remaining

This is a completed repaint batch, not completion of the whole-game material objective. Large science furniture, other priority wall installations and drone machinery remain brighter than the new target. Characters, UI and animation-frame consistency still require their own review. No Windows distribution rebuild was made; the previous packaged executable predates these changes.
