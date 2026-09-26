extends SceneTree
## Exercise lazy directional loaders even when bought layouts hide their props.
const Grid = preload("res://scripts/grid_canvas.gd")
const DB = preload("res://scripts/room_database.gd")
const SafeImage = preload("res://scripts/safe_image.gd")
var checks := 0
var errors := 0

func _init() -> void:
	call_deferred("run")

func check_texture(texture: Texture2D) -> void:
	checks += 1
	if texture == null or texture.get_width() <= 0:
		errors += 1

func run() -> void:
	preload("res://scripts/room_layout_store.gd").loaded = true
	preload("res://scripts/room_layout_store.gd").data = {}
	var grid = Grid.new()
	grid.hide()
	grid.process_mode = Node.PROCESS_MODE_DISABLED
	root.add_child(grid)
	# raw_texture returns null without recording SafeImage.failures, so check directly.
	for variant in Grid.FOUNDATION_PATHS:
		check_texture(grid._foundation_texture(variant))
	for id in ["cold_store", "galley", "salvage_workshop", "observation_room", "tidal_condenser", "construction_drone_bay", "command_center"]:
		var room = grid._bill_room_view(DB.get_room(id))
		if room == null:
			push_error("Missing runtime room: " + id)
			errors += 1
			continue
		for q in range(4):
			room.quarter = q
			var center: Vector2 = [Vector2(0,-100),Vector2(100,0),Vector2(0,100),Vector2(-100,0)][q]
			var prop := {"rect": Rect2(center-Vector2(10,10),Vector2(20,20))}
			match id:
				"cold_store", "galley", "salvage_workshop":
					var ids: Array = {"cold_store":["cooler","fridge","rack"],"galley":["kitchen","serving","mess-table"],"salvage_workshop":["bench","tote"]}[id]
					for item in ids: check_texture(room.overhead_texture(item))
				"observation_room":
					for item in ["wooden-desk","chair-rear","observation_north","observation_east","observation_west"]:
						check_texture(room.furnishing_texture(item))
				"tidal_condenser":
					for item in ["tidal_pump","tidal_monitor"]:
						prop.id = item
						check_texture(room._equipment_texture(prop))
				"command_center":
					for item in ["command_table","command_comms","command_systems"]:
						prop.id = item
						check_texture(room._overhead_texture(prop))
				"construction_drone_bay":
					for method in ["_cradle_texture","_hatch_texture","_bench_texture","_panel_texture"]:
						check_texture(room.call(method,prop))
	for path in SafeImage.failures:
		push_error("Runtime art failed: " + path)
	errors += SafeImage.failures.size()
	print("RUNTIME ROOM ART: %d directional/foundation checks, %d failures" % [checks,errors])
	grid.queue_free()
	await process_frame
	quit(1 if errors else 0)
