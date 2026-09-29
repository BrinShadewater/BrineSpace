extends RefCounted
## Small live effects drawn in the station's foreground pass (owner playtest, Sept 16):
## - current flowing into each working Current Turbine's intake, so a turbine visibly works
##   whichever way it points (a north intake sat behind the raised wall and looked dead);
## - sparks and a flickering glow at a welding torch, for crew welds and Josh's torch repairs.
## Everything is deterministic from visual time, so it freezes with pause, and reduced motion
## draws a calm, static version.

const Preferences = preload("res://scripts/title_settings.gd")
const DIRECTIONS := {"north":Vector2(0,-1), "east":Vector2(1,0), "south":Vector2(0,1), "west":Vector2(-1,0)}

static func draw(canvas, game, rooms: Array, size: float) -> void:
	draw_turbine_flow(canvas, game, rooms, size)
	draw_torch_sparks(canvas, game, size)
	draw_hull_bubbles(canvas, game, rooms, size)
	draw_hazards(canvas, game, rooms, size)
	draw_build_flourish(canvas, game, rooms, size)

static func draw_turbine_flow(canvas, game, rooms: Array, size: float) -> void:
	var time: float = game.get_visual_time_seconds()
	var reduced: bool = Preferences.reduced_motion
	for room in rooms:
		if room.id != "current_turbine" or room.get("suspended", false): continue
		if not game.powered_room_cells.has(room.pos) or not game._turbine_intake_clear(room): continue
		var intake: Vector2i = game._turbine_intake_cell(room)
		var inward := Vector2(room.pos - intake)
		var across := Vector2(-inward.y, inward.x)
		var mouth := (Vector2(room.pos) + Vector2.ONE * 0.5 - inward * 0.5) * size
		if reduced:
			for i in range(3):
				var at := mouth - inward * size * (0.18 + 0.2 * i)
				canvas.draw_polyline(PackedVector2Array([at + (across - inward) * size * 0.05, at, at + (-across - inward) * size * 0.05]), Color(0.62, 0.84, 0.88, 0.45), maxf(1.0, size * 0.006))
			continue
		# Streaks drift from the far edge of the intake cell toward the turbine and converge.
		for i in range(12):
			var phase := fposmod(time * 0.55 + i * 0.137, 1.0)
			var lane := (float(i % 5) - 2.0) / 2.0 * (1.0 - phase * 0.7)
			var head := mouth - inward * size * (0.95 - phase * 0.9) + across * lane * size * 0.32
			var length := size * (0.08 + 0.05 * float(i % 3))
			var alpha := sin(phase * PI) * 0.42
			canvas.draw_line(head, head - inward * length, Color(0.66, 0.86, 0.9, alpha), maxf(1.0, size * 0.005))
		for i in range(4):
			var phase := fposmod(time * 0.35 + i * 0.29, 1.0)
			var bubble := mouth - inward * size * (0.8 - phase * 0.75) + across * sin(time * 1.3 + i * 2.1) * size * 0.12
			canvas.draw_arc(bubble, maxf(1.0, size * (0.008 + 0.004 * (i % 2))), 0, TAU, 8, Color(0.78, 0.93, 0.95, sin(phase * PI) * 0.5), maxf(1.0, size * 0.003))

static func torch_actors(game) -> Array:
	var result: Array = []
	for actor in [game.bill_npc, game.veld_npc, game.branforth_npc, game.marsh_npc]:
		if actor == null or not actor.active or actor.dead: continue
		if actor.state != "weld" or actor.movement_medium != "dry" or not actor.path.is_empty(): continue
		if actor.goal == "construction" and (actor.timer < 0.52 or actor.timer >= 9.48): continue
		result.append(actor)
	var josh = game.companion_actors.get("josh")
	if josh != null and josh.active and not josh.dead and josh.behavior == "torch" and josh.movement_medium == "dry" and josh.path.is_empty():
		var enter: float = josh.poses.cycle_seconds("torch-enter-" + josh.direction)
		var leave: float = josh.poses.cycle_seconds("torch-exit-" + josh.direction)
		if josh.behavior_elapsed >= enter and josh.behavior_elapsed < josh.behavior_duration - leave: result.append(josh)
	return result

const TORCH_TIPS := {
	"south": Vector2(0, -59),
	"north": Vector2(16, -127),
	"east": Vector2(37, -75),
	"west": Vector2(-35, -75),
}

# Where a crew member's construction weld lands: the centre of the doorway between the cell they
# stand in and the cell going up, lifted to the door's middle rather than the deck. Vector2.INF
# when this actor is not building a room.
static func construction_door(game, actor) -> Vector2:
	if str(actor.goal) != "construction": return Vector2.INF
	var fleet = game.get("drone_fleet")
	if fleet == null: return Vector2.INF
	for order in fleet.orders:
		var builder := str(order.get("builder", ""))
		if builder.is_empty(): continue
		if game.get(builder + "_npc") != actor: continue
		if not order.has("work_cell"): continue
		var standing: Vector2i = order.work_cell
		var building: Vector2i = order.pos
		var middle: Vector2 = (Vector2(standing) + Vector2(building)) * 0.5 + Vector2(0.5, 0.5)
		return middle * 384.0 - Vector2(0, 34.0)
	return Vector2.INF

# Air seeping from the hull (owner playtest, Sept 29: bubbles from vents). Some exposed north, east and
# west walls (about a third, chosen by a hash of the cell) loose a slow stream of small bubbles that rise
# beside the wall and fade. South walls are skipped: from above, bubbles there would seem to rise across
# the room. Deterministic from visual time, so it freezes with pause; Reduced Motion and Low quality draw
# none; High draws a longer stream.
static func draw_hull_bubbles(canvas, game, rooms: Array, size: float) -> void:
	var quality: int = Preferences.effects_quality
	if quality == 0 or Preferences.reduced_motion: return
	var time: float = game.get_visual_time_seconds()
	var unit := size / 384.0
	var bubbles := 7 if quality >= 2 else 4
	for room in rooms:
		var cell: Vector2i = room.pos
		for side in ["north", "east", "west"]:
			var offset: Vector2i = {"north": Vector2i.UP, "east": Vector2i.RIGHT, "west": Vector2i.LEFT}[side]
			if game.occupied.has(cell + offset): continue
			if posmod(hash([cell, side, 91]), 3) != 0: continue
			var edge := (Vector2(cell) + Vector2(0.5, 0.5) + Vector2(offset) * 0.5) * size
			var along := Vector2(float(offset.y != 0) * (float(posmod(hash([cell, side, 5]), 60)) - 30.0) * unit * 4.0, 0.0)
			for i in range(bubbles):
				var cycle := 7.0
				var phase := fposmod(time / cycle + float(i) / float(bubbles) + float(posmod(hash([cell, side, 17]), 100)) / 100.0, 1.0)
				var sway := sin(time * 0.9 + float(i) * 1.7 + float(cell.x)) * 5.0 * unit
				var rise := phase * size * 0.75
				var at := edge + along + Vector2(sway + float(offset.x) * 10.0 * unit, -rise)
				var radius := (1.6 + float(posmod(hash([cell, side, i]), 20)) / 10.0) * unit * 1.6
				var fade := sin(phase * PI)
				canvas.draw_arc(at, radius, 0.0, TAU, 12, Color(0.72, 0.92, 0.98, 0.42 * fade), maxf(1.0, unit * 1.2), true)
				canvas.draw_circle(at + Vector2(-radius * 0.3, -radius * 0.3), maxf(0.6, radius * 0.22), Color(1.0, 1.0, 1.0, 0.5 * fade))

# Rooms with a cracked hull or a local containment fault vent steam and spit sparks (owner-approved,
# Sept 29). Steam is a slow rising column of soft puffs; sparks are a burst of 0.2 s once every couple
# of seconds per room, never a steady strobe. Reduced Motion draws one still puff and no sparks; Low
# quality draws nothing. Deterministic from visual time, so it freezes with pause.
static func draw_hazards(canvas, game, rooms: Array, size: float) -> void:
	var quality: int = Preferences.effects_quality
	if quality == 0: return
	var time: float = game.get_visual_time_seconds()
	var unit := size / 384.0
	var reduced: bool = Preferences.reduced_motion
	for room in rooms:
		var cracked: bool = float(room.get("hull_crack", 0)) > 0
		if not cracked and not room.get("local_incident", false): continue
		var cell: Vector2i = room.pos
		var seed := int(hash([cell, 33]) % 1000)
		var vent := (Vector2(cell) + Vector2(0.28 + float(seed % 44) / 100.0, 0.55)) * size
		var puffs := 1 if reduced else (6 if quality >= 2 else 4)
		for i in range(puffs):
			var phase := 0.35 if reduced else fposmod(time / 3.2 + float(i) / float(puffs) + float(seed) / 1000.0, 1.0)
			var at := vent + Vector2(sin(phase * 5.0 + float(i)) * 10.0 * unit, -phase * size * 0.5)
			var radius := (10.0 + phase * 26.0) * unit
			canvas.draw_circle(at, radius, Color(0.86, 0.93, 0.95, 0.22 * sin(phase * PI)))
		if reduced: continue
		var cycle := 2.3 + float(seed % 7) * 0.2
		var local := fposmod(time + float(seed) * 0.37, cycle)
		if local > 0.2: continue
		var burst := int((time + float(seed) * 0.37) / cycle)
		for i in range(7):
			var h := int(hash([seed, burst, i]))
			var angle := -PI * (0.15 + float(h % 70) / 100.0)
			var reach := (12.0 + float((h / 7) % 26)) * unit * (local / 0.2)
			var spark := vent + Vector2(cos(angle), sin(angle)) * reach + Vector2(0, reach * reach / (40.0 * unit) * 0.5)
			canvas.draw_circle(spark, maxf(1.0, unit * 2.0), Color(1.0, 0.82, 0.45, 0.9 * (1.0 - local / 0.2)))

# Build flourishes (owner-approved, Sept 29): a bright scan line sweeps down a room the moment it
# appears, and a ring of light spreads from its centre the first time the room gets power. Rooms already
# on the map when the view starts (a loaded save, several arriving at once) get neither. One gentle
# sweep and one ring per room, so nothing repeats or strobes; Reduced Motion and Low quality skip them.
const SCAN_SECONDS := 1.1
const RIPPLE_SECONDS := 1.0
static var _seen: Dictionary = {}
static var _seen_game := 0
static var _scan_start: Dictionary = {}
static var _powered: Dictionary = {}
static var _ripple_start: Dictionary = {}
static var _awaiting: Dictionary = {} # built rooms still waiting for their first power

static func draw_build_flourish(canvas, game, _rooms: Array, size: float) -> void:
	var time: float = game.get_visual_time_seconds()
	var grid = game.grid_view
	var all_rooms: Array = game.placed_rooms
	if _seen_game != game.get_instance_id():
		_seen_game = game.get_instance_id()
		_seen.clear(); _scan_start.clear(); _powered.clear(); _ripple_start.clear(); _awaiting.clear()
	var fresh: Array = []
	for room in all_rooms:
		if not _seen.has(room.pos): fresh.append(room)
	# Many rooms at once means a load or a reset, not building: register them quietly.
	var quiet: bool = fresh.size() > 2 or _seen.is_empty()
	for room in fresh:
		_seen[room.pos] = true
		_powered[room.pos] = quiet and grid._room_light_level(room) > 0.5
		if not quiet:
			_scan_start[room.pos] = time
			_awaiting[room.pos] = true
	for room in all_rooms:
		var cell: Vector2i = room.pos
		var lit: bool = grid._room_light_level(room) > 0.5
		if lit and _awaiting.has(cell):
			_awaiting.erase(cell)
			_ripple_start[cell] = time
		_powered[cell] = lit
	if Preferences.effects_quality == 0 or Preferences.reduced_motion: return
	var unit := size / 384.0
	for cell in _scan_start.keys():
		var age: float = time - float(_scan_start[cell])
		if age < 0.0 or age > SCAN_SECONDS:
			if age > SCAN_SECONDS: _scan_start.erase(cell)
			continue
		var fraction := age / SCAN_SECONDS
		var rect := Rect2(Vector2(cell) * size, Vector2.ONE * size)
		var y := rect.position.y + rect.size.y * fraction
		var fade := 1.0 - fraction * 0.6
		canvas.draw_rect(Rect2(rect.position.x, y - unit * 3.0, rect.size.x, unit * 6.0), Color(0.55, 0.95, 1.0, 0.75 * fade))
		canvas.draw_rect(Rect2(rect.position.x, rect.position.y, rect.size.x, y - rect.position.y), Color(0.4, 0.85, 1.0, 0.10 * fade))
	for cell in _ripple_start.keys():
		var age: float = time - float(_ripple_start[cell])
		if age > RIPPLE_SECONDS:
			_ripple_start.erase(cell)
			continue
		var fraction := age / RIPPLE_SECONDS
		var centre := (Vector2(cell) + Vector2(0.5, 0.5)) * size
		canvas.draw_arc(centre, size * (0.1 + 0.7 * fraction), 0.0, TAU, 40, Color(0.7, 0.98, 1.0, 0.6 * (1.0 - fraction)), maxf(1.5, unit * 5.0 * (1.0 - fraction)), true)

static func draw_torch_sparks(canvas, game, size: float) -> void:
	var actors := torch_actors(game)
	if actors.is_empty(): return
	var time: float = game.get_visual_time_seconds()
	var unit := size / 384.0
	var pixel := maxf(1.0, unit * 2.0)
	var reduced: bool = Preferences.reduced_motion
	for actor in actors:
		var facing: Vector2 = DIRECTIONS.get(str(actor.direction), Vector2.DOWN)
		# The flame in this pose, measured from the frames.
		var tip: Vector2 = (actor.foot + TORCH_TIPS.get(str(actor.direction), TORCH_TIPS.south)) / 384.0 * size
		# Building a room is work on the doorway between the two cells, not on the welder's own
		# hand: the sparks belong in the middle of that door, on whichever side the room is going
		# up (owner playtest, Sept 18). Repairs and Josh's torch keep the pose's own flame.
		var door: Vector2 = construction_door(game, actor)
		if door.is_finite(): tip = door / 384.0 * size
		var seed := int(actor.foot.x * 7.0 + actor.foot.y * 13.0)
		var flicker := 0.35 + 0.15 * float(hash([seed, floori(time * 20.0)]) % 100) / 100.0
		canvas.draw_circle(tip, unit * 10.0, Color(1.0, 0.62, 0.25, (0.3 if reduced else flicker) * 0.6))
		canvas.draw_circle(tip, unit * 3.5, Color(1.0, 0.95, 0.85, 0.9))
		var count := 3 if reduced else 11
		for i in range(count):
			var phase := fposmod(time * (0.6 if reduced else 1.8) + i * 0.113 + seed * 0.01, 1.0)
			var h := hash([seed, i, floori(time * (0.6 if reduced else 1.8) + i * 0.113 + seed * 0.01)])
			var angle := float(h % 628) / 100.0
			var speed := 14.0 + float((h / 7) % 24)
			var spray := Vector2(cos(angle), sin(angle)) * speed * phase - facing * 6.0 * phase
			var at := tip + (spray + Vector2(0, phase * phase * 22.0)) * unit
			var heat := Color(1.0, 0.97, 0.8).lerp(Color(1.0, 0.45, 0.12), phase)
			heat.a = 1.0 - phase
			at = (at / pixel).floor() * pixel
			canvas.draw_rect(Rect2(at, Vector2(pixel, pixel)), heat)
