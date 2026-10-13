extends SceneTree
## Normal running: full saves, actual visible Title Continues, exact source/root/phase joins.
const Marsh=preload("res://scripts/marsh_npc.gd")
const Loading=preload("res://scripts/loading_transition.gd")
const Save=preload("res://scripts/run_save.gd")
const OUTPUT="res://output/marsh-animation-audit/east-run-normal-native-v1-2026-10-02/"
var game
var checks:=0
var failures:=0
var records: Array=[]
var checkpoints: Array=[]
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func quiet():
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
func settle(camera: Vector2) -> bool:
	game._set_grid_zoom(.8,true,camera)
	for unused in range(180):
		await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:return true
	return false
func capture(label: String,moment: String,texture: Texture2D):
	game.paused=true;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
	var native_file: String="native-%03d.png"%records.size();var source_file: String="source-%03d.png"%records.size()
	check(root.get_texture().get_image().save_png(OUTPUT+native_file)==OK and texture.get_image().save_png(OUTPUT+source_file)==OK,"native/source capture "+label+"/"+moment)
	var position: Vector2=game.get_marsh_position()
	var canvas_position: Vector2=game.grid_view.get_global_transform_with_canvas()*(position+Vector2(0,game.get_cell_size()*.038))
	records.append({"case":label,"moment":moment,"file":native_file,"sourceFile":source_file,"foot":[game.marsh_npc.foot.x,game.marsh_npc.foot.y],"key":game.marsh_npc.animation_state()+"-east","canvasPosition":[canvas_position.x,canvas_position.y],"designSize":[root.get_visible_rect().size.x,root.get_visible_rect().size.y],"imageSize":[root.get_texture().get_width(),root.get_texture().get_height()]})
func tick(delta: float,draw:=true):
	game.paused=false;game.visual_time_seconds+=delta;game.marsh_npc.update(game,delta);game.paused=true
	if draw:game.grid_view._get_marsh_frame(game)
func reset_actor(cell: Vector2i,start: Vector2):
	game.marsh_npc=Marsh.new();var actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
	actor.foot=start;actor.direction="east";actor.state="idle";actor.goal="";actor.goal_cell=cell;actor.timer=10
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.powered_room_cells[cell]=true
	var player=game.grid_view.marsh_player;player.current_key="";player.motion={}
	# No test bindings or custom player: normal update/renderer own movement.
	return actor
func save_case(label: String,cell: Vector2i,camera: Vector2):
	game.paused=true
	var disk: String="user://east-run-normal-%s.loop"%label
	check(Save.write(game,disk)==OK,"full normal checkpoint written "+label+": "+Save.last_error)
	var data: Dictionary=Save.read(disk)
	check(not data.is_empty() and Marsh.valid_marsh_snapshot(data.crew.marsh),"full checkpoint validates "+label)
	if data.is_empty():return
	var texture: Texture2D=game.grid_view._get_marsh_frame(game)
	await capture(label,"before",texture)
	checkpoints.append({"case":label,"disk":disk,"camera":camera,"cell":cell,"pixels":texture.get_image().get_data(),"position":game.get_marsh_position(),"data":data,"drawn_actor":game.marsh_npc.snapshot(),"drawn_player":game.grid_view.marsh_player.snapshot()})

func clear_loading(required:=false) -> bool:
	var overlay=null
	for child in root.get_children():
		if child.get_script()==Loading:overlay=child;break
	if overlay==null:return not required
	var deadline:=Time.get_ticks_msec()+20000
	while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
	if overlay.continue_button.disabled:return false
	overlay.continue_button.pressed.emit()
	while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
	return not is_instance_valid(overlay)

func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	preload("res://scripts/title_settings.gd").reduced_motion=true
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://east-run-normal.meta";game.run_save_path="user://east-run-normal-root.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	var deadline:=Time.get_ticks_msec()+120000
	while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
	check(game.startup_complete,"observable normal startup")
	if not game.startup_complete:quit(1);return
	quiet();check(await clear_loading(),"initial loading overlay gone")
	game._confirm_doctrines();quiet();game.paused=false;game.Architects.advance_core(game,10)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures and game.architect_run.core.recovered,"normal economy/failure flags and recovered roster")
	check(game.marsh_npc.get_script()==Marsh,"exact normal Marsh factory")
	var cell:=Vector2i(20,21)
	for y in range(20,28):
		for x in range(20,28):
			var candidate:=Vector2i(x,y)
			if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
		if not game.occupied.has(cell) and not game.wrecks.has(cell):break
	check(not game.occupied.has(cell) and not game.wrecks.has(cell),"unoccupied prescribed room site")
	if game.occupied.has(cell) or game.wrecks.has(cell):quit(1);return
	game._place_room("cold_store",cell,true);game.powered_room_cells[cell]=true
	var actor=game.marsh_npc;actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	var start:=Vector2.INF
	var desired: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384.0+Vector2(0,25)
	var best_distance:=INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		var clear: bool=actor.can_stand(point)
		for x in [-45.0,0.0,45.0]:
			for y in [-75.0,-35.0,5.0]:
				if not actor.can_stand(point+Vector2(x,y)):clear=false
		if clear and point.distance_squared_to(desired)<best_distance:start=point;best_distance=point.distance_squared_to(desired)
	check(start.is_finite(),"actual furnished room clears actor envelope")
	if not start.is_finite():quit(1);return
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle(camera),"original camera/layers settled")
	var player=game.grid_view.marsh_player
	check(player.frames["run-east"].size()==6 and player.timing["run-east"].loop,"normal selected six-frame loop")
	check(is_equal_approx(player.strides["run-east"],.11027027027027027),"normal selected run distance cadence")
	for slot in range(6):
		var expected=Image.load_from_file(["res://character/marsh-east-run-material-v1/candidate-03/000.png","res://character/marsh-east-run-material-v1/candidate-03/001.png","res://character/marsh-east-run-material-v1/candidate-03/002.png","res://character/marsh-east-run-material-v1/candidate-03/003.png","res://character/marsh-east-run-material-v1/candidate-03/004.png","res://character/marsh-east-run-material-v1/candidate-03/005.png"][slot])
		check(player.frames["run-east"][slot].get_image().get_data()==expected.get_data(),"normal factory loaded exact03 source "+str(slot))
	var route_start := Vector2.INF
	var route_probes:Array=[]
	for dx in [-80.0,-60.0,-40.0,-20.0,0.0,20.0,40.0,60.0,80.0,100.0,120.0]:
		for dy in [-130.0,-110.0,-100.0,-90.0,-85.0,-70.0]:
			var candidate: Vector2 = desired+Vector2(dy,dx)
			var clear := true
			var blocked:=0
			for travel in range(0,169,4):
				var point := candidate+Vector2(travel,0)
				if not actor.can_stand(point): clear=false;blocked+=1
				for side in [-25.0,25.0]:
					if not actor.can_stand(point+Vector2(side,-45)):clear=false;blocked+=1
			route_probes.append({"candidate":[candidate.x,candidate.y],"blockedSamples":blocked,"segmentClear":actor.segment_clear(candidate,candidate+Vector2(168,0))})
			if clear and actor.segment_clear(candidate,candidate+Vector2(168,0)):route_start=candidate;break
		if route_start.is_finite():break
	var probe_file=FileAccess.open(OUTPUT+"route-probes.json",FileAccess.WRITE);probe_file.store_string(JSON.stringify(route_probes,"\t"));probe_file.close()
	check(route_start.is_finite(),"clear168world East segment with whole-body envelope")
	if not route_start.is_finite():quit(1);return
	actor=reset_actor(cell,route_start);game.visual_time_seconds=100.0
	game.grid_view._get_marsh_frame(game);await save_case("idle-before",cell,camera)
	actor.state="walk";actor.goal="curiosity";actor.path=PackedVector2Array([route_start+Vector2(168,0)])
	var seen:Dictionary={};var walk_saved:=false
	for step in range(95):
		tick(.02)
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		if actor.run_motion_active():
			var slot:int=player.frames["run-east"].find(texture)
			check(slot>=0 and slot<6,"normal full update drives selected run source")
			if not seen.has(slot):seen[slot]=true;await save_case("run-%d"%slot,cell,camera)
		elif not walk_saved:
			check(seen.size()==6,"six running holds precede normal slowing")
			await save_case("walk-after",cell,camera);walk_saved=true
	check(seen.size()==6 and walk_saved and checkpoints.size()==8,"idle six run phases and slowing walk checkpoints")
	current_scene=null;game.queue_free();await process_frame
	for item in checkpoints:
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=item.disk;title._continue_loop()
		deadline=Time.get_ticks_msec()+120000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		game=current_scene
		check(game!=title and game.get("startup_complete")==true,"fresh Title Continue startup "+item.case)
		if game==title or not game.get("startup_complete"):quit(1);return
		game.run_save_path="user://east-run-normal-continued-scratch.loop";quiet()
		check(await clear_loading(true),"actual visible transmission gone before capture "+item.case)
		quiet();actor=game.marsh_npc;player=game.grid_view.marsh_player
		check(actor.get_script()==Marsh and game.paused and game.running,"exact normal paused actor after visible Continue "+item.case)
		var texture: Texture2D=game.grid_view._get_marsh_frame(game)
		check(actor.snapshot()==item.drawn_actor,"whole actor first-draw parity "+item.case)
		check(player.snapshot()==item.drawn_player,"whole normal player first-draw parity "+item.case)
		check(texture.get_image().get_data()==item.pixels,"first restored RGBA exact "+item.case)
		check(game.get_marsh_position().is_equal_approx(item.position),"first restored root/draw position exact "+item.case)
		var baseline: Dictionary=actor.snapshot();actor.update(game,.5)
		check(actor.snapshot()==baseline and game.grid_view._get_marsh_frame(game)==texture,"restored pause preserves state/source "+item.case)
		game.hand_panel.hide();check(await settle(item.camera),"restored native camera/layers settle "+item.case)
		await capture(item.case,"continued",texture)
		if item.case.begins_with("run-"):
			check(actor.run_motion_active(),"restored ongoing run classification "+item.case)
			var before:Vector2=actor.foot;var phase_before:float=player.phase
			tick(.02)
			check(actor.foot.x>before.x and actor.direction=="east" and actor.run_motion_active(),"continued normal route progresses after unpause "+item.case)
			check(player.current_key=="run-east" and player.phase>phase_before,"continued distance phase advances without idle reset "+item.case)
		else:
			check(not actor.run_motion_active(),"restored nonrun endpoint stays nonrun "+item.case)
		check(Marsh.valid_marsh_snapshot(actor.snapshot()),"completed normal snapshot validates "+item.case)
		current_scene=null;game.queue_free();await process_frame
	var cases:Array=[]
	for item in checkpoints:cases.append({"case":item.case,"disk":item.disk})
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"checkpoints":cases,"captures":records,"scope":"Normal ordered catalog and exact Marsh factory/main/grid/player.8full RunSave checkpoints/8fresh actual visible TitleContinues: selectedidle,six running phases,normal slowing walk. Whole actor/player/source/root parity,pause and ongoing route/distance phase after unpause. Prescribed clear168world furnished site, world/peers paused, normal global cost/failure flags, free authored fixture room. Provisional master/material/contacts; no natural traffic/equipment or continuous film acceptance."},"\t"));file.close()
	print("MARSH EAST RUN NORMAL: %dchecks,%dcheckpoints,%dviews,%dfailures"%[checks,checkpoints.size(),records.size(),failures])
	quit(1 if failures else 0)
