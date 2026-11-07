# Floors and floor details, batch 3

Generated with the built-in image generator; raw sources preserved, no raster post-processing. See manifest.json for exact sizes, hashes and alpha ranges. None are integrated into live rooms or collision.

Selected artwork candidates: agriculture-floor.png and anomaly-floor.png (opaque floor materials); drain.png (wet service areas); cable-cover.png (maintenance/workshop crossings); service-marking.png (equipment service pads). Three detail sprites have real alpha; the service marking has residual alpha in its intended empty center (recorded in the manifest); clean that before live integration. Native scale, edge-fringe and furnished-room acceptance remain pending. Floors are not certified seamless.

Access panel studies are retained separately: access-source.png has halo and excessive wear; access-repair-source.png has a baked checkerboard; access-simple-source.png is cleaner but still has an unwanted halo. None is an accepted ready-to-use cutout. Do not substitute them silently for a clean sprite.

## Exact prompts

### agriculture

BrineSpace underwater station game asset, strict top-down orthographic flat surface, deliberate chunky pixel-art clusters matching detailed retro-futurist machinery. Low contrast, restrained desaturated colours, diffuse neutral lighting, no bloom, no bright reflections, no cast shadows. No perspective, walls, furniture, machinery, doors, text or labels. One square opaque edge-to-edge AGRICULTURE floor texture. Broad matte grey-sage moisture-resistant composite plates with thin dark waterproof joints, narrow flush drainage strips at widely spaced intervals, tiny muted green service tabs. Mostly clean restored greenhouse work deck, subtle mineral marks only immediately around drains. Large plain panel centers, low texture noise, no plants or soil or scattered leaves. Four broad modular rows, no outer border. Material stays quiet beneath growing beds at 384px room scale.

### anomaly

BrineSpace underwater station game asset, strict top-down orthographic flat surface, deliberate chunky pixel-art clusters matching detailed retro-futurist machinery. Low contrast, restrained desaturated colours, diffuse neutral lighting, no bloom, no bright reflections, no cast shadows. No perspective, walls, furniture, machinery, doors, text or labels. One square opaque edge-to-edge ANOMALY CONTAINMENT floor texture. Dark charcoal ceramic-composite large angular panels over conventional modular steel structure. Thin closed graphite gasket joints, sparse muted dusty-violet inset ceramic tabs and restrained double etched seam lines. Quiet unsettling precision, no magical runes, no glowing circuitry, no holes, no cracks, no tendrils, no biological growth. Broad plain panel centers, four-by-four modular grid, matte low-contrast finish, no border. Violet occupies less than two percent of area. Intact maintained research compartment, not derelict.

### access

BrineSpace underwater station game asset, strict top-down orthographic flat surface, deliberate chunky pixel-art clusters matching detailed retro-futurist machinery. Low contrast, restrained desaturated colours, diffuse neutral lighting, no bloom, no bright reflections, no cast shadows. No perspective, walls, furniture, machinery, doors, text or labels. Single isolated flush rectangular maintenance access plate sprite on REAL TRANSPARENT alpha background. Medium-dark matte steel panel, chamfered corners, thin waterproof rubber perimeter gasket, four captive recessed corner screws, small folded-flat central pull handle in a recessed slot. Plate lies perfectly flat on deck, no visible raised sidewalls. 3:2 rectangle centered with transparent margin, subtle tiny worn ochre service tab at one edge, no writing. Clear readable large forms at 40x28 gameplay pixels. No surrounding floor tile, no background, no checkerboard. Reusable engineering floor detail.

### drain

BrineSpace underwater station game asset, strict top-down orthographic flat surface, deliberate chunky pixel-art clusters matching detailed retro-futurist machinery. Low contrast, restrained desaturated colours, diffuse neutral lighting, no bloom, no bright reflections, no cast shadows. No perspective, walls, furniture, machinery, doors, text or labels. Single isolated long narrow rectangular stainless floor drain sprite, 6:1 width to height, centered on REAL TRANSPARENT alpha background. Flush thin charcoal-grey rim, simple row of twelve broad dark drainage slots with black backing mesh inside slots, four small recessed attachment screws. Matte subdued stainless steel, no shiny white trim. Mostly clean with very slight mineral deposits inside corners only. Perfect overhead view, no upright grate, no sidewall, no surrounding floor, no glow or drop shadow, no painted background or checkerboard. Low-profile life-support and agriculture service detail, readable at 60 by 10 gameplay pixels.

### cover

BrineSpace underwater station game asset, strict top-down orthographic flat surface, deliberate chunky pixel-art clusters matching detailed retro-futurist machinery. Low contrast, restrained desaturated colours, diffuse neutral lighting, no bloom, no bright reflections, no cast shadows. No perspective, walls, furniture, machinery, doors, text or labels. Single isolated low-profile rubber cable crossing cover sprite on REAL TRANSPARENT alpha background. Wide horizontal 5:1 graphite-black rubber strip, gently tapered flush edges, three simple longitudinal grip ribs, two short muted ochre end tabs, small molded fastener recesses. Strict overhead plan view, no visible height, not an upright wall fixture or tall ramp. Underwater station maintenance and drone workshop deck utility. Restrained clean matte rubber with subtle pixel clusters, no gleaming highlights, no haze, no outer shadow, no floor background or checkerboard. All exterior pixels fully transparent. Readable at 64x13 gameplay pixels.

### marking

BrineSpace underwater station game asset, strict top-down orthographic flat surface, deliberate chunky pixel-art clusters matching detailed retro-futurist machinery. Low contrast, restrained desaturated colours, diffuse neutral lighting, no bloom, no bright reflections, no cast shadows. No perspective, walls, furniture, machinery, doors, text or labels. Single reusable painted floor service-zone marking decal on REAL TRANSPARENT alpha. Four disconnected thin L-shaped corner brackets defining a wide rectangular equipment maintenance pad, muted dusty ochre paint, lightly chipped intentional pixel edges. Completely transparent EMPTY center and exterior, only paint pixels visible. No filled rectangle, no panel, no floor, no metal, no writing, no symbols, no arrows, no drop shadow, no glow, no checkerboard. Brackets are broad enough to read at 70x45 gameplay pixels, sober industrial stencil marks. Strict flat top-down 2D decal. All empty regions have actual zero alpha.

### access_repair

Edit this access plate sprite only: remove ALL soft halo, fog, glow and exterior shadow, make every pixel outside the crisp metal silhouette truly alpha zero. Preserve plate shape, camera, handle and screw positions. Make the steel mostly clean matte dark grey, remove orange rust speckling and most scratches, retain only a very small subdued ochre service tab on the right edge. No bright screw highlights, soften highlights to medium grey. Actual transparent background, no checkerboard or black background. Top-down game floor detail, no perspective change.

### access_final

Transparent-background game sprite, a single flat rectangular charcoal metal maintenance lid viewed from directly overhead. Clean industrial pixel art. Six simple screws, a shallow horizontal recessed handle, clipped corners, muted grey top surface and dark rubber gasket. Entire object perfectly flat, 3:2 aspect. Small centered object with generous fully transparent margin. No halo, no shadows, no glow, no background texture, no floor, no checkerboard pattern, no rust, no bright highlights, no lettering. Output genuine RGBA PNG with transparent exterior. This is a low-profile floor insert for a subdued underwater station game.


