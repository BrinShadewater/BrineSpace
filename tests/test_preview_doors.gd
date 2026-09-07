extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
var failures := 0
func _init() -> void: call_deferred("run")
func run() -> void:
	Preferences.save_path = "user://preview_doors.cfg"
	Preferences.reduced_motion = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://preview_doors.meta"
	game.run_save_path = "user://preview_doors.loop"
	root.add_child(game)
	current_scene = game
	game._set_paused(true,false)
	game.tick_timer.stop()
	Preferences.placement_guides = true
	var toggle := InputEventKey.new()
	toggle.keycode = int(Preferences.keys["Placement guides"])
	toggle.pressed = true
	game._unhandled_input(toggle)
	assert(not Preferences.placement_guides, "Hotkey disables guides")
	var saved := ConfigFile.new()
	saved.load(Preferences.save_path)
	assert(saved.get_value("accessibility","placement_guides",true)==false, "Guide preference persists")
	game._open_menu()
	game._unhandled_input(toggle)
	assert(not Preferences.placement_guides, "Modal menu blocks guide hotkey")
	game._close_menu()
	var count := 0
	for id in game.RoomDatabaseScript.all_rooms():
		var room: Dictionary = game.RoomDatabaseScript.get_room(id)
		room.pos = Vector2i(21,20)
		for q in range(4):
			room.rotation = q
			var sides: Array = game.grid_view.preview_open_sides(room)
			var view = game.grid_view._bill_room_view(room)
			if view != null and view.has_method("configure_embedded"):
				view.configure_embedded(q,sides,false,0.0)
				# Opening/rotation configuration must not leak into the next installed render.
				view.configure_embedded(q,[],false,0.0)
			if sides.size()!=game.get_room_doors(room).size() or sides.has(-1):
				failures+=1
				push_error("Invalid preview apertures: " + id)
			count+=1
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*0.6)
	await process_frame
	await process_frame
	await process_frame
	game.selected_card_id = "corridor"
	game.selected_rotation = 0
	game.selected_room_cell = Vector2i(-1,-1)
	game.grid_scroll.scroll_horizontal = int(20.5*game.get_cell_size()-game.grid_scroll.size.x*0.4)
	game.grid_scroll.scroll_vertical = int(20.5*game.get_cell_size()-game.grid_scroll.size.y*0.5)
	await process_frame
	if DisplayServer.get_name() != "headless":
		for q in range(4):
			game.selected_rotation = q
			var motion := InputEventMouseMotion.new()
			motion.position = game.grid_view.get_global_transform_with_canvas() * (Vector2(21.5,20.5)*game.get_cell_size())
			root.warp_mouse(motion.position)
			root.push_input(motion,true)
			await process_frame
			game.grid_view.queue_redraw()
			await RenderingServer.frame_post_draw
			root.get_texture().get_image().save_png("res://output/preview-corridor-q%d.png" % q)
	for path in [Preferences.save_path,game.meta.save_path,game.run_save_path]:
		if FileAccess.file_exists(path): DirAccess.remove_absolute(path)
	print("PREVIEW DOORS: %d cases, %d failures" % [count,failures])
	quit(failures)
