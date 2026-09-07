extends "res://tests/playtest_nursery_art.gd"
const NPC = preload("res://scripts/bill_npc.gd")

func run() -> void:
	capture_dir = "res://character/crew-underwater-v1/pilot/native/death"
	DirAccess.make_dir_recursive_absolute(capture_dir)
	game = MainScene.instantiate()
	game.Preferences.save_path = "user://crew_death_visual_settings_%d.cfg" % OS.get_process_id()
	game.meta.save_path = "user://crew_death_visual_meta_%d.json" % OS.get_process_id()
	game.run_save_path = "user://crew_death_visual_run_%d.json" % OS.get_process_id()
	root.add_child(game)
	current_scene = game
	root.mode = Window.MODE_WINDOWED
	root.borderless = false
	root.size = Vector2i(1600, 900)
	game.pending_doctrines.assign(["biosphere", "recovery"])
	game._confirm_doctrines()
	game._set_paused(true)
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	var origin := Vector2i(20, 20)
	game._place_room("maintenance_bay", origin, true)
	for offset in [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]:
		game._place_room("storage_bay", origin + offset, true)
	for cell in game.occupied: game.powered_room_cells[cell] = true
	game.test_walker_cell = origin
	game.bill_npc = NPC.new()
	game.rng.seed = 2231
	game.branforth_npc.decision_rng.seed = 9912
	game.selected_card_id = ""
	game.hover_cell = Vector2i(-1, -1)
	game._refresh_all()
	game._set_grid_zoom(game.DEFAULT_GRID_ZOOM * 0.9)
	await settle()
	game._center_grid_on_station_now()
	await settle()
	game._update_test_walker(0.1)
	var crew := [game.bill_npc, game.veld_npc, game.branforth_npc]
	for npc in crew: npc.die()
	game._update_test_walker(0.1)
	game.visual_time_seconds = 100.0
	game.grid_view._get_human_frame("death-ground", "east")
	game.grid_view._get_veld_frame(game)
	game.grid_view._get_branforth_frame(game)
	for phase in [0.0,0.22,0.4,0.6,0.8,1.1,3.0]:
		game.visual_time_seconds = 100.0 + phase
		await capture("death-%04d" % roundi(phase*1000))
		room_pixels(origin).save_png(capture_dir.path_join("death-%04d-crop.png" % roundi(phase*1000)))
		for npc in crew: expect(npc.dead and npc.path.is_empty(), "Native death remains terminal")
	for save_path in [game.meta.save_path, game.run_save_path, game.Preferences.save_path]:
		if FileAccess.file_exists(save_path): DirAccess.remove_absolute(save_path)
	print("CREW DEATH NATIVE: %s" % ("PASS" if failures == 0 else "FAIL"))
	game.free()
	quit(0 if failures == 0 else 1)
