extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT="res://output/marsh-animation-audit/repair-joins-continue-v1-2026-10-04/"
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
	game._place_room("maintenance_bay", cell, true); game.powered_room_cells[cell] = true
	actor.signature = ""; actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]: peer.active = false


	var contact:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point:Vector2=actor.graph.get_point_position(id)
		var local:Vector2=point-(Vector2(cell)+Vector2.ONE*.5)*384
		if actor.can_stand(point) and actor.equipment_facing(cell,local)=="south" and actor.RoomActivity.at(actor.geometry[cell],local).is_empty():contact=point;break
	check(contact.is_finite(),"actual South maintenance contact")
	if not contact.is_finite():quit(1);return
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera:Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera),"native repair checkpoint camera settled")
	var player=game.grid_view.marsh_player
	for label in ["kneel-south","stand-south"]:
		game.marsh_npc=Normal.new();actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=contact;actor.direction="east";actor.goal="maintenance";actor.goal_cell=cell;actor.state="idle";actor.stage="";actor.timer=0;actor.path=PackedVector2Array()
		actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":80.0}
		actor.arrive();player.current_key="";player.motion={}
		var reached:=false
		for step in range(350):
			game.paused=false
			if step>0:actor.update(game,.02);game.visual_time_seconds+=.02
			game.paused=true
			var submitted:Texture2D=game.grid_view._get_marsh_frame(game)
			var key:String=actor.animation_state()+"-"+actor.direction
			if key==label and player.frames[key].find(submitted)==1:reached=true;break
		check(reached,"production controller reaches transition middle slot "+label)
		if not reached:quit(1);return
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		var disk:String="user://marsh-repair-"+label+".loop"
		check(Save.write(game,disk)==OK,"full checkpoint write "+label+": "+Save.last_error)
		var data:Dictionary=Save.read(disk)
		check(not data.is_empty() and data.crew.marsh==actor.snapshot(),"full checkpoint validates whole actor "+label)
		await capture("before/"+label,1)
		checkpoints.append({"label":label,"disk":disk,"actor":actor.snapshot(),"player":player.snapshot(),"pixels":texture.get_image().get_data(),"position":game.get_marsh_position()})
	current_scene=null;game.queue_free();await process_frame
	var cases:Array=[]
	for item in checkpoints:
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=item.disk;title._continue_loop()
		deadline=Time.get_ticks_msec()+120000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		game=current_scene
		check(game!=title and game.get("startup_complete")==true,"fresh actual Title Continue startup "+item.label)
		if game==title or not game.get("startup_complete"):quit(1);return
		game.run_save_path="user://marsh-repair-continued-scratch.loop";quiet()
		check(await clear_loading(),"actual visible Continue overlay dismissed "+item.label);quiet()
		actor=game.marsh_npc;player=game.grid_view.marsh_player
		check(actor.get_script()==Normal and game.running and game.paused,"normal paused actor factory restored")
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		check(actor.snapshot()==item.actor,"whole actor first draw parity "+item.label)
		check(player.snapshot()==item.player,"whole player first draw parity "+item.label)
		check(texture.get_image().get_data()==item.pixels,"normal exact first restored source "+item.label)
		check(game.get_marsh_position().is_equal_approx(item.position),"first restored root/draw position")
		check(actor.animation_state()+"-"+actor.direction==item.label,"restored transition animation key parity")
		actor.update(game,.5);check(actor.snapshot()==item.actor and game.grid_view._get_marsh_frame(game)==texture,"pause holds restored whole repair actor")
		game.hand_panel.hide();check(await settle_camera(camera),"restored camera/layers settled")
		await capture("continued/"+item.label,1)
		var completed:=false;var visited:Dictionary={}
		for step in range(400):
			game.paused=false;actor.update(game,.02);game.visual_time_seconds+=.02;game.paused=true
			game.grid_view._get_marsh_frame(game)
			visited[actor.stage]=true
			if actor.stage.is_empty():completed=true;break
		check(completed,"continued production repair sequence completes "+item.label)
		if item.label=="kneel-south":check(visited.has("repair") and visited.has("stand"),"continued kneel traverses actual repair and stand")
		check(Normal.valid_marsh_snapshot(actor.snapshot()),"continued repair completion snapshot validates")
		await capture("completed/"+item.label,-1)
		cases.append({"label":item.label,"slot":1,"fullSave":true,"freshVisibleTitleContinue":true,"sequenceCompleted":completed,"visitedStages":visited.keys()})
		current_scene=null;game.queue_free();await process_frame
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"scope":"Two full normal repair transition middle-slot checkpoints and two fresh actual visible TitleContinues, produced through real arrive/update from a prescribed valid service contact. Whole actor/player/source/root/pause parity and actual repair completion. No injected art or work states. Not every save phase, autonomous route selection, continuous cadence, wet salvage or full-set artwork acceptance."},"\t"));file.close()
	print("MARSH REPAIR CONTINUE: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
