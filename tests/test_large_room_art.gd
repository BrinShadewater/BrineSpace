extends SceneTree

const Rooms = preload("res://scripts/room_database.gd")
const Footprint = preload("res://scripts/room_footprint.gd")
const Cards = preload("res://scripts/room_card_art.gd")
const Main = preload("res://scripts/main.gd")
const Grid = preload("res://scripts/grid_canvas.gd")

const IDS := ["hydroponics_farm", "storage_depot", "moonbay", "tidal_power_plant"]
const COSTS := [{"metal": 16, "biomass": 3}, {"metal": 18},
	{"metal": 20, "rare_minerals": 2}, {"metal": 18, "rare_minerals": 3}]
const COLORS := ["Life Support", "Engineering", "Robotics", "Engineering"]
const VIEWS := ["res://rooms/large-rooms/hydroponics_farm.gd",
	"res://rooms/large-rooms/storage_depot.gd", "res://rooms/large-rooms/moonbay.gd",
	"res://rooms/large-rooms/tidal_power_plant.gd"]
const ART := ["res://rooms/large-rooms/art/grow_beds.png",
	"res://rooms/large-rooms/art/cargo_gantry.png", "res://rooms/large-rooms/art/mini_sub.png",
	"res://rooms/large-rooms/art/tidal_turbine.png"]
const WALL_ART := ["res://rooms/large-rooms/art/grow_wall_bank.png",
	"res://rooms/large-rooms/art/cargo_wall_bank.png", "res://rooms/large-rooms/art/launch_wall_bank.png",
	"res://rooms/large-rooms/art/tidal_wall_bank.png"]
const Common = preload("res://rooms/large-rooms/common.gd")

var failures := 0

func check(ok: bool, message: String) -> void:
	if not ok:
		failures += 1
		push_error(message)

func doors_share_walkable_floor(room: Dictionary, bounds: Array, rotation: int) -> bool:
	const STEP := 16.0
	const COUNT := 48
	var blockers: Array[Rect2] = []
	for source in bounds:
		var bound: Rect2 = source
		for turn in range(rotation):
			bound = Rect2(Vector2(768.0 - bound.end.y, bound.position.x), Vector2(bound.size.y, bound.size.x))
		blockers.append(bound.grow(10.0))
	var blocked := {}
	for y in range(COUNT):
		for x in range(COUNT):
			var point := Vector2(x + 0.5, y + 0.5) * STEP
			for bound in blockers:
				if bound.has_point(point):
					blocked[Vector2i(x, y)] = true
					break
	var entries: Array[Vector2i] = []
	for port in room.ports:
		var point: Vector2 = Common.port_center(port).rotated(float(rotation) * PI * 0.5) + Vector2.ONE * 384.0
		match Common.rotated_side(str(port.side), rotation):
			"north": point.y = 48.0
			"east": point.x = 720.0
			"south": point.y = 720.0
			"west": point.x = 48.0
		var entry := Vector2i(int(point.x / STEP), int(point.y / STEP))
		if blocked.has(entry): return false
		entries.append(entry)
	var queue: Array[Vector2i] = [entries[0]]
	var seen := {entries[0]: true}
	var head := 0
	while head < queue.size():
		var current: Vector2i = queue[head]
		head += 1
		for direction in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
			var next: Vector2i = current + direction
			if next.x < 0 or next.y < 0 or next.x >= COUNT or next.y >= COUNT or blocked.has(next) or seen.has(next): continue
			seen[next] = true
			queue.append(next)
	for entry in entries:
		if not seen.has(entry): return false
	return true

func _init() -> void:
	for i in range(IDS.size()):
		var id: String = IDS[i]
		var room: Dictionary = Rooms.get_room(id)
		check(not room.is_empty(), id + " has a blueprint")
		if room.is_empty(): continue
		check(room.get("size") == Vector2i(2, 2), id + " occupies 2x2")
		check(room.get("cost", {}) == COSTS[i], id + " has premium cost")
		check(room.get("category", "") == COLORS[i], id + " uses accepted department color")
		check(Rooms.STARTING_UNLOCKS.has(id), id + " can enter the first run sequence")
		room["pos"] = Vector2i(10, 10)
		room["rotation"] = 0
		check(Footprint.ports(room).size() == 4, id + " has four perimeter doors")
		check(Cards.PATHS.has(id) and str(Cards.PATHS.get(id, "")).begins_with("res://assets/"), id + " has a whole card art path")
		if Cards.PATHS.has(id): check(FileAccess.file_exists(str(Cards.PATHS[id])), id + " card image exists")
		check(ResourceLoader.exists(VIEWS[i]), id + " fixed view exists")
		var painted := Image.new()
		check(painted.load_png_from_buffer(FileAccess.get_file_as_bytes(ART[i])) == OK, id + " painted installation decodes without an import")
		if painted.get_width()>0:
			check(painted.get_pixel(0,0).a < 0.1 and painted.get_pixel(int(painted.get_width()/2),int(painted.get_height()/2)).a > 0.5, id + " installation has true exterior alpha and visible interior")
		var wall_bank := Image.new()
		check(wall_bank.load_png_from_buffer(FileAccess.get_file_as_bytes(WALL_ART[i])) == OK, id + " painted riser bank decodes without an import")
		if wall_bank.get_width()>0:
			check(wall_bank.get_pixel(0,0).a < 0.1 and wall_bank.get_pixel(int(wall_bank.get_width()/2),int(wall_bank.get_height()/2)).a > 0.5, id + " riser bank has true exterior alpha and visible interior")
			var raster: Vector2i = Common.wall_bank_raster_size(wall_bank.get_size())
			check(raster.x <= 1020 and raster.y <= 310 and raster.x >= 400, id + " wall bank normalizes to riser-scale pixel density")
		if ResourceLoader.exists(VIEWS[i]):
			var view = load(VIEWS[i])
			var style: Dictionary = view.WALL_STYLE
			check(preload("res://rooms/whole-room/riser_catalog.gd").catalog().has(str(style.material)), id + " uses a registered painted riser face")
			check(str(style.art) == WALL_ART[i], id + " mounts its own riser bank")
			for rotation in range(4):
				var axis: float = Common.north_art_axis(room, style, rotation)
				check(absf(axis) <= 230.0, id + " riser bank remains on the north wall in rotation " + str(rotation))
				for port in room.ports:
					if Common.rotated_side(str(port.side), rotation) != "north": continue
					var entry: float = Common.port_center(port).rotated(float(rotation)*PI*0.5).x
					check(absf(axis-entry) >= 148.0, id + " north wall art clears its door in rotation " + str(rotation))
				if room.has("ocean_side") and Common.rotated_side(str(room.ocean_side), rotation) == "north":
					check(absf(axis) >= 198.0, id + " north wall art clears its ocean face in rotation " + str(rotation))
			var bounds: Array = view.fixed_bounds()
			check(not bounds.is_empty() and bounds[0].size.x >= 150 and bounds[0].size.y >= 100, id + " has a very large fixed prop")
			var features: Array = view.FEATURES
			check(features.size() >= 3, id + " has supporting work areas")
			var centerpiece := Rect2(bounds[0].position - Vector2.ONE * 384.0, bounds[0].size)
			for feature_index in range(features.size()):
				var feature: Dictionary = features[feature_index]
				var feature_rect: Rect2 = feature.rect
				check(str(feature.path).begins_with("res://assets/station-props-v2/") and FileAccess.file_exists(str(feature.path)), id + " supporting art is an installed station prop")
				check(feature_rect.position.x >= -312.0 and feature_rect.position.y >= -312.0 and feature_rect.end.x <= 312.0 and feature_rect.end.y <= 312.0, id + " support clears the north riser in every rotation")
				check(not feature_rect.intersects(centerpiece), id + " support leaves the fixed centerpiece clear")
				for earlier in range(feature_index):
					check(not feature_rect.intersects(features[earlier].rect), id + " supports do not overlap")
			for rotation in range(4):
				check(doors_share_walkable_floor(room, bounds, rotation), id + " connects all doors around fixed props in rotation " + str(rotation))
			for port in room.ports:
				var cell: Vector2i = port.cell
				var access := Rect2()
				match str(port.side):
					"north": access = Rect2(cell.x * 384.0 + 122, 0, 140, 180)
					"east": access = Rect2(588, cell.y * 384.0 + 122, 180, 140)
					"south": access = Rect2(cell.x * 384.0 + 122, 588, 140, 180)
					"west": access = Rect2(0, cell.y * 384.0 + 122, 180, 140)
				for bound in bounds:
					check(not bound.intersects(access), id + " prop stays clear of door approach")
	var farm: Dictionary = Rooms.get_room("hydroponics_farm")
	check(farm.get("production", {}) == {"food": 6, "oxygen": 3} and farm.get("consumption", {}) == {"water": 2, "power": 3}, "Farm has proposed cycle rates")
	var depot: Dictionary = Rooms.get_room("storage_depot")
	check(depot.get("storage", {}) == {"metal": 180, "food": 80, "oxygen": 80, "water": 80}, "Depot adds large shared capacity")
	var plant: Dictionary = Rooms.get_room("tidal_power_plant")
	check(plant.get("production", {}).get("power", 0) == 14 and plant.get("ocean_side", "") == "north", "Tidal plant has major ocean-dependent output")
	var moonbay: Dictionary = Rooms.get_room("moonbay")
	check(moonbay.get("ocean_side", "") == "west" and moonbay.get("consumption", {}).get("power", 0) > 0, "Moonbay has a west launch wall and power need")
	var bay = preload("res://rooms/large-rooms/moonbay.gd")
	check(bay.BAY_DOOR_WIDTH > 92.0, "Moonbay enclosure has a larger sub-bay door than a station port")
	check(bay.SUB_BOUNDS.size.y + 20.0 <= bay.BAY_DOOR_WIDTH, "The mini-sub clears the launch gate with room on both sides")
	var grid = Grid.new()
	moonbay.pos = Vector2i(10,10)
	var base: Dictionary = grid.bill_room_geometry(moonbay, [], moonbay.pos)
	moonbay.rotation = 1
	var rotated: Dictionary = grid.bill_room_geometry(moonbay, [], moonbay.pos)
	check(not base.blockers.is_empty() and not rotated.blockers.is_empty() and rotated.blockers[0].position.x > base.blockers[0].position.x, "Fixed sub collision follows room rotation")
	grid.free()
	if not plant.is_empty():
		var game = Main.new()
		plant.pos = Vector2i(10, 10)
		plant.rotation = 0
		check(game.has_method("_ocean_face_problem"), "Plant has a whole-side intake check")
		if game.has_method("_ocean_face_problem"):
			check(game.call("_ocean_face_problem", plant).is_empty(), "Open ocean supports the plant")
			game.occupied[Vector2i(10, 9)] = {"id": "corridor"}
			check(not game.call("_ocean_face_problem", plant).is_empty(), "Blocked ocean intake stops the plant")
		game.free()
	print("LARGE ROOM ART ", "PASS" if failures == 0 else "FAIL", " / ", failures, " failures")
	quit(0 if failures == 0 else 1)
