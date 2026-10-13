extends SceneTree
## Actual normal catalog/controller, full checkpoints and fresh Title Continue.
const Marsh=preload("res://scripts/marsh_npc.gd")
const Save=preload("res://scripts/run_save.gd")
const OUTPUT="res://output/marsh-animation-audit/south-normal-native-v1-2026-10-02/"
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
func stop_actor(cell: Vector2i,start: Vector2,phase: int):
	var actor=reset_actor(cell,start);var player=game.grid_view.marsh_player
	var join:=.68;var wanted:=phase*.15+.075
	var distance: float=actor.SOUTH_ADVANCE+fposmod(wanted-join,.9)/.9*.128*384
	while distance<20:distance+=.128*384
	actor.path=PackedVector2Array([start+Vector2(0,distance)]);actor._arm_selected_route()
	for step in range(160):
		tick(.02)
		if actor.south_stop_active():break
	check(actor.south_stop_active() and actor.south_stop_phase==phase,"normal route chooses outgoing phase%d"%phase)
	return actor
func save_case(label: String,cell: Vector2i,camera: Vector2):
	game.paused=true
	var disk: String="user://south-normal-%s.loop"%label
	check(Save.write(game,disk)==OK,"full normal checkpoint written "+label+": "+Save.last_error)
	var data: Dictionary=Save.read(disk)
	check(not data.is_empty() and Marsh.valid_marsh_snapshot(data.crew.marsh),"full checkpoint validates "+label)
	if data.is_empty():return
	var texture: Texture2D=game.grid_view._get_marsh_frame(game)
	await capture(label,"before",texture)
	checkpoints.append({"case":label,"disk":disk,"camera":camera,"cell":cell,"pixels":texture.get_image().get_data(),"position":game.get_marsh_position(),"data":data,"drawn_actor":game.marsh_npc.snapshot(),"drawn_player":game.grid_view.marsh_player.snapshot()})
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	DirAccess.make_dir_recursive_absolute(OUTPUT)
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://south-normal.meta";game.run_save_path="user://south-normal-root.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	quiet();game._confirm_doctrines();quiet();game.paused=false;game.Architects.advance_core(game,10)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures and game.architect_run.core.recovered,"normal paid/failure loop and exact recovered roster")
	check(game.marsh_npc.get_script()==Marsh,"normal factory exact Marsh identity")
	var witness=FileAccess.open(OUTPUT+"loaded-grid-source.txt",FileAccess.WRITE);witness.store_string(game.grid_view.get_script().source_code);witness.close()
	var cell:=Vector2i(-1,-1)
	for y in range(20,28):
		for x in range(20,28):
			var p:=Vector2i(x,y)
			if not game.occupied.has(p) and not game.wrecks.has(p):cell=p;break
		if cell.x>=0:break
	check(cell.x>=0,"fixture preserves original core/wards")
	if cell.x<0:quit(1);return
	game._place_room("cold_store",cell,true);game.powered_room_cells[cell]=true
	var actor=game.marsh_npc;actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	var start:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point+Vector2(0,100)) and actor.segment_clear(point,point+Vector2(0,100)):start=point;break
	check(start.is_finite(),"actual furnished clear100-unit South route")
	if not start.is_finite():quit(1);return
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle(camera),"original native camera settled")
	var player=game.grid_view.marsh_player
	for phase in range(6):check(player.frames.has("walk-stop-phase%d-south"%phase),"normal selected stop branch%d"%phase)
	for clock in [.18,.4,.7]:
		actor=reset_actor(cell,start);actor.path=PackedVector2Array([start+Vector2(0,100)]);actor._arm_selected_route()
		for step in range(roundi(clock/.02)):tick(.02,step*.02+.02<.4-.000001)
		check(actor.south_pending if clock>=.4 else actor.south_active(),"normal undrawn authored start/gait state")
		await save_case("start-%.2f"%clock,cell,camera)
	for phase in range(6):
		actor=stop_actor(cell,start,phase);tick(.16)
		await save_case("stop-%d"%phase,cell,camera)
	actor=stop_actor(cell,start,4);tick(.16);game.powered_room_cells.erase(cell);tick(.02)
	check(actor.south_stop_cancelled and actor.goal.is_empty(),"actual power-loss checkpoint clears former work")
	await save_case("cancel-4",cell,camera)
	actor=stop_actor(cell,start,4);tick(.7,false)
	check(actor.south_stop_idle_pending and actor.south_stop_idle_elapsed>0,"completion residue remains undrawn at capture")
	await save_case("idle-pending-4",cell,camera)
	tick(.7)
	await save_case("idle-drawn-4",cell,camera)
	current_scene=null;game.queue_free();await process_frame
	for item in checkpoints:
		var title=load("res://scenes/title_screen.tscn").instantiate();root.add_child(title);current_scene=title
		title.run_save_path=item.disk;title._continue_loop()
		var deadline:=Time.get_ticks_msec()+90000
		while (current_scene==title or not is_instance_valid(current_scene) or not current_scene.get("startup_complete")) and Time.get_ticks_msec()<deadline:await process_frame
		game=current_scene
		check(game!=title and game.get("startup_complete")==true,"fresh Title Continue startup "+item.case)
		if game==title or game.get("startup_complete")!=true:quit(1);return
		game.run_save_path="user://south-normal-continued-scratch.loop";quiet()
		actor=game.marsh_npc;player=game.grid_view.marsh_player
		check(actor.get_script()==Marsh and game.paused and game.running,"fresh exact normal paused Marsh "+item.case)
		# Prewarming can draw before startup_complete is observable. Compare the
		# same first submitted state, including one-shot gait/idle seed consumption.
		if item.data.crew.marsh.south_start.pending or item.data.crew.marsh.south_stop.idle_pending:
			print("STARTUP HANDOFF PROBE ",item.case," saved_start=",item.data.crew.marsh.south_start," observed_start=",actor.snapshot().south_start," saved_stop=",item.data.crew.marsh.south_stop," observed_stop=",actor.snapshot().south_stop," saved_player=",item.data.crew.playback.marsh," observed_player=",player.snapshot())
		var texture: Texture2D=game.grid_view._get_marsh_frame(game)
		check(actor.snapshot().south_start==item.drawn_actor.south_start and actor.snapshot().south_stop==item.drawn_actor.south_stop and actor.foot==item.data.crew.marsh.foot,"fresh first-draw namespaces/root "+item.case)
		check(player.snapshot()==item.drawn_player,"fresh first-draw saved player handoff "+item.case)
		var baseline: Dictionary=actor.snapshot();actor.update(game,.5);actor.move(0)
		check(actor.snapshot()==baseline,"fresh paused and zero motion unchanged "+item.case)
		check(texture.get_image().get_data()==item.pixels,"normal first restored RGBA "+item.case)
		check(game.get_marsh_position().is_equal_approx(item.position),"normal first restored draw offset/root "+item.case)
		game.hand_panel.hide();check(await settle(item.camera),"fresh native camera settled "+item.case)
		await capture(item.case,"continued",texture)
		if actor.south_stop_active():
			var anchor: Vector2=actor.foot;var cancelled: bool=actor.south_stop_cancelled
			tick(.4-actor.south_stop_clock)
			check(not actor.south_stop_active() and actor.foot==anchor,"continued finite stop retains anchor "+item.case)
			if cancelled:check(actor.goal.is_empty() and actor.stage.is_empty(),"cancelled Continue never revives former work")
		check(Marsh.valid_marsh_snapshot(actor.snapshot()),"post Continue strict normal snapshot "+item.case)
		current_scene=null;game.queue_free();await process_frame
	var report=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	var cases: Array=[]
	for item in checkpoints:cases.append({"case":item.case,"disk":item.disk})
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"checkpoints":cases,"captures":records,"scope":"Normal Marsh factory/catalog/main/grid, prescribed real South route and six outgoing phases, full RunSave checkpoints and12fresh Title Continue stations. World/peers paused, normal cost/failure flags. First source/contact parity and cancelled work. No natural traffic or full-family visual acceptance."},"\t"));report.close()
	print("MARSH SOUTH NORMAL PRODUCTION: %d checks,%d checkpoints,%d captures,%d failures"%[checks,checkpoints.size(),records.size(),failures]);quit(1 if failures else 0)
