extends Control
class_name GridCanvas

signal cell_clicked(cell: Vector2i)
signal cell_secondary_clicked(cell: Vector2i)
signal cell_hovered(cell: Vector2i)

const RoomDatabaseScript := preload("res://scripts/room_database.gd")
const DOOR_SHEET_COLUMNS := 4
const DOOR_SHEET_ROWS := 3
const DOOR_OPEN_FRAMES := 10
const DOOR_DRAW_SIZE := Vector2(0.225, 0.162)
const DOOR_UNDERLAY_FRACTION := 0.28
const ROOM_TEXTURE_OVERDRAW := 0.012
const ROOM_SOURCE_MARGIN := 8

var human_sprite: Texture2D
var door_texture: Texture2D
var space_background_texture: Texture2D
var human_sprites := {}
var human_animations := {}
var drone_sprites := {}
var drone_animations := {}
var brine_core_overlays := {}
var room_textures := {}
var room_texture_variants := {}
var texture_source_regions := {}
var star_points: Array[Dictionary] = []
var room_texture_paths := {
	"battery_array": "res://rooms/batteryarray.png",
	"biodome": "res://rooms/biodome.png",
	"clone_lab": "res://rooms/clonelab.png",
	"brine_core": "res://rooms/brinecore.png",
	"crew_hab": "res://rooms/crewhab.png",
	"cryo_chamber": "res://rooms/cryolab.png",
	"data_archive": "res://rooms/holographiccore.png",
	"hydroponics_bay": "res://rooms/hydroponics.png",
	"life_support": "res://rooms/lifesupport1.png",
	"mining_drone_bay": "res://rooms/miningdronebay.png",
	"ore_refinery": "res://rooms/orerefinery.png",
	"quarantine_cell": "res://rooms/quaratinecell.png",
	"reactor": "res://rooms/reactor.png",
	"research_lab": "res://rooms/researchlab2.png",
	"salvage_drone_bay": "res://rooms/salvagedronebay1.png",
	"solar_array": "res://rooms/solararray.png",
	"storage_bay": "res://rooms/storagebay1.png",
	"med_bay": "res://rooms/medbay.png",
	"xeno_lab": "res://rooms/xenolab.png",
	"anomaly_lab": "res://rooms/anomolylab.png",
	"bio_lab": "res://rooms/biolab.png",
	"command_center": "res://rooms/commandcenter.png",
	"corridor": "res://rooms/corridor1.png",
	"corner": "res://rooms/corner.png",
	"crew_lounge": "res://rooms/crewlounge1.png",
	"holographic_core": "res://rooms/holographiccore.png",
	"maintenance_bay": "res://rooms/maintenancebay.png",
	"med_center": "res://rooms/medcenter.png",
	"med_office": "res://rooms/medoffice.png",
	"radio_lab": "res://rooms/radiolab.png",
	"shield_generator": "res://rooms/sheildgenerator1.png"
}
var room_texture_variant_paths := {
	"battery_array": ["res://rooms/batteryarray.png", "res://rooms/batteryarray2.png", "res://rooms/batteryarray3.png"],
	"corner": ["res://rooms/corner.png", "res://rooms/corrner1.png", "res://rooms/corner2.png", "res://rooms/corner3.png", "res://rooms/corner4.png", "res://rooms/corner5.png", "res://rooms/corner6.png", "res://rooms/corner7.png", "res://rooms/corner8.png"],
	"corridor": ["res://rooms/corridor1.png", "res://rooms/corridor2.png", "res://rooms/corridor3.png", "res://rooms/corridor4.png", "res://rooms/corridor5.png", "res://rooms/corridor6.png"],
	"crew_hab": ["res://rooms/crewhab.png", "res://rooms/crewhab2.png", "res://rooms/crewhab3.png", "res://rooms/crewhab4.png"],
	"crew_lounge": ["res://rooms/crewlounge1.png", "res://rooms/crewlounge2.png", "res://rooms/crewlounge3.png", "res://rooms/crewlounge4.png", "res://rooms/crewlounge5.png", "res://rooms/crewlounge6.png"],
	"hydroponics_bay": ["res://rooms/hydroponics.png", "res://rooms/hydroponics2.png", "res://rooms/hydroponics3.png", "res://rooms/hydroponics4.png"],
	"life_support": ["res://rooms/lifesupport1.png", "res://rooms/lifesupport3.png"],
	"maintenance_bay": ["res://rooms/maintenancebay.png", "res://rooms/maintenancebay2.png"],
	"mining_drone_bay": ["res://rooms/miningdronebay.png", "res://rooms/miningdronebay2.png"],
	"reactor": ["res://rooms/reactor.png", "res://rooms/reactor2.png", "res://rooms/reactor3.png", "res://rooms/reactor4.png"],
	"research_lab": ["res://rooms/researchlab2.png", "res://rooms/researchlab3.png"],
	"salvage_drone_bay": ["res://rooms/salvagedronebay1.png", "res://rooms/salvagedronebay2.png"],
	"shield_generator": ["res://rooms/sheildgenerator1.png", "res://rooms/sheildgenerator2.png", "res://rooms/sheildgenerator3.png"],
	"solar_array": ["res://rooms/solararray.png", "res://rooms/solararray2.png", "res://rooms/solararray3.png"],
	"storage_bay": ["res://rooms/storagebay1.png", "res://rooms/storagebay2.png", "res://rooms/storagebay3.png", "res://rooms/storagebay4.png", "res://rooms/storagebay5.png"],
	"xeno_lab": ["res://rooms/xenolab.png", "res://rooms/xenolab2.png"]
}

func _ready() -> void:
	texture_filter = CanvasItem.TEXTURE_FILTER_NEAREST
	_generate_star_points()
	space_background_texture = _load_png_texture("res://space texture.jpg")
	door_texture = _load_png_texture("res://dooranimated.png")
	for id in room_texture_paths:
		var texture := _load_png_texture(room_texture_paths[id])
		if texture != null:
			room_textures[id] = texture
	for id in room_texture_variant_paths:
		var textures: Array[Texture2D] = []
		for path_value in room_texture_variant_paths[id]:
			var texture: Texture2D = _load_png_texture(str(path_value))
			if texture != null:
				textures.append(texture)
		if not textures.is_empty():
			room_texture_variants[id] = textures
	human_sprite = _load_png_texture("res://character/Major_Bill/rotations/south.png")
	for direction in ["north", "east", "south", "west"]:
		var texture := _load_png_texture("res://character/Major_Bill/rotations/%s.png" % direction)
		if texture != null:
			human_sprites[direction] = texture
	_load_human_animation("idle", "res://character/Major_Bill/animations/Breathing_Idle-70a80927")
	_load_human_animation("walk", "res://character/Major_Bill/animations/Walking-5c23139e")
	_load_human_animation("run", "res://character/Major_Bill/animations/Running-3a3748f6")
	_load_drone_assets()
	_load_brine_core_overlays()

func _generate_star_points() -> void:
	star_points.clear()
	for i in range(520):
		var point := {
			"x": float((i * 15485863) % 100000) / 100000.0,
			"y": float((i * 32452843) % 100000) / 100000.0,
			"twinkle": float((i * 97) % 100) / 100.0,
			"size": 1.0
		}
		if i % 23 == 0:
			point["size"] = 2.0
		if i % 113 == 0:
			point["size"] = 3.0
		star_points.append(point)

func _load_png_texture(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var resource := ResourceLoader.load(path)
		if resource is Texture2D:
			_cache_texture_source_region(resource)
			return resource
	var image := Image.new()
	var error := image.load(path)
	if error != OK:
		return null
	var texture := ImageTexture.create_from_image(image)
	_cache_texture_source_region(texture, image)
	return texture

func _cache_texture_source_region(texture: Texture2D, image: Image = null) -> void:
	if texture == null:
		return
	var source_image := image
	if source_image == null:
		source_image = texture.get_image()
	if source_image == null:
		return
	texture_source_regions[texture.get_instance_id()] = _find_content_region(source_image)

func _find_content_region(image: Image) -> Rect2:
	var width := image.get_width()
	var height := image.get_height()
	var min_x := width
	var min_y := height
	var max_x := -1
	var max_y := -1
	for y in range(0, height, 2):
		for x in range(0, width, 2):
			var pixel := image.get_pixel(x, y)
			var is_visible_pixel := pixel.a > 0.04 and maxf(maxf(pixel.r, pixel.g), pixel.b) > 0.018
			if is_visible_pixel:
				min_x = mini(min_x, x)
				min_y = mini(min_y, y)
				max_x = maxi(max_x, x)
				max_y = maxi(max_y, y)
	if max_x < min_x or max_y < min_y:
		return Rect2(Vector2.ZERO, Vector2(width, height))
	min_x = maxi(min_x - ROOM_SOURCE_MARGIN, 0)
	min_y = maxi(min_y - ROOM_SOURCE_MARGIN, 0)
	max_x = mini(max_x + ROOM_SOURCE_MARGIN, width - 1)
	max_y = mini(max_y + ROOM_SOURCE_MARGIN, height - 1)
	return Rect2(Vector2(min_x, min_y), Vector2(max_x - min_x + 1, max_y - min_y + 1))

func _load_human_animation(state: String, base_path: String) -> void:
	var by_direction := {}
	for direction in ["north", "east", "south", "west"]:
		var frames := []
		var dir := DirAccess.open("%s/%s" % [base_path, direction])
		if dir == null:
			continue
		dir.list_dir_begin()
		var file_name := dir.get_next()
		while not file_name.is_empty():
			if not dir.current_is_dir() and file_name.ends_with(".png"):
				frames.append("%s/%s/%s" % [base_path, direction, file_name])
			file_name = dir.get_next()
		dir.list_dir_end()
		frames.sort()
		var textures := []
		for frame_path in frames:
			var texture := _load_png_texture(frame_path)
			if texture != null:
				textures.append(texture)
		if not textures.is_empty():
			by_direction[direction] = textures
	human_animations[state] = by_direction

func _load_drone_assets() -> void:
	var directions := ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
	for direction in directions:
		var texture: Texture2D = _load_png_texture("res://mining-drone-animation/rotations/%s.png" % direction)
		if texture != null:
			drone_sprites[direction] = texture
	_load_drone_animation("fly", "res://mining-drone-animation/animations/2._Flying_Moving_The_drone_tilts_slightly_forward-30d7af04", directions)
	_load_drone_animation("mine", "res://mining-drone-animation/animations/3._Mining_The_drone_stops_in_place_and_extends_its-32d99183", directions)
	_load_drone_animation("idle", "res://mining-drone-animation/animations/Idle_Hover_The_drone_floats_in_place_with_a_slow_m-0332a189", directions)

func _load_drone_animation(state: String, base_path: String, directions: Array) -> void:
	var by_direction := {}
	for direction_value in directions:
		var direction := str(direction_value)
		var direction_dir := _find_direction_animation_dir(base_path, direction)
		if direction_dir.is_empty():
			continue
		var frames: Array[String] = []
		var dir := DirAccess.open(direction_dir)
		if dir == null:
			continue
		dir.list_dir_begin()
		var file_name := dir.get_next()
		while not file_name.is_empty():
			if not dir.current_is_dir() and file_name.ends_with(".png"):
				frames.append("%s/%s" % [direction_dir, file_name])
			file_name = dir.get_next()
		dir.list_dir_end()
		frames.sort()
		var textures: Array[Texture2D] = []
		for frame_path in frames:
			var texture: Texture2D = _load_png_texture(frame_path)
			if texture != null:
				textures.append(texture)
		if not textures.is_empty():
			by_direction[direction] = textures
	drone_animations[state] = by_direction

func _find_direction_animation_dir(base_path: String, direction: String) -> String:
	var exact_path := "%s/%s" % [base_path, direction]
	if DirAccess.dir_exists_absolute(exact_path):
		return exact_path
	var dir := DirAccess.open(base_path)
	if dir == null:
		return ""
	dir.list_dir_begin()
	var file_name := dir.get_next()
	while not file_name.is_empty():
		if dir.current_is_dir() and file_name.begins_with(direction):
			dir.list_dir_end()
			return "%s/%s" % [base_path, file_name]
		file_name = dir.get_next()
	dir.list_dir_end()
	return ""

func _load_brine_core_overlays() -> void:
	var overlay_paths := {
		"body": "res://brinecore-animation/assets/brine_body_temp.png",
		"bubble": "res://brinecore-animation/assets/bubble_particle.png",
		"console": "res://brinecore-animation/assets/console_flicker_spritesheet_temp.png",
		"glass": "res://brinecore-animation/assets/tank_glass_overlay_temp.png",
		"glow": "res://brinecore-animation/assets/tank_glow_overlay.png"
	}
	for id in overlay_paths:
		var texture: Texture2D = _load_png_texture(str(overlay_paths[id]))
		if texture != null:
			brine_core_overlays[id] = texture

const GRID_SIZE := 40
const CELL_SIZE := 720
const GRID_PIXEL_SIZE := GRID_SIZE * CELL_SIZE

func _gui_input(event: InputEvent) -> void:
	var main = _get_main()
	if main.menu_open:
		accept_event()
		return
	if event is InputEventMouseButton and event.pressed and event.shift_pressed:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			main._set_grid_zoom(main.grid_zoom + 0.05)
			accept_event()
			return
		if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			main._set_grid_zoom(main.grid_zoom - 0.05)
			accept_event()
			return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var cell_size := _cell_size()
		var cell := Vector2i(floori(event.position.x / cell_size), floori(event.position.y / cell_size))
		cell_clicked.emit(cell)
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_RIGHT:
		var cell_size := _cell_size()
		var cell := Vector2i(floori(event.position.x / cell_size), floori(event.position.y / cell_size))
		cell_secondary_clicked.emit(cell)
	if event is InputEventMouseMotion:
		var cell_size := _cell_size()
		var cell := Vector2i(floori(event.position.x / cell_size), floori(event.position.y / cell_size))
		cell_hovered.emit(cell)

func _process(_delta: float) -> void:
	var main = _get_main()
	if not main.paused or not main.selected_card_id.is_empty():
		queue_redraw()

func _draw() -> void:
	var main = _get_main()
	var cell_size := _cell_size()
	var grid_pixel_size := GRID_SIZE * cell_size
	_draw_space_background(grid_pixel_size)
	_draw_stars()
	if main.admin_mode:
		for x in range(GRID_SIZE + 1):
			var c := Color(0.18, 0.28, 0.34, 0.42)
			draw_line(Vector2(x * cell_size, 0), Vector2(x * cell_size, grid_pixel_size), c)
			draw_line(Vector2(0, x * cell_size), Vector2(grid_pixel_size, x * cell_size), c)
	for room in main.placed_rooms:
		_draw_connectors(room, main.occupied)
	for room in main.placed_rooms:
		_draw_room(room)
	_draw_synergy_links(main)
	_draw_door_foregrounds(main, true)
	_draw_humans(main)
	_draw_door_foregrounds(main, false)
	_draw_orbit_marker(main)
	_draw_drones(main)
	if not main.selected_card_id.is_empty():
		var mouse_cell := Vector2i(floori(get_local_mouse_position().x / cell_size), floori(get_local_mouse_position().y / cell_size))
		var valid: bool = main.get_placement_problem(main.selected_card_id, mouse_cell).is_empty()
		_draw_room_hologram(main, mouse_cell, valid)

func _draw_space_background(grid_pixel_size: float) -> void:
	var bounds := Rect2(Vector2.ZERO, Vector2(grid_pixel_size, grid_pixel_size))
	if space_background_texture != null:
		var texture_size := space_background_texture.get_size()
		var tile_size := texture_size * 0.42
		for x in range(-1, int(ceil(grid_pixel_size / tile_size.x)) + 2):
			for y in range(-1, int(ceil(grid_pixel_size / tile_size.y)) + 2):
				var tile_rect := Rect2(Vector2(float(x) * tile_size.x, float(y) * tile_size.y), tile_size)
				draw_texture_rect(space_background_texture, tile_rect, false, Color(0.72, 0.82, 0.92, 0.48))
		draw_rect(bounds, Color(0.0, 0.025, 0.035, 0.46))
	else:
		draw_rect(bounds, Color("#01050a"))
	var center := bounds.get_center()
	var band_count := 18
	for i in range(band_count):
		var t := float(i) / float(band_count - 1)
		var radius := grid_pixel_size * (0.22 + t * 0.72)
		var alpha := 0.055 * (1.0 - t)
		draw_circle(center + Vector2(grid_pixel_size * 0.04, -grid_pixel_size * 0.05), radius, Color(0.02, 0.09, 0.12, alpha))

func _draw_stars() -> void:
	var grid_pixel_size := GRID_SIZE * _cell_size()
	for i in range(star_points.size()):
		var star: Dictionary = star_points[i]
		var x: float = float(star["x"]) * grid_pixel_size
		var y: float = float(star["y"]) * grid_pixel_size
		var alpha: float = 0.18 + float(star["twinkle"]) * 0.55
		var star_size: float = float(star["size"])
		if star_size >= 2.0:
			alpha = 0.85
		if star_size >= 3.0:
			alpha = 0.95
		var star_color := Color(0.65, 0.85, 0.95, alpha)
		draw_rect(Rect2(Vector2(x, y), Vector2(star_size, star_size)), star_color)
		if i % 41 == 0:
			draw_line(Vector2(x - 5, y), Vector2(x + 5, y), Color(0.45, 0.75, 0.90, alpha * 0.42), 1)
			draw_line(Vector2(x, y - 5), Vector2(x, y + 5), Color(0.45, 0.75, 0.90, alpha * 0.42), 1)

func _draw_room(room: Dictionary) -> void:
	var main = _get_main()
	var pos: Vector2i = room["pos"]
	var cell_size := _cell_size()
	var rect := Rect2(Vector2(pos) * cell_size + Vector2.ONE, Vector2(cell_size - 2, cell_size - 2))
	var color := RoomDatabaseScript.category_color(room["category"])
	var offline: bool = main.unpowered_room_cells.has(pos)
	var room_texture: Texture2D = _get_room_texture(room)
	var has_texture := room_texture != null
	if not has_texture:
		var shadow_rect := rect.grow(cell_size * 0.018)
		draw_rect(Rect2(shadow_rect.position + Vector2(cell_size * 0.018, cell_size * 0.025), shadow_rect.size), Color(0, 0, 0, 0.34))
	if not has_texture:
		draw_rect(rect, Color("#151a1f"))
	if has_texture:
		var overdraw: float = cell_size * ROOM_TEXTURE_OVERDRAW
		var texture_rect: Rect2 = Rect2(-rect.size * 0.5, rect.size).grow(overdraw)
		var source_rect: Rect2 = texture_source_regions.get(room_texture.get_instance_id(), Rect2(Vector2.ZERO, room_texture.get_size()))
		draw_set_transform(rect.get_center(), deg_to_rad(float(int(room.get("rotation", 0)) * 90)), Vector2.ONE)
		draw_texture_rect_region(room_texture, texture_rect, source_rect)
		draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
		if room["id"] == "brine_core":
			_draw_brine_core_overlay(rect)
	else:
		draw_rect(rect.grow(-2), color.darkened(0.62) if offline else color.darkened(0.25))
	if offline:
		draw_rect(rect.grow(-1), Color(0.05, 0.02, 0.03, 0.58))
	var border_color := Color("#d34e58") if offline else color.darkened(0.10)
	var border_width := 1.5 if not has_texture or main.admin_mode or offline else 0.0
	if main.selected_room_cell == pos:
		border_color = Color("#4fa38d")
		border_width = 4.0
	elif main.hover_cell == pos:
		border_color = Color("#6ab8a3")
		border_width = 3.0
	if border_width > 0.0:
		draw_rect(rect, border_color, false, border_width)
	var center := rect.get_center()
	if offline and main.admin_mode:
		draw_line(rect.position + Vector2(4, 4), rect.end - Vector2(4, 4), Color("#ff7580"), 2)
		draw_line(Vector2(rect.end.x - 4, rect.position.y + 4), Vector2(rect.position.x + 4, rect.end.y - 4), Color("#ff7580"), 2)
		draw_circle(center, 4, Color("#ff2537"))
	elif not offline and not has_texture:
		match room["category"]:
			"Core":
				draw_circle(center, 4, Color("#e8feff"))
			"Engineering":
				draw_line(center + Vector2(-4, 3), center + Vector2(0, -4), Color.BLACK, 2)
				draw_line(center + Vector2(0, -4), center + Vector2(4, 3), Color.BLACK, 2)
			"Science":
				draw_circle(center, 3, Color.BLACK)
			"Bio":
				draw_line(center + Vector2(0, 4), center + Vector2(0, -4), Color.BLACK, 2)
				draw_circle(center + Vector2(-3, -1), 2, Color.BLACK)
				draw_circle(center + Vector2(3, -1), 2, Color.BLACK)
			"Crew":
				draw_circle(center + Vector2(0, -3), 2, Color.BLACK)
				draw_line(center + Vector2(0, 0), center + Vector2(0, 4), Color.BLACK, 2)
			"Drone":
				draw_rect(Rect2(center - Vector2(3, 3), Vector2(6, 6)), Color.BLACK)
			_:
				draw_circle(center, 3, Color.BLACK)
	if main.admin_mode:
		_draw_room_path(room, rect)
		_draw_room_doors(room, rect)

func _draw_brine_core_overlay(rect: Rect2) -> void:
	var main = _get_main()
	var time_seconds: float = main.get_visual_time_seconds()
	var glow_texture := brine_core_overlays.get("glow") as Texture2D
	if glow_texture != null:
		var glow_alpha := 0.55 + sin(time_seconds * 0.9) * 0.20
		draw_texture_rect(glow_texture, rect, false, Color(0.65, 1.0, 1.0, glow_alpha))
	var body_texture := brine_core_overlays.get("body") as Texture2D
	if body_texture != null:
		var body_size := Vector2(rect.size.x * 0.092, rect.size.y * 0.223)
		var body_center := rect.get_center() + Vector2(rect.size.x * 0.005, -rect.size.y * 0.008)
		var body_pos := body_center - body_size * 0.5 + Vector2(0, sin(time_seconds * 1.1) * rect.size.y * 0.004)
		draw_texture_rect(body_texture, Rect2(body_pos, body_size), false, Color(1, 1, 1, 0.64))
	var bubble_texture := brine_core_overlays.get("bubble") as Texture2D
	if bubble_texture != null:
		for i in range(10):
			var phase: float = fmod(time_seconds * (0.12 + float(i) * 0.014) + float(i) * 0.17, 1.0)
			var bubble_size: float = rect.size.x * (0.006 + float(i % 4) * 0.002)
			var x_offset: float = sin(float(i) * 2.73 + time_seconds * 0.55) * rect.size.x * 0.044
			var y_start: float = rect.size.y * 0.105
			var y_end: float = -rect.size.y * 0.082
			var y_offset: float = y_start + (y_end - y_start) * phase
			var bubble_pos: Vector2 = rect.get_center() + Vector2(x_offset, y_offset) - Vector2.ONE * bubble_size * 0.5
			draw_texture_rect(bubble_texture, Rect2(bubble_pos, Vector2.ONE * bubble_size), false, Color(0.75, 1.0, 1.0, 0.42))
	var glass_texture := brine_core_overlays.get("glass") as Texture2D
	if glass_texture != null:
		draw_texture_rect(glass_texture, rect, false, Color(1, 1, 1, 0.72))

func _draw_room_doors(room: Dictionary, rect: Rect2) -> void:
	var main = _get_main()
	for door in main.get_room_doors(room):
		var door_rect := _door_rect(str(door), rect)
		draw_rect(door_rect, Color("#4654ff"))
		draw_rect(door_rect.grow(-2), Color("#9aa4ff"))

func _draw_door_foregrounds(main, underlay: bool = false) -> void:
	if door_texture == null:
		if not underlay:
			_draw_static_door_foregrounds(main)
		return
	if door_texture.get_width() <= 0 or door_texture.get_height() <= 0:
		if not underlay:
			_draw_static_door_foregrounds(main)
		return
	var cell_size: float = _cell_size()
	var drawn: Dictionary = {}
	for room in main.placed_rooms:
		var pos: Vector2i = room["pos"]
		for side_value in main.get_room_doors(room):
			var side: String = str(side_value)
			var offset: Vector2i = _offset_from_side(side)
			var neighbor_pos: Vector2i = pos + offset
			var connected: bool = _door_has_connected_neighbor(main, room, neighbor_pos, offset)
			if connected and _is_duplicate_connected_door_side(side) and not _always_draw_room_doors(room):
				continue
			var key: String = "%s:%s" % [str(pos), side]
			if drawn.has(key):
				continue
			drawn[key] = true
			var edge_center: Vector2 = _door_edge_center(pos, side, cell_size)
			var frame_index: int = _door_frame_for_pair(main, pos, neighbor_pos) if connected else 0
			var source_rect: Rect2 = _door_source_rect(frame_index)
			var door_size: Vector2 = Vector2(cell_size * DOOR_DRAW_SIZE.x, cell_size * DOOR_DRAW_SIZE.y)
			var door_rotation: float = PI * 0.5 if side == "east" or side == "west" else 0.0
			draw_set_transform(edge_center, door_rotation, Vector2.ONE)
			if underlay:
				_draw_door_floor_patch(door_size)
			_draw_door_texture_layer(source_rect, door_size, underlay)
			draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)

func _draw_static_door_foregrounds(main) -> void:
	var cell_size: float = _cell_size()
	var drawn: Dictionary = {}
	for room in main.placed_rooms:
		var pos: Vector2i = room["pos"]
		for side_value in main.get_room_doors(room):
			var side: String = str(side_value)
			var offset: Vector2i = _offset_from_side(side)
			var neighbor_pos: Vector2i = pos + offset
			var connected: bool = _door_has_connected_neighbor(main, room, neighbor_pos, offset)
			if connected and _is_duplicate_connected_door_side(side) and not _always_draw_room_doors(room):
				continue
			var key: String = "%s:%s" % [str(pos), side]
			if drawn.has(key):
				continue
			drawn[key] = true
			var edge_center: Vector2 = _door_edge_center(pos, side, cell_size)
			var vertical: bool = side == "east" or side == "west"
			var frame_size: Vector2 = Vector2(cell_size * 0.026, cell_size * 0.10) if vertical else Vector2(cell_size * 0.10, cell_size * 0.026)
			draw_rect(Rect2(edge_center - frame_size * 0.5, frame_size), Color(0.04, 0.07, 0.08, 0.82))

func _door_has_connected_neighbor(main, room: Dictionary, neighbor_pos: Vector2i, offset: Vector2i) -> bool:
	return main.occupied.has(neighbor_pos) and main._placed_rooms_connected(room, main.occupied[neighbor_pos], offset)

func _is_duplicate_connected_door_side(side: String) -> bool:
	return side == "north" or side == "west"

func _always_draw_room_doors(room: Dictionary) -> bool:
	var id := str(room.get("id", ""))
	return id == "reactor" or id == "brine_core"

func _door_frame_for_pair(main, cell_a: Vector2i, cell_b: Vector2i) -> int:
	if main.test_walker_next_cell == Vector2i(-1, -1):
		return 0
	var current: Vector2i = main.test_walker_cell
	var next: Vector2i = main.test_walker_next_cell
	var crossing: bool = (current == cell_a and next == cell_b) or (current == cell_b and next == cell_a)
	if not crossing:
		return 0
	var progress: float = clampf(float(main.test_walker_progress), 0.0, 1.0)
	var open_amount: float = 1.0
	if progress < 0.16:
		open_amount = progress / 0.16
	elif progress > 0.84:
		open_amount = (1.0 - progress) / 0.16
	return clampi(int(round(open_amount * float(DOOR_OPEN_FRAMES - 1))), 0, DOOR_OPEN_FRAMES - 1)

func _door_source_rect(frame_index: int) -> Rect2:
	var clamped_frame: int = clampi(frame_index, 0, DOOR_OPEN_FRAMES - 1)
	var frame_width: float = float(door_texture.get_width()) / float(DOOR_SHEET_COLUMNS)
	var frame_height: float = float(door_texture.get_height()) / float(DOOR_SHEET_ROWS)
	var column: int = clamped_frame % DOOR_SHEET_COLUMNS
	var row: int = floori(float(clamped_frame) / float(DOOR_SHEET_COLUMNS))
	return Rect2(Vector2(float(column) * frame_width, float(row) * frame_height), Vector2(frame_width, frame_height))

func _draw_door_texture_layer(source_rect: Rect2, door_size: Vector2, underlay: bool) -> void:
	var underlay_height: float = source_rect.size.y * DOOR_UNDERLAY_FRACTION
	var overlay_height: float = source_rect.size.y - underlay_height
	var underlay_dest_height: float = door_size.y * DOOR_UNDERLAY_FRACTION
	var overlay_dest_height: float = door_size.y - underlay_dest_height
	if underlay:
		var source: Rect2 = Rect2(
			source_rect.position + Vector2(0.0, overlay_height),
			Vector2(source_rect.size.x, underlay_height)
		)
		var dest: Rect2 = Rect2(
			Vector2(-door_size.x * 0.5, -door_size.y * 0.5 + overlay_dest_height),
			Vector2(door_size.x, underlay_dest_height)
		)
		draw_texture_rect_region(door_texture, dest, source, Color(1.85, 1.85, 1.85, 1.0))
		_draw_door_light_wash(dest, false)
	else:
		var source: Rect2 = Rect2(source_rect.position, Vector2(source_rect.size.x, overlay_height))
		var dest: Rect2 = Rect2(
			Vector2(-door_size.x * 0.5, -door_size.y * 0.5),
			Vector2(door_size.x, overlay_dest_height)
		)
		draw_texture_rect_region(door_texture, dest, source, Color(2.25, 2.25, 2.25, 1.0))
		_draw_door_light_wash(dest, true)

func _draw_door_light_wash(dest: Rect2, upper_piece: bool) -> void:
	var wash_alpha := 0.10 if upper_piece else 0.07
	draw_rect(dest, Color(0.36, 0.78, 0.95, wash_alpha))
	var stripe_height := maxf(dest.size.y * 0.08, 1.0)
	var stripe := Rect2(
		dest.position + Vector2(dest.size.x * 0.18, dest.size.y * (0.28 if upper_piece else 0.54)),
		Vector2(dest.size.x * 0.64, stripe_height)
	)
	draw_rect(stripe, Color(0.68, 0.96, 1.0, wash_alpha * 1.8))

func _draw_door_floor_patch(door_size: Vector2) -> void:
	var patch_size: Vector2 = Vector2(door_size.x * 0.72, door_size.y * 0.86)
	var patch: Rect2 = Rect2(-patch_size * 0.5 + Vector2(0.0, door_size.y * 0.02), patch_size)
	draw_rect(patch, Color("#323c40"))
	draw_rect(patch.grow(-2), Color("#3f484b"))
	var line_color := Color(0.68, 0.75, 0.74, 0.30)
	draw_line(Vector2(patch.position.x, patch.get_center().y), Vector2(patch.end.x, patch.get_center().y), line_color, 1.0)
	draw_line(Vector2(patch.get_center().x, patch.position.y), Vector2(patch.get_center().x, patch.end.y), line_color, 1.0)

func _offset_from_side(side: String) -> Vector2i:
	match side:
		"north":
			return Vector2i.UP
		"east":
			return Vector2i.RIGHT
		"south":
			return Vector2i.DOWN
		_:
			return Vector2i.LEFT

func _door_edge_center(pos: Vector2i, side: String, cell_size: float) -> Vector2:
	var origin: Vector2 = Vector2(pos) * cell_size
	match side:
		"north":
			return origin + Vector2(cell_size * 0.5, 0.0)
		"east":
			return origin + Vector2(cell_size, cell_size * 0.5)
		"south":
			return origin + Vector2(cell_size * 0.5, cell_size)
		_:
			return origin + Vector2(0.0, cell_size * 0.5)

func _draw_synergy_links(main) -> void:
	if main.active_synergies.is_empty():
		return
	var cell_size := _cell_size()
	var drawn := {}
	for synergy in main.active_synergies.values():
		var room_ids: Array = synergy.get("rooms", [])
		if room_ids.size() < 2:
			continue
		for pos in main.occupied:
			var room: Dictionary = main.occupied[pos]
			if not room_ids.has(room.get("id", "")):
				continue
			for offset in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
				var neighbor_pos: Vector2i = pos + offset
				if not main.occupied.has(neighbor_pos):
					continue
				var neighbor: Dictionary = main.occupied[neighbor_pos]
				if room.get("id", "") == neighbor.get("id", "") or not room_ids.has(neighbor.get("id", "")):
					continue
				if not main._placed_rooms_connected(room, neighbor, offset):
					continue
				var key := "%s:%s:%s" % [synergy["id"], str(pos), str(neighbor_pos)]
				var reverse_key := "%s:%s:%s" % [synergy["id"], str(neighbor_pos), str(pos)]
				if drawn.has(key) or drawn.has(reverse_key):
					continue
				drawn[key] = true
				var edge_center := (Vector2(pos) + Vector2(neighbor_pos) + Vector2.ONE) * cell_size * 0.5
				var link_color := Color("#4fa38d")
				draw_circle(edge_center, cell_size * 0.035, Color(link_color.r, link_color.g, link_color.b, 0.20))
				draw_rect(Rect2(edge_center - Vector2.ONE * cell_size * 0.018, Vector2.ONE * cell_size * 0.036), link_color, false, 2.0)
				draw_line(edge_center + Vector2(-cell_size * 0.022, 0), edge_center + Vector2(cell_size * 0.022, 0), link_color, 2.0)
				draw_line(edge_center + Vector2(0, -cell_size * 0.022), edge_center + Vector2(0, cell_size * 0.022), link_color, 2.0)
				break

func _draw_room_hologram(main, cell: Vector2i, valid: bool) -> void:
	var cell_size := _cell_size()
	var room := RoomDatabaseScript.get_room(main.selected_card_id).duplicate(true)
	if room.is_empty():
		return
	room["pos"] = cell
	room["rotation"] = main.selected_rotation
	var rect := Rect2(Vector2(cell) * cell_size + Vector2.ONE, Vector2(cell_size - 2, cell_size - 2))
	var tint := Color(0.22, 0.74, 0.60, 0.045) if valid else Color(0.88, 0.18, 0.20, 0.085)
	draw_rect(rect, tint)
	var room_texture: Texture2D = _get_room_texture(room)
	if room_texture != null:
		draw_set_transform(rect.get_center(), deg_to_rad(float(main.selected_rotation * 90)), Vector2.ONE)
		draw_texture_rect(room_texture, Rect2(-rect.size * 0.5, rect.size), false, Color(0.64, 0.95, 0.82, 0.17) if valid else Color(1.0, 0.54, 0.54, 0.19))
		draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	else:
		draw_rect(rect.grow(-4), tint)
	draw_rect(rect, Color(0.35, 0.82, 0.68, 0.58) if valid else Color(1.0, 0.35, 0.39, 0.58), false, 2.0)
	var corner_len := cell_size * 0.16
	var corner_color := Color(0.68, 0.96, 0.84, 0.50) if valid else Color(1.0, 0.55, 0.58, 0.50)
	for corner in [rect.position, Vector2(rect.end.x, rect.position.y), rect.end, Vector2(rect.position.x, rect.end.y)]:
		var sx := 1.0 if corner.x == rect.position.x else -1.0
		var sy := 1.0 if corner.y == rect.position.y else -1.0
		draw_line(corner, corner + Vector2(corner_len * sx, 0), corner_color, 4)
		draw_line(corner, corner + Vector2(0, corner_len * sy), corner_color, 4)
	if main.admin_mode:
		_draw_room_path(room, rect)
		_draw_room_doors(room, rect)

func _get_room_texture(room: Dictionary) -> Texture2D:
	var id := str(room.get("id", ""))
	if room_texture_variants.has(id):
		var textures: Array = room_texture_variants[id]
		if not textures.is_empty():
			var variant_index := int(room.get("art_variant", 0)) % textures.size()
			return textures[variant_index]
	if room_textures.has(id):
		return room_textures[id]
	return null

func _door_rect(side: String, rect: Rect2) -> Rect2:
	var thickness := 40.0
	var length := 196.0
	match side:
		"north":
			return Rect2(Vector2(rect.get_center().x - length * 0.5, rect.position.y - 2), Vector2(length, thickness))
		"east":
			return Rect2(Vector2(rect.end.x - thickness + 2, rect.get_center().y - length * 0.5), Vector2(thickness, length))
		"south":
			return Rect2(Vector2(rect.get_center().x - length * 0.5, rect.end.y - thickness + 2), Vector2(length, thickness))
		_:
			return Rect2(Vector2(rect.position.x - 2, rect.get_center().y - length * 0.5), Vector2(thickness, length))

func _draw_room_path(room: Dictionary, rect: Rect2) -> void:
	var main = _get_main()
	var center := rect.get_center()
	var points := {
		"north": Vector2(center.x, rect.position.y + 2),
		"east": Vector2(rect.end.x - 2, center.y),
		"south": Vector2(center.x, rect.end.y - 2),
		"west": Vector2(rect.position.x + 2, center.y)
	}
	var doors: Array = main.get_room_doors(room)
	var path_type := str(main.get_room_layout(room).get("path", "cross"))
	match path_type:
		"ring":
			var ring := Rect2(center - Vector2(186, 186), Vector2(372, 372))
			draw_rect(ring, Color("#ff2537"), false, 20)
			for door in doors:
				draw_line(center, points[str(door)], Color("#ff2537"), 20)
		"perimeter":
			var loop := Rect2(center - Vector2(168, 168), Vector2(336, 336))
			draw_rect(loop, Color("#ff2537"), false, 20)
			for door in doors:
				var side := str(door)
				var anchor := center
				match side:
					"north":
						anchor = Vector2(center.x - 168, center.y - 168)
					"east":
						anchor = Vector2(center.x + 168, center.y - 168)
					"south":
						anchor = Vector2(center.x + 168, center.y + 168)
					_:
						anchor = Vector2(center.x - 168, center.y + 168)
				draw_line(anchor, points[side], Color("#ff2537"), 20)
		"elbow":
			if doors.size() >= 2:
				var corner := Vector2(points[str(doors[0])].x, points[str(doors[1])].y)
				draw_line(points[str(doors[0])], corner, Color("#ff2537"), 20)
				draw_line(corner, points[str(doors[1])], Color("#ff2537"), 20)
		_:
			for door in doors:
				draw_line(center, points[str(door)], Color("#ff2537"), 20)

func _draw_humans(main) -> void:
	if human_sprite == null or not main.has_test_walker():
		return
	var direction: String = main.get_test_walker_direction()
	var state: String = main.get_test_walker_state()
	var texture: Texture2D = _get_human_frame(state, direction)
	var pos: Vector2 = main.get_test_walker_position()
	var cell_size := _cell_size()
	var time_seconds: float = main.get_visual_time_seconds()
	var bob: float = 0.0 if state == "idle" else sin(time_seconds * 6.6) * cell_size * 0.0025
	var source_rect := Rect2(Vector2(26, 18), Vector2(40, 56))
	var sprite_size := Vector2(cell_size * 0.12, cell_size * 0.17)
	var foot_pos := pos + Vector2(0, cell_size * 0.038)
	var sprite_rect := Rect2(foot_pos - Vector2(sprite_size.x * 0.5, sprite_size.y) + Vector2(0, bob), sprite_size)
	var shadow_pos := Vector2(sprite_rect.get_center().x, sprite_rect.position.y + sprite_rect.size.y * 0.86)
	draw_set_transform(shadow_pos, 0.0, Vector2(cell_size * 0.00125, cell_size * 0.00028))
	draw_circle(Vector2.ZERO, 23, Color(0, 0, 0, 0.36))
	draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
	draw_texture_rect_region(texture, sprite_rect, source_rect)

func _get_human_frame(state: String, direction: String) -> Texture2D:
	if human_animations.has(state):
		var by_direction: Dictionary = human_animations[state]
		if by_direction.has(direction):
			var frames: Array = by_direction[direction]
			var fps := 3.0
			if state == "walk":
				fps = 4.0
			elif state == "run":
				fps = 7.0
			var time_seconds: float = _get_main().get_visual_time_seconds()
			var index: int = int(time_seconds * fps) % frames.size()
			return frames[index]
	return human_sprites.get(direction, human_sprite)

func _draw_connectors(room: Dictionary, occupied: Dictionary) -> void:
	var main = _get_main()
	var cell_size := _cell_size()
	var pos: Vector2i = room["pos"]
	var center := Vector2(pos) * cell_size + Vector2(cell_size, cell_size) * 0.5
	for offset in [Vector2i.RIGHT, Vector2i.DOWN]:
		if occupied.has(pos + offset) and main._placed_rooms_connected(room, occupied[pos + offset], offset):
			var neighbor_center := Vector2(pos + offset) * cell_size + Vector2(cell_size, cell_size) * 0.5
			draw_line(center, neighbor_center, Color("#88939a"), 5)
			draw_line(center, neighbor_center, Color("#1d252b"), 2)

func _draw_orbit_marker(main) -> void:
	var cell_size := _cell_size()
	var grid_pixel_size := GRID_SIZE * cell_size
	var marker_pos := Vector2(grid_pixel_size - cell_size * 2, cell_size * 2)
	draw_circle(marker_pos, 10, Color("#6b8cff"))
	draw_circle(marker_pos, 16, Color(0.42, 0.55, 1.0, 0.18))
	var poi_name: String = main.get_current_poi_name()
	draw_string(get_theme_default_font(), marker_pos + Vector2(-80, -18), poi_name, HORIZONTAL_ALIGNMENT_LEFT, 160, 12, Color("#b8c6ff"))
	var progress: float = main.get_current_poi_progress()
	var bar_rect := Rect2(marker_pos + Vector2(-38, 18), Vector2(76, 6))
	draw_rect(bar_rect, Color("#1d2530"))
	draw_rect(Rect2(bar_rect.position, Vector2(bar_rect.size.x * progress, bar_rect.size.y)), Color("#6b8cff"))
	draw_rect(bar_rect, Color("#b8c6ff"), false, 1)

func _draw_drones(main) -> void:
	var drone_rooms: Array = []
	for room in main.placed_rooms:
		if room["id"] == "mining_drone_bay" or room["id"] == "salvage_drone_bay":
			drone_rooms.append(room)
	if drone_rooms.is_empty():
		return
	var cell_size := _cell_size()
	var grid_pixel_size := GRID_SIZE * cell_size
	var target := Vector2(grid_pixel_size - cell_size * 2, cell_size * 2)
	var time: float = main.get_visual_time_seconds()
	for i in range(drone_rooms.size()):
		var room: Dictionary = drone_rooms[i]
		var start := Vector2(room["pos"]) * cell_size + Vector2(cell_size, cell_size) * 0.5
		var phase: float = fmod(time * 0.18 + float(i) * 0.23, 1.0)
		var outbound := phase < 0.5
		var path_progress := phase * 2.0 if outbound else (1.0 - phase) * 2.0
		var lane_offset := Vector2(-0.42, 0.36).normalized() * cell_size * (0.05 + float(i % 3) * 0.035)
		var destination := target + lane_offset
		var pos := start.lerp(destination, path_progress)
		var travel_vector := (target - start) if outbound else (start - target)
		var direction := _direction_for_vector(travel_vector)
		var state := "fly"
		if path_progress > 0.90:
			state = "mine"
			pos += Vector2(sin(time * 3.0 + float(i)) * cell_size * 0.01, cos(time * 2.2 + float(i)) * cell_size * 0.006)
		elif path_progress < 0.10:
			state = "idle"
			pos += Vector2(sin(time * 2.0 + float(i)) * cell_size * 0.006, cos(time * 1.7 + float(i)) * cell_size * 0.005)
		var texture: Texture2D = _get_drone_frame(state, direction)
		draw_line(start, destination, Color(0.45, 0.58, 0.66, 0.14), 1)
		var color := Color(0.72, 0.95, 1.0, 0.92) if room["id"] == "salvage_drone_bay" else Color(1.0, 0.88, 0.42, 0.96)
		var drone_size := Vector2.ONE * cell_size * 0.105
		var glow_size := drone_size * 1.18
		var trail_back := pos - travel_vector.normalized() * cell_size * 0.08
		draw_line(trail_back, pos, Color(color.r, color.g, color.b, 0.22), 2.0)
		draw_circle(pos, cell_size * 0.036, Color(color.r, color.g, color.b, 0.10))
		if texture != null:
			draw_texture_rect(texture, Rect2(pos - drone_size * 0.5, drone_size), false, color)
		else:
			draw_rect(Rect2(pos - drone_size * 0.18, drone_size * 0.36), color)
		draw_rect(Rect2(pos - glow_size * 0.5, glow_size), Color(color.r, color.g, color.b, 0.22), false, 1.5)

func _get_drone_frame(state: String, direction: String) -> Texture2D:
	if drone_animations.has(state):
		var by_direction: Dictionary = drone_animations[state]
		if by_direction.has(direction):
			var frames: Array = by_direction[direction]
			var fps := 8.0
			if state == "mine":
				fps = 6.0
			elif state == "idle":
				fps = 4.0
			var time_seconds: float = _get_main().get_visual_time_seconds()
			var index: int = int(time_seconds * fps) % frames.size()
			return frames[index]
	if drone_sprites.has(direction):
		return drone_sprites[direction]
	if drone_sprites.has("south"):
		return drone_sprites["south"]
	return null

func _direction_for_vector(vector: Vector2) -> String:
	if vector.length() <= 0.001:
		return "south"
	var angle := rad_to_deg(vector.angle())
	if angle < 0.0:
		angle += 360.0
	if angle >= 337.5 or angle < 22.5:
		return "east"
	if angle < 67.5:
		return "south-east"
	if angle < 112.5:
		return "south"
	if angle < 157.5:
		return "south-west"
	if angle < 202.5:
		return "west"
	if angle < 247.5:
		return "north-west"
	if angle < 292.5:
		return "north"
	return "north-east"

func _get_main():
	return get_tree().current_scene

func _cell_size() -> float:
	return _get_main().get_cell_size()
