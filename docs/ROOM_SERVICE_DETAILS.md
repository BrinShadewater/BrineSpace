# Room service detail trial

Reactor, Hydroponics and Crew Hab now render service details from actual furniture
rectangles through `rooms/whole-room/room_services.gd`. Paired reactor lines connect
the cooler and chamber; Hydroponics connects nutrient equipment to both beds;
crew furniture has short local leads, junction housings and small tags.

Layered casings, highlights, couplings and endpoint fittings supply depth. Junction
indicators reflect operating state. Runs remain floor-only and add no collision.
A solid flush bridge covers horizontal runs crossing the central aisle. These are
procedural trial details, not new raster artwork or a complete pipe simulation.

Initial six-room checks passed three window sizes in output/room-services-v1.log.
After adding the cover, output/room-services-rotations-v2.log verifies all three
rooms at four asserted rotations. The first rotation fixture incorrectly relied on
selected_rotation during free placement, which forces rotation zero; v2 explicitly
sets and asserts the placed room rotation. V1 is not rotation evidence.
The existing production-ten walker-path test exits successfully. No new standalone
export, flow animation verification or owner visual approval is claimed.

[Review the rooms](../rooms/whole-room/services-review.html)

## Medical, Research and Command

Medical gains bedside service fittings and teal foot mats. Research gains violet equipment pads and a specimen/analyzer utility link. Command gains a navy briefing-table mat and linked control equipment. Floor details follow furniture bounds without adding collision geometry. `output/room-character-v2.log` passes three rooms at four asserted rotations; captures remain in output/room-character-v1. The first run failed on an out-of-scope restart button reference in main.gd; the callback now uses the existing summary-layer default_button metadata. No new standalone export is claimed. Preview: rooms/whole-room/character-review.html.
