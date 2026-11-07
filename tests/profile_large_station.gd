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
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	game.set_process(false)
	game.grid_view.profile_draw = true
	game.tick_timer.stop()
	game.testing_free_build = true
	game.testing_disable_failures = true
	game.rng.seed = 9406
	game.drone_fleet.sites.clear()
	game.drone_fleet.sites_initialized = true
	game.selected_card_id = ""
	game.Architects.advance_core(game,10.0)
	for resource in game.resources: game.resources[resource] = 1000
	game._place_room("construction_drone_bay",Vector2i(15,15),true)
	var ids := ["reactor","life_support","hydroponics_bay","research_lab","storage_bay","crew_hab","corridor","med_bay"]
	for target in [50,100]:
		for y in range(15,game.GRID_SIZE):
			for x in range(15,game.GRID_SIZE):
				if game.placed_rooms.size()>=target: break
				var cell := Vector2i(x,y)
				if game.occupied.has(cell) or game.wrecks.has(cell): continue
				game._place_room(ids[(x+y*11)%ids.size()],cell,true)
		if game.placed_rooms.size()!=target:
			push_error("Large-station fixture built %d rooms, expected %d" % [game.placed_rooms.size(),target])
			quit(1)
			return
		# Bays only dispatch after their operating cycle has actually been paid.
		game._apply_room_economy()
		if not game.powered_room_cells.has(Vector2i(15,15)):
			push_error("Profile construction bay did not receive paid operating power")
			quit(1);return
		game._refresh_all()
		await frame()
		game._fit_station_view()
		for i in range(6): await frame()
		game._center_grid_on_station_now()
		game.drone_fleet.enqueue("corridor",Vector2i(15,14 if target==50 else 13),0)
		game._set_paused(false,false)
		# Wait for observable flight, not an assumed launch delay.
		for attempt in range(300):
			game._process(1.0/60.0)
			await frame()
			var drone: Dictionary=game.drone_fleet.drones.get(Vector2i(15,15),{})
			if not drone.is_empty() and drone.phase!="docked":break
		if game.drone_fleet.drones.get(Vector2i(15,15),{}).get("phase","docked")=="docked":
			push_error("Profile drone never launched")
			quit(1);return
		await sample("%d-fit" % target)
		# Supply the destination to zoom itself: its deferred center restore otherwise
		# overwrites an immediate scroll correction on the next frame. Use an occupied
		# cell, since the bounds midpoint can fall in a gap in this irregular station.
		var close_room: Dictionary=game.placed_rooms[game.placed_rooms.size()/2]
		game._set_grid_zoom(game.DEFAULT_GRID_ZOOM,true,(Vector2(close_room.pos)+Vector2.ONE*0.5)/float(game.GRID_SIZE))
		await sample("%d-close" % target)
	game._set_paused(true,false)
	game.tick_timer.stop()
	for action in ["construction","menu-open","menu-close","zoom-fit-instant","zoom-close","save","load","zoom-fit-button"]:
		await interaction(action)
	if not records.any(func(record):return record.get("interaction","")=="zoom-fit-button"):
		failures+=1;push_error("Missing animated Fit button result")
	var path := output_dir+"/large-render-profile.json"
	var file := FileAccess.open(path,FileAccess.WRITE)
	file.store_string(JSON.stringify(records,"\t"))
	file.close()
	for suffix in [".cfg",".meta",".meta.bak",".loop",".loop.bak"]:
		if FileAccess.file_exists(prefix+suffix): DirAccess.remove_absolute(prefix+suffix)
	print("LARGE RENDER PROFILE COMPLETE: ",failures," failures")
	quit(failures)
func visible_room_centers() -> int:
	var clip: Rect2=game.grid_scroll.get_global_rect()
	var count:=0
	for room in game.placed_rooms:
		var center: Vector2=game.grid_view.get_global_transform()*((Vector2(room.pos)+Vector2.ONE*0.5)*game.get_cell_size())
		if clip.has_point(center):count+=1
	return count

func sample(label: String) -> void:
	game._set_paused(false,false)
	game.tick_timer.stop()
	for i in range(30):
		game._process(1.0/60.0)
		await frame()
	assert(not game.paused, "Active profile must advance gameplay")
	var visible_start:=visible_room_centers()
	if visible_start<3:
		failures+=1
		push_error("Profile %s sees only %d room centers; camera fixture invalid"%[label,visible_start])
		quit(1)
		return
	var timings: Array = []
	var calls := 0.0
	var simulation_ms := 0.0
	var render_cpu_ms := 0.0
	var render_gpu_ms := 0.0
	var stages := {}
	var moving_drone_frames := 0
	var drone_phases: Dictionary={}
	var start: int = Time.get_ticks_usec()
	var rooms_before: int = game.placed_rooms.size()
	var foot_before: Vector2 = game.bill_npc.foot
	for i in range(90):
		var sim_start := Time.get_ticks_usec()
		game._process(1.0/60.0)
		simulation_ms += (Time.get_ticks_usec()-sim_start)/90000.0
		for drone in game.drone_fleet.drones.values():
			if not drone.bootstrap: drone_phases[drone.phase]=int(drone_phases.get(drone.phase,0))+1
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
	result["drone_phase_samples"]=drone_phases
	if moving_drone_frames==0:
		failures+=1
		push_error("Profile has no active drone frames: "+label)
	result["visible_room_centers_start"]=visible_start
	result["visible_room_centers_end"]=visible_room_centers()
	if result.visible_room_centers_end<3:
		failures+=1
		push_error("Profile lost visible rooms: "+label)
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
	if action=="zoom-fit-button":
		await profile_fit_button()
		return
	var timings: Array = []
	game.grid_view.draw_profile_totals_usec.clear()
	var first_stages: Dictionary = {}
	var started := Time.get_ticks_usec()
	match action:
		"construction": game._place_room("storage_bay",Vector2i(28,20),false,true)
		"menu-open": game._open_menu()
		"menu-close": game._close_menu()
		"zoom-fit-instant": game._fit_station_view()
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

func profile_fit_button() -> void:
	# Exercise the shipped button and normal camera processing. The older instant
	# jump remains a diagnostic, not a proxy for this animated interaction.
	game.paused=true
	game.set_process(true)
	var toolbar=game.find_child("ViewportTools",true,false)
	var button=null
	if toolbar!=null:
		for child in toolbar.get_children():
			if child is Button and child.get_meta("key_hint","")=="RECENTER [{Fit station}]":button=child
	if button==null:
		failures+=1;push_error("Fit toolbar button missing");return
	button.pressed.emit()
	if game.camera_zoom_target<0:
		failures+=1;push_error("Fit button did not request animated zoom");return
	var samples: Array=[]
	var timings: Array=[]
	var started:=Time.get_ticks_usec()
	var previous:=started
	var settled_frames:=0
	var deadline:=Time.get_ticks_msec()+15000
	while Time.get_ticks_msec()<deadline and settled_frames<3:
		await process_frame
		await RenderingServer.frame_post_draw
		var now:=Time.get_ticks_usec()
		var elapsed: float=(now-previous)/1000.0
		previous=now
		timings.append(elapsed)
		var settled: bool=game.camera_zoom_target<0 and not game.grid_view.zoom_preparing and not game.grid_view.zoom_settling
		settled_frames=settled_frames+1 if settled else 0
		samples.append({"frame_ms":elapsed,"zoom":game.grid_zoom,"preparing":game.grid_view.zoom_preparing,"settling":game.grid_view.zoom_settling,"target":game.camera_zoom_target,"visible_rooms":visible_room_centers()})
	game.set_process(false)
	if settled_frames<3:
		failures+=1;push_error("Animated Fit button did not settle")
	var result:=summarize(timings)
	result.merge({"interaction":"zoom-fit-button","first_frame_ms":timings[0],"elapsed_ms":(Time.get_ticks_usec()-started)/1000.0,"settled":settled_frames>=3,"frames":samples,"forced_draw":false})
	records.append(result)
	print("FIT BUTTON: ",samples.size()," frames, settled=",settled_frames>=3," max_ms=",result.max_ms)
	root.get_texture().get_image().save_png(output_dir+"/fit-button-settled.png")

func accumulate_stages(totals: Dictionary, divisor: float) -> void:
	for key in game.grid_view.draw_profile_usec:
		totals[key] = float(totals.get(key,0.0))+float(game.grid_view.draw_profile_usec[key])/(divisor*1000.0)
	for canvas in game.grid_view.content_canvases.values():
		if not canvas.visible: continue
		for part in ["prepare_usec","draw_usec"]:
			var key: String = "content_"+part
			totals[key] = float(totals.get(key,0.0))+float(canvas.get(part))/(divisor*1000.0)
