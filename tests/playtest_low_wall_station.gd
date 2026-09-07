extends SceneTree

var game
var capture_dir := ""
var failures := 0

func _initialize() -> void: call_deferred("run")

func expect(value: bool, label: String) -> void:
	if not value:
		failures += 1
		push_error(label)

func settle() -> void:
	for i in range(8): await process_frame
	await RenderingServer.frame_post_draw

func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--output="): capture_dir = arg.trim_prefix("--output=")
	if not capture_dir.begins_with("res://output/") or DirAccess.dir_exists_absolute(capture_dir):
		push_error("A fresh res://output/ directory is required")
		quit(1)
		return
	DirAccess.make_dir_recursive_absolute(capture_dir)
	root.size = Vector2i(1600, 900)
	root.content_scale_size = Vector2i(1920, 1080)
	var prefs = preload("res://scripts/title_settings.gd")
	prefs.initialized = true
	expect(not prefs.raised_walls, "Production default retains low walls")
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://low_wall_station_%d.meta" % OS.get_process_id()
	game.run_save_path = "user://low_wall_station_%d.loop" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	game._confirm_doctrines()
	game._set_paused(true, false)
	await settle()
	var captures := 0
	for q in range(4):
		for room_id in ["command_center", "crew_hab", "med_bay", "hydroponics_bay", "corridor", "corner"]:
			if preload("res://scripts/room_database.gd").get_room(room_id).is_empty():
				expect(false, "Missing room: " + room_id)
				continue
			game.placed_rooms.clear()
			game.occupied.clear()
			game.wrecks.clear()
			game.selected_rotation = q
			game._place_room(room_id, Vector2i(20, 20), true)
			game._set_grid_zoom(0.60)
			game.selected_card_id = ""
			game.hovered_card_id = ""
			game.hover_cell = Vector2i(-1, -1)
			game._refresh_all()
			await settle()
			var at: Vector2 = Vector2(20.5,20.5) * game.get_cell_size() - game.grid_scroll.size * 0.5
			game.grid_scroll.scroll_horizontal = roundi(at.x)
			game.grid_scroll.scroll_vertical = roundi(at.y)
			game.grid_view.queue_redraw()
			await settle()
			var frame := root.get_texture().get_image()
			if room_id in ["corridor", "corner"]:
				for canvas in game.grid_view.content_canvases.values():
					expect(not canvas.visible, "Corridor cannot retain the previous room's prop canvas")
			expect(frame.get_size() == Vector2i(1600,900), "Native frame dimensions")
			expect(frame.save_png(capture_dir.path_join("%s-q%d.png" % [room_id,q])) == OK, "Capture saved")
			captures += 1
	for direction in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
		game.placed_rooms.clear()
		game.occupied.clear()
		game.selected_rotation = 0
		var origin := Vector2i(20,20)
		game._place_room("command_center", origin, true)
		game._place_room("command_center", origin + direction, true)
		expect(game._placed_rooms_connected(game.occupied[origin], game.occupied[origin + direction], direction), "Pair has reciprocal doors")
		game._set_grid_zoom(0.38)
		game._refresh_all()
		await settle()
		var center: Vector2 = (Vector2(origin) + Vector2.ONE * 0.5 + Vector2(direction) * 0.5) * game.get_cell_size() - game.grid_scroll.size * 0.5
		game.grid_scroll.scroll_horizontal = roundi(center.x)
		game.grid_scroll.scroll_vertical = roundi(center.y)
		game.grid_view.queue_redraw()
		await settle()
		var frame := root.get_texture().get_image()
		expect(frame.get_size() == Vector2i(1600,900), "Connected native frame dimensions")
		expect(frame.save_png(capture_dir.path_join("pair-%d-%d.png" % [direction.x,direction.y])) == OK, "Connected capture saved")
		captures += 1
	print("LOW WALL STATION: %d captures; %d failures" % [captures,failures])
	quit(1 if failures else 0)
