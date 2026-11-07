extends "res://tests/playtest_nursery_art.gd"
func wait_visual_advance(start: float) -> void:
	var deadline=Time.get_ticks_msec()+10000
	while game.visual_time_seconds<start+0.35 and Time.get_ticks_msec()<deadline:
		await process_frame
	expect(game.visual_time_seconds>=start+0.35,"Real station visual clock advances while running")
func run() -> void:
	if capture_dir.is_empty(): capture_dir="res://output/command-owner-repair-2026-09-12/station-pause"
	DirAccess.make_dir_recursive_absolute(capture_dir)
	preload("res://scripts/title_settings.gd").save_path="user://command_asset_pause.cfg"
	game=MainScene.instantiate()
	game.meta.save_path="user://command_asset_pause.meta"
	game.run_save_path="user://command_asset_pause.loop"
	root.add_child(game); current_scene=game; root.size=Vector2i(1600,900)
	root.gui_disable_input=true
	game.set_process_input(false); game.set_process_unhandled_input(false)
	game.testing_free_build=true; game.testing_disable_failures=true
	game.tick_timer.stop(); game.running=true
	game.placed_rooms.clear(); game.occupied.clear()
	game.selected_card_id=""; game.wrecks.clear()
	var cell=Vector2i(20,20)
	game._place_room("command_center",cell,true)
	game.crew_comms.dismiss()
	game.crew_comms.set_process(false)
	game._refresh_all(); await settle(); game._fit_station_view(); await settle()
	var records=[]
	for q in range(4):
		game.occupied[cell].rotation=q
		game.powered_room_cells[cell]=true
		game._refresh_all(); game.powered_room_cells[cell]=true
		game._set_paused(false,false)
		var start: float=game.visual_time_seconds
		await wait_visual_advance(start)
		game._set_paused(true,false)
		await capture("q%d-paused-a"%q)
		var frozen=room_pixels(cell).get_data()
		var clock: float=game.visual_time_seconds
		var machine: float=game.grid_view.command_view.machine_clock
		var deadline=Time.get_ticks_msec()+350
		while Time.get_ticks_msec()<deadline: await process_frame
		await capture("q%d-paused-b"%q)
		expect(game.visual_time_seconds==clock,"Paused station visual clock frozen")
		expect(game.grid_view.command_view.machine_clock==machine,"Paused Command renderer clock frozen")
		expect(game.grid_view.command_view.operating,"Command is powered during pause review")
		expect(frozen==room_pixels(cell).get_data(),"Paused Command native pixels frozen")
		records.append({"quarter":q,"clock_before_run":start,"paused_clock":clock,"machine_clock":machine,"operating":game.grid_view.command_view.operating,"pixels_equal":frozen==room_pixels(cell).get_data()})
	var record=FileAccess.open(capture_dir+"/result.json",FileAccess.WRITE)
	record.store_string(JSON.stringify({"failures":failures,"samples":records},"\t")); record.close()
	print("COMMAND STATION PAUSE: failures=",failures)
	quit(1 if failures else 0)
