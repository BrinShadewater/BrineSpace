extends SceneTree
const Expedition = preload("res://scripts/crew_expedition.gd")
const Architects = preload("res://scripts/architects.gd")
const Cycle = preload("res://scripts/airlock_cycle.gd")
const Save = preload("res://scripts/run_save.gd")
const Records = preload("res://scripts/transmission_archive.gd")
const Sound = preload("res://scripts/station_audio.gd")
var failures := 0
var game
var capture_dir := ""
func _init():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="): capture_dir = arg.trim_prefix("--capture-dir=")
	call_deferred("run")
func check(ok: bool,message: String):
	if not ok:
		failures += 1
		push_error(message)
func run():
	game = load("res://scenes/main.tscn").instantiate()
	var prefix := "user://systems_%d" % OS.get_process_id()
	game.meta.save_path = prefix+".meta"
	game.run_save_path = prefix+".loop"
	game.meta.selected_architect = "bill"
	game.meta.recovered_memory_ids.clear()
	root.add_child(game)
	current_scene = game
	game.set_process(false)
	game.tick_timer.stop()
	game.paused = false
	Architects.advance_core(game,10)
	var cell := Vector2i(20,19)
	game.wrecks.erase(cell)
	game.wrecks.erase(Vector2i(20,18))
	game.wrecks.erase(Vector2i(20,17)) # Clear a short route within the new 60-second tank range.
	game.drone_fleet.sites.erase(Vector2i(20,18))
	game._place_room("airlock",cell,true) # Isolated geometry fixture; production costs unchanged.
	game.occupied[cell].rotation = 0
	game.powered_room_cells[cell] = true
	game.resources.oxygen = 12
	game.drone_fleet.sites = {Vector2i(20,16):game.drone_fleet.Sites.make_site("salvage",3)}
	game.drone_fleet.sites[Vector2i(20,16)].discovered = true
	game.drone_fleet.sites_initialized = true
	var actor = game.bill_npc
	check(not Expedition.dispatch(game,"bill",cell),"Dispatch requires a fitted helmet")
	check(preload("res://scripts/airlock_service.gd").request(game,"bill",cell),"Real locker route assigned")
	for i in range(3000):
		game._update_test_walker(0.1)
		if actor.helmet_equipped and not actor.helmet_action_active(): break
	check(actor.helmet_equipped,"Helmet fitting completes before dispatch")
	var before_oxygen: int = game.resources.oxygen
	check(Expedition.dispatch(game,"bill",cell),"Safe exterior expedition dispatches")
	check(game.station_sound.voices.has("crew_dispatch"),"Successful crew dispatch has confirmation audio")
	if actor.expedition.is_empty():
		print("DISPATCH REASON: "+Expedition.reason(game,"bill",cell))
		quit(1)
		return
	check(game.resources.oxygen == before_oxygen-2,"Oxygen paid exactly once")
	check(not Expedition.dispatch(game,"bill",cell),"Double dispatch rejected")
	check(not preload("res://scripts/airlock_service.gd").request(game,"bill",cell),"Locker cannot interrupt a dispatched crew member")
	var target: Vector2i = actor.expedition.target
	var units: int = game.drone_fleet.sites[target].units
	var metal: int = game.resources.metal
	var seen := {}
	var audible_stages := {}
	for i in range(6000):
		if actor.expedition.is_empty(): break
		var phase: String = actor.expedition.phase
		if not seen.has(phase):
			seen[phase] = true
			if not capture_dir.is_empty() and phase in ["pressurize","outbound","salvage","return","exit","unload"] and DisplayServer.get_name() != "headless":
				game.selected_room_cell = cell
				game.selected_card_id = ""
				game._refresh_all()
				game.crew_comms.set_process(false)
				game.crew_comms.panel.hide()
				game._set_grid_zoom(0.7,true,actor.foot/(384.0*40.0))
				for panel in game.find_children("*","VBoxContainer",true,false):
					if panel.get_script() != null and panel.get_script().resource_path == "res://scripts/airlock_panel.gd": panel.refresh()
				for frame in range(3): await process_frame
				await RenderingServer.frame_post_draw
				root.get_texture().get_image().save_png(capture_dir.path_join("expedition-"+phase+".png"))
			check(actor.valid_snapshot(actor.snapshot()),"Checkpoint validates phase "+phase)
			check(Expedition.reserved(game,cell),"Airlock remains reserved")
			if phase=="pickup":
				check(actor.animation_state()=="swim-pickup","Pickup has its own pose")
				check(actor.expedition.cargo.is_empty() and game.drone_fleet.sites[target].units==units,"Pickup has not extracted early")
				var picking:=Save.capture(game)
				check(Save.restore(game,picking),"Pickup checkpoint restores")
				game.tick_timer.stop();actor=game.bill_npc;game.paused=true
				game._process(0.3)
				check(actor.expedition.phase=="pickup" and actor.expedition.elapsed==0.0,"Pause holds pickup")
				game.paused=false
			if phase=="unload":
				check(actor.animation_state()=="unload","Recovered case has an unload pose")
				check(game.resources.metal==metal,"Unloading has not credited cargo early")
				var unloading:=Save.capture(game)
				check(Save.restore(game,unloading),"Unloading checkpoint restores")
				game.tick_timer.stop()
				actor=game.bill_npc
				game.paused=true
				game._process(0.3)
				check(actor.expedition.phase=="unload" and actor.expedition.elapsed==0.0,"Pause holds unloading")
				game.paused=false
			if phase == "pressurize":
				var position: Vector2 = actor.foot
				game.powered_room_cells.erase(cell)
				Cycle.advance(game,2)
				Expedition.advance(game,actor,2)
				check(actor.foot == position,"Power loss holds crew inside chamber")
				game.powered_room_cells[cell] = true
			if phase == "return":
				check(game.resources.metal == metal,"Cargo not credited before safe return")
				var snapshot := Save.capture(game)
				var position: Vector2 = actor.foot
				game.station_sound.prior_airlocks[cell] = "opening_inner"
				check(Save.restore(game,snapshot),"Exterior checkpoint restores")
				game.tick_timer.stop()
				game.paused = false
				game.station_sound._process(0.1)
				check(not game.station_sound.voices.has("airlock_ready") and not game.station_sound.voices.has("airlock_release"),"Restored phase is primed without replaying airlock cues")
				actor = game.bill_npc
				check(actor.foot == position and actor.expedition.phase == "return","Continue preserves exterior position and cargo")
		Cycle.advance(game,0.1)
		game._update_test_walker(0.1)
		game.station_sound._process(0.1)
		for cue in ["airlock_pressure","airlock_release","airlock_ready"]:
			if game.station_sound.voices.has(cue): audible_stages[cue] = true
	check(actor.expedition.is_empty(),"Crew returns through complete chamber cycle")
	check(audible_stages.size() == 3,"Actual airlock cycle triggers pressure, release and ready cues")
	check(seen.size() == Expedition.PHASES.size(),"Every travel and interlock phase exercised")
	check(actor.movement_medium == "dry" and actor.helmet_equipped,"Crew returns dry with reusable helmet")
	check(game.drone_fleet.sites[target].units == units-1,"Exactly one finite salvage load extracted")
	check(game.resources.metal == mini(metal+1,game._get_resource_capacity("metal")),"Cargo credited once at storage capacity")
	check(Records.available(game.meta).has("survey"),"Exterior recorder unlocks after return")
	var recovered := Records.available(game.meta)
	game.meta.load_from_disk()
	check(Records.available(game.meta) == recovered,"Transmission unlock survives disk reload")
	check(not Records.available(game.meta).has("receiver"),"Unrecovered receiver text stays sealed")
	check(preload("res://scripts/airlock_service.gd").request(game,"bill",cell,true),"Request actual locker refill route")
	for i in range(2000):
		game._update_test_walker(0.1)
		if actor.tank_oxygen>=59.9: break
	check(actor.tank_oxygen>=59.9,"Locker restores tank before second dispatch")
	# Recall from exterior water returns without consuming a site's finite stock.
	check(Expedition.dispatch(game,"bill",cell),"A second expedition can dispatch after safe return")
	var recall_units: int = game.drone_fleet.sites[target].units
	for i in range(6000):
		if actor.expedition.is_empty(): break
		if actor.expedition.phase == "outbound" and not actor.expedition.recall:
			check(Expedition.request_recall(game,actor),"Recall is accepted once")
			check(game.station_sound.voices.has("ui_recall"),"Recall confirmation sounds")
			check(not Expedition.request_recall(game,actor),"Repeated recall does not replay feedback")
		Cycle.advance(game,0.1)
		game._update_test_walker(0.1)
	check(actor.expedition.is_empty() and actor.movement_medium == "dry","Recall returns to dry preparation area")
	check(game.drone_fleet.sites[target].units == recall_units,"Recall never creates or spends cargo")
	check(game.station_sound.voices.has("crew_return"),"Safe return without cargo has dedicated feedback")
	game.inspector_label.meta_clicked.emit("resource:power")
	check(game._journal_is_open() and game.journal_tabs.current_tab == 2 and game.inspected_resource == "power","Inspector supply link opens actionable Power details")
	game._toggle_journal()
	game.occupied[cell].suspended = true
	game.inspector_label.meta_clicked.emit("resume:20,19")
	check(not game.occupied[cell].suspended,"Inspector resume link resumes the selected room")
	for q in [1,2,3]:
		var id: String = Architects.IDS[q%3]
		game.meta.unlocked_architect_ids[id] = true
		game.meta.selected_architect = id
		game._start_reboot_cycle()
		game.tick_timer.stop()
		game.paused = false
		Architects.advance_core(game,10)
		var offset: Vector2i = [Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][q]
		var home := Vector2i(20,20)+offset
		var site_cell := Vector2i(20,20)+offset*4
		for step in range(1,5): game.wrecks.erase(Vector2i(20,20)+offset*step)
		game._place_room("airlock",home,true)
		game.occupied[home].rotation = q
		game.powered_room_cells[home] = true
		game.resources.oxygen = 12
		game.drone_fleet.sites = {site_cell:game.drone_fleet.Sites.make_site("salvage",2)}
		game.drone_fleet.sites[site_cell].discovered = true
		game.drone_fleet.sites_initialized = true
		actor = Architects.actor_for(game,id)
		check(preload("res://scripts/airlock_service.gd").request(game,id,home),"Rotated locker route accepted: "+id)
		for i in range(3000):
			game._update_test_walker(0.1)
			if actor.helmet_equipped and not actor.helmet_action_active(): break
		check(Expedition.dispatch(game,id,home),"Rotated expedition dispatch: "+id)
		for i in range(6000):
			if actor.expedition.is_empty(): break
			Cycle.advance(game,0.1)
			game._update_test_walker(0.1)
		check(actor.expedition.is_empty() and actor.movement_medium == "dry","Rotated expedition returns: "+id)
		check(game.drone_fleet.sites[site_cell].units == 1,"Rotated salvage remains finite")
	var archive = preload("res://scripts/title_archive.gd").new()
	archive.meta_state = game.meta
	archive.mode = "codex"
	archive.codex_tab = 2
	root.add_child(archive)
	check(archive.grid.columns == 1 and archive.codex_count.text.contains("2 RECORDINGS"),"Codex exposes only recovered replay recordings")
	if not capture_dir.is_empty() and DisplayServer.get_name() != "headless":
		for frame in range(15): await process_frame
		await RenderingServer.frame_post_draw
		root.get_texture().get_image().save_png(capture_dir.path_join("transmission-archive.png"))
	var replay_button: Button = archive.grid.get_child(2)
	replay_button.pressed.emit()
	var playback = root.get_child(root.get_child_count()-1)
	check(playback.get_script().resource_path == "res://scripts/loading_transition.gd" and playback.replay_mode,"Archive starts the scrolling recording without changing scenes")
	var skip := InputEventKey.new()
	skip.keycode = KEY_ENTER
	skip.pressed = true
	playback._input(skip)
	await process_frame
	check(not is_instance_valid(playback) and current_scene == game,"Skipping replay returns to the same station")
	archive.queue_free()
	var invalid: Dictionary = actor.snapshot()
	invalid.expedition = {"phase":"return"}
	check(not actor.valid_snapshot(invalid),"Malformed expedition checkpoint rejected")
	var sound := Sound.new()
	sound.game = game
	check(sound.targets().machinery > -80,"Powered machinery is audible")
	game.powered_room_cells.clear()
	check(sound.targets().machinery == -80,"Power failure silences machinery")
	game.resources.integrity = 40
	check(sound.targets().pressure > -40,"Hull stress rises at low integrity")
	for kind in ["machinery","pressure","receiver"]:
		check(Sound.tone(kind).data.size() == 22050*4*2,"Bounded original audio stream: "+kind)
	sound.free()
	game.process_mode = Node.PROCESS_MODE_DISABLED
	var music := root.get_node_or_null("StationMusic")
	if music != null: music.process_mode = Node.PROCESS_MODE_DISABLED
	preload("res://scripts/audio_shutdown.gd").stop_audio(root)
	await create_timer(0.2,true,false,true).timeout
	game.queue_free()
	if music != null: music.queue_free()
	await process_frame
	print("STATION SYSTEMS PASS" if failures == 0 else "STATION SYSTEMS FAIL")
	quit(failures)

