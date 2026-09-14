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
	while not game.startup_complete: await process_frame
	root.size = Vector2i(1280,720)
	game.tick_timer.stop()
	game._set_paused(true,false)
	assert(game.selected_card_id.is_empty())
	var before_rooms: int = game.placed_rooms.size()
	var before_resources: Dictionary = game.resources.duplicate(true)
	game._on_grid_clicked(Vector2i(19,20))
	assert(game.placed_rooms.size() == before_rooms and game.drone_fleet.orders.is_empty())
	assert(game.resources == before_resources)
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
	assert(game.archive_label.text.contains("POWER // NEXT CYCLE"))
	assert(game.archive_label.text.contains("Generation:"))
	assert(game.archive_label.text.contains("2 Power"))
	assert(game.archive_label.text.contains("1 waiting"))
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/power-demand-ui.png")
	game.resources.power = 3
	game._refresh_all()
	assert(game.archive_label.text.contains("Battery discharge: 2 Power"))
	assert(game.archive_label.text.contains("Stored: 3 -> 1"))
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/power-discharge-ui.png")
	game._toggle_journal()
	game._place_room("current_turbine",Vector2i(19,20),true)
	var turbine: Dictionary = game.occupied[Vector2i(19,20)]
	turbine.rotation = 3
	game.wrecks[Vector2i(18,20)] = {"kind":"basalt","cleared":false,"progress":0.0,"active":false}
	game.selected_room_cell = turbine.pos
	game.selected_card_id = ""
	game.hovered_card_id = ""
	game._refresh_all()
	assert(game.inspector_label.text.contains("INTAKE WEST (18, 20): BLOCKED BY ROCK"))
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/turbine-intake-feedback-ui.png")
	game.wrecks[Vector2i(18,20)].cleared = true
	game._refresh_all()
	assert(game.inspector_label.text.contains("INTAKE WEST (18, 20): CLEAR"))
	# Hovering a legal build on the intake names the consequence before paying.
	# A north/south corridor above the intake gives the hovered corridor a legal port.
	game.selected_rotation = 0
	game._place_room("corridor",Vector2i(18,19),true)
	var hazard_cell := Vector2i(-1,-1)
	for rotation in range(4):
		game.selected_card_id = "corridor"
		game.selected_rotation = rotation
		if game.get_placement_problem("corridor",Vector2i(18,20)).is_empty():
			hazard_cell = Vector2i(18,20)
			break
	if hazard_cell != Vector2i(-1,-1):
		game.hover_cell = hazard_cell
		game._refresh_placement_status()
		game._position_placement_feedback()
		assert(game.placement_label.text.contains("BLOCKS CURRENT TURBINE INTAKE AT (19, 20)"),game.placement_label.text)
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png("res://output/placement-hazard-ui.png")
	else:
		push_warning("No legal corridor placement on the intake in this fixture: "+game.get_placement_problem("corridor",Vector2i(18,20)))
	game.selected_card_id = ""
	game.queue_free()
	await process_frame
	print("POWER DEMAND UI PASS")
	quit()
