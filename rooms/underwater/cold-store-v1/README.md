# Cold Store

Current selection: smaller matte V2. Owner rejected V1 size/gloss; use matte-v2-prompts.md for revision provenance. Live props are 92 units wide (previously 124). V1 sources and registrations below are retained history.

Primary visual department Logistics (Engineering gameplay category), secondary Crew provisions; maintained neutral steel with mustard-yellow protection and restrained cyan refrigeration indicators. A fridge and weighing/ingredient rack flank a clear north/south aisle. Cabinets face south; the blueprint keeps its fixed orientation. The Galley's south door can connect to this room's north door.

Build cost: 8 Metal. Adds 40 Food and 20 Biomass capacity; consumes 1 Power per functioning cycle. Capacity remains during suspension/outages, matching existing storage behavior. No spoilage mechanic added. Connected functioning Galley discovers Cold Chain (+1 Food/cycle), with three-cycle stabilization for its research reward. All three crew can visit for stock checks using existing maintenance needs and north idle sprites.

## Sources and processing
Fridge source: 1190×1322 RGBA; alpha-threshold 200 vector registration. Rack source: 1122×1402 RGB with baked checkerboard; read-only neutral registration at 180 plus enclosed gap seeds (500,150), (500,455), (500,770). Native Godot renders real-alpha exports at source dimensions. Original rasters preserved. JSON source hashes and polygon registrations retained; render_assets.gd rebuilds cutouts. Open rack gaps and final room visually reviewed.

## Fridge prompt
ONE standalone industrial REFRIGERATION CABINET for BrineSpace underwater station cold store. Reference supplies painterly pixel-art rendering and straight-on elevated orthographic SOUTH camera ONLY, not kitchen layout or warm lighting. Tall practical double-door insulated fridge, brushed neutral grey steel, muted mustard yellow frame corners, charcoal rubber seals, two small frost-edged inspection windows showing neatly packed food containers, horizontal compressor grille at bottom, small subdued cyan temperature indicator. Logistics department, mostly maintained, modest wear on handles, condensation localized at door seals, no heavy rust. Flat SOUTH front, visible top surface, no diagonal yaw. Complete isolated upright prop about 0.9 width to height, ample margins, transparent alpha background and gaps; NO checkerboard, floor, walls, room, people, text, loose objects or external shadows. Clear large silhouette at game scale; detailed construction, cool restrained light.

Reference: rooms/underwater/galley-v1/kitchen-source.png, camera/rendering only.

## Rack prompt
ONE standalone chilled INGREDIENT RACK AND WEIGHING BENCH installation for BrineSpace cold store. Match reference industrial grey steel, muted mustard-yellow logistics framing, charcoal joints and painterly pixel-art detail, same straight-on elevated orthographic SOUTH camera. Reference is material/camera only; do not make another refrigerator. Tall narrow open metal shelving above an integrated low weighing bench: two shelves of sealed clear biomass/leafy ingredient tubs and a few labelled-looking blank food boxes; lower stainless counter holds a compact platform scale and one closed insulated delivery crate. Open shelving shows real gaps, small frost at tub edges, practical supported objects, restrained cool light, mostly maintained with handled scuffs. About 0.8 width to height. Level front horizontal edges, no diagonal yaw. Complete isolated silhouette with margin. Genuine transparent alpha exterior and open shelf gaps, no checkerboard, floor, room, walls, people, readable text, or shadows beyond object. Muted yellow accents, mostly neutral grey. Distinct large silhouette from the fridge.

Reference: fridge-source.png, camera/material only.

## Verification
Native bounds, continuous north/south clearance, prop collision and operating/frozen/offline image checks pass. Paid Cold Store plus Galley construction, connected through-route, deck, Save/Continue, all three crew stock checks, disk snapshots, zero-time freeze and suspension pass. Economy verifies additive capacity, outage stock retention, Power consumption, functioning Galley discovery, hidden forecast and three-cycle stabilization. Three viewport captures and completed-room image reviewed. No standalone package rebuilt. See docs/COLD_STORE_2026-09-08.md.
