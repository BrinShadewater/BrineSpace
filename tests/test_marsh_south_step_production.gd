extends SceneTree
## Actual normal catalog/controller, full checkpoints and fresh Title Continue.
const Marsh=preload("res://scripts/marsh_npc.gd")
const Loading=preload("res://scripts/loading_transition.gd")
const Save=preload("res://scripts/run_save.gd")
const OUTPUT="res://output/marsh-animation-audit/south-step-normal-native-v1-2026-10-02/"
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
	records.append({"case":label,"moment":moment,"file":native_file,"sourceFile":source_file,"foot":[game.marsh_npc.foot.x,game.marsh_npc.foot.y],"key":game.marsh_npc.animation_state()+"-south"})
func tick(delta: float,draw:=true):
	game.paused=false;game.visual_time_seconds+=delta;game.marsh_npc.update(game,delta);game.paused=true
	if draw:game.grid_view._get_marsh_frame(game)
func reset_actor(cell: Vector2i,start: Vector2):
	game.marsh_npc=Marsh.new();var actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
	actor.foot=start;actor.direction="south";actor.state="idle";actor.goal="curiosity";actor.goal_cell=cell;actor.timer=10
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.powered_room_cells[cell]=true
	var player=game.grid_view.marsh_player;player.current_key="";player.motion={}
	# No test binding or South gait hook: normal update/renderer own both.
	return actor
func save_case(label: String,cell: Vector2i,camera: Vector2):
	game.paused=true
	var disk: String="user://south-step-normal-%s.loop"%label
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
	game.meta.save_path="user://south-step-normal.meta";game.run_save_path="user://south-step-normal-root.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	var deadline:=Time.get_ticks_msec()+120000
	while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
	check(game.startup_complete,"observable normal startup")
	if not game.startup_complete:quit(1);return
	quiet();check(await clear_loading(),"initial loading overlay gone")
	game._confirm_doctrines();quiet();game.paused=false;game.Architects.advance_core(game,10)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures and game.architect_run.core.recovered,"normal paid/failure loop and recovered roster")
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
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point) and actor.can_stand(point+Vector2(0,20)) and actor.segment_clear(point,point+Vector2(0,20)):start=point;break
	check(start.is_finite(),"actual furnished room clears South step")
	if not start.is_finite():quit(1);return
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle(camera),"original camera/layers settled")
	var player=game.grid_view.marsh_player
	check(player.frames.has("walk-step-south"),"normal catalog selects South step without test manifest")
	for phase in [.10,.30,.42,.54,.66,.78]:
		actor=reset_actor(cell,start)
		actor.path=PackedVector2Array([start+Vector2(0,actor.SOUTH_STEP_WORLD)]);actor._arm_selected_route()
		check(actor.south_step_active(),"normal route arms finite South step")
		actor.move(phase)
		check(actor.south_step_active() and actor.south_step_slot()==player.frames["walk-step-south"].find(game.grid_view._get_marsh_frame(game)),"normal source/contact slot agree")
		await save_case("phase-%02d"%roundi(phase*100),cell,camera)
	actor=reset_actor(cell,start);actor.path=PackedVector2Array([start+Vector2(0,actor.SOUTH_STEP_WORLD)])
	actor._arm_selected_route();actor.move(.42);game.powered_room_cells.erase(cell)
	tick(.02,false)
	check(actor.south_step_active() and actor.south_step_cancelled and actor.goal.is_empty(),"actual service loss clears work before full save")
	await save_case("cancelled-reach",cell,camera)
	actor=reset_actor(cell,start);actor.path=PackedVector2Array([start+Vector2(0,actor.SOUTH_STEP_WORLD)])
	actor._arm_selected_route();actor.move(.86)
	check(not actor.south_step_active() and actor.south_stop_idle_pending,"finite completion leaves exact idle seed before draw")
	await save_case("idle-handoff",cell,camera)
	current_scene=null;game.queue_free();await process_frame
	for item in checkpoints:
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=item.disk;title._continue_loop()
		deadline=Time.get_ticks_msec()+120000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		game=current_scene
		check(game!=title and game.get("startup_complete")==true,"fresh Title Continue startup "+item.case)
		if game==title or not game.get("startup_complete"):quit(1);return
		game.run_save_path="user://south-step-normal-continued-scratch.loop";quiet()
		check(await clear_loading(true),"actual Continue transmission gone before capture "+item.case)
		quiet();actor=game.marsh_npc;player=game.grid_view.marsh_player
		check(actor.get_script()==Marsh and game.paused and game.running,"exact normal paused actor after visible Continue "+item.case)
		var texture: Texture2D=game.grid_view._get_marsh_frame(game)
		check(actor.snapshot().south_short==item.drawn_actor.south_short and actor.foot==item.data.crew.marsh.foot,"normal first-draw short namespace/root parity "+item.case)
		check(actor.snapshot().south_stop==item.drawn_actor.south_stop,"first-draw idle seed parity "+item.case)
		check(player.snapshot()==item.drawn_player,"normal first-draw player parity "+item.case)
		check(texture.get_image().get_data()==item.pixels,"first restored RGBA exact "+item.case)
		check(game.get_marsh_position().is_equal_approx(item.position),"first restored normal source root exact "+item.case)
		var baseline: Dictionary=actor.snapshot();actor.update(game,.5);actor.move(0)
		check(actor.snapshot()==baseline,"restored pause and zero dt preserve state "+item.case)
		game.hand_panel.hide();check(await settle(item.camera),"fresh native camera settled "+item.case)
		await capture(item.case,"continued",texture)
		if actor.south_step_active():
			var target: Vector2=actor.south_step_target;var cancelled: bool=actor.south_step_cancelled
			tick(.84-actor.south_step_clock)
			check(not actor.south_step_active() and actor.path.is_empty() and actor.foot==target,"continued finite step completes exact target "+item.case)
			if cancelled:check(actor.goal.is_empty() and actor.stage.is_empty(),"cancelled Continue never revives old work")
		check(Marsh.valid_marsh_snapshot(actor.snapshot()),"post Continue normal snapshot valid "+item.case)
		current_scene=null;game.queue_free();await process_frame
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE);var cases: Array=[]
	for item in checkpoints:cases.append({"case":item.case,"disk":item.disk})
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"checkpoints":cases,"captures":records,"scope":"Exact normal Marsh/main/grid/catalog. Eight full RunSave checkpoints and eight fresh Title Continue stations, actual transmission acknowledged before capture. Six short-step phases, service-cancelled reach and pending idle handoff. Prescribed furnished room, peers/world paused, normal costs/failure flags. Not natural traffic or full-family art acceptance."},"\t"));file.close()
	print("MARSH SOUTH STEP NORMAL: %d checks,%d checkpoints,%d captures,%d failures"%[checks,checkpoints.size(),records.size(),failures]);quit(1 if failures else 0)
