# Paired north sconces in the layered station

Four current layered identities share `rooms/whole-room/room_lighting.gd`:
Nursery, Life Support, Hydroponics and Reactor. Each has two screen-north fixtures
at x ±110, y -188, independent of room rotation and north-door availability.
The 20-unit housing clears both the 72-unit doorway and wall corners. Floor pools
remain inside the 368-unit interior and precede props. Separate housings and
lenses render after cell-clipped room darkness, including on shared north walls.
There is no dynamic shadow casting or light spill through doors or solid walls.

`powered_room_cells` means functioning, not merely electrically supplied.
Lighting therefore checks existing offline reasons: NEEDS POWER and SUSPENDED
are dark; other explicit failures (e.g. NEEDS WATER) retain lighting. Unknown
offline states retain the previous dark fallback. This changes no consumption,
room allocation, costs, unlocks or failure rules. The room light cache advances
only while unpaused, fading over 0.65 seconds. Machinery retains its existing
functioning-state effects; the isolated Nursery fan study remains separate.

Native evidence: `tests/playtest_station_lighting.gd` extends the isolated-save
four-room harness. `output/whole-room-pilot-01/station-lighting.log` passes the
existing 1,616 four-room path samples and motion/containment checks, plus four
mixed-light rotations, fixed anchors, powered-idle classification, fade/pause,
and unchanged pixels in an adjacent powered room. Screenshots show the crew in
the dark room. This fixture does not certify a continuous electrical simulation.

Cards regenerated with fixtures as Nursery v5 and the other three v3, originals
retained. Card potential sockets remain exposed technical views pending their
separate infill pass. Legacy bitmap rooms do not yet use the new lighting kit.
Sconce artwork remains a procedural prototype; no new image generation was used.
