extends SceneTree
func _init() -> void: call_deferred("run")
func run() -> void:
	var prefs = preload("res://scripts/title_settings.gd")
	prefs.save_path = "user://power_demand_ui.cfg"
	prefs.reduced_motion = true
	var game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = "user://power_demand_ui.meta"
	game.run_save_path = "user://power_demand_ui.loop"
	root.add_child(game)
	current_scene = game
	root.size = Vector2i(1280,720)
	game.tick_timer.stop()
	game._set_paused(true,false)
	game.testing_free_build = true
	game._place_room("mining_drone_bay",Vector2i(20,19),true)
	game.drone_fleet.synchronize(game.placed_rooms)
	var d: Dictionary = game.drone_fleet.drones[Vector2i(20,19)]
	d.battery = 0.0
	d.charge_credit = 0.0
	game.powered_room_cells[Vector2i(20,19)] = true
	game.resources.power = 0
	game._open_resource_details("power",game.grid_view)
	for frame in range(10): await process_frame
	assert(game.archive_label.text.contains("DRONE CHARGING"))
	assert(game.archive_label.text.contains("2 Power"))
	assert(game.archive_label.text.contains("1 waiting"))
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/power-demand-ui.png")
	game.queue_free()
	await process_frame
	print("POWER DEMAND UI PASS")
	quit()
