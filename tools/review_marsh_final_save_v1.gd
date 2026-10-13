extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-animation-audit/final-closeout-save-v1-2026-10-03/"
var game
var checks := 0
var failures := 0
var captures: Array = []
var samples: Array = []
var checkpoints:Array=[]
const Save=preload("res://scripts/run_save.gd")

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
	var canvas_position: Vector2 = root.get_final_transform() * game.grid_view.get_global_transform_with_canvas() * (position + Vector2(0, game.get_cell_size() * .038))
	captures.append({"file":native,"sourceFile":source,"label":label,"slot":slot,"visualTime":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"position":[position.x,position.y],"canvasPosition":[canvas_position.x,canvas_position.y],"imageSize":[root.get_texture().get_width(),root.get_texture().get_height()]})


func quiet():
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()

func clear_loading() -> bool:
	var overlay=null
	for child in root.get_children():
		if child.get_script()==Loading:overlay=child;break
	if overlay==null:return false
	var deadline=Time.get_ticks_msec()+20000
	while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
	if overlay.continue_button.disabled:return false
	overlay.continue_button.pressed.emit()
	while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
	return not is_instance_valid(overlay)

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
		if clear and actor.can_stand(point+Vector2(0,96)) and actor.segment_clear(point,point+Vector2(0,96)) and point.distance_squared_to(desired) < best_distance:
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

	var inventory:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-selected-normal-audit-2026-10-03-post-south-walk/inventory.json"))
	var selected_slots:=0
	for key in inventory.states:
		var selected:Dictionary=inventory.states[key]
		check(player.frames.has(key) and player.frames[key].size()==selected.frames.size(),"normal selected family present "+key)
		var elapsed:=0.0
		for index in range(selected.frames.size()):
			var decoded:=Image.new()
			check(decoded.load_png_from_buffer(FileAccess.get_file_as_bytes("res://"+selected.frames[index].path))==OK,"selected source decoded")
			var submitted:Texture2D=player.frame_at_elapsed(key,elapsed+.001)
			check(submitted!=null and submitted.get_image().get_data()==decoded.get_data(),"normal exact source/hold "+key+"/"+str(index))
			elapsed+=float(selected.state.frameDurationsMs[index])/1000.0;selected_slots+=1
	check(selected_slots==1190 and inventory.states.size()==228,"whole selected normal frame/hold coverage")
	check(not actor.needs_air() and not actor.begin_helmet_action(true),"Marsh helmet/air compatibility remains deliberate")
	for label in ["walk-south","stop-south"]:
		game.marsh_npc=Normal.new();actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction="south";actor.state="idle";actor.stage="";actor.goal="";actor.goal_cell=cell;actor.timer=10
		actor.path=PackedVector2Array([start+Vector2(0,96)])
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		actor._arm_selected_route();game.paused=false;player.current_key="";player.motion={}
		var reached:=false
		for step in range(250):
			actor.update(game,.02);game.visual_time_seconds+=.02
			var current_texture:Texture2D=game.grid_view._get_marsh_frame(game)
			var key:String=actor.animation_state()+"-"+actor.direction
			var slot:int=player.frames[key].find(current_texture)
			if (label=="walk-south" and key=="walk-south" and slot==2) or (label=="stop-south" and key.begins_with("walk-stop-phase") and slot==2):reached=true;break
		check(reached,"observable actual normal checkpoint phase "+label)
		if not reached:quit(1);return
		game.paused=true
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		var disk:String="user://marsh-final-"+label+".loop"
		check(Save.write(game,disk)==OK,"full checkpoint write "+label+": "+Save.last_error)
		var data:Dictionary=Save.read(disk)
		check(not data.is_empty() and data.crew.marsh==actor.snapshot(),"full checkpoint read validates whole actor "+label)
		await capture(label,-1)
		checkpoints.append({"label":label,"disk":disk,"actor":actor.snapshot(),"player":player.snapshot(),"pixels":texture.get_image().get_data(),"position":game.get_marsh_position(),"presentation":{"key":actor.animation_state()+"-"+actor.direction}})
	current_scene=null;game.queue_free();await process_frame
	var cases:Array=[]
	for item in checkpoints:
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=item.disk;title._continue_loop()
		deadline=Time.get_ticks_msec()+120000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		game=current_scene
		check(game!=title and game.get("startup_complete")==true,"fresh Title Continue startup "+item.label)
		if game==title or not game.get("startup_complete"):quit(1);return
		game.run_save_path="user://marsh-final-continued-scratch.loop";quiet()
		check(await clear_loading(),"actual visible Continue overlay dismissed "+item.label);quiet()
		actor=game.marsh_npc;player=game.grid_view.marsh_player
		check(actor.get_script()==Normal and game.running and game.paused,"normal paused factory restored")
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		check(actor.snapshot()==item.actor,"whole actor first draw parity "+item.label)
		check(player.snapshot()==item.player,"whole player first draw parity "+item.label)
		check(texture.get_image().get_data()==item.pixels,"normal catalogue exact first restored source "+item.label)
		check(game.get_marsh_position().is_equal_approx(item.position),"first restored root/draw position")
		check(actor.animation_state()+"-"+actor.direction==item.presentation.key,"restored animation key parity")
		actor.update(game,.5);check(actor.snapshot()==item.actor and game.grid_view._get_marsh_frame(game)==texture,"pause holds restored arrival")
		game.hand_panel.hide();check(await settle_camera(camera),"restored camera/layers settled")
		await capture(item.label,-1)
		var timer_before:float=actor.timer;var foot_before:Vector2=actor.foot
		game.paused=false;actor.update(game,.02);game.paused=true
		check(actor.snapshot()!=item.actor,"unpaused restored animation resumes actual controller")
		check(Normal.valid_marsh_snapshot(actor.snapshot()),"continued arrival validates")
		cases.append({"label":item.label,"presentation":item.presentation,"fullSave":true,"freshVisibleTitleContinue":true})
		current_scene=null;game.queue_free();await process_frame
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"scope":"Two full walk/stop checkpoints and two fresh actual visible TitleContinues plus228state/1190normal-source holds, current normal catalogue with no injected art. Actual96unit South route updated to observable walk/stop phases; whole actor/player/source/root/pause/resume parity. Not staged family persistence, complete routes, helmet acceptance or full-set artwork acceptance."},"\t"));file.close()
	print("MARSH FINAL SAVE CHECK: ",checks,"checks,",failures,"failures")
	quit(1 if failures else 0)
