extends SceneTree
const Preferences = preload("res://scripts/title_settings.gd")
var game
var records: Array = []
var failures := 0
var measure_render := false
var output_dir:="res://output/game-pass/baseline"
func _init() -> void: call_deferred("run")
func frame() -> void:
	await process_frame
	RenderingServer.force_draw()
func run() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--label="): output_dir="res://output/game-pass/"+arg.trim_prefix("--label=")
	DirAccess.make_dir_recursive_absolute(output_dir)
	var prefix := "user://large_render_%d" % OS.get_process_id()
	Preferences.save_path = prefix+".cfg"
	game = load("res://scenes/main.tscn").instantiate()
	game.meta.save_path = prefix+".meta"
	game.run_save_path = prefix+".loop"
	root.add_child(game)
	current_scene = game
	Preferences.pause_unfocused = false
	root.size = Vector2i(1600,900)
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	measure_render = RenderingServer.has_method("viewport_set_measure_render_time")
	if measure_render: RenderingServer.call("viewport_set_measure_render_time",root.get_viewport_rid(),true)
	game.set_process(false)
	game.grid_view.profile_draw = true
	game.tick_timer.stop()
	game.testing_free_build = true
	game.testing_disable_failures = true
	game.rng.seed = 9406
	game.drone_fleet.sites.clear()
	game.drone_fleet.sites_initialized = true
	game.selected_card_id = ""
	game.Architects.advance_core(game,7.0)
	for resource in game.resources: game.resources[resource] = 1000
	game._place_room("construction_drone_bay",Vector2i(15,15),true)
	var ids := ["reactor","life_support","hydroponics_bay","research_lab","storage_bay","crew_hab","corridor","med_bay"]
	for target in [50,100]:
		for y in range(15,26):
			for x in range(15,26):
				if game.placed_rooms.size()>=target: break
				var cell := Vector2i(x,y)
				if game.occupied.has(cell) or game.wrecks.has(cell): continue
				game._place_room(ids[(x+y*11)%ids.size()],cell,true)
		game._refresh_all()
		await frame()
		game._fit_station_view()
		for i in range(6): await frame()
		game._center_grid_on_station_now()
		game.drone_fleet.enqueue("corridor",Vector2i(15,14 if target==50 else 13),0)
		await sample("%d-fit" % target)
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM)
		game._center_grid_on_station_now()
		await sample("%d-close" % target)
	game._set_paused(true,false)
	game.tick_timer.stop()
	for action in ["construction","menu-open","menu-close","zoom-fit","zoom-close","save","load"]:
		await interaction(action)
	var path := output_dir+"/large-render-profile.json"
	var file := FileAccess.open(path,FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"\t"))
	file.close()
	for suffix in [".cfg",".meta",".meta.bak",".loop",".loop.bak"]:
		if FileAccess.file_exists(prefix+suffix): DirAccess.remove_absolute(prefix+suffix)
	print("LARGE RENDER PROFILE COMPLETE: ",failures," failures")
	quit(failures)
func sample(label: String) -> void:
	game._set_paused(false,false)
	game.tick_timer.stop()
	for i in range(30):
		game._process(1.0/60.0)
		await frame()
	var timings: Array = []
	var calls := 0.0
	var simulation_ms := 0.0
	var render_cpu_ms := 0.0
	var render_gpu_ms := 0.0
	var stages := {}
	var moving_drone_frames := 0
	var start: int = Time.get_ticks_usec()
	var rooms_before: int = game.placed_rooms.size()
	var foot_before: Vector2 = game.bill_npc.foot
	for i in range(90):
		var sim_start := Time.get_ticks_usec()
		game._process(1.0/60.0)
		simulation_ms += (Time.get_ticks_usec()-sim_start)/90000.0
		for drone in game.drone_fleet.drones.values():
			if drone.phase != "docked":
				moving_drone_frames += 1
				break
		await frame()
		var now := Time.get_ticks_usec()
		timings.append((now-start)/1000.0)
		start = now
		accumulate_stages(stages,90.0)
		if measure_render:
			render_cpu_ms += float(RenderingServer.call("viewport_get_measured_render_time_cpu",root.get_viewport_rid()))/90.0
			render_gpu_ms += float(RenderingServer.call("viewport_get_measured_render_time_gpu",root.get_viewport_rid()))/90.0
		calls += Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)/90.0
	var result := summarize(timings)
	result.merge({"render_cpu_ms":render_cpu_ms if measure_render else null,"render_gpu_ms":render_gpu_ms if measure_render else null,"simulation_ms":simulation_ms,"stages_ms":stages,"scenario":label,"rooms_start":rooms_before,"rooms_end":game.placed_rooms.size(),"draw_calls":calls,"drone_active_frames":moving_drone_frames,"crew_displacement":game.bill_npc.foot.distance_to(foot_before)})
	records.append(result)
	print(JSON.stringify(result))
	root.get_texture().get_image().save_png(output_dir+"/large-render-"+label+".png")
func summarize(timings: Array) -> Dictionary:
	var mean := 0.0
	for value in timings: mean += value/timings.size()
	var ordered := timings.duplicate()
	ordered.sort()
	return {"mean_ms":mean,"p95_ms":ordered[mini(ordered.size()-1,ceili(ordered.size()*0.95)-1)],"max_ms":ordered.back()}
func interaction(action: String) -> void:
	var timings: Array = []
	game.grid_view.draw_profile_totals_usec.clear()
	var first_stages: Dictionary = {}
	var started := Time.get_ticks_usec()
	match action:
		"construction": game._place_room("storage_bay",Vector2i(28,20),false,true)
		"menu-open": game._open_menu()
		"menu-close": game._close_menu()
		"zoom-fit": game._fit_station_view()
		"zoom-close": game._set_grid_zoom(game.DEFAULT_GRID_ZOOM)
		"save":
			game.testing_free_build = false
			game.testing_disable_failures = false
			if not game._save_active_loop():
				failures += 1
				push_error("Save fixture failed: "+game.RunSave.last_error)
		"load":
			if not game.RunSave.restore(game,game.RunSave.read(game.run_save_path)):
				failures += 1
				push_error("Load fixture failed: "+game.RunSave.last_error)
	var cpu_ms := (Time.get_ticks_usec()-started)/1000.0
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = true
	var previous := started
	for i in range(12):
		await frame()
		var now := Time.get_ticks_usec()
		timings.append((now-previous)/1000.0)
		previous = now
		if i==0: first_stages = game.grid_view.draw_profile_totals_usec.duplicate()
	var result := summarize(timings)
	result.merge({"interaction":action,"cpu_ms":cpu_ms,"first_frame_ms":timings[0]})
	result["first_frame_stage_usec"] = first_stages
	records.append(result)
	print(JSON.stringify(result))

func accumulate_stages(totals: Dictionary, divisor: float) -> void:
	for key in game.grid_view.draw_profile_usec:
		totals[key] = float(totals.get(key,0.0))+float(game.grid_view.draw_profile_usec[key])/(divisor*1000.0)
	for canvas in game.grid_view.content_canvases.values():
		if not canvas.visible: continue
		for part in ["prepare_usec","draw_usec"]:
			var key: String = "content_"+part
			totals[key] = float(totals.get(key,0.0))+float(canvas.get(part))/(divisor*1000.0)
