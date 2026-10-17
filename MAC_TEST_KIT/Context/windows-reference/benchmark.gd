extends Node
var root: Window:
	get: return get_tree().root
func quit(code := 0): get_tree().quit(code)
## Reproducible native workload. Run through run_release_benchmark.py for isolation.
const Prefetch = preload("res://scripts/image_prefetch.gd")
const Companions = preload("res://scripts/companions.gd")
const Scrap = preload("res://scripts/room_scrap.gd")
const ROOMS = ["reactor", "storage_bay", "crew_hab", "life_support", "hydroponics_bay", "galley", "mining_drone_bay", "salvage_workshop", "research_lab", "solar_array"]
var options := {}
var game
var output := {}
var rows := []
var samples := []
var action_cell := Vector2i(-1, -1)
var tick_elapsed := 0.0
var trace_pre_usec := 0
var trace_post_usec := 0
var trace_frames := []
class FrameDriver extends Node:
	var action: Callable
	var advance: Callable
	var started := 0
	var after_action := 0
	var after_step := 0
	var process_frame_index := -1
	var steps := 0
	func _process(_delta: float) -> void:
		if not advance.is_valid(): return
		var work := advance
		advance = Callable()
		started = Time.get_ticks_usec()
		process_frame_index = Engine.get_process_frames()
		if action.is_valid(): action.call()
		after_action = Time.get_ticks_usec()
		work.call()
		after_step = Time.get_ticks_usec()
		steps += 1
var benchmark_zoom:=0.0
var benchmark_center:=Vector2.ZERO
var frame_driver: FrameDriver
func trace_pre() -> void: trace_pre_usec = Time.get_ticks_usec()
func trace_post() -> void: trace_post_usec = Time.get_ticks_usec()
func _init() -> void:
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--") and "=" in arg: options[arg.get_slice("=", 0).trim_prefix("--")] = arg.substr(arg.find("=") + 1)
	call_deferred("run")
func fail(message: String) -> void:
	push_error(message)
	quit(1)
static func isolate_viewport_input(viewport: Viewport) -> bool:
	# Workload actions call game methods directly. Physical mouse/keyboard events
	# must not change hover, selection or camera state between paired runs.
	viewport.set_disable_input(true)
	return viewport.is_input_disabled()
static func configure_test_window(window: Window) -> Dictionary:
	# Owner preference: native tests stay silent and off the primary display.
	OS.set_environment("BRINE_SILENT", "1")
	AudioServer.set_bus_mute(AudioServer.get_bus_index("Master"), true)
	var primary := DisplayServer.get_primary_screen()
	var selected := -1
	for screen in DisplayServer.get_screen_count():
		var extent := DisplayServer.screen_get_size(screen)
		if screen != primary and extent.x >= 1920 and extent.y >= 1080:
			selected = screen
			break
	if selected < 0: return {"muted": true, "secondary_available": false}
	window.current_screen = selected
	window.position = DisplayServer.screen_get_position(selected) + Vector2i(100, 100)
	return {"muted": AudioServer.is_bus_mute(AudioServer.get_bus_index("Master")), "secondary_available": true, "screen": selected, "primary_screen": primary, "position": str(window.position)}
func visible_for_measurement() -> bool:
	if not AudioServer.is_bus_mute(AudioServer.get_bus_index("Master")):
		fail("Benchmark invalid: test audio was unmuted")
		return false
	if output.has("test_window") and output.test_window.get("secondary_available", false) and root.current_screen == DisplayServer.get_primary_screen():
		fail("Benchmark invalid: test window moved to primary display")
		return false
	if not root.is_input_disabled():
		fail("Benchmark invalid: external viewport input was re-enabled")
		return false
	if root.mode == Window.MODE_MINIMIZED:
		fail("Benchmark invalid: test window was minimized")
		return false
	return true
func wait_for_render() -> bool:
	var previous := trace_post_usec
	var deadline := Time.get_ticks_msec() + 5000
	while trace_post_usec <= previous:
		if not visible_for_measurement(): return false
		if Time.get_ticks_msec() >= deadline:
			fail("Benchmark invalid: no rendered frame within five seconds")
			return false
		await get_tree().process_frame
	return true
func run() -> void:
	if OS.is_debug_build(): fail("Actual release runtime required"); return
	var expected: String = options.get("user-dir", "")
	if expected.is_empty() or OS.get_user_data_dir().replace("\\", "/").simplify_path() != expected.replace("\\", "/").simplify_path():
		fail("Benchmark refused: user data isolation mismatch"); return
	if DisplayServer.get_name() == "headless": fail("Native display required"); return
	if not isolate_viewport_input(root): fail("Benchmark input isolation unavailable"); return
	output["benchmark_input_disabled"] = true
	output["input_scope"] = "Physical viewport input disabled; workload actions call game methods. This does not certify actual keyboard, mouse or trackpad interaction."
	var tracing: bool = options.get("trace", "false") == "true"
	RenderingServer.frame_post_draw.connect(trace_post)
	if tracing:
		RenderingServer.frame_pre_draw.connect(trace_pre)
	var size := Vector2i(int(options.get("width", "1920")), int(options.get("height", "1080")))
	root.size = size
	output["test_window"] = configure_test_window(root)
	var load_requested := Time.get_ticks_usec()
	var scene = load("res://scenes/main.tscn")
	output["scene_load_ms"] = (Time.get_ticks_usec() - load_requested) / 1000.0
	var loading = preload("res://scripts/loading_transition.gd").new()
	root.add_child(loading)
	await get_tree().process_frame
	if not await wait_for_render(): return
	Prefetch.begin()
	Prefetch.progress_callback = loading.show_startup_progress
	var started := Time.get_ticks_usec()
	game = scene.instantiate()
	game.set_meta("site_seed", 101)
	game.run_save_path = "user://benchmark.loop"
	game.meta.save_path = "user://benchmark.meta"
	game.Preferences.save_path = "user://benchmark.cfg"
	var scenario: String = options.get("scenario", "reported")
	if scenario != "fresh":
		var checkpoint: Dictionary = game.RunSave.read(options.get("save", ""))
		if checkpoint.is_empty(): fail("Missing frozen benchmark save"); return
		game.RunSave.pending = checkpoint
	root.add_child(game)
	get_tree().current_scene = game
	while not game.startup_complete: await get_tree().process_frame
	game.run_save_path = "user://benchmark.loop"
	output["ready_ms"] = (Time.get_ticks_usec() - started) / 1000.0
	output["scene_request_to_ready_ms"] = (Time.get_ticks_usec() - load_requested) / 1000.0
	output["engine_uptime_at_ready_ms"] = Time.get_ticks_usec() / 1000.0
	output["loaded_room_count"] = game.placed_rooms.size()
	output["loading_scope"] = "Initial save/new game only; synthetic fixture preparation is measured separately"
	Prefetch.end()
	output["image_prefetch"] = Prefetch.stats()
	loading.queue_free()
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.minimize()
	game.crew_comms.set_process(false)
	game.testing_free_build = true
	game.testing_disable_failures = true
	var fixture_started := Time.get_ticks_usec()
	if scenario=="mixed_large" and not qa_prepare_bill_ward():return
	if scenario in ["large","mixed_large"]:
		var added: Array[String] = []
		if scenario=="mixed_large":
			added.assign(["moonbay","tidal_power_plant","hydroponics_farm","storage_depot"])
		for i in range(40 - game.placed_rooms.size() - added.size()):
			added.append(ROOMS[i % ROOMS.size()])
		# Put extractors on the final perimeter rather than burying their exits
		# under later fixture rooms. The normal placement rules still apply.
		added.sort_custom(func(a, b): return int(a == "mining_drone_bay") < int(b == "mining_drone_bay"))
		for id in added:
			var cell := find_space(id)
			if cell.x < 0: fail("Could not build deterministic 40-room fixture"); return
			game._place_room(id, cell, true)
		if game.placed_rooms.size() != 40: fail("Large fixture room count mismatch"); return
		# Dedicated workload reserves keep production and battery charging active.
		# These flags/resources are never applied to an ordinary run or source save.
		for key in game.resources: game.resources[key] = maxi(int(game.resources[key]), 10000)
		var occupied_sites := 0
		for cell in game.drone_fleet.sites:
			var site: Dictionary = game.drone_fleet.sites[cell]
			if game.occupied.has(cell):
				if site.kind == "mining": occupied_sites += 1
				site.units = 0
				site.active = false
			elif site.kind == "mining":
				site.active = true; site.discovered = true; site.units = 1000; site.capacity = 1000
		output["fixture_occupied_sites_not_seeded"] = occupied_sites
		game.running = true
		game.paused = false
		game._on_tick_timer_timeout()
		game.tick_timer.stop()
		if not game.drone_fleet.valid(game.drone_fleet.snapshot(), game.placed_rooms):
			fail("Generated benchmark drone fleet is not save-valid"); return
		output["fixture_seeded_reserves"] = true
	if scenario=="mixed_large":
		if not qa_release_bill():return

	game.grid_view.prewarm_station_views(game)
	# Report the physical room mix explicitly: a 40-room workload can still
	# contain only single-cell rooms and cannot certify larger room rendering.
	var room_counts:Dictionary={}
	var multi_cell_room_count:=0
	for placed in game.placed_rooms:
		var room_id:String=str(placed.id)
		room_counts[room_id]=int(room_counts.get(room_id,0))+1
		var footprint:Vector2i=placed.get("size",Vector2i.ONE)
		if footprint.x>1 or footprint.y>1:multi_cell_room_count+=1
	output["room_composition"]={"by_id":room_counts,"multi_cell_room_count":multi_cell_room_count,"occupied_cells":game.occupied.size()}
	game.bill_npc.rebuild(game)
	game.grid_view.profile_draw = true
	game.running = true
	game.paused = false
	if scenario=="mixed_large" and not dispatch_mixed_mission():return
	game.Preferences.pause_unfocused = false
	root.size = size
	if not await initialize_benchmark_camera(): return
	DisplayServer.window_set_vsync_mode(DisplayServer.VSYNC_DISABLED)
	Engine.max_fps = 0
	# process_frame is followed by a deferred-call flush BEFORE node processing.
	# Stepping there made the grid redraw once before and again after its _process.
	# Drive simulation in the normal node-processing phase, before the grid.
	var signal_driver: bool = options.get("signal-driver", "false") == "true"
	frame_driver = FrameDriver.new()
	frame_driver.process_priority = -1000
	root.add_child(frame_driver)
	output["simulation_driver"] = "process_frame signal (historical diagnostic)" if signal_driver else "node process; deterministic 1/60 step"
	RenderingServer.viewport_set_measure_render_time(root.get_viewport_rid(), true)
	# Require observable camera/layer completion as well as a minimum warm-up.
	var warm_frames := 0
	var settled_frames := 0
	while warm_frames < 180 or settled_frames < 30 or (scenario in ["large","mixed_large"] and not active_drone()):
		if signal_driver: step()
		else: frame_driver.advance = step
		await get_tree().process_frame
		warm_frames += 1
		settled_frames = settled_frames + 1 if not game.camera_zoom_moving and not game.grid_view.settle_backlog and game.grid_view.pending_layers.is_empty() else 0
		if warm_frames > 1800: fail("Benchmark scene did not settle"); return
	output["fixture_preparation_ms"] = (Time.get_ticks_usec() - fixture_started) / 1000.0
	output.merge({"scenario": scenario, "rooms": game.placed_rooms.size(), "viewport": size,
		"adapter": RenderingServer.get_video_adapter_name(), "os": OS.get_name(), "debug": OS.is_debug_build(),
		"fixture_free_build": true, "fixture_failures_disabled": true, "startup_stages": game.startup_stage_ms,
		"texture_sharing": game.grid_view.crew_texture_pool.stats.duplicate(), "memory_start_mb": texture_mb(), "warm_frames": warm_frames})
	var actors := []
	for actor in Companions.all_actors(game):
		if actor.active and not actor.dead: actors.append(actor.identity if "identity" in actor else actor.get_script().resource_path.get_file())
	output["active_actors"] = actors
	# Engine counters report previous-second peaks; retain legacy fields but
	# distinguish their scope from the workload's directly timed frame samples.
	output["engine_process_time_scope"] = "TIME_PROCESS and TIME_PHYSICS_PROCESS are previous reporting-second maxima, not current-frame durations; profile_mean averages sampled maxima."
	output["render_timing_scope"] = "Compatibility CPU/GPU viewport timings are delayed engine query results, not aligned current-frame costs; do not add them to script or frame wall timings."
	if scenario in ["large","mixed_large"] and (actors.is_empty() or game.powered_room_cells.size() < 20):
		fail("Large fixture lacks active crew or production: actors=%s powered=%d cycle=%d drones=%s" % [str(actors),game.powered_room_cells.size(),game.cycle,str(drone_phases())]); return
	if scenario=="mixed_large":
		if multi_cell_room_count<4:fail("Mixed fixture lacks multi-cell rooms");return
		for room in game.placed_rooms:
			if room.has("ocean_side") and not game._ocean_face_problem(room).is_empty():fail("Mixed fixture ocean face obstructed: "+str(room.id));return
		output["mixed_large_intakes_clear"]=true
	output["initial_drone_phases"] = drone_phases()
	output["initial_powered_rooms"] = game.powered_room_cells.size()
	var qa_snapshot_problem:String=game.RunSave.problem(game.RunSave.capture(game))
	if not qa_snapshot_problem.is_empty():
		qa_save_diagnostic(qa_snapshot_problem)
		fail("Corrected mixed fixture checkpoint invalid before timing: "+qa_snapshot_problem);return
	output["qa_fixture_revision"]="Production BillNPC actor paired with production carry player; complete pre-timing checkpoint validates. Original plain-Bill fixture failure retained separately."
	# Drain warm-up drawing, then read on every sample, including fast frames.
	# Otherwise a hitch can inherit accumulated drawing from earlier frames.
	game.grid_view.take_draw_timing()
	var frames := int(options.get("frames", "180"))
	for speed in range(3):
		game._set_time_speed(speed)
		game.tick_timer.stop()
		for action in str(options.get("actions", "idle,pan,zoom,lighting,placement,demolition,interface,save")).split(","):
			if not await reset_benchmark_camera(): return
			var camera_start:=camera_snapshot()
			var minimum_visible_rooms:int=camera_start.intersecting_rooms
			samples = []
			var profile := {}
			var origin: Vector2 = Vector2(game.grid_scroll.scroll_horizontal, game.grid_scroll.scroll_vertical)
			var zoom: float = game.grid_zoom
			for i in range(frames):
				if not visible_for_measurement(): return
				var stamp := Time.get_ticks_usec()
				var action_started := stamp
				var after_action := stamp
				var after_step := stamp
				var sampled_process_frame := Engine.get_process_frames()
				if signal_driver:
					act(action, i, origin, zoom)
					after_action = Time.get_ticks_usec()
					step()
					after_step = Time.get_ticks_usec()
				else:
					frame_driver.action = act.bind(action, i, origin, zoom)
					frame_driver.advance = step
				await get_tree().process_frame
				var frame_end := Time.get_ticks_usec()
				if not visible_for_measurement(): return
				if not signal_driver:
					action_started = frame_driver.started
					after_action = frame_driver.after_action
					after_step = frame_driver.after_step
					sampled_process_frame = frame_driver.process_frame_index
				var ms := (frame_end - stamp) / 1000.0
				samples.append(ms)
				minimum_visible_rooms=mini(minimum_visible_rooms,int(camera_snapshot().intersecting_rooms))
				for key in game.grid_view.draw_profile_usec:
					profile[key] = float(profile.get(key, 0.0)) + float(game.grid_view.draw_profile_usec[key]) / frames
				var content_draw := 0
				var content_prepare := 0
				for canvas in game.grid_view.content_canvases.values():
					content_draw += canvas.draw_usec
					content_prepare += canvas.prepare_usec
				for pair in [["content_draw_usec", content_draw], ["content_prepare_usec", content_prepare], ["engine_process_ms", Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0], ["engine_physics_ms", Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0]]:
					profile[pair[0]] = float(profile.get(pair[0], 0.0)) + float(pair[1]) / frames
				for pair in [["render_cpu_ms", RenderingServer.viewport_get_measured_render_time_cpu(root.get_viewport_rid())], ["render_gpu_ms", RenderingServer.viewport_get_measured_render_time_gpu(root.get_viewport_rid())], ["draw_calls", Performance.get_monitor(Performance.RENDER_TOTAL_DRAW_CALLS_IN_FRAME)], ["station_usec", game.frame_timing_usec.get("station_total", 0)]]:
					profile[pair[0]] = float(profile.get(pair[0], 0.0)) + float(pair[1]) / frames
				var draw_timing:Dictionary=game.grid_view.take_draw_timing()
				if ms > 50.0: rows.append({"action": action, "speed": game.time_speeds[speed], "frame": i, "ms": ms, "action_usec": after_action - action_started, "step_usec": after_step - after_action, "engine_wait_usec": frame_end - after_step, "engine_process_ms": Performance.get_monitor(Performance.TIME_PROCESS)*1000.0, "render_cpu_ms": RenderingServer.viewport_get_measured_render_time_cpu(root.get_viewport_rid()), "render_gpu_ms": RenderingServer.viewport_get_measured_render_time_gpu(root.get_viewport_rid()), "process_frame": Engine.get_process_frames(), "drone_upload": preload("res://scripts/drone_animation.gd").last_texture_upload.duplicate(), "drone_frame_uploads": preload("res://scripts/drone_animation.gd").frame_upload_diagnostics(), "sampled_process_frame":sampled_process_frame, "sampled_drone_uploads":preload("res://scripts/drone_animation.gd").frame_upload_diagnostics(sampled_process_frame), "drone_latest_upload_frame": preload("res://scripts/drone_animation.gd").frame_upload_diagnostics(preload("res://scripts/drone_animation.gd").upload_frame), "draw": draw_timing, "systems": game.frame_timing_usec.duplicate(), "stages": game.grid_view.draw_profile_usec.duplicate()})
				if tracing and trace_frames.size() < 4096:
					trace_frames.append({"action":action,"speed":game.time_speeds[speed],"frame":i,"start_usec":stamp,"end_usec":frame_end,"frame_ms":ms,"action_usec":after_action-action_started,"step_usec":after_step-after_action,"boundaries":preload("res://scripts/performance_monitor.gd").frame_boundaries(after_step,trace_pre_usec,trace_post_usec,frame_end),"collection_usec":Time.get_ticks_usec()-frame_end,"render_cpu_ms":RenderingServer.viewport_get_measured_render_time_cpu(root.get_viewport_rid()),"render_gpu_ms":RenderingServer.viewport_get_measured_render_time_gpu(root.get_viewport_rid()),"drone_upload":preload("res://scripts/drone_animation.gd").last_texture_upload.duplicate(), "drone_frame_uploads": preload("res://scripts/drone_animation.gd").frame_upload_diagnostics(), "sampled_process_frame":sampled_process_frame, "sampled_drone_uploads":preload("res://scripts/drone_animation.gd").frame_upload_diagnostics(sampled_process_frame), "drone_latest_upload_frame": preload("res://scripts/drone_animation.gd").frame_upload_diagnostics(preload("res://scripts/drone_animation.gd").upload_frame),"process_frame":Engine.get_process_frames(),"draw_timing":draw_timing,"systems_snapshot":game.frame_timing_usec.duplicate()})
			var ordered := samples.duplicate(); ordered.sort()
			var sum := 0.0
			for ms in samples: sum += ms
			var phase := {"action": action, "speed": game.time_speeds[speed], "samples_ms": samples,
				"mean_ms": sum / frames, "p95_ms": ordered[ceili(frames * 0.95) - 1], "p99_ms": ordered[ceili(frames * 0.99) - 1], "max_ms": ordered.back(), "texture_mb": texture_mb(), "profile_mean": profile, "zoom": game.grid_zoom, "powered_rooms": game.powered_room_cells.size(), "drone_phases": drone_phases()}
			phase["camera_start"]=camera_start
			phase["camera_end"]=camera_snapshot()
			phase["minimum_intersecting_rooms"]=minimum_visible_rooms
			if minimum_visible_rooms<maxi(1,ceili(game.placed_rooms.size()*.5)):
				fail("Benchmark lost station coverage: %s %dx, %d/%d rooms"%[action,game.time_speeds[speed],minimum_visible_rooms,game.placed_rooms.size()]);return
			if not output.has("phases"): output.phases = []
			output.phases.append(phase)
			print("PHASE ", action, " ", game.time_speeds[speed], "x p95=", phase.p95_ms, " max=", phase.max_ms)
	output["hitches"] = rows
	output["draw_timing_scope"] = "Accumulator read on every measured sample, after draining warm-up; other observers may also drain it. Callback count is not a count of whole-station redraws. Engine wait excludes report collection."
	if tracing:
		output["frame_trace"] = trace_frames
		output["frame_trace_work_scope"] = "Draw timings cover callbacks since the last collector read and may nest; system snapshot values keep their named units, with cycle metrics/timestamps potentially retained from an earlier cycle. These are not additive GPU or total frame costs."
		output["frame_trace_scope"] = "At most 4096 frames; signal boundaries are CPU wall intervals, not GPU timings. Collection is outside samples_ms."
	output["memory_end_mb"] = texture_mb()
	if options.get("texture-inventory", "false") == "true":
		output["texture_inventory"] = {}
		for pair in [["crew", game.grid_view.crew_texture_pool], ["rooms", game.grid_view.room_texture_pool]]:
			if pair[1] != null and pair[1].has_method("inventory_snapshot"):
				output.texture_inventory[pair[0]] = pair[1].inventory_snapshot()
			else:
				output.texture_inventory[pair[0]] = {"enabled": false, "complete": false, "reason": "Pool inventory unavailable in this runtime"}
	output["room_texture_sharing"] = game.grid_view.room_texture_pool.stats.duplicate() if "room_texture_pool" in game.grid_view and game.grid_view.room_texture_pool != null else {}
	output["safe_image_failures"] = preload("res://scripts/safe_image.gd").failures.duplicate()
	var reporter = root.get_node_or_null("BugReport")
	if reporter != null and reporter.performance_monitor != null:
		output["automatic_reports_enabled"] = reporter.performance_monitor.auto_capture
		output["automatic_reports_saved"] = reporter.performance_monitor.auto_reports
	var file := FileAccess.open(options["out"], FileAccess.WRITE)
	file.store_string(JSON.stringify(output)); file.close()
	if not await wait_for_render(): return
	root.get_texture().get_image().save_png(str(options["out"]).trim_suffix(".json") + ".png")
	print("RELEASE BENCHMARK COMPLETE ", scenario)
	quit()
func texture_mb() -> float:
	return Performance.get_monitor(Performance.RENDER_TEXTURE_MEM_USED) / 1048576.0
func drone_phases() -> Dictionary:
	var result := {}
	for drone in game.drone_fleet.drones.values(): result[drone.phase] = int(result.get(drone.phase, 0)) + 1
	return result
func active_drone() -> bool:
	for drone in game.drone_fleet.drones.values():
		if drone.phase in ["launching", "outbound", "working", "returning", "docking"]: return true
	return false
func dispatch_mixed_mission()->bool:
	var Mission=preload("res://scripts/moonbay_missions.gd")
	var Architects=preload("res://scripts/architects.gd")
	var issues:Array=[]
	for room in game.placed_rooms:
		if room.id!="moonbay":continue
		for crew_id in Architects.IDS:
			var crew_issue:String=Mission.crew_problem(game,room,crew_id)
			if not crew_issue.is_empty():issues.append({"crew":crew_id,"problem":crew_issue});continue
			for target in game.drone_fleet.sites:
				var site:Dictionary=game.drone_fleet.sites[target]
				if not site.get("active",false) or not site.get("discovered",false) or int(site.get("units",0))<=0:continue
				var problem:String=Mission.dispatch(game,room,crew_id,target,"recover")
				if not problem.is_empty():issues.append({"crew":crew_id,"problem":problem});continue
				output["mixed_large_mission"]={"crew":crew_id,"room":room.pos,"target":target,"phase":Mission.mission_state(room).phase}
				return true
	print("MIXED_MISSION_DIAGNOSTIC ",JSON.stringify(issues))
	fail("Mixed fixture cannot dispatch an available crew member through a safe Moonbay route")
	return false
func step() -> void:
	game.paused = false
	game._process(1.0 / 60.0)
	tick_elapsed += 1.0 / 60.0
	if tick_elapsed >= game._cycle_wait_seconds():
		tick_elapsed -= game._cycle_wait_seconds()
		game._on_tick_timer_timeout()
		game.tick_timer.stop()
func find_space(id: String, visible_only:=false) -> Vector2i:
	for radius in range(1, 19):
		for y in range(20 - radius, 21 + radius):
			for x in range(20 - radius, 21 + radius):
				var cell := Vector2i(x, y)
				if visible_only:
					var footprint:Vector2i=game.RoomDatabaseScript.get_room(id).get("size",Vector2i.ONE)
					var hull:=Rect2(Vector2(cell)*game.get_cell_size(),Vector2(footprint)*game.get_cell_size())
					var view:=Rect2(Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical),game.grid_scroll.size)
					if not view.encloses(hull):continue
				if game.get_footprint_placement_problem(id, cell, 0).is_empty(): return cell
	return Vector2i(-1, -1)
func act(action: String, i: int, origin: Vector2, zoom: float) -> void:
	if action == "pan":
		game.grid_scroll.scroll_horizontal = int(origin.x + sin(i * 0.03) * 250)
		game.grid_scroll.scroll_vertical = int(origin.y + cos(i * 0.03) * 150)
	elif action == "zoom" and i % 30 == 0: game._request_grid_zoom(zoom * (0.85 if i % 60 == 0 else 1.1))
	elif action == "lighting" and i % 60 == 0:
		preload("res://scripts/station_hardware.gd").set_control(game, "interior", not game.hardware.interior)
	elif action == "placement" and i == 30:
		action_cell = find_space("solar_array",true)
		if action_cell.x >= 0: game._place_room("solar_array", action_cell, true)
		else: fail("No visible valid placement site for benchmark")
	elif action == "demolition" and i == 30 and action_cell.x >= 0:
		var reason: String = Scrap.blocker(game, action_cell)
		if reason.is_empty(): Scrap.scrap(game, action_cell); game._refresh_all()
		else: rows.append({"action": "demolition_blocked", "reason": reason})
	elif action == "interface" and i % 60 == 0: game._refresh_all()
	elif action == "save" and i == 30:
		# Dedicated fixture flags prevent ordinary checkpoint writes. Suspend only
		# for this synchronous isolated write; no simulation or building runs here.
		var free_build:bool=game.testing_free_build
		var disabled_failures:bool=game.testing_disable_failures
		game.testing_free_build=false;game.testing_disable_failures=false
		var saved:bool=game._save_active_loop()
		game.testing_free_build=free_build;game.testing_disable_failures=disabled_failures
		if not saved:fail("Benchmark save failed: "+game.RunSave.last_error);return
		var checkpoint:Dictionary=game.RunSave.read(game.run_save_path)
		if checkpoint.is_empty():fail("Benchmark save readback failed: "+game.RunSave.last_error);return
		output["verified_save_path"]=ProjectSettings.globalize_path(game.run_save_path)
		output["verified_save_actions"]=int(output.get("verified_save_actions",0))+1

# Independent action origins avoid accumulating the pan's final offset across speeds.
# Geometry coverage describes hull rectangles, not visibility through HUD/toast overlays.
func benchmark_station_bounds()->Rect2:
	var bounds:=Rect2(Vector2(game.placed_rooms[0].pos),Vector2(game.placed_rooms[0].get("size",Vector2i.ONE)))
	for room in game.placed_rooms:
		bounds=bounds.merge(Rect2(Vector2(room.pos),Vector2(room.get("size",Vector2i.ONE))))
	return bounds
func initialize_benchmark_camera()->bool:
	var previous:=Vector2.INF
	var stable:=0
	for i in range(120):
		await get_tree().process_frame
		var current:Vector2=game.grid_scroll.size
		stable=stable+1 if current==previous and current.x>0 and current.y>0 else 0
		previous=current
		if stable>=3:break
	if stable<3:fail("Benchmark viewport layout did not settle");return false
	var bounds:=benchmark_station_bounds()
	var usable:Vector2=game.grid_scroll.size-Vector2(120,110)
	benchmark_zoom=minf(minf(usable.x/((bounds.size.x+.6)*game.CELL_SIZE),usable.y/((bounds.size.y+.6)*game.CELL_SIZE)),game.DEFAULT_GRID_ZOOM*.60)
	benchmark_center=bounds.get_center()/float(game.GRID_SIZE)
	output["benchmark_camera_scope"]="Fitted full room footprints; camera restored before each independent action. Hull geometry coverage does not account for HUD occlusion."
	return await reset_benchmark_camera()
func reset_benchmark_camera()->bool:
	var bounds:=benchmark_station_bounds()
	var usable:Vector2=game.grid_scroll.size-Vector2(120,110)
	benchmark_zoom=minf(minf(usable.x/((bounds.size.x+.6)*game.CELL_SIZE),usable.y/((bounds.size.y+.6)*game.CELL_SIZE)),game.DEFAULT_GRID_ZOOM*.60)
	benchmark_center=bounds.get_center()/float(game.GRID_SIZE)
	game._set_grid_zoom(benchmark_zoom,true,benchmark_center)
	var previous:=Vector2.INF
	var stable:=0
	for i in range(1200):
		await get_tree().process_frame
		var current:=Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical)
		stable=stable+1 if current==previous and game.camera_zoom_target<0.0 and not game.grid_view.settle_backlog and game.grid_view.pending_layers.is_empty() else 0
		previous=current
		if stable>=3:
			var camera:=camera_snapshot()
			if camera.fully_visible_rooms!=game.placed_rooms.size():
				fail("Fitted benchmark does not fully show every room: %d/%d"%[camera.fully_visible_rooms,game.placed_rooms.size()]);return false
			return true
	fail("Benchmark camera/layers did not settle");return false
func camera_snapshot()->Dictionary:
	var region:=Rect2(Vector2(game.grid_scroll.scroll_horizontal,game.grid_scroll.scroll_vertical),game.grid_scroll.size)
	var full:=0
	var partial:=0
	for room in game.placed_rooms:
		var hull:=Rect2(Vector2(room.pos)*game.get_cell_size(),Vector2(room.get("size",Vector2i.ONE))*game.get_cell_size())
		if region.encloses(hull):full+=1
		if region.intersects(hull):partial+=1
	return {"zoom":game.grid_zoom,"scroll":region.position,"viewport_size":region.size,"fully_visible_rooms":full,"intersecting_rooms":partial,"rooms":game.placed_rooms.size()}

var qa_bill_cell:=Vector2i(-1,-1)
func qa_prepare_bill_ward()->bool:
	if game.Architects.present(game,"bill"):return true
	for cell in game.wrecks:
		if game.wrecks[cell].kind=="recovery":game.surveyed_water[cell]=true
	# Use production seeded shuffle consistently across cold/warm scratch meta.
	# This temporary knowledge mask avoids newly-sighted ordering and disk writes.
	var prior_sightings:Dictionary=game.meta.sighted_character_ids.duplicate(true)
	for id in game.Architects.IDS:game.meta.sighted_character_ids[id]=true
	preload("res://scripts/site_discovery.gd").reveal(game)
	game.meta.sighted_character_ids=prior_sightings
	output["qa_discovery_scope"]="Temporary all-identities-sighted mask selects stable production shuffle; prior scratch knowledge restored. Dedicated fixture only."

	for cell in game.wrecks:
		var ward:Dictionary=game.wrecks[cell]
		if ward.kind!="cryo":continue
		for pod in ward.pods:
			if pod.get("architect_id","")!="bill":continue
			if game.occupied.has(cell):fail("Bill recovery fixture origin occupied");return false
			qa_bill_cell=cell
			ward.paid=true;ward.cleared=true;ward.active=false;ward.progress=preload("res://scripts/wreck_field.gd").DURATION
			game._place_room("cryo_chamber",cell,true)
			game.occupied[cell].rotation=ward.rotation
			game.occupied[cell]["recovered_derelict"]=true
			game.occupied[cell].display_name="Recovered Cryo Ward"
			output["qa_recovery_fixture"]={"origin":str(cell),"pod_id":pod.id,"scope":"Synthetic completed seeded ward and normal release/roster schema before timing; not recovery gameplay acceptance."}
			return true
	fail("No real seeded Bill recovery pod");return false
func qa_release_bill()->bool:
	if not game.Architects.present(game,"bill"):
		var ward:Dictionary=game.wrecks[qa_bill_cell]
		var pod:Dictionary=ward.pods[0]
		if not game.Architects.release(game,pod,qa_bill_cell):fail("Production Bill release failed in dedicated recovery fixture");return false
		pod.wake=preload("res://scripts/cryo_recovery.gd").duration(ward);pod.recovered=true
		game.recovered_crew.append({"id":pod.id,"architect_id":pod.architect_id,"name":pod.name,"origin":qa_bill_cell,"alive":true,"thawed_at":game.get_visual_time_seconds(),"thaw_foot":game.bill_npc.foot})
		game.crew_count+=1;game.had_crew=true
	game.bill_npc.rebuild(game)
	# Keep the original workload's dedicated pre-timing core pilot normalization.
	for room in game.placed_rooms:
		if room.id=="brine_core" and not game.bill_npc.room_nodes.get(room.pos,[]).is_empty():
			game.bill_npc.foot=game.bill_npc.graph.get_point_position(game.bill_npc.room_nodes[room.pos][0])
	output["fixture_moonbay_pilot"]="bill"
	return true

func qa_save_diagnostic(original_error:String)->void:
	var data:Dictionary=game.RunSave.capture(game)
	var actor:Dictionary=data.crew.bill
	var player:Dictionary=data.crew.playback.bill.water
	var details:Dictionary={"original_save_error":original_error,"snapshot_problem":game.RunSave.problem(data),"actor_script":game.bill_npc.get_script().resource_path,"actor_keys":actor.keys(),"actor_binding":actor.get("carry_binding",""),"player_binding":player.get("carry_binding",""),"carry_validator":preload("res://scripts/bill_carry_checkpoint.gd").valid(data),"roster":data.recovered_crew,"architects":data.architects,"wards":data.wrecks}
	var diagnostic:=FileAccess.open(str(options["out"])+".save-failure.bin",FileAccess.WRITE)
	if diagnostic!=null:diagnostic.store_buffer(var_to_bytes(data));diagnostic.close()
	var context:=FileAccess.open(str(options["out"])+".save-failure.json",FileAccess.WRITE)
	if context!=null:context.store_string(JSON.stringify(details,"\t"));context.close()
	print("QA_CARRY_FAILURE_DIAGNOSTIC ",JSON.stringify(details))
