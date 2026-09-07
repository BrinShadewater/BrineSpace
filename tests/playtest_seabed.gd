extends SceneTree
var game
var output := "res://output/seabed-v1"

func _init() -> void:
	call_deferred("run")

func settle() -> void:
	for i in range(4):
		await process_frame
	await RenderingServer.frame_post_draw

func run() -> void:
	DirAccess.make_dir_recursive_absolute(output)
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://seabed_fixture_meta_%d.json" % OS.get_process_id()
	game.run_save_path = "user://seabed_fixture_run_%d.json" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	await settle()
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.placed_rooms.clear()
	game.occupied.clear()
	for entry in [["brine_core",20,20],["corridor",21,20],["life_support",22,20],["hydroponics_bay",20,21],["crew_hab",22,21]]:
		game._place_room(entry[0], Vector2i(entry[1],entry[2]), true)
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1,-1)
	game._refresh_all()
	for width in [1280,1600,2560]:
		root.size = Vector2i(width,roundi(width*9.0/16.0))
		await settle()
		game._fit_station_view()
		game.grid_view.queue_redraw()
		await settle()
		var frame := root.get_texture().get_image()
		frame.save_png(output.path_join("station-%d.png" % width))
		var background_colors: Dictionary = {}
		var sample := Vector2i(roundi(frame.get_width()*0.06),roundi(frame.get_height()*0.20))
		for y in range(sample.y,sample.y+16):
			for x in range(sample.x,sample.x+16):
				background_colors[frame.get_pixel(x,y).to_rgba32()] = true
		assert(background_colors.size()>8, "Seabed texture must render after window resize")
	var renderer = game.grid_view.seabed_background
	assert(renderer.textures.has("silt-plain"), "Seabed must load raw PNG")
	var positions = renderer.scenery.duplicate(true)
	game.grid_view.queue_redraw()
	await settle()
	assert(positions == renderer.scenery, "Scenery must remain stable across redraws")
	var paths := [game.meta.save_path, game.run_save_path]
	game.free()
	for path in paths:
		if FileAccess.file_exists(path):
			DirAccess.remove_absolute(ProjectSettings.globalize_path(path))
	print("SEABED PASS: raw load, stable scenery, three native station captures; fixture-only saves")
	quit()
