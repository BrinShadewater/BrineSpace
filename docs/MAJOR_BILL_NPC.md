# Major Bill: room wandering and needs

Bill now picks places to visit and activities to perform instead of repeatedly
choosing a random neighboring room. Hunger and fatigue build slowly; curiosity
and a desire to check equipment provide reasons to move between breaks.

- Food breaks favor functioning hydroponics, nursery, and lounge rooms.
- Rest favors functioning crew quarters, medical rooms, and lounges.
- Equipment checks favor maintenance, life support, reactors, and storage.
  Bill approaches a prop from its west side, then plays kneel → repair → stand.
- Exploration favors less-visited rooms. Corridors remain travel routes, with
  safe pacing when no suitable destination is available.
- Activities finish before another need is chosen. A suspended or unavailable
  service cancels the activity without satisfying its need.

Navigation uses the renderer's registered prop footprints and wall openings,
including room rotations and the narrow straight/corner corridor polygons.
A 16-unit floor graph uses a 10-unit foot clearance. Links and smoothed shortcuts
are swept at intervals no greater than four canonical units. Inter-room links
only pass through reciprocal, connected doors. Center aisles have a small travel
preference; destinations can lie elsewhere on the reachable floor.

Bill's physical foot stays in canonical 384-unit room coordinates. Zoom changes
only rendering. Movement drives facing and the existing distance-based walk
animation. Pause and game speed apply to movement, needs, and activities together.
Construction or door rotation rebuilds navigation and cancels stale plans.

The existing status text shows his activity, hunger, and fatigue. This is a
behavior prototype: meals and repairs are visual activities, do not consume
resources, and do not change production, health, failure conditions, or rewards.
Both crew members now save their needs, exact positions, routes, current
activities, visit history and animation clocks in the existing checkpoint.
Continue remains paused and preserves the action frame. Checkpoints predating
crew data remain compatible and start fresh NPC loops. Social relationships,
population simulation, and task assignment are not implemented.

Bill and Veld maintain 20 units of separation between their foot collision areas.
They yield and detour around one another, or choose a new goal if a colleague
blocks the destination for several seconds. Every detour retains wall/prop
clearance; horizontal corridor passing favors the front lane. Both actors sort
by foot depth while passing. This is local avoidance for the current two crew.

Legacy rooms without registered footprints retain conservative perimeter lanes
around central equipment. They do not receive unrestricted interior wandering.
If an edit invalidates Bill's current floor, he stops rather than jumping through
obstacles. Initial spawning may select a nearby clear floor point.

## Verification

- `tests/test_crew_polish.gd`: head-on corridor encounters, swept clearance,
  saved needs/routes/activities, action-frame recovery, malformed data rejection,
  and older-checkpoint compatibility. Native mode captures the passing sequence.

- `tests/test_bill_npc.gd`: real room geometry, swept movement, connected food
  trips, blocked/disconnected doors, needs satisfaction, off-axis wandering,
  equipment action sequence, pause, zoom, and every layered room/socket rotation.
- `tests/playtest_bill_npc.gd`: native station captures of autonomous wandering
  and equipment work. Output: `character/major-bill-v2/qa/npc-native/` (ignored).
- `tests/test_major_bill_animations.gd`: existing 17-animation/102-frame coverage,
  frame timing, transitions, and distance-based playback regression checks.

Run the first and third with Godot's `--headless --path . --script res://tests/…`.
Run the native fixture without `--headless`, using `--rendering-method gl_compatibility`.
