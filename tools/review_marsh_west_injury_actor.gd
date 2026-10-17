extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-animation-audit/west-injury-actor-01-2026-10-02/"
const MANIFEST = "res://character/marsh-west-injury-material-v1/candidate-01/manifest.json"
var game
var checks := 0
var failures := 0
var captures: Array = []
var samples: Array = []

func _init(): call_deferred("run")
func check(ok: bool, message: String):
	checks += 1
	if not ok: failures += 1; push_error(message)

func settle_camera(camera: Vector2) -> bool:
	game._set_grid_zoom(.8, true, camera)
	for unused in range(180):
		await process_frame
		await RenderingServer.frame_post_draw
		game._restore_grid_view_center(camera)
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera) < .002: return true
	return false

func capture(label: String, slot: int):
	var actor = game.marsh_npc
	var texture: Texture2D = game.grid_view._get_marsh_frame(game)
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	check(game.grid_view._get_marsh_frame(game).get_image().get_data() == texture.get_image().get_data(), "submitted source remains frozen during rendering")
	var index := captures.size()
	var native := "world-%03d.png" % index
	var source := "source-%03d.png" % index
	check(root.get_texture().get_image().save_png(OUTPUT + native) == OK and texture.get_image().save_png(OUTPUT + source) == OK, "native actor/source pair saved")
	var position: Vector2 = game.get_marsh_position()
	var canvas_position: Vector2 = game.grid_view.get_global_transform_with_canvas() * (position + Vector2(0, game.get_cell_size() * .038))
	captures.append({"file":native,"sourceFile":source,"label":label,"slot":slot,"visualTime":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"position":[position.x,position.y],"canvasPosition":[canvas_position.x,canvas_position.y],"imageSize":[root.get_texture().get_width(),root.get_texture().get_height()]})

func run():
	if DisplayServer.get_name() == "headless": quit(2); return
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	preload("res://scripts/title_settings.gd").reduced_motion = true
	var store = preload("res://scripts/room_layout_store.gd")
	store.loaded = true; store.data = {}
	game = load("res://scenes/main.tscn").instantiate()
	game.set_meta("authored_site_fixture", true)
	game.meta.save_path = "user://injury-study.meta"
	game.run_save_path = "user://injury-study.loop"
	game.meta.unlocked_architect_ids = {"bill":true,"marsh":true}
	game.meta.selected_architect = "marsh"
	root.add_child(game); current_scene = game
	var deadline := Time.get_ticks_msec() + 120000
	while not game.startup_complete and Time.get_ticks_msec() < deadline: await process_frame
	check(game.startup_complete, "observable normal main startup")
	if not game.startup_complete: quit(1); return
	game.set_process(false); game.tick_timer.stop(); game.crew_comms.set_process(false); game.crew_comms.dismiss()
	var overlay = null
	for child in root.get_children():
		if child.get_script() == Loading: overlay = child; break
	if overlay != null:
		deadline = Time.get_ticks_msec() + 20000
		while overlay.continue_button.disabled and Time.get_ticks_msec() < deadline: await process_frame
		check(not overlay.continue_button.disabled, "actual Continue enabled")
		overlay.continue_button.pressed.emit()
		while is_instance_valid(overlay) and Time.get_ticks_msec() < deadline: await process_frame
		check(not is_instance_valid(overlay), "loading overlay gone before capture")
	game._confirm_doctrines(); game.tick_timer.stop(); game.set_process(false)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures, "normal economy/failure flags unchanged")
	game.marsh_npc = Normal.new()
	var actor = game.marsh_npc
	actor.rebuild(game); actor.active = true; actor.battery = 100
	game.paused = false; game.Architects.advance_core(game, 10)
	var cell := Vector2i(-1,-1)
	for y in range(20,28):
		for x in range(20,28):
			var candidate := Vector2i(x,y)
			if not game.occupied.has(candidate) and not game.wrecks.has(candidate): cell = candidate; break
		if cell.x >= 0: break
	check(cell.x >= 0, "unoccupied furnished room site")
	if cell.x < 0: quit(1); return
	game._place_room("cold_store", cell, true); game.powered_room_cells[cell] = true
	actor.signature = ""; actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]: peer.active = false
	var start := Vector2.INF
	var desired: Vector2 = (Vector2(cell)+Vector2.ONE*.5)*384.0 + Vector2(0,25)
	var best_distance := INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2 = actor.graph.get_point_position(id)
		var clear: bool = actor.can_stand(point)
		for x in [-45.0,0.0,45.0]:
			for y in [-75.0,-35.0,5.0]:
				if not actor.can_stand(point+Vector2(x,y)): clear = false
		if clear and point.distance_squared_to(desired) < best_distance:
			start = point; best_distance = point.distance_squared_to(desired)
	check(start.is_finite(), "actual clear furnished-room actor site")
	if not start.is_finite(): quit(1); return
	actor.foot = start; actor.direction = "west"; actor.state = "idle"; actor.goal = ""; actor.stage = ""; actor.timer = 10
	actor.path = PackedVector2Array()
	actor.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.selected_room_cell = cell; game.paused = true; game._refresh_all(); game.hand_panel.hide()
	var camera: Vector2 = (Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera), "camera and room layers observably settled")
	var player = game.grid_view.marsh_player
	var key := "injury-ground-west"
	var old_pixels: PackedByteArray = player.frames[key][5].get_image().get_data()
	player.load_manifest(MANIFEST, true)
	check(old_pixels != player.frames[key][5].get_image().get_data(), "new injury source loaded explicitly in study only")
	game.visual_time_seconds = 100.0; player.current_key = ""
	check(game.grid_view._get_marsh_frame(game).get_image().get_data() == player.frames["idle-west"][0].get_image().get_data(), "exact selected idle study baseline")
	await capture("selected idle before impact", -1)
	check(actor.receive_physical_damage(game,"staged native material review"), "actual physical impact trigger accepted")
	game.paused = false; actor.update(game,.000001)
	check(actor.injury_phase == "fall" and actor.state == "idle" and actor.path.is_empty() and actor.goal.is_empty() and not actor.dead, "actual nonfatal injury controller clears work")
	var last_tag := ""
	var restores := 0
	var seen: Dictionary = {}
	var first_idle_matches_endpoint := false
	for step in range(110):
		if step > 0:
			game.visual_time_seconds += .02
			actor.update(game,.02)
		var phase: String = actor.injury_phase
		key = actor.animation_state()+"-west"
		var texture: Texture2D = game.grid_view._get_marsh_frame(game)
		var slot: int = player.frames[key].find(texture)
		check(slot >= 0, "actual grid selects injury/recovery/idle source")
		check(actor.foot == start and not actor.dead, "nonfatal response retains root")
		if not phase.is_empty():
			check(texture == player.frame_at_elapsed(key,actor.injury_elapsed), "actual injury elapsed selects complete authored source")
			seen[key+":"+str(slot)] = true
		samples.append({"phase":phase,"key":key,"slot":slot,"elapsed":actor.injury_elapsed,"simulationTime":step*.02+.000001})
		var tag: String = key+":"+str(slot)
		game.grid_view.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
		if tag == last_tag: continue
		await capture("impact/recovery "+tag if not phase.is_empty() else "first normal idle after recovery",slot)
		last_tag = tag
		if phase.is_empty():
			first_idle_matches_endpoint = texture.get_image().get_data() == player.frames["injury-rise-west"][5].get_image().get_data()
			check(actor.state == "idle" and actor.goal.is_empty() and actor.path.is_empty(), "recovery returns to normal idle without stale work")
			break
		var saved: Dictionary = actor.snapshot(); var playback: Dictionary = player.snapshot()
		check(Normal.valid_marsh_snapshot(saved), "active injury snapshot validates")
		var restored = Normal.new(); game.marsh_npc = restored
		await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true)
		player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
		check(restored.snapshot() == saved and game.grid_view._get_marsh_frame(game).get_image().get_data() == texture.get_image().get_data(), "actor/player restore retains exact injury source/root")
		game.paused = true; restored.update(game,.5)
		check(restored.snapshot() == saved and game.grid_view._get_marsh_frame(game).get_image().get_data() == texture.get_image().get_data(), "pause holds exact response phase/source")
		game.paused = false; actor = restored; restores += 1
	check(seen.size() == 12 and restores == 12 and actor.injury_phase.is_empty(), "all twelve authored holds complete through actual controller")
	check(player.frames["injury-ground-west"][5].get_image().get_data() == player.frames["injury-rise-west"][0].get_image().get_data(), "injury floor to recovery first pose is exact")
	check(player.frames["injury-rise-west"][5].get_image().get_data() == player.frames["idle-west"][0].get_image().get_data(), "recovery authored endpoint is selected idle0")
	check(first_idle_matches_endpoint, "first normal idle after recovery joins exact authored idle0 instead of old breathing phase")
	var file = FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"actorRestores":restores,"firstNormalIdleMatchesAuthoredEndpoint":first_idle_matches_endpoint,"scope":"Actual normal physical impact/fall/rise controller and main/grid/player, explicit staged fluid/body manifest.12 actor+player restores, pause, fixed root. Normal catalog unchanged. First normal idle endpoint equality reported as observation, not presumed. No full RunSave/Title Continue."},"\t"));file.close()
	print("MARSH WEST INJURY ACTOR: %d checks,%d captures,%d restores,%d failures,idle join exact=%s" % [checks,captures.size(),restores,failures,str(first_idle_matches_endpoint)])
	quit(1 if failures else 0)
