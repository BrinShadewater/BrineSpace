extends SceneTree
const North=preload("res://scripts/marsh_npc.gd")
const Save=preload("res://scripts/run_save.gd")
var game
var failures:=0
var checks:=0
var records: Array=[]
var output="res://output/marsh-animation-audit/north-production-native-2026-10-02/"
func _init():call_deferred("run")
func check(ok: bool,message: String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func texture():
	return game.grid_view._get_marsh_frame(game)
func settle_camera(camera: Vector2) -> bool:
	game._set_grid_zoom(.8,true,camera)
	for unused in range(180):
		await process_frame;await RenderingServer.frame_post_draw
		game._restore_grid_view_center(camera)
		if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:return true
	print("CAMERA PROBE center=",game._grid_view_center_ratio()," wanted=",camera," pending=",game.grid_view.pending_layers.size()," settling=",game.grid_view.zoom_settling," preparing=",game.grid_view.zoom_preparing)
	return false
func run():
	if DisplayServer.get_name()=="headless":quit(2);return
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
	DirAccess.make_dir_recursive_absolute(output)
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://north_root.meta";game.run_save_path="user://north_root.loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
	game._confirm_doctrines();game.tick_timer.stop();game.set_process(false)
	check(game.running and not game.testing_free_build and not game.testing_disable_failures,"genuine normal loop save eligibility")
	game.marsh_npc=North.new();var actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
	game.paused=false;game.Architects.advance_core(game,10)
	check(game.architect_run.core.recovered,"real core wake establishes exact save roster")
	var cell:=Vector2i(20,21)
	for y in range(20,28):
		for x in range(20,28):
			var candidate:=Vector2i(x,y)
			if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
		if not game.occupied.has(cell) and not game.wrecks.has(cell):break
	check(not game.occupied.has(cell) and not game.wrecks.has(cell),"clear fixture room preserves original rooms/wards")
	game._place_room("corridor",cell,true);game.powered_room_cells[cell]=true
	actor.signature="";actor.rebuild(game)
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	var center: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	var start:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point: Vector2=actor.graph.get_point_position(id)
		if actor.can_stand(point) and actor.segment_clear(point,point+Vector2(0,-100)) and actor.can_stand(point+Vector2(0,-100)):
			start=point;break
	check(start.is_finite(),"default corridor has clear100-unit North route")
	if not start.is_finite():quit(1);return
	actor.foot=start;actor.direction="north";actor.state="idle";actor.goal="";actor.stage="";actor.timer=10
	actor.path=PackedVector2Array([start+Vector2(0,-100)])
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
	var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera),"native room camera settled")
	game.paused=false
	var last:="";var seen: Dictionary={};var saved_checkpoints:=0;var saw_start:=false;var saw_join:=false
	for step in range(180):
		if step>0:game.visual_time_seconds+=.02;actor.update(game,.02)
		var tex: Texture2D=texture();var key: String=actor.animation_state()+"-"+actor.direction
		var slot: int=game.grid_view.marsh_player.frames[key].find(tex)
		check(slot>=0,"world renderer returns selected pose")
		seen[key+":"+str(slot)]=true
		if step>0 and step<20:check(actor.foot==start,"actual update keeps source support root planted")
		if key=="walk-start-north":saw_start=true;check(actor.foot==start,"every actual start update remains planted")
		if saw_start and not saw_join and key=="walk-north":
			saw_join=true;check(is_equal_approx(game.grid_view.marsh_player.phase,.23),"gait starts after already-shown slot1 hold")
		var selector:=key+":"+str(slot)
		if selector!=last:
			var name: String="world-%03d.png" % records.size()
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			check(root.get_texture().get_image().save_png(output+name)==OK,"native world capture")
			records.append({"file":name,"time":step*.02,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"sourceClock":actor.action_elapsed(),"gaitPhase":game.grid_view.marsh_player.phase})
			last=selector
		if step in [10,22,40]:
			var file: String="user://north-root-%d.loop" % step
			var result=Save.write(game,file)
			check(result==OK,"real scratch checkpoint write: "+Save.last_error)
			if result!=OK:
				print("SAVE PROBE: running=",game.running," free=",game.testing_free_build," failures-disabled=",game.testing_disable_failures," problem=",Save.problem(Save.capture(game)))
				quit(1);return
			var data: Dictionary=Save.read(file)
			check(North.valid_marsh_snapshot(data.crew.marsh),"strict staged North snapshot valid from disk")
			var previous_foot: Vector2=actor.foot;var previous_clock: float=actor.action_elapsed()
			var pixels=tex.get_image().get_data();var previous_phase: float=game.grid_view.marsh_player.phase
			check(await Save.restore_staged(game,data),"actual staged disk restore: "+Save.last_error)
			game.run_save_path="user://north_root.loop";game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false)
			actor=game.marsh_npc
			check(actor is North,"standard restore constructs production controller")
			check(actor.foot.is_equal_approx(previous_foot) and is_equal_approx(actor.action_elapsed(),previous_clock),"disk restore exact root/source clock")
			check(is_equal_approx(game.grid_view.marsh_player.phase,previous_phase) and texture().get_image().get_data()==pixels,"disk restore exact gait phase/pixels")
			game.paused=true;actor.update(game,.5)
			check(actor.foot.is_equal_approx(previous_foot) and is_equal_approx(actor.action_elapsed(),previous_clock),"paused Continue freezes start/root")
			game.paused=false;saved_checkpoints+=1
			game.hand_panel.hide();check(await settle_camera(camera),"restored candidate room camera settled")
	for i in range(5):check(seen.has("walk-start-north:"+str(i)),"all start source slots in world")
	for i in range(6):check(seen.has("walk-north:"+str(i)),"all gait slots in world")
	check(actor.foot.is_equal_approx(start+Vector2(0,-100)) and actor.path.is_empty(),"actual North route finishes exactly")
	check(saved_checkpoints==3,"entry,early gait and later gait disk restore covered")
	check(saw_join,"observable North start to gait handoff")
	var report={"checks":checks,"failures":failures,"captures":records,"checkpoints":saved_checkpoints,"scope":"Production Marsh at prescribed clear100-unit North route, default corridor, actual20ms actor updates;world/peers paused. Normal catalog/grid/controller with three standard scratch disk same-scene restores; no candidate rehydration. Fresh-scene/title Continue and natural chooser remain separate checks."}
	var file=FileAccess.open(output+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify(report,"\t"));file.close()
	print("MARSH PRODUCTION NORTH: %d checks,%d captures,%d disk restores,%d failures" % [checks,records.size(),saved_checkpoints,failures]);quit(1 if failures else 0)
