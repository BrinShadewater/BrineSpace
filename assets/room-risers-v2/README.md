# Room-specific riser walls

Six new built-in imagegen sources installed for Med Bay, Hydroponics Bay, Maintenance Bay, Galley, Command Center and Observation Room. Shared riser construction is retained, with room-specific gas outlets, irrigation valves, recessed tools, hygiene fixtures, communications controls and window treatments baked into the upright face.

## Geometry and windows
The current 384×60 riser face remains authoritative. Each source face is registered at 6.4:1 without stretching, with a separately registered cap. A central 92-unit bay reserves the existing 72-unit doorway and clearance. Fittings and windows sit in left/right zones, outside that bay; plain surrounding panels remain usable for further fitting work. No new door locations, wall height or collision changes.

Windows are static baked art: oval, panoramic, circular inspection and mullioned variants. The workshop inspection port depicts an interior equipment view; other glazed sources depict ocean views. They are not transparent live views into the station environment. Galley retains a quiet panel beside its notice rail. Baked fittings cannot be individually moved in Studio; explicitly positioned older mounts remain available, while duplicate default mounts are suppressed for these six faces.

## Sources and integration
prompts.json preserves exact prompts, reference role and original paths. The clinical department source supplied geometry/rendering; fittings and materials were room-specific edits. Raw outputs remain unchanged and opaque. Black source margins are excluded by registered face/cap regions. registrations.json records actual sizes, hashes, source regions, reserved bay and fitting zones, plus refreshed card hashes. Original department sources remain intact.

riser_catalog.gd selects these room-specific faces and caps, falling back to department art for other rooms. Six new native cards are bound in room_card_art.gd and grid_canvas.gd. BRINE and Airlock keep their dedicated paths. Furniture and personal save files are unchanged.

## Review
[Gallery](review.html) contains all six originals and 24 furnished native rotation captures. All visually reviewed. Godot 4.6.1 checks pass for source bounds/aspect, authored door reserve and fitting-zone separation, 24 room rotations, shared-edge adjacency, Studio duplicate suppression/explicit mount retention and all 47 card bindings. Evidence and reproducible scripts: output/room-risers-v2/.

The shared-edge fixture records existing image-loading/export warnings from environment sources. It does not establish a new packaged build or full door animation acceptance. Source-only integration; no executable rebuild. All PNGs follow Git LFS rules.
