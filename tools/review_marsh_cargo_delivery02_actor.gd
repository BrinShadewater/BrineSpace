extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-animation-audit/cargo-delivery-02-2026-10-02/"
const MANIFEST = "res://character/marsh-carry-turn-material-v1/opposite-01-unselected/family-manifest.json"
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
	actor.foot = start; actor.direction = "east"; actor.state = "idle"; actor.goal = ""; actor.stage = ""; actor.timer = 10
	actor.path = PackedVector2Array()
	actor.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.selected_room_cell = cell; game.paused = true; game._refresh_all(); game.hand_panel.hide()
	var camera: Vector2 = (Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera), "camera and room layers observably settled")
	var player=game.grid_view.marsh_player
	player.load_manifest("res://character/marsh-east-carry-material-v1/candidate-03/manifest.json",true)
	player.load_manifest("res://character/marsh-west-carry-material-v1/candidate-03/manifest.json",true)
	player.load_manifest("res://character/marsh-south-carry-material-v1/candidate-01/manifest.json",true)
	player.load_manifest("res://character/marsh-north-carry-material-v1/candidate-01/manifest.json",true)
	player.load_manifest("res://character/marsh-carry-turn-material-v1/opposite-01-unselected/family-manifest.json",true)
	player.load_manifest("res://character/marsh-cargo-held-material-v1/side02-cross-review/family-manifest.json",true)


	var cases:Array=[]
	for origin in ["east","west","south","north"]:
		actor=Normal.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction=origin;actor.state="idle";actor.goal="curiosity";actor.goal_cell=cell
		actor.path=PackedVector2Array();actor.stage="workshop_work";actor.timer=.02;actor.activity="sorting recovered components"
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		game.paused=false;game.visual_time_seconds=100.0;player.current_key="";player.motion={}
		actor.update(game,.02)
		check(actor.stage=="workshop_pickup" and is_equal_approx(actor.timer,.52),"normal work enters pickup")
		var seen:Dictionary={};var pickup_seen:Dictionary={};var unload_seen:Dictionary={};var arrival_seen:Dictionary={};var stages:Array=[];var joins:Array=[]
		var restores:=0;var first_capture:int=captures.size();var first_sample:int=samples.size();var carried:=false;var unloaded:=false;var completed:=false
		var previous_stage:String=actor.stage;var previous_key:="";var previous_slot:=-1;var previous_texture:Texture2D=null
		for step in range(1600):
			if unloaded and actor.stage!="workshop_unload":completed=true;break
			if stages.is_empty() or stages.back()!=actor.stage:stages.append(actor.stage)
			if actor.stage=="workshop_carry":carried=true
			if actor.stage=="workshop_unload":
				if not unloaded:check(carried and actor.direction=="north" and actor.path.is_empty() and is_equal_approx(actor.timer,2),"automatic carry arrival enters North unload")
				unloaded=true
			var texture:Texture2D=game.grid_view._get_marsh_frame(game)
			var presentation:Dictionary=actor.workshop_arrival_presentation(player)
			var key:String=str(presentation.key) if not presentation.is_empty() else (actor.animation_state()+"-"+actor.direction if actor.action_elapsed()>=0 else str(player.motion.get("clip","")))
			if key.is_empty():key="carry-"+actor.direction
			check(player.frames.has(key),"actual complete-route source key loaded")
			if not player.frames.has(key):break
			var slot:int=player.frames[key].find(texture)
			check(slot>=0,"actual complete-route source is in declared clip")
			if slot<0:break
			if actor.stage=="workshop_pickup":pickup_seen[slot]=true
			if actor.stage=="workshop_unload":
				if key=="carry-turn-west-north":
					arrival_seen[slot]=true
					check(actor.action_elapsed()<.400001,"arrival turn consumes first400ms of unchanged2second timer")
				else:
					check(key=="unload-north" and arrival_seen.size()==5,"all5arrival phases precede lowering")
					if unload_seen.is_empty():check(slot==0,"arrival finishes into exact North unload0")
					unload_seen[slot]=true
					if actor.action_elapsed()>=.92:check(slot==3,"remaining unload timer holds authored finalidle after400+520ms")
			if actor.stage!=previous_stage:
				joins.append({"fromStage":previous_stage,"toStage":actor.stage,"fromKey":previous_key,"fromSlot":previous_slot,"toKey":key,"toSlot":slot,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction})
				if actor.stage=="workshop_carry":check(pickup_seen.size()==4 and not actor.path.is_empty(),"all pickup phases create real automatic carry route")
				if actor.stage=="workshop_unload":check(key=="carry-turn-west-north" and slot==0,"actual arrival begins authored WestNorth turn0")
			var signature:String=key+":"+str(slot)
			if not seen.has(signature):
				seen[signature]=true;await capture(origin+" complete delivery "+signature,slot);captures.back()["expectedKey"]=key;captures.back()["case"]=origin
				var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
				check(Normal.valid_marsh_snapshot(saved),"complete-route actor snapshot valid")
				var restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"complete-route phase root/source restored exactly")
				game.paused=true;restored.update(game,.5)
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"complete-route restored pause holds")
				game.paused=false;actor=restored;restores+=1
			samples.append({"case":origin,"step":step,"stage":actor.stage,"key":key,"slot":slot,"elapsed":actor.action_elapsed(),"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"remainingRoute":actor.path.size()})
			previous_stage=actor.stage;previous_key=key;previous_slot=slot;previous_texture=texture
			actor.update(game,.02);game.visual_time_seconds+=.02
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		check(completed and carried and unloaded and pickup_seen.size()==4 and unload_seen.size()==4 and arrival_seen.size()==5,"complete normal pickup/carry/arrival/unload lifecycle finishes")
		check(stages==["workshop_pickup","workshop_carry","workshop_unload"],"exact normal lifecycle stage order")
		cases.append({"origin":origin,"stages":stages,"pickupSlots":pickup_seen.keys(),"unloadSlots":unload_seen.keys(),"arrivalSlots":arrival_seen.keys(),"completed":completed,"actorRestores":restores,"captureStart":first_capture,"captureCount":captures.size()-first_capture,"sampleStart":first_sample,"samples":samples.size()-first_sample,"joins":joins,"exitStage":actor.stage,"exitPose":actor.animation_state(),"exitElapsed":actor.action_elapsed()})
		print("DELIVERY DONE "+origin+" samples="+str(samples.size()-first_sample)+" views="+str(captures.size()-first_capture))
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"samples":samples,"scope":"Four initial facing normal Marsh.update work->pickup->automatically planned carry route/turns->actual North arrival->unload/hold/exit. Staged cardinal/turn/heldfamily02,normal main/grid/player,actor-player restores/pause. No route/facing override after work begins. Marsh-only persisted arrival presentation turns WestNorth400ms then lowers520ms inside unchanged2second unload timer. Furnished free fixture,normalflagsfalse. NOT expedition/fullRunSave/visibleTitleContinue/continuouscontact/normaladmission/fullsetacceptance."},"\t"));file.close()
	print("MARSH DELIVERY02 ARRIVAL JOIN: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures]);quit(1 if failures else 0)
