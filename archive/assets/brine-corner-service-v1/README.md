# BRINE corner life-support console

First corner-fitted room asset: northwest-facing L-shaped service furniture. Pearl-white matte ceramic, aquamarine circulation channel, sealed filter cassettes and one small water-quality display. The central BRINE chamber remains focal.

- Source: `source.png`, with exact `source.prompt.txt`; unchanged raw imagegen output.
- Transparent native export: `asset.png`. Vector registration excludes the exterior and the open inner notch.
- Nominal size: 128 x 118.08 world units. Northwest fitted preview origin: (-184, -192); left back aligns with the west inner wall and top back with the north riser base.
- Studio: BRINE Core > Room Default > **BRINE corner life-support console · NW**. Single authored orientation; other corner views are not included yet.
- Runtime library ID: `library/brine-corner-service-nw`. Available to place; the preview fixture does not overwrite personal layouts or automatically add it to existing rooms.

Native source and fitted room reviewed. `tools/review_brine_corner.gd` checks the default tray, intended size, mount bounds and editor prop/door clearance, and writes native captures plus the alpha export. Evidence: `output/brine-corner-service-2026-09-08/review-final.log`, `room.png`, `studio.png`. This is static furniture placement review, not crew-route or new life-support behavior acceptance. The empty notch is transparent artwork; the current editor uses a conservative rectangular prop bound.

Owner visual acceptance remains pending. Next corner assets should keep flush outer backs, inward-facing controls and each room's material identity; produce authored corner views when changing orientation.
