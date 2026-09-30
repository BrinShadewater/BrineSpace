extends RefCounted
## Alien sea life outside the hull (owner playtest, Sept 29: real creatures, but this is a different
## world with different aquatic life; an alien whale may pass by now and then). Everything is drawn from
## registered artwork (with procedural fallback), deterministic from the visual clock: pause freezes it.
##
##   drifters  lantern-bells: a three-lobed glowing bell with curling tendrils, rising slowly
##   shoals    ribbon-swimmers: thin luminous ribbons that stream past together
##   whale     the tidewalker: a huge dark spindle with leaf fins, a crest of glowing sails and a
##             constellation of lights along its flanks, crossing the whole map every few minutes
##
## Drawn after the fog and before the station, so it sits in the water beneath the hull. Low quality and
## Reduced Motion draw none; High draws more. Spec: docs/superpowers/specs/2026-09-29-lighting-atmosphere-design.md

const TitleSettings = preload("res://scripts/title_settings.gd")
const SafeImage = preload("res://scripts/safe_image.gd")
const SHEETS := {
	"lantern": "res://assets/sea-life-v1/lantern-bell-body.png",
	"lantern_core": "res://assets/sea-life-v1/lantern-bell-core.png",
	"ribbon": "res://assets/sea-life-v1/ribbon-swimmer.png",
	"ribbon_core": "res://assets/sea-life-v1/ribbon-head.png",
	"body": "res://assets/sea-life-v1/tidewalker-body.png",
	"fin": "res://assets/sea-life-v1/tidewalker-fin.png",
	"sail": "res://assets/sea-life-v1/tidewalker-sail.png",
	"lights": "res://assets/sea-life-v1/tidewalker-lights.png",
	"glass": "res://assets/sea-life-v1/glass-choir-body.png",
	"glass_core": "res://assets/sea-life-v1/glass-choir-core.png",
	"veil": "res://assets/sea-life-v1/veil-kite-body.png",
	"veil_core": "res://assets/sea-life-v1/veil-kite-core.png",
}
const DIMENSIONS := {
	"lantern": Vector2i(1280,960), "lantern_core": Vector2i(1280,960),
	"ribbon": Vector2i(640,768), "ribbon_core": Vector2i(640,768),
	"body": Vector2i(1600,420), "fin": Vector2i(320,256),
	"sail": Vector2i(160,160), "lights": Vector2i(1600,420),
	"glass": Vector2i(1024,512), "glass_core": Vector2i(1024,512),
	"veil": Vector2i(1024,512), "veil_core": Vector2i(1024,512),
}
static var sheets: Dictionary = {}
static var attempted := false
static var authored_enabled := true

static func ready() -> bool:
	if attempted: return sheets.size() == SHEETS.size()
	attempted = true
	for key in SHEETS:
		var texture := SafeImage.raw_texture(SHEETS[key])
		if texture == null or Vector2i(texture.get_size()) != DIMENSIONS[key]:
			push_warning("Sea-life artwork missing or invalid; procedural fallback: " + SHEETS[key])
			continue
		sheets[key] = texture
	return sheets.size() == SHEETS.size()

static func frame(clock: float, fps: float, phase: int = 0) -> int:
	return posmod(floori(clock * fps) + phase, 8)

static func _sprite(canvas: CanvasItem, key: String, cell: Vector2, columns: int, pivot: Vector2, scale: float, clock: float, fps: float, phase: int, tint: Color) -> void:
	var index := frame(clock, fps, phase)
	canvas.draw_texture_rect_region(sheets[key], Rect2(-pivot * scale, cell * scale), Rect2(Vector2(index % columns, index / columns) * cell, cell), tint)
const PALETTE := [Color(0.25, 0.95, 0.85), Color(0.62, 0.48, 1.0), Color(1.0, 0.72, 0.32), Color(0.60, 1.0, 0.62)]
const DRIFTER_EPOCH := 80.0
const SHOAL_EPOCH := 60.0
const WHALE_PERIOD := 180.0   # seconds of game clock between whales
const WHALE_CROSSING := 110.0 # seconds one takes to cross the map
const WHALE_LENGTH := 13.0    # cells

# Tests switch the life off to measure exactly what it adds to a frame.
static var enabled := true

static var _centre_key := ""
static var _centre := Vector2(20, 20)

static func _h(a: float, b: float, c: float) -> float:
	return fposmod(sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453, 1.0)

# The middle of the station, in cells: the life keeps to the waters around it.
static func station_centre(game) -> Vector2:
	var key := "%d:%s" % [game.placed_rooms.size(), str(game.occupied.keys().size())]
	if key == _centre_key: return _centre
	_centre_key = key
	var sum := Vector2.ZERO
	for room in game.placed_rooms: sum += Vector2(room.pos)
	_centre = sum / float(maxi(1, game.placed_rooms.size())) + Vector2(0.5, 0.5)
	return _centre

static func draw(canvas: CanvasItem, game, size: float, view: Rect2) -> void:
	var quality: int = TitleSettings.effects_quality
	if not enabled or quality == 0 or TitleSettings.reduced_motion or game.placed_rooms.is_empty(): return
	var t: float = game.get_visual_time_seconds()
	var centre := station_centre(game)
	for slot in range(2 if quality >= 2 else 1):
		_draw_shoal(canvas, centre, size, view, t, slot)
	for slot in range(9 if quality >= 2 else 5):
		_draw_drifter(canvas, centre, size, view, t, slot)

# The whale passes over the station, not under it (owner playtest, Sept 29), so it is drawn by its own
# pass after the station surfaces. Everything else stays in the water beneath the hull.
static func draw_over(canvas: CanvasItem, game, size: float, view: Rect2) -> void:
	if not enabled or TitleSettings.effects_quality == 0 or TitleSettings.reduced_motion or game.placed_rooms.is_empty(): return
	_draw_whale(canvas, station_centre(game), size, view, game.get_visual_time_seconds())

# A creature's life is split into epochs; each epoch re-places it somewhere new around the station.
static func _epoch(t: float, slot: int, length: float) -> Vector3:
	var shifted := (t + float(slot) * 13.7) / length
	return Vector3(floorf(shifted), fposmod(shifted, 1.0), float(slot))

static func _fade(phase: float) -> float:
	return sqrt(clampf(sin(phase * PI), 0.0, 1.0))

static func _draw_drifter(canvas: CanvasItem, centre: Vector2, size: float, view: Rect2, t: float, slot: int) -> void:
	var e := _epoch(t, slot, DRIFTER_EPOCH)
	var seed := e.x * 3.1 + e.z * 17.0
	var base := centre + Vector2((_h(seed, 1.0, 0.0) - 0.5) * 36.0, (_h(seed, 2.0, 0.0) - 0.5) * 26.0)
	var drift := Vector2((_h(seed, 3.0, 0.0) - 0.5) * 3.0, -1.4 - _h(seed, 4.0, 0.0) * 2.0)
	var at := (base + drift * (e.y - 0.5)) * size
	var radius := (0.20 + _h(seed, 5.0, 0.0) * 0.20) * size
	if not view.grow(radius * 4.0).has_point(at): return
	var colour: Color = PALETTE[int(_h(seed, 6.0, 0.0) * 4.0) % 4]
	var fade := _fade(e.y)
	if authored_enabled and ready():
		var species: String = ["lantern", "glass", "veil"][slot % 3]
		var extra := species != "lantern"
		var cell := Vector2(256,256) if extra else Vector2(320,480)
		var pivot := Vector2(128,128) if extra else Vector2(160,160)
		var scale := radius / (110.0 if extra else 103.0)
		var rotation := sin(t * 0.16 + seed) * 0.12 if species == "veil" else (t * 0.04 if species == "glass" else 0.0)
		canvas.draw_set_transform(at, rotation)
		_sprite(canvas, species, cell, 4, pivot, scale, t, 6, slot, Color(colour.r, colour.g, colour.b, fade * 0.55))
		_sprite(canvas, species + "_core", cell, 4, pivot, scale, t, 6, slot, Color(1,1,1,fade * 0.65))
		canvas.draw_set_transform(Vector2.ZERO)
		return
	var pulse := 0.5 + 0.5 * sin(t * 1.3 + seed * 6.0)
	var height := radius * (0.80 + 0.20 * pulse)
	# Three lobes make the bell: a wide middle and two smaller shoulders, not a plain dome.
	var bell := PackedVector2Array()
	for k in range(13):
		var angle := PI + PI * float(k) / 12.0
		var lobe := 1.0 + 0.16 * cos(angle * 3.0)
		bell.append(at + Vector2(cos(angle) * radius * lobe, sin(angle) * height * lobe))
	bell.append(at + Vector2(radius * 0.7, height * 0.18))
	bell.append(at + Vector2(-radius * 0.7, height * 0.18))
	canvas.draw_colored_polygon(bell, Color(colour.r, colour.g, colour.b, 0.20 * fade))
	canvas.draw_circle(at + Vector2(0, -height * 0.25), radius * 0.42, Color(colour.r, colour.g, colour.b, (0.16 + 0.18 * pulse) * fade))
	canvas.draw_circle(at + Vector2(0, -height * 0.25), radius * 0.16, Color(1, 1, 1, 0.45 * fade))
	# Tendrils curl as they trail.
	var line_width := maxf(1.0, size * 0.012)
	for i in range(5):
		var spread := (float(i) - 2.0) * radius * 0.30
		var points := PackedVector2Array()
		for step in range(6):
			var f := float(step) / 5.0
			points.append(at + Vector2(spread + sin(t * 1.6 + f * 4.0 + float(i)) * radius * 0.22 * f, height * 0.18 + f * radius * 1.7))
		canvas.draw_polyline(points, Color(colour.r, colour.g, colour.b, 0.30 * fade), line_width, true)

static func _draw_shoal(canvas: CanvasItem, centre: Vector2, size: float, view: Rect2, t: float, slot: int) -> void:
	var e := _epoch(t, slot + 20, SHOAL_EPOCH)
	var seed := e.x * 5.7 + e.z * 11.0
	var angle := _h(seed, 1.0, 0.0) * TAU
	var direction := Vector2(cos(angle), sin(angle))
	var across := Vector2(-direction.y, direction.x)
	var head := centre + across * (_h(seed, 2.0, 0.0) - 0.5) * 22.0 + direction * (e.y * 60.0 - 30.0)
	var colour: Color = PALETTE[int(_h(seed, 3.0, 0.0) * 4.0) % 4]
	var fade := _fade(e.y)
	if not view.grow(size * 8.0).has_point(head * size): return
	if authored_enabled and ready():
		for r in range(9):
			var lane := (float(r) - 4.0) * 0.34 + sin(t * 0.7 + float(r) * 1.9) * 0.16
			var back := float(r % 3) * 0.7
			var wave := sin(t * 3.2 + float(r)) * 0.11
			var at := (head + across * (lane + wave) - direction * back) * size
			canvas.draw_set_transform(at, angle)
			_sprite(canvas, "ribbon", Vector2(640,96), 1, Vector2(604,48), size * 1.4 / 580.0, t, 10, r, Color(colour.r,colour.g,colour.b,fade * 0.6))
			_sprite(canvas, "ribbon_core", Vector2(640,96), 1, Vector2(604,48), size * 1.4 / 580.0, t, 10, r, Color(1,1,1,fade * 0.75))
		canvas.draw_set_transform(Vector2.ZERO)
		return
	var line_width := maxf(1.5, size * 0.016)
	for r in range(9):
		var lane := (float(r) - 4.0) * 0.34 + sin(t * 0.7 + float(r) * 1.9) * 0.16
		var back := float(r % 3) * 0.7
		var points := PackedVector2Array()
		for k in range(8):
			var behind := float(k) * 0.20 + back
			var wave := sin(t * 3.2 - float(k) * 0.75 + float(r)) * 0.11
			points.append((head + across * (lane + wave) - direction * behind) * size)
		canvas.draw_polyline(points, Color(colour.r, colour.g, colour.b, 0.42 * fade), line_width, true)
		canvas.draw_circle(points[0], line_width * 1.5, Color(1, 1, 1, 0.55 * fade))

static func _draw_whale(canvas: CanvasItem, centre: Vector2, size: float, view: Rect2, t: float) -> void:
	var epoch := floorf(t / WHALE_PERIOD)
	var local := t - epoch * WHALE_PERIOD
	if local > WHALE_CROSSING: return
	var frac := local / WHALE_CROSSING
	var seed := epoch * 7.3
	var angle := _h(seed, 1.0, 0.0) * TAU
	var direction := Vector2(cos(angle), sin(angle))
	var across := Vector2(-direction.y, direction.x)
	var at := (centre + across * (_h(seed, 2.0, 0.0) - 0.5) * 16.0 + direction * (frac * 84.0 - 42.0)) * size
	var reach := WHALE_LENGTH * size * 0.6
	if not view.grow(reach).has_point(at): return
	var fade := smoothstep(0.0, 0.08, frac) * (1.0 - smoothstep(0.92, 1.0, frac))
	if authored_enabled and ready():
		_draw_authored_whale(canvas, at, direction.angle(), size, t, fade)
		return
	canvas.draw_set_transform(at, direction.angle(), Vector2.ONE * size)
	var body_colour := Color(0.05, 0.11, 0.20, 0.72 * fade)
	# Spindle body, mirrored top and bottom, ending in a forked tail. x runs nose to tail.
	var top := [Vector2(6.5, 0.0), Vector2(5.6, -0.9), Vector2(3.4, -1.55), Vector2(0.0, -1.75), Vector2(-3.4, -1.3), Vector2(-5.6, -0.55), Vector2(-6.2, -0.28), Vector2(-7.6, -1.25)]
	var outline := PackedVector2Array()
	for point in top: outline.append(point)
	outline.append(Vector2(-6.8, 0.0))
	for i in range(top.size() - 1, -1, -1): outline.append(Vector2(top[i].x, -top[i].y))
	canvas.draw_colored_polygon(outline, body_colour)
	# A pale rim so the silhouette reads against dark water.
	var rim := PackedVector2Array(outline)
	rim.append(outline[0])
	canvas.draw_polyline(rim, Color(0.30, 0.65, 0.75, 0.30 * fade), 0.05, true)
	# Leaf fins, three pairs, waving slowly out of step.
	for pair in range(3):
		var x := 2.6 - float(pair) * 3.1
		var sway := sin(t * 0.5 + float(pair) * 1.4) * 0.25
		for side in [-1.0, 1.0]:
			var root := Vector2(x, side * 1.35)
			var tip := Vector2(x - 1.7, side * (2.6 + sway))
			var mid := Vector2(x - 0.4, side * (2.3 + sway * 0.5))
			canvas.draw_colored_polygon(PackedVector2Array([root, mid, tip, root + Vector2(-1.1, 0.0)]), Color(body_colour.r, body_colour.g, body_colour.b, 0.5 * fade))
	# A crest of sails along the back, each with a glowing tip.
	for s in range(7):
		var sx := 4.2 - float(s) * 1.35
		var sail := 0.40 + 0.18 * sin(t * 0.9 + float(s))
		canvas.draw_colored_polygon(PackedVector2Array([Vector2(sx, -1.6), Vector2(sx - 0.5, -1.6 - sail), Vector2(sx - 1.0, -1.55)]), Color(0.10, 0.20, 0.32, 0.55 * fade))
		canvas.draw_circle(Vector2(sx - 0.5, -1.6 - sail), 0.05, Color(0.55, 0.95, 1.0, (0.35 + 0.3 * sin(t * 1.3 + float(s) * 0.8)) * fade))
	# Constellations of lights along the flanks.
	for i in range(26):
		var lx := 5.3 - float(i) * 0.42
		var ly := (0.55 if i % 2 == 0 else -0.45) * (0.4 + 0.6 * cos(lx * 0.16))
		var glow := 0.5 + 0.5 * sin(t * 0.8 + float(i) * 0.9)
		var colour: Color = PALETTE[i % 4]
		canvas.draw_circle(Vector2(lx, ly), 0.03 + 0.02 * glow, Color(colour.r, colour.g, colour.b, (0.25 + 0.4 * glow) * fade))
	canvas.draw_set_transform(Vector2.ZERO)

const FIN_ROOTS := [Vector2(1047,119), Vector2(1047,307), Vector2(753,133), Vector2(753,294), Vector2(459,196), Vector2(459,227)]
const SAIL_ROOTS := [Vector2(1198,161), Vector2(1070,130), Vector2(942,98), Vector2(814,128), Vector2(686,150), Vector2(558,185), Vector2(430,189)]
const LIGHT_POSITIONS := [Vector2(1303,227), Vector2(1263,195), Vector2(1223,239), Vector2(1183,186), Vector2(1143,252), Vector2(1104,179), Vector2(1064,262), Vector2(1024,166), Vector2(984,278), Vector2(944,160), Vector2(904,280), Vector2(864,165), Vector2(825,267), Vector2(785,174), Vector2(745,259), Vector2(705,180), Vector2(665,244), Vector2(625,193), Vector2(586,234), Vector2(546,199), Vector2(506,223), Vector2(466,202), Vector2(426,226), Vector2(386,189), Vector2(347,263), Vector2(307,153)]

static func _draw_authored_whale(canvas: CanvasItem, at: Vector2, angle: float, size: float, t: float, fade: float) -> void:
	var unit := size / 94.84615384615384
	# Fins sit behind the body, registered four pixels inside its actual rim.
	for i in range(6):
		var side := -1.0 if i % 2 == 0 else 1.0
		var sway := sin(t * 0.5 + float(i / 2) * 1.4) * 0.12 * side
		var root: Vector2 = (FIN_ROOTS[i] - Vector2(800,210)) * unit
		canvas.draw_set_transform(at + root.rotated(angle), angle + sway, Vector2(unit,unit * side))
		canvas.draw_texture_rect(sheets.fin, Rect2(-Vector2(299,18),Vector2(320,256)), false, Color(1,1,1,0.55 * fade))
	canvas.draw_set_transform(at, angle, Vector2.ONE * unit)
	canvas.draw_texture_rect(sheets.body, Rect2(Vector2(-800,-210),Vector2(1600,420)), false, Color(1,1,1,0.72 * fade))
	for i in range(7):
		var root: Vector2 = SAIL_ROOTS[i] - Vector2(800,210)
		var pulse := 0.8 + 0.12 * sin(t * 0.9 + float(i))
		var scale := Vector2(0.8,0.65 * pulse)
		canvas.draw_texture_rect(sheets.sail, Rect2(root - Vector2(80,148) * scale,Vector2(160,160) * scale), false, Color(1,1,1,0.65 * fade))
	for i in range(26):
		var glow := 0.5 + 0.5 * sin(t * 0.8 + float(i) * 0.9)
		var point: Vector2 = LIGHT_POSITIONS[i]
		var colour: Color = PALETTE[i % 4]
		canvas.draw_texture_rect_region(sheets.lights, Rect2(point - Vector2(800,210) - Vector2(10,10),Vector2(20,20)), Rect2(point - Vector2(10,10),Vector2(20,20)), Color(colour.r,colour.g,colour.b,(0.25 + 0.4 * glow) * fade))
	canvas.draw_set_transform(Vector2.ZERO)
