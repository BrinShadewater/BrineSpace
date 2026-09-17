extends RefCounted
## Bioluminescent seabed plants (owner playtest, Sept 17: the darkness outside needed glowing
## life). Plant clumps grow on open seabed a short swim from the station, chosen by a stable hash
## of the cell so they never jump between frames or saves. The terrain pass draws their stems and
## bulbs; the fog shader adds a slow pulsing glow at each clump so they show through dark water.

const Field = preload("res://scripts/wreck_field.gd")
const PALETTE := [Color("3ef2d0"), Color("9d7bff"), Color("4fb4ff"), Color("7dffa6"), Color("ff7ad9")]
const MAX_GLOWS := 32
const CHANCE := 0.16

static var _cache_key := ""
static var _cache: Array = []

static func _hash(cell: Vector2i, salt: float) -> float:
	return fposmod(sin(float(cell.x) * 127.1 + float(cell.y) * 311.7 + salt * 74.7) * 43758.5453, 1.0)

# Clumps: {cell, position (in cells), color, stems, phase}.
static func spots(game) -> Array:
	var key := "%d:%d:%d" % [game.placed_rooms.size(), game.wrecks.size(), hash(game.occupied.keys())]
	if key == _cache_key: return _cache
	_cache_key = key
	_cache = []
	if game.placed_rooms.is_empty(): return _cache
	for x in range(40):
		for y in range(40):
			var cell := Vector2i(x, y)
			if game.occupied.has(cell) or game.wrecks.has(cell) or Field.blocks(game.wrecks, cell): continue
			if _hash(cell, 1.0) > CHANCE: continue
			var nearest := 99
			for room in game.placed_rooms:
				nearest = mini(nearest, absi(room.pos.x - x) + absi(room.pos.y - y))
			if nearest < 1 or nearest > 6: continue
			var position := Vector2(cell) + Vector2(0.2 + _hash(cell, 2.0) * 0.6, 0.35 + _hash(cell, 3.0) * 0.5)
			_cache.append({"cell": cell, "position": position, "color": PALETTE[int(_hash(cell, 4.0) * PALETTE.size()) % PALETTE.size()], "stems": 3 + int(_hash(cell, 5.0) * 4.0), "phase": _hash(cell, 6.0) * TAU})
	return _cache

# Stems and glowing bulbs, drawn in the static terrain pass below the fog.
static func draw_plants(canvas: CanvasItem, game, size: float) -> void:
	for spot in spots(game):
		var base: Vector2 = spot.position * size
		var color: Color = spot.color
		for i in range(int(spot.stems)):
			var lean := (float(i) - float(spot.stems - 1) * 0.5) * 0.28 + (_hash(spot.cell, 10.0 + i) - 0.5) * 0.3
			var height := size * (0.07 + _hash(spot.cell, 20.0 + i) * 0.07)
			var tip := base + Vector2(sin(lean) * height, -cos(lean) * height)
			var bend := base.lerp(tip, 0.55) + Vector2(lean * size * 0.02, 0)
			var stem := PackedVector2Array([base, bend, tip])
			canvas.draw_polyline(stem, color.darkened(0.55), maxf(1.0, size * 0.006), true)
			canvas.draw_circle(tip, maxf(1.5, size * (0.008 + _hash(spot.cell, 30.0 + i) * 0.007)), color.lightened(0.35))
			canvas.draw_circle(bend, maxf(1.0, size * 0.004), color)
		canvas.draw_circle(base, maxf(1.5, size * 0.012), color.darkened(0.7))

# Up to MAX_GLOWS clumps nearest the view centre, for the fog shader.
static func glow_uniforms(game, center: Vector2) -> Array:
	var list: Array = spots(game).duplicate()
	list.sort_custom(func(a, b): return a.position.distance_squared_to(center) < b.position.distance_squared_to(center))
	var glows := PackedVector4Array()
	var colors := PackedVector4Array()
	for i in range(MAX_GLOWS):
		if i < list.size():
			glows.append(Vector4(list[i].position.x, list[i].position.y - 0.08, 0.34, list[i].phase))
			colors.append(Vector4(list[i].color.r, list[i].color.g, list[i].color.b, 1.0))
		else:
			glows.append(Vector4.ZERO)
			colors.append(Vector4.ZERO)
	return [glows, colors, mini(MAX_GLOWS, list.size())]
