extends Node2D
## Layered nursery renderer; embedded hosts own position, state, and connections.
const Geometry = preload("res://tools/modular_room_geometry.gd")
@export var embedded := false
var show_actor := true
var painter: CanvasItem = self
var external_actor_texture: Texture2D
var quarter := 0
var individual := [0, 0]
var layout: Array
var structure: Array
var furnishings: Array
var actor := Vector2.ZERO
var actor_direction := "south"
var actor_clock := 0.0
var actor_walking := false
var actor_frames := {}
var debug := false
var paused := false
var operating := true
var phase := 0.0
var font := ThemeDB.fallback_font
var ivory := Color("c6bfa9")
var teal := Color("69b7aa")
var world_scale := 1.0
var origin := Vector2.ZERO
var art := {}
var use_art := true
var layered_rack := true
var rack_board := false
var focus_art := false
var last_asset_rect := Rect2()
const ART_ROOT := "res://rooms/modular/art-trial-01/"

func _ready() -> void:
	var errors := Geometry.recipe_errors(Geometry.recipe)
	if not errors.is_empty():
		push_error("Cannot load nursery view: " + str(errors))
		set_process(false)
		set_process_unhandled_key_input(false)
		hide()
		return
	load_art()
	if embedded:
		set_process(false)
		set_process_unhandled_key_input(false)
		show_actor = false
		configure_embedded(0, [], false, 0.0)
	else:
		load_actor_art()
		rebuild()

## Sides use screen-space N/E/S/W = 0/1/2/3. Host resolves adjacency once.
## This view never advances external clocks or reads gameplay resources/saves.
func configure_embedded(q: int, open_sides: Array, running: bool, time_seconds: float, omitted_sides: Array = []) -> void:
	embedded = true
	show_actor = false
	external_actor_texture = null
	set_process(false)
	set_process_unhandled_key_input(false)
	quarter = posmod(q, 4)
	operating = running
	phase = time_seconds
	focus_art = true
	layout = [{"cell": Vector2i.ZERO, "rotation": quarter, "kind": 0}]
	furnishings = Geometry.props(layout)
	structure = Geometry.edges(layout)
	for side in range(4):
		structure[side].open = open_sides.has(side) and Geometry.has_port(layout[0], side)
	# Omit an edge only when its shared assembly belongs to another host view.
	for side in range(3, -1, -1):
		if omitted_sides.has(side):
			structure.remove_at(side)
	queue_redraw()

## Called only inside the host CanvasItem's draw notification.
func render_into(target: CanvasItem, at: Vector2, world_to_host: float, floor_only := false, include_floor := true) -> void:
	painter = target
	painter.draw_set_transform(at, 0.0, Vector2.ONE * world_to_host)
	if floor_only:
		draw_floor_layers()
	else:
		draw_world_layers(include_floor)
	painter.draw_set_transform(Vector2.ZERO)
	painter = self

func load_actor_art() -> void:
	for state in ["idle", "walk"]:
		var folder := "Breathing_Idle-70a80927" if state == "idle" else "Walking-5c23139e"
		for direction in ["east", "south-east", "south", "south-west", "west", "north-west", "north", "north-east"]:
			var frames: Array[Texture2D] = []
			# Existing diagonal idle art is a static rotation, not a missing animation.
			var static_idle: bool = state == "idle" and "-" in direction
			for frame in range(1 if static_idle else (4 if state == "idle" else 6)):
				var source := Image.new()
				var path := "res://character/Major_Bill/animations/%s/%s/frame_%03d.png" % [folder, direction, frame]
				if static_idle:
					path = "res://character/Major_Bill/rotations/%s.png" % direction
				if source.load_png_from_buffer(FileAccess.get_file_as_bytes(path)) != OK:
					push_error("Missing actor frame: " + path)
					continue
				frames.append(ImageTexture.create_from_image(source))
			actor_frames[state + "/" + direction] = frames
	print("ACTOR LOAD: %d directional animation tracks" % actor_frames.size())

func load_art() -> void:
	for art_root in Geometry.recipe.asset_roots:
		load_art_root(str(art_root))

func load_art_root(art_root: String) -> void:
	var path := art_root + "registration.json"
	if not FileAccess.file_exists(path):
		return
	var registration = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not registration is Dictionary or not registration.get("assets") is Dictionary:
		push_error("Invalid modular art registration")
		return
	for name in registration.assets:
		var record: Dictionary = registration.assets[name]
		if not bool(record.get("enabled_in_pilot", false)):
			continue
		var source := Image.new()
		if source.load(art_root + str(record.file)) != OK:
			push_error("Cannot load modular art: " + str(name))
			continue
		var b: Array = record.bounds
		var region := Rect2(float(b[0]), float(b[1]), float(b[2]) - float(b[0]), float(b[3]) - float(b[1]))
		art[name] = {"texture": ImageTexture.create_from_image(source), "region": region, "directions": record.get("directions", [])}
		if record.has("pivot_normalized"):
			art[name].pivot = Vector2(record.pivot_normalized[0], record.pivot_normalized[1])
			art[name].world_size = Vector2(record.world_size[0], record.world_size[1])
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	texture_repeat = CanvasItem.TEXTURE_REPEAT_ENABLED
	print("ART LOAD: %d registered textures; collision contract unchanged" % art.size())

func asset_supports(name: String, facing: int) -> bool:
	if not art.has(name):
		return false
	# JSON numbers are floats; normalize before matching integer orientations.
	for direction in art[name].directions:
		if int(direction) == facing:
			return true
	return false

func paint_asset(name: String, box: Rect2) -> bool:
	if not use_art or not art.has(name):
		return false
	var record: Dictionary = art[name]
	var region: Rect2 = record.region
	var scale_factor := minf(box.size.x / region.size.x, box.size.y / region.size.y)
	var size := region.size * scale_factor
	# Preserve aspect ratio; ground anchor is bottom-center of the fixed visual box.
	var target := Rect2(Vector2(box.get_center().x - size.x * 0.5, box.end.y - size.y), size)
	last_asset_rect = target
	painter.draw_texture_rect_region(record.texture, target, region)
	return true

func paint_registered_prop(name: String, anchor: Vector2, facing: int) -> bool:
	if not use_art or not asset_supports(name, facing) or not art[name].has("pivot"):
		return false
	var record: Dictionary = art[name]
	var target := Rect2(anchor - record.pivot * record.world_size, record.world_size)
	painter.draw_texture_rect_region(record.texture, target, record.region)
	return true

func paint_material(name: String, rect: Rect2, facing: int = 0, tint := Color.WHITE, uv_offset := Vector2.ZERO) -> void:
	if not use_art or not art.has(name):
		return
	var corners := PackedVector2Array([rect.position, rect.position + Vector2(rect.size.x, 0), rect.end, rect.position + Vector2(0, rect.size.y)])
	var uv := PackedVector2Array()
	for p in corners:
		# Uniform texel density, not a stretched whole image per rectangle.
		uv.append(Geometry.turn(p, -facing) / 128.0 + uv_offset)
	painter.draw_polygon(corners, PackedColorArray([tint]), uv, art[name].texture)

func rebuild() -> void:
	layout = Geometry.rooms(quarter, individual)
	structure = Geometry.edges(layout)
	furnishings = Geometry.props(layout)
	actor = Vector2.ZERO
	queue_redraw()

func _unhandled_key_input(event: InputEvent) -> void:
	if not event is InputEventKey or not event.pressed or event.echo:
		return
	match event.keycode:
		KEY_R:
			quarter = (quarter + 1) % 4
			rebuild()
		KEY_1, KEY_2:
			var index := 0 if event.keycode == KEY_1 else 1
			individual[index] = (individual[index] + 1) % 4
			rebuild()
		KEY_TAB:
			debug = not debug
		KEY_G:
			use_art = not use_art
		KEY_L:
			layered_rack = not layered_rack
		KEY_B:
			rack_board = not rack_board
		KEY_F:
			focus_art = not focus_art
		KEY_SPACE:
			paused = not paused
		KEY_O:
			operating = not operating
		KEY_HOME:
			quarter = 0
			individual = [0, 0]
			rebuild()
	queue_redraw()

func _process(delta: float) -> void:
	if not paused:
		actor_clock += delta
		var previous_actor := actor
		if operating:
			phase += delta
		var motion := Vector2(float(Input.is_physical_key_pressed(KEY_D) or Input.is_physical_key_pressed(KEY_RIGHT)) - float(Input.is_physical_key_pressed(KEY_A) or Input.is_physical_key_pressed(KEY_LEFT)), float(Input.is_physical_key_pressed(KEY_S) or Input.is_physical_key_pressed(KEY_DOWN)) - float(Input.is_physical_key_pressed(KEY_W) or Input.is_physical_key_pressed(KEY_UP)))
		motion = motion.normalized() * minf(delta, 0.05) * 130.0
		# Small substeps prevent tunneling; independent axes allow wall sliding.
		for unused in range(4):
			for offset in [Vector2(motion.x / 4.0, 0), Vector2(0, motion.y / 4.0)]:
				if Geometry.can_stand(actor + offset, layout, furnishings, structure):
					actor += offset
		actor_walking = actor.distance_to(previous_actor) > 0.001
		if motion.length_squared() > 0:
			var direction_index := posmod(roundi(motion.angle() / (PI / 4)), 8)
			actor_direction = ["east", "south-east", "south", "south-west", "west", "north-west", "north", "north-east"][direction_index]
	queue_redraw()

func label(at: Vector2, text: String, size: int, color := Color("b7c8cf")) -> void:
	painter.draw_string(font, at, text, HORIZONTAL_ALIGNMENT_LEFT, -1, size, color)

func _draw() -> void:
	if embedded:
		draw_world_layers()
		return
	var viewport := get_viewport_rect().size
	painter.draw_rect(Rect2(Vector2.ZERO, viewport), Color("10191f"))
	label(Vector2(32, 42), "BRINE / MODULAR ROOM LAB", 26, Color("ece4cf"))
	label(Vector2(32, 71), "Mycelium nursery / full layered-prop study / fixed camera, procedural materials", 16)
	if rack_board:
		var row_height := (viewport.y - 150) * 0.5
		var board_scale := minf((viewport.x * 0.5 - 80) / 140, row_height / 170)
		for q in range(4):
			var center := Vector2(viewport.x * (0.25 + (q % 2) * 0.5), 110 + (q / 2 + 0.5) * row_height)
			var size := Vector2(102, 74) if q % 2 == 0 else Vector2(74, 102)
			painter.draw_set_transform(center, 0, Vector2.ONE * board_scale)
			draw_layered_rack({"rect": Rect2(-size * 0.5, size), "facing": q})
			painter.draw_set_transform(Vector2.ZERO)
			label(center + Vector2(-70, row_height * 0.42), ["SOUTH / 0", "WEST / 90", "NORTH / 180", "EAST / 270"][q], 20)
		label(Vector2(32, viewport.y - 15), "B  Room / four-view board    |    Upright growth + fixed-screen lighting    |    No flattened sprite rotation", 16)
		return
	var bounds := Rect2(Vector2.ONE * -200, Vector2.ONE * 400)
	for room in layout:
		bounds = bounds.merge(Rect2(Vector2(room.cell) * Geometry.CELL - Vector2.ONE * 200, Vector2.ONE * 400))
	if focus_art:
		bounds = Rect2(-200, -200, 400, 450)
	world_scale = minf((viewport.x - 390) / bounds.size.x, (viewport.y - 155) / bounds.size.y)
	origin = Vector2((viewport.x - 310) * 0.5, (viewport.y + 65) * 0.5) - bounds.get_center() * world_scale
	painter.draw_set_transform(origin, 0, Vector2.ONE * world_scale)
	draw_world_layers()
	painter.draw_set_transform(Vector2.ZERO)
	painter.draw_rect(Rect2(0, 0, viewport.x, 88), Color("10191f"))
	label(Vector2(32, 42), "BRINE / MYCELIUM NURSERY", 26, Color("ece4cf"))
	label(Vector2(32, 71), "Full room study / layered props, clear routes and separate functioning effects", 16)
	var panel_x := viewport.x - 282
	painter.draw_rect(Rect2(panel_x - 18, 100, 280, viewport.y - 130), Color("17242c"))
	label(Vector2(panel_x, 135), "STRUCTURAL CONTRACT", 17, ivory)
	var lines := ["Cell: 384 world units", "Clear opening: 96 units", "Wall band: 16 units", "Door center: edge midpoint", "One owner per shared edge", "", "WASD / arrows   Walk", "R   Rotate connected pair", "1 / 2   Rotate single room", "Home   Reset layout", "Tab   Collision / depth guides", "O   Machinery on / off", "Space   Pause", "", "Pair orientation: %d degrees" % (quarter * 90), "Machinery: " + ("RUNNING" if operating else "OFFLINE"), "Clock: " + ("PAUSED" if paused else "LIVE"), "", "Coral marker = closed edge", "Teal marker = shared opening", "", "No player save is loaded.", "No gameplay costs changed."]
	var line_height := minf(25, (viewport.y - 200) / 28)
	for i in range(lines.size()):
		label(Vector2(panel_x, 169 + i * line_height), lines[i], 14)
	var control_y := 169 + (lines.size() + 1) * line_height
	label(Vector2(panel_x, control_y), "G   Art / geometry comparison", 14)
	label(Vector2(panel_x, control_y + line_height), "F   Detail zoom (nursery origin)", 14)
	label(Vector2(panel_x, control_y + line_height * 2), "L   Layered props / prior study", 14)
	label(Vector2(panel_x, control_y + line_height * 3), "B   Four-view layered board", 14, Color("dfac7c"))

func draw_floor_layers() -> void:
	for room in layout:
		if focus_art and room.kind != 0:
			continue
		var center := Vector2(room.cell) * Geometry.CELL
		painter.draw_rect(Rect2(center - Vector2.ONE * 192, Vector2.ONE * 384), Color("303740"))
		for x in range(-3, 3):
			for y in range(-3, 3):
				var tile := Rect2(center + Vector2(x, y) * 64 + Vector2.ONE, Vector2.ONE * 62)
				painter.draw_rect(tile, Color("343b44") if (x + y) % 2 else Color("323943"))
				if room.kind == 0:
					var local_tile := Geometry.turn(tile.get_center() - center, -room.rotation) / 64.0
					var tile_seed := posmod(floori(local_tile.x) * 73 + floori(local_tile.y) * 41, 17)
					# Stable room-local material sampling, not a repeated stain every two tiles.
					paint_material("floor", tile, room.rotation, Color.WHITE, Vector2(tile_seed * 0.137, tile_seed * 0.239))
		if room.kind == 0:
			draw_nursery_floor(room)
		if not embedded:
			label(center + Vector2(-68, 45), "01 / MYCELIUM" if room.kind == 0 else "02 / RECLAMATION", 12, Color("8b949b"))
	for prop in furnishings:
		if focus_art and prop.room != 0:
			continue
		painter.draw_rect(prop.rect.grow(4), Color(0, 0, 0, 0.17))

func draw_world_layers(include_floor := true) -> void:
	if include_floor:
		draw_floor_layers()
	var queue := furnishings.duplicate()
	if show_actor:
		queue.append({"kind": "actor", "sort_y": actor.y})
	for edge in structure:
		if focus_art and (absf(edge.center.x) > 193 or absf(edge.center.y) > 193):
			continue
		for rect in Geometry.wall_rects(edge):
			queue.append({"kind": "wall", "rect": rect, "horizontal": edge.horizontal, "sort_y": rect.end.y})
		if edge.open:
			for jamb in Geometry.jamb_rects(edge):
				queue.append({"kind": "jamb", "rect": jamb, "sort_y": jamb.end.y})
	queue.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return float(a.sort_y) < float(b.sort_y))
	for item in queue:
		if item.kind == "actor":
			draw_actor()
		elif item.kind == "wall":
			draw_wall_piece(item.rect, item.horizontal)
		elif item.kind == "jamb":
			paint_asset("jamb", item.rect)
		else:
			if focus_art and item.room != 0:
				continue
			draw_prop(item)
	for edge in structure:
		if focus_art and (absf(edge.center.x) > 193 or absf(edge.center.y) > 193):
			continue
		if edge.open:
			var axis := Vector2.RIGHT if edge.horizontal else Vector2.DOWN
			for sign_value in [-1, 1]:
				var end: Vector2 = edge.center + axis * (Geometry.OPENING * 0.5 + 3) * sign_value
				painter.draw_circle(end, 3, teal)
		if debug:
			painter.draw_circle(edge.center, 4, teal if edge.open else Color("cf795f"))
	if debug:
		for prop in furnishings:
			painter.draw_rect(prop.rect, Color("e3a568"), false, 1)
			painter.draw_line(Vector2(prop.rect.position.x, prop.sort_y), Vector2(prop.rect.end.x, prop.sort_y), teal, 2)
		painter.draw_circle(actor, Geometry.RADIUS, Color("ffcb76"), false, 1)


func draw_wall_piece(rect: Rect2, horizontal: bool) -> void:
	painter.draw_rect(rect, Color("151e25"))
	painter.draw_rect(rect.grow(-1), Color("797a73"))
	painter.draw_rect(rect.grow(-3), ivory)
	paint_material("enamel", rect.grow(-3), quarter)
	var span: float = rect.size.x if horizontal else rect.size.y
	for s in range(20, int(span) - 8, 36):
		var p := rect.position + (Vector2(s, 3) if horizontal else Vector2(3, s))
		painter.draw_line(p, p + (Vector2(0, 10) if horizontal else Vector2(10, 0)), Color("9b998c"), 1)
		painter.draw_circle(p + Vector2(3, 3), 1, Color("efdfbd"))

func draw_actor() -> void:
	paint_ellipse(actor + Vector2(0, -1), Vector2(10, 4), Color(0, 0, 0, 0.3))
	if external_actor_texture != null:
		if external_actor_texture.get_meta("major_bill_v2", false):
			var pixel_scale := 65.28 / 74.0
			var pivot: Vector2 = external_actor_texture.get_meta("crew_pivot", Vector2(46, 86))
			painter.draw_texture_rect(external_actor_texture, Rect2(actor - pivot * pixel_scale, external_actor_texture.get_size() * pixel_scale), false)
			return
		painter.draw_texture_rect_region(external_actor_texture, Rect2(actor - Vector2(23.04, 65.28), Vector2(46.08, 65.28)), Rect2(26, 18, 40, 56))
		return
	var key := ("walk/" if actor_walking else "idle/") + actor_direction
	if actor_frames.has(key) and not actor_frames[key].is_empty():
		var frames: Array = actor_frames[key]
		var frame := int(actor_clock * (6 if actor_walking else 3)) % frames.size()
		# Shared 92px canvas; fixed feet at (46,68), no per-frame tight fitting.
		painter.draw_texture_rect(frames[frame], Rect2(actor - Vector2(34.5, 51), Vector2(69, 69)), false)
		return
	painter.draw_line(actor + Vector2(-3, -2), actor + Vector2(-3, -11), Color("bec8c7"), 4)
	painter.draw_line(actor + Vector2(3, -2), actor + Vector2(3, -11), Color("bec8c7"), 4)
	painter.draw_rect(Rect2(actor + Vector2(-8, -24), Vector2(16, 15)), Color("db9b68"))
	painter.draw_circle(actor + Vector2(0, -29), 8, Color("ddd5be"))
	painter.draw_rect(Rect2(actor + Vector2(-6, -32), Vector2(12, 5)), Color("385563"))

func paint_ellipse(center: Vector2, radius: Vector2, color: Color) -> void:
	var points := PackedVector2Array()
	for i in range(32):
		points.append(center + Vector2(cos(i * TAU / 32), sin(i * TAU / 32)) * radius)
	painter.draw_colored_polygon(points, color)

func draw_prop(prop: Dictionary) -> void:
	var footprint: Rect2 = prop.rect
	if layered_rack and prop.get("room", -1) == 0 and prop.kind != "rack":
		draw_nursery_prop(prop)
		return
	if prop.kind == "rack" and layered_rack:
		draw_layered_rack(prop)
		return
	if prop.kind == "rack":
		var names := ["rack-south", "rack-west", "rack-north", "rack-east"]
		var visual_box := Rect2(footprint.position - Vector2(0, 23), footprint.size + Vector2(0, 23))
		if paint_asset(names[prop.facing], visual_box):
			# Functioning effect is separate from the offline texture.
			if operating:
				var anchor := last_asset_rect.position + last_asset_rect.size * Vector2(0.87, 0.44)
				painter.draw_arc(anchor, 5, phase * 2, phase * 2 + PI, 10, teal, 1.5)
			return
	var height := 32.0 if prop.kind == "tank" else 23.0
	var top := Rect2(footprint.position - Vector2(0, height), footprint.size)
	var front := Rect2(Vector2(footprint.position.x, top.end.y), Vector2(footprint.size.x, height))
	# Camera remains fixed: only footprints and local surface details rotate.
	painter.draw_rect(front, Color("797f7b"))
	painter.draw_rect(top.grow(2), Color("1d252c"))
	painter.draw_rect(top, ivory)
	if prop.kind == "tank":
		painter.draw_rect(front.grow(-7), Color("456e77"))
		paint_ellipse(top.get_center(), top.size * 0.49, Color("9caaa6"))
		paint_ellipse(top.get_center(), top.size * 0.35, Color("44626a"))
		paint_ellipse(top.get_center(), top.size * 0.28, Color("65918f"))
	elif prop.kind == "rack":
		for i in range(3):
			var stripe := Rect2(top.position + Vector2(7, 6 + i * (top.size.y - 12) / 3), Vector2(top.size.x - 14, (top.size.y - 18) / 3))
			if prop.facing % 2:
				stripe = Rect2(top.position + Vector2(6 + i * (top.size.x - 12) / 3, 7), Vector2((top.size.x - 18) / 3, top.size.y - 14))
			painter.draw_rect(stripe, Color("303c3e"))
			for j in range(5):
				var p := stripe.position + stripe.size * Vector2((j + 0.6) / 5, 0.52)
				if prop.facing % 2:
					p = stripe.position + stripe.size * Vector2(0.52, (j + 0.6) / 5)
				painter.draw_circle(p, 4, Color("e1d9b9"))
	elif prop.kind == "filter":
		for i in range(3):
			var p := top.get_center() + Geometry.turn(Vector2((i - 1) * 22, 0), prop.facing)
			painter.draw_circle(p, 10, Color("48565a"))
			painter.draw_circle(p, 6, Color("9ab4aa"))
	else:
		var center := top.get_center()
		painter.draw_rect(Rect2(center - Vector2(18, 12), Vector2(36, 24)), Color("4b6067"))
		painter.draw_circle(center + Geometry.turn(Vector2(29, -13), prop.facing), 7, Color("dce0cc"))
		painter.draw_line(front.position + Vector2(8, 5), front.end - Vector2(8, 5), Color("4b5152"), 3)
	var anchor := top.get_center() + Geometry.turn(Vector2(0, 15), prop.facing)
	painter.draw_circle(anchor, 3, teal if operating else Color("475652"))
	if operating:
		painter.draw_arc(anchor, 6, phase * 2, phase * 2 + PI, 10, teal, 1.5)

# Only ground anchors rotate. Every vertical layer projects screen-up.
func rack_point(prop: Dictionary, local: Vector2, elevation: float) -> Vector2:
	return prop.rect.get_center() + Geometry.turn(local, prop.facing) - Vector2(0, elevation)

func rack_panel(prop: Dictionary, local: Rect2, elevation: float, color: Color) -> void:
	var points := PackedVector2Array()
	for corner in [local.position, local.position + Vector2(local.size.x, 0), local.end, local.position + Vector2(0, local.size.y)]:
		points.append(rack_point(prop, corner, elevation))
	painter.draw_colored_polygon(points, color)

func draw_layered_rack(prop: Dictionary) -> void:
	var footprint: Rect2 = prop.rect
	var top := Rect2(footprint.position - Vector2(0, 23), footprint.size)
	var face := Rect2(Vector2(top.position.x, top.end.y), Vector2(top.size.x, 23))
	# Chassis, fixed-screen bevels, and the visible vertical side.
	painter.draw_rect(face, Color("20232d"))
	painter.draw_rect(face.grow(-2), Color("8d897d"))
	painter.draw_rect(top, Color("242631"))
	painter.draw_rect(top.grow(-2), Color("b3aa96"))
	painter.draw_rect(top.grow(-4), Color("e2d5b9"))
	paint_material("enamel", top.grow(-4), prop.facing)
	paint_material("enamel", face.grow(-2), prop.facing, Color("a3a5a3"))
	cabinet_face_details(prop, face, true)
	painter.draw_line(top.position + Vector2(3, 3), top.position + Vector2(top.size.x - 3, 3), Color("fff0cf"), 2)
	# Local patches stay attached to the physical chassis, not the screen.
	rack_panel(prop, Rect2(-45, 31, 24, 5), 23, Color("9b9383"))
	for i in range(3):
		var y := -24.0 + i * 24.0
		rack_panel(prop, Rect2(-44, y - 9, 88, 18), 24, Color("777774"))
		rack_panel(prop, Rect2(-42, y - 7, 84, 14), 24, Color("252a34"))
		for rib in range(16):
			rack_panel(prop, Rect2(-40 + rib * 5, y - 6, 1, 12), 24, Color("39404a"))
	# Each small growth sprite has its own ground anchor and fixed upright shape.
	var growth: Array = []
	for row in range(3):
		for column in range(5):
			var local := Vector2(-33 + column * 16, -24 + row * 24)
			growth.append({"point": rack_point(prop, local, 25), "variant": (row * 7 + column * 3) % 5})
	growth.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return a.point.y < b.point.y)
	for cluster in growth:
		var p: Vector2 = cluster.point
		var variant: int = cluster.variant
		if paint_asset("growth", Rect2(p - Vector2(8, 15), Vector2(16, 15))):
			continue
		for sprout in range(3):
			var foot := p + Vector2((sprout - 1) * 4, (sprout % 2) * 2)
			var h := 4.0 + (variant + sprout) % 4
			paint_ellipse(foot, Vector2(4, 2), Color(0, 0, 0, 0.25))
			painter.draw_line(foot, foot - Vector2(0, h), Color("a6967e"), 2)
			paint_ellipse(foot - Vector2(0, h), Vector2(4, 2.5), Color("bba889"))
			paint_ellipse(foot - Vector2(0.6, h + 1), Vector2(3.6, 2), Color("ead9b5"))
	# Upright service valve follows its room-local mount.
	var valve := rack_point(prop, Vector2(43, -31), 24)
	painter.draw_line(valve, valve - Vector2(0, 8), Color("354c50"), 4)
	paint_ellipse(valve - Vector2(0, 8), Vector2(4, 2), Color("78938a"))
	painter.draw_circle(valve - Vector2(0, 8), 1, Color("263b40"))
	if operating:
		# Local irrigation droplets rise vertically, never rotate as a bitmap.
		for i in range(3):
			var t := fmod(phase * 0.7 + i / 3.0, 1.0)
			var drop := valve + Vector2(-4 - i * 2, -10 - t * 10)
			painter.draw_circle(drop, 1.2, Color(0.45, 0.8, 0.73, (1 - t) * 0.7))

func draw_nursery_floor(room: Dictionary) -> void:
	var center := Vector2(room.cell) * Geometry.CELL
	# Flush maintenance grates: no raised objects or pipes across the aisle.
	for local in [Vector2(-107, -48), Vector2(108, -48), Vector2(-108, 162), Vector2(108, 162)]:
		var prop := {"rect": Rect2(center - Vector2.ONE, Vector2.ONE * 2), "facing": room.rotation}
		rack_panel(prop, Rect2(local - Vector2(36, 4), Vector2(72, 8)), 0, Color("232c34"))
		for i in range(12):
			rack_panel(prop, Rect2(local + Vector2(-33 + i * 6, -3), Vector2(2, 6)), 0, Color("485057"))
	for sign_value in [-1, 1]:
		var a := center + Geometry.turn(Vector2(sign_value * 51, -160), room.rotation)
		var b := center + Geometry.turn(Vector2(sign_value * 51, -65), room.rotation)
		painter.draw_line(a, b, Color("53574f"), 1)
	# A small flush service hatch remains quiet beneath foot traffic.
	var floor_prop := {"rect": Rect2(center - Vector2.ONE, Vector2.ONE * 2), "facing": room.rotation}
	var hatch := Rect2(-18, 65, 36, 26)
	rack_panel(floor_prop, hatch, 0, Color("29333b"))
	rack_panel(floor_prop, hatch.grow(-2), 0, Color("3b444a"))
	for side in [-1, 1]:
		painter.draw_circle(rack_point(floor_prop, hatch.get_center() + Vector2(side * 13, 8), 0), 1, Color("7b807b"))

func cabinet(prop: Dictionary, height: float) -> Rect2:
	var r: Rect2 = prop.rect
	var top := Rect2(r.position - Vector2(0, height), r.size)
	var face := Rect2(Vector2(r.position.x, top.end.y), Vector2(r.size.x, height))
	painter.draw_rect(face, Color("202630"))
	painter.draw_rect(face.grow(-2), Color("85867c"))
	painter.draw_rect(top, Color("1f2730"))
	painter.draw_rect(top.grow(-2), Color("a59e8d"))
	painter.draw_rect(top.grow(-4), Color("dbcfb3"))
	var material_offset := Vector2(0.31, 0.57) if prop.kind == "bench" else Vector2(0.79, 0.18)
	paint_material("enamel", top.grow(-4), prop.facing, Color.WHITE, material_offset)
	paint_material("enamel", face.grow(-2), prop.facing, Color("a3a5a3"), material_offset)
	cabinet_face_details(prop, face, false)
	painter.draw_line(top.position + Vector2(4, 3), top.position + Vector2(top.size.x - 4, 3), Color("f4e7c9"), 2)
	for p in [top.position + Vector2(6, 6), top.end - Vector2(6, 6)]:
		painter.draw_circle(p, 1.5, Color("7e8077"))
	return top

func cabinet_face_details(prop: Dictionary, face: Rect2, rack: bool) -> void:
	# In this fixed projection, the visible wall is local front/right/back/left.
	# Do not repaint the same service front onto whichever side faces the camera.
	var inner := face.grow(-4)
	if prop.facing == 0:
		if rack:
			for x in range(2, int(inner.size.x) - 2, 5):
				painter.draw_rect(Rect2(inner.position + Vector2(x, 1), Vector2(2, inner.size.y - 2)), Color("40434b"))
		else:
			for y in [2, 10]:
				painter.draw_line(inner.position + Vector2(0, y), inner.position + Vector2(inner.size.x, y), Color("444b50"), 1)
				painter.draw_rect(Rect2(inner.position + Vector2(inner.size.x * 0.5 - 7, y + 2), Vector2(14, 2)), Color("303c42"))
	elif prop.facing == 2:
		painter.draw_rect(inner, Color("3b454b"))
		for y in [3, 7, 11]:
			painter.draw_line(inner.position + Vector2(6, y), inner.position + Vector2(inner.size.x - 18, y), Color("202a32"), 2)
		painter.draw_circle(inner.end - Vector2(8, 7), 3, Color("83948b"))
		painter.draw_circle(inner.end - Vector2(8, 7), 1.5, Color("26343c"))
	else:
		painter.draw_rect(inner, Color("777c75"))
		painter.draw_line(inner.position + Vector2(2, 2), inner.end - Vector2(2, 2), Color("a8a692"), 2)
		# A maintenance hatch belongs only to the physical right side.
		if prop.facing == 1:
			var hatch := Rect2(inner.end - Vector2(17, 13), Vector2(13, 10))
			painter.draw_rect(hatch, Color("34434b"))
			painter.draw_line(hatch.position + Vector2(3, 5), hatch.end - Vector2(3, 5), Color("84948a"), 1)
	for x in [1.0, inner.size.x - 1]:
		painter.draw_circle(inner.position + Vector2(x, 1), 1, Color("c5bba4"))

func console_point(prop: Dictionary, u: float, v: float, back := false) -> Vector2:
	return rack_point(prop, Vector2(25 + (u - 0.5) * 28, 16 - v * 4 - (3 if back else 0)), 26 + v * 14)

func draw_console(prop: Dictionary) -> void:
	# Tilted screen with physical thickness; ground yaw never turns height sideways.
	rack_panel(prop, Rect2(18, 10, 14, 10), 24, Color("303d43"))
	var front := PackedVector2Array()
	var rear := PackedVector2Array()
	for uv in [Vector2(0, 0), Vector2(1, 0), Vector2(1, 1), Vector2(0, 1)]:
		front.append(console_point(prop, uv.x, uv.y))
		rear.append(console_point(prop, uv.x, uv.y, true))
	painter.draw_colored_polygon(rear, Color("899387"))
	painter.draw_colored_polygon(PackedVector2Array([front[0], rear[0], rear[3], front[3]]), Color("626f69"))
	painter.draw_colored_polygon(PackedVector2Array([front[1], rear[1], rear[2], front[2]]), Color("46524f"))
	if prop.facing == 2:
		painter.draw_colored_polygon(rear, Color("56615c"))
		for v in [0.3, 0.5, 0.7]:
			painter.draw_line(console_point(prop, 0.2, v, true), console_point(prop, 0.8, v, true), Color("29363b"), 1)
	else:
		painter.draw_colored_polygon(front, Color("242f37"))
		var screen := PackedVector2Array()
		for uv in [Vector2(0.1, 0.12), Vector2(0.9, 0.12), Vector2(0.9, 0.88), Vector2(0.1, 0.88)]:
			screen.append(console_point(prop, uv.x, uv.y))
		painter.draw_colored_polygon(screen, Color("3d615f") if operating else Color("394342"))
		if operating:
			for i in range(4):
				var v := 0.25 + i * 0.15
				painter.draw_line(console_point(prop, 0.18, v), console_point(prop, 0.65 + sin(phase * 2 + i) * 0.1, v), Color("88b8a1"), 1)
	painter.draw_colored_polygon(PackedVector2Array([front[3], front[2], rear[2], rear[3]]), Color("b2b29d"))

func vial(p: Vector2, radius: float, height: float, liquid: Color) -> void:
	paint_ellipse(p, Vector2(radius + 1, radius * 0.45), Color("253039"))
	painter.draw_rect(Rect2(p - Vector2(radius, height), Vector2(radius * 2, height)), Color("758d8e"))
	painter.draw_rect(Rect2(p - Vector2(radius - 1, height * 0.65), Vector2(radius * 2 - 2, height * 0.65)), liquid)
	painter.draw_line(p + Vector2(-radius + 1, -height + 2), p + Vector2(-radius + 1, -2), Color("c0c9ba"), 1)
	paint_ellipse(p - Vector2(0, height), Vector2(radius, radius * 0.45), Color("d3c8ae"))
	paint_ellipse(p - Vector2(0, height + 1), Vector2(radius * 0.65, radius * 0.25), Color("89978b"))

func draw_nursery_prop(prop: Dictionary) -> void:
	if prop.kind == "tank":
		draw_reservoir(prop)
		return
	var top := cabinet(prop, 23)
	if prop.kind == "bench":
		# Recessed work mat and specimen tray rotate on the tabletop.
		rack_panel(prop, Rect2(-40, -28, 43, 50), 24, Color("465557"))
		rack_panel(prop, Rect2(-36, -24, 35, 42), 24, Color("2a3941"))
		rack_panel(prop, Rect2(-32, 1, 27, 14), 25, Color("969a88"))
		rack_panel(prop, Rect2(-30, 3, 23, 10), 25, Color("343d40"))
		var items: Array = []
		for i in range(3):
			items.append({"p": rack_point(prop, Vector2(13 + i * 11, -20), 24), "i": i})
		items.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return a.p.y < b.p.y)
		for item in items:
			vial(item.p, 3.5, 8 + item.i * 3, Color("64847a"))
			if operating:
				painter.draw_circle(item.p - Vector2(0, 2 + fmod(phase * 4 + item.i, 5 + item.i * 3)), 0.9, Color("bed9c6"))
		# Microscope is an upright component, not a rotated picture.
		var scope := rack_point(prop, Vector2(-19, -13), 25)
		# Four guided views share a ground pivot; G still enables the diagnostic proxy.
		if not paint_registered_prop("microscope_%d" % prop.facing, scope, prop.facing):
			paint_ellipse(scope, Vector2(9, 4), Color("b9b5a1"))
			painter.draw_line(scope + Vector2(4, 0), scope + Vector2(4, -16), Color("4b5c60"), 5)
			painter.draw_line(scope + Vector2(4, -16), scope + Vector2(-4, -21), Color("c6c6b0"), 5)
			painter.draw_rect(Rect2(scope + Vector2(-8, -24), Vector2(7, 4)), Color("253741"))
		draw_console(prop)
	else:
		# Cartridges share a manifold; each cylinder stays vertical.
		rack_panel(prop, Rect2(-40, -28, 80, 8), 24, Color("394e53"))
		var cartridges: Array = []
		for i in range(3):
			cartridges.append({"p": rack_point(prop, Vector2((i - 1) * 25, 0), 24), "i": i})
		cartridges.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return a.p.y < b.p.y)
		for item in cartridges:
			if not paint_asset("cartridge", Rect2(item.p - Vector2(9, 25), Vector2(18, 25))):
				vial(item.p, 9, 19, Color("71867d") if item.i == 1 else Color("9caa99"))
			var p: Vector2 = item.p
			painter.draw_rect(Rect2(p + Vector2(-5, -11), Vector2(10, 5)), Color("d8ccb0"))
			if operating:
				painter.draw_circle(p + Vector2(2, -3 - fmod(phase * 4 + item.i * 3, 11)), 1, Color("c3ddd0"))
		var gauge := rack_point(prop, Vector2(33, 25), 24)
		painter.draw_circle(gauge, 6, Color("273a43"))
		painter.draw_circle(gauge, 4.5, Color("d8d2b8"))
		painter.draw_line(gauge, gauge + Vector2(2, -2), Color("48695f"), 1)
	# Sparse wear is attached to the local service edge.
	for i in range(5):
		rack_panel(prop, Rect2(-39 + i * 7, 30, 3, 1), 24, Color("a39a87"))

func draw_reservoir(prop: Dictionary) -> void:
	var r: Rect2 = prop.rect
	var c := r.get_center()
	# Round vessel with fixed-screen cylindrical shading; ground footprint unchanged.
	var base := c + Vector2(0, 22)
	var lid := c - Vector2(0, 40)
	var valve_ground := Geometry.turn(Vector2(25, 22), prop.facing)
	if valve_ground.y < 0:
		draw_reservoir_valve(prop)
	if paint_asset("reservoir", Rect2(c + Vector2(-31, -54), Vector2(62, 88))):
		if valve_ground.y >= 0:
			draw_reservoir_valve(prop)
		if operating:
			for i in range(4):
				var t := fmod(phase * 0.22 + i * 0.23, 1.0)
				painter.draw_circle(c + Vector2(-4 + sin(i * 2.1) * 11, 16 - t * 47), 1.5, Color(0.67, 0.85, 0.79, 0.55))
		return
	paint_ellipse(base + Vector2(0, 5), Vector2(31, 12), Color("202a32"))
	painter.draw_rect(Rect2(c + Vector2(-30, -40), Vector2(60, 62)), Color("657774"))
	painter.draw_rect(Rect2(c + Vector2(-24, -38), Vector2(48, 61)), Color("567b7b"))
	painter.draw_rect(Rect2(c + Vector2(-17, -35), Vector2(8, 54)), Color("8ba8a0"))
	painter.draw_rect(Rect2(c + Vector2(19, -34), Vector2(6, 52)), Color("344d57"))
	paint_ellipse(base, Vector2(30, 10), Color("a5a692"))
	paint_ellipse(base - Vector2(0, 3), Vector2(25, 7), Color("536c6a"))
	paint_ellipse(lid, Vector2(31, 15), Color("242e37"))
	paint_ellipse(lid - Vector2(0, 2), Vector2(28, 13), Color("d2c5a8"))
	paint_ellipse(lid - Vector2(0, 3), Vector2(21, 9), Color("7e8981"))
	paint_ellipse(lid - Vector2(0, 4), Vector2(17, 7), Color("36494f"))
	for i in range(5):
		painter.draw_line(c + Vector2(11, -26 + i * 8), c + Vector2(16, -26 + i * 8), Color("b6c2b0"), 1)
	if valve_ground.y >= 0:
		draw_reservoir_valve(prop)
	if operating:
		for i in range(4):
			var t := fmod(phase * 0.22 + i * 0.23, 1.0)
			painter.draw_circle(c + Vector2(-4 + sin(i * 2.1) * 11, 16 - t * 47), 1.5, Color(0.67, 0.85, 0.79, 0.55))

func draw_reservoir_valve(prop: Dictionary) -> void:
	var valve := rack_point(prop, Vector2(25, 22), 5)
	painter.draw_line(valve, valve - Vector2(0, 10), Color("344b51"), 4)
	paint_ellipse(valve - Vector2(0, 10), Vector2(5, 3), Color("8bafa0"))
