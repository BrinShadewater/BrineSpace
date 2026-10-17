extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-animation-audit/south-run-actor-04-v2-2026-10-02/"
const MANIFEST = "res://character/marsh-south-run-material-v1/candidate-04/manifest.json"
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
	game.meta.save_path = "user://run-study.meta"
	game.run_save_path = "user://run-study.loop"
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
	actor.foot = start; actor.direction = "south"; actor.state = "idle"; actor.goal = ""; actor.stage = ""; actor.timer = 10
	actor.path = PackedVector2Array()
	actor.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.selected_room_cell = cell; game.paused = true; game._refresh_all(); game.hand_panel.hide()
	var camera: Vector2 = (Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera), "camera and room layers observably settled")
	var route_start := Vector2.INF
	for dx in [-30.0,0.0,30.0]:
		for dy in [-100.0,-85.0,-70.0]:
			var candidate: Vector2 = desired+Vector2(dx,dy)
			var clear := true
			for travel in range(0,169,4):
				var point := candidate+Vector2(0,travel)
				if not actor.can_stand(point): clear=false
				for side in [-25.0,25.0]:
					if not actor.can_stand(point+Vector2(side,-45)):clear=false
			if clear and actor.segment_clear(candidate,candidate+Vector2(0,168)):route_start=candidate;break
		if route_start.is_finite():break
	check(route_start.is_finite(),"clear168world South segment with whole-body envelope")
	if not route_start.is_finite():quit(1);return
	actor.foot=route_start;actor.state="idle";actor.goal="";actor.path=PackedVector2Array()
	var player=game.grid_view.marsh_player
	var old_stride:float=player.strides["run-south"]
	player.load_manifest(MANIFEST,true)
	check(player.strides["run-south"]==old_stride,"staged override retains selected distance cadence")
	check(is_equal_approx(player.cycle_seconds("run-south"),.6),"six100ms cycle retained")
	game.visual_time_seconds=100.0;player.current_key=""
	await capture("selected idle before run",-1)
	actor.state="walk";actor.goal="curiosity";actor.path=PackedVector2Array([route_start+Vector2(0,168)])
	game.paused=false
	var seen:Dictionary={};var previous_slot:=-1;var wraps:=0;var restores:=0;var left_run:=false
	for step in range(95):
		var before:Vector2=actor.foot
		actor.move(.02)
		game.visual_time_seconds=100.02+step*.02
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		var running:bool=actor.run_motion_active()
		var slot:int=player.frames["run-south"].find(texture) if running else -1
		check(actor.direction=="south" and actor.foot.x==route_start.x,"actual movement keeps South heading/root axis")
		check(actor.foot.y>=before.y and actor.foot.y<=route_start.y+168,"actual controller progresses within route")
		if running:
			check(slot>=0 and slot<6,"normal grid uses staged run source")
			check(absf(actor.foot.distance_to(before)-69.0*.02)<.001,"normal run rate is69world/sec within submillimetre world-coordinate precision")
			if previous_slot==5 and slot==0:wraps+=1
			if slot!=previous_slot and previous_slot>=0:check(slot==(previous_slot+1)%6,"distance gait advances phase order including wrap")
			if not seen.has(slot):
				seen[slot]=true
				await capture("actual South run pose%d"%slot,slot)
				var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
				check(Normal.valid_marsh_snapshot(saved),"moving normal run snapshot validates")
				var restored=Normal.new();game.marsh_npc=restored
				await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true)
				player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"run actor/player restore preserves root and source")
				game.paused=true;restored.update(game,.5)
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"pause freezes moving actor and source")
				game.paused=false;actor=restored;restores+=1
			previous_slot=slot
		else:
			left_run=true
			check(actor.foot.distance_to(route_start+Vector2(0,168))<=Normal.RUN_STOP_DISTANCE+1.4,"run only stops within normal hysteresis range")
			check(texture not in player.frames["run-south"],"normal slowing hands off from run sources")
		if step%1==0:samples.append({"elapsed":(step+1)*.02,"slot":slot,"running":running,"foot":[actor.foot.x,actor.foot.y],"playerPhase":player.phase})
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	check(seen.size()==6 and restores==6 and wraps>=2,"all six phases restored and cycle wraps twice")
	check(left_run,"normal controller slows near destination")
	await capture("normal walk after run",-2)
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"actorRestores":restores,"wraps":wraps,"strideDistanceCells":old_stride,"scope":"Normal Marsh.move/run guards/rate, main/grid/player with explicit staged run manifest on clear168world furnished-room segment; controlled95x20ms simulation/render samples, six actor+player restores/pause holds, near-destination walk. No fullRunSave/TitleContinue or realtime film/contact acceptance."},"\t"));file.close()
	print("MARSH SOUTH RUN ACTOR: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures])
	quit(1 if failures else 0)
