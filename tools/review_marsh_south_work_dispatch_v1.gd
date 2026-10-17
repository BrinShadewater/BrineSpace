extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-animation-audit/south-work-dispatch-v5-2026-10-04/"
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

	var repair_point:=Vector2.INF
	for id in actor.room_nodes.get(cell,[]):
		var point:Vector2=actor.graph.get_point_position(id)
		var local:Vector2=point-(Vector2(cell)+Vector2.ONE*.5)*384
		if actor.can_stand(point) and actor.equipment_facing(cell,local)=="south" and actor.RoomActivity.at(actor.geometry[cell],local).is_empty():repair_point=point;break
	check(repair_point.is_finite(),"actual maintenance bay has clear South equipment contact")
	if not repair_point.is_finite():write_report();quit(1);return
	await journey("repair",cell,repair_point,"maintenance",6.3)
	var workshop_cell:=Vector2i(-1,-1)
	for y in range(20,28):
		for x in range(20,28):
			var candidate:=Vector2i(x,y)
			if not game.occupied.has(candidate) and not game.wrecks.has(candidate):workshop_cell=candidate;break
		if workshop_cell.x>=0:break
	check(not game.occupied.has(workshop_cell) and not game.wrecks.has(workshop_cell),"unoccupied workshop fixture site")
	game.selected_rotation=1
	game._place_room("salvage_workshop",workshop_cell,true);game.occupied[workshop_cell].rotation=1;game.powered_room_cells[workshop_cell]=true
	game.marsh_npc=Normal.new();actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
	var station_list:Array=actor.RoomActivity.stations(actor.geometry[workshop_cell])
	var contact:=Vector2.INF
	for station in station_list:
		if station.facing=="south":contact=(Vector2(workshop_cell)+Vector2.ONE*.5)*384+Vector2(station.point);break
	check(contact.is_finite() and actor.can_stand(contact),"actual rotated workshop has clear South station")
	if contact.is_finite() and actor.can_stand(contact):await journey("workshop",workshop_cell,contact,"curiosity",7.7)
	write_report()
	print("MARSH WORK DISPATCH: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)

func journey(label:String,cell:Vector2i,point:Vector2,need:String,seconds:float):
	var actor=game.marsh_npc
	actor.foot=point;actor.direction="east";actor.goal=need;actor.goal_cell=cell;actor.state="idle";actor.stage="";actor.timer=0;actor.path=PackedVector2Array()
	actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0};actor.needs[need]=80.0
	game.paused=true;game.selected_room_cell=cell;game._refresh_all();game.hand_panel.hide()
	check(await settle_camera((Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)),"native camera settled "+label)
	actor.arrive()
	check(actor.direction=="south","production arrive derives South service facing "+label)
	var previous:=""
	var seen:Dictionary={}
	var selected_manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-v2/supplemental/south-work-polish-v1/manifest.json"))
	var player=game.grid_view.marsh_player
	for step in range(int(seconds/.04)+1):
		game.paused=false
		if step>0:actor.update(game,.04);game.visual_time_seconds+=.04
		game.paused=true
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		var pose:String=actor.animation_state()+"-"+actor.direction
		var identity:String=actor.stage+"/"+pose
		if identity!=previous or step%25==0:
			await capture(label+"/"+identity,step)
			previous=identity
		samples.append({"journey":label,"time":step*.04,"stage":actor.stage,"state":actor.state,"pose":pose,"playerKey":player.current_key,"timer":actor.timer,"goal":actor.goal,"foot":[actor.foot.x,actor.foot.y],"pathCount":actor.path.size()})
		seen[actor.stage]=true
		for entry in selected_manifest.states:
			if entry.id==pose:
				check(player.current_key==pose,"actual controller uses revised normal key "+pose)
				check(texture in player.frames[pose],"actual controller draws revised source "+pose)
		if label=="repair" and actor.stage=="stand":check(actor.direction=="south","repair exits in matching South facing")
		if label=="workshop" and actor.stage=="workshop_carry":break
	if label=="repair":check(seen.has("kneel") and seen.has("repair") and seen.has("stand") and seen.has(""),"production kneel repair stand completion chain")
	else:check(seen.has("workshop_inspect") and seen.has("workshop_work") and seen.has("workshop_pickup") and seen.has("workshop_carry"),"production inspection work pickup carry chain")

func write_report():
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"scope":"Prescribed valid production room contacts and goals, then real arrive/update transitions at 40ms samples, current normal catalogue. No actor work state or stage injection after arrival. Not autonomous goal selection, route entry, wet salvage, continuously watched cadence or new full SaveContinue."},"\t"));file.close()
