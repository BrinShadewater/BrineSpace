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

static func draw_torch_sparks(canvas, game, size: float) -> void:
	var actors := torch_actors(game)
	if actors.is_empty(): return
	var time: float = game.get_visual_time_seconds()
	var unit := size / 384.0
	var pixel := maxf(1.0, unit * 2.0)
	var reduced: bool = Preferences.reduced_motion
	for actor in actors:
		var facing: Vector2 = DIRECTIONS.get(str(actor.direction), Vector2.DOWN)
		# Hand height, a little ahead of the body in the facing direction.
		var tip: Vector2 = (actor.foot + facing * 26.0 + Vector2(0, -30.0 if facing.y >= 0 else -44.0)) / 384.0 * size
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
