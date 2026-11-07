# Tidal-reference matching pass

Owner direction: use the approved matte Tidal room as the quality and material reference for other room props and walls. Preserve departmental colors, physical scale and clean maintained condition.

## Integrated

- Life Support: north, south and paired side wall sections, auxiliary machinery, wall trim and caps. Eight split sections remain independently placed; no doorway-layout changes. Removed the old bright procedural wall-edge stroke to match the repaint.
- Research Lab: north installation and paired side views, smaller instruments, structural wall trim/caps, and shared laboratory bench. Sink and analysis arm no longer contain a static running stream/beam in their source art.
- Clone Lab: north installation and paired side views, auxiliary equipment, and structural trim/caps. The local wall draw now samples the new room-specific atlas instead of inherited generic trim. Glass retains biological subject visibility with less cyan glare and reflective edging.
- Shared bench source updated in six active compositions: Research, Tidal, Med Bay, Bio Lab, Clone Lab and Quarantine. Some defaults omit this bench through existing placement rules; updating a composition does not mean the bench is visible in every orientation.
- Eleven new source images, preserved prompts and source hashes under assets/material-polish-v2. Original images preserved. New RGB backgrounds are excluded through vector silhouettes, not raster postprocessing. Existing footprints, pivots, UV dimensions and player saves retained.
- Seven new cards mapped to current card/grid/alternate-preview consumers.

## Evidence

Native room review: seven rooms, 56 rotation/state renders, exit 0 and no ERROR output. Architecture review: four rooms including Tidal, 16 rotation views with risers/foundation, exit 0. All seven q0 room views, every orientation of the three repainted rooms, and four q0 architecture views visually inspected. Review folders: output/art-material-polish-v2/final and architecture. Cards: assets/material-polish-v2/cards.

Side-wall regression passed: 20 variants, hashes, library entries, state, invalid-draft fallback and valid drafts. Native layout workflow also passed copy/duplicate, movement, ordering, guides, light settings, reload and recovery. The headless renderer was not used for viewport-capture tests.

## Remaining scope

This batch does not complete the all-assets objective. Medical/Bio/Xeno walls, engineering/drone installations, other shared furniture and riser decorations still need comparison and targeted repair. Character, terrain and animation families have not been accepted against this reference. Research/Clone reuse the existing north source at q2; no new bespoke south camera was added. No Windows distribution rebuild was made.
