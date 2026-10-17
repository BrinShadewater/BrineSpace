extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-east-run-smooth-2026-10-14/after-native/"
var game
var checks := 0
var failures := 0
var captures: Array = []
var samples: Array = []
var checkpoints:Array=[]
var marker: ColorRect
var marker_layer: CanvasLayer
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
	seed(20261014)
	if not OS.get_environment("APPDATA").contains("marsh-east-run-smooth-2026-10-14"):
		push_error("Explicit isolated APPDATA required");quit(1);return
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
	var starts:Dictionary={}
	var routes:Dictionary={"run-east":Vector2(168,0)}
	var desired:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384.0
	for facing in routes:
		var chosen:=Vector2.INF
		var best:=INF
		for id in actor.room_nodes.get(cell,[]):
			var point:Vector2=actor.graph.get_point_position(id)
			var target:Vector2=point+routes[facing]
			if actor.can_stand(point) and actor.can_stand(target) and actor.segment_clear(point,target) and point.distance_squared_to(desired)<best:
				chosen=point;best=point.distance_squared_to(desired)
		check(chosen.is_finite(),"actual clear furnished-room route "+facing)
		if not chosen.is_finite():quit(1);return
		starts[facing]=chosen
	var start:Vector2=starts["run-east"]
	actor.foot = start; actor.direction = "east"; actor.state = "idle"; actor.goal = ""; actor.stage = ""; actor.timer = 10
	actor.path = PackedVector2Array()
	actor.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.selected_room_cell = cell; game.paused = true; game._refresh_all(); game.hand_panel.hide()
	var camera: Vector2 = (Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera), "camera and room layers observably settled")
	var player=game.grid_view.marsh_player

	marker_layer=CanvasLayer.new();marker_layer.layer=1000;root.add_child(marker_layer)
	marker=ColorRect.new();marker.size=Vector2(8,8);marker_layer.add_child(marker)
	var cases:Array=[]
	for case_label in routes:
		var facing: String=case_label.get_slice("-",1)
		start=starts[case_label]
		game.marsh_npc=Normal.new();actor=game.marsh_npc;actor.rebuild(game);actor.active=true;actor.battery=100
		actor.foot=start;actor.direction=facing;actor.state="idle";actor.stage="";actor.goal="";actor.goal_cell=cell;actor.timer=10
		actor.path=PackedVector2Array();actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
		player.current_key="";player.motion={};game.paused=true
		var target:Vector2=start+routes[case_label]
		check(await settle_camera(camera),"per-route camera settled before fixed movie crop")
		game.grid_view._get_marsh_frame(game);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var center_world:Vector2=game.get_marsh_position()+routes[case_label]/384.0*game.get_cell_size()*.5
		var center:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*center_world
		var region:=Rect2i(Vector2i(center)-Vector2i(200,240),Vector2i(400,400))
		var index:=0
		for hold in range(6):
			await motion_capture(case_label,index,region);index+=1;game.visual_time_seconds+=1.0/60.0
		actor.path=PackedVector2Array([target]);actor._arm_selected_route();game.paused=false
		var arrived:=false
		for step in range(480):
			actor.update(game,1.0/60.0);game.visual_time_seconds+=1.0/60.0
			await motion_capture(case_label,index,region);index+=1
			if actor.path.is_empty() and actor.animation_state()=="idle" and actor.foot.is_equal_approx(target):arrived=true;break
		check(arrived,"normal start/walk/stop reaches idle at actual endpoint "+facing)
		if not arrived:quit(1);return
		game.paused=true
		for hold in range(7):
			game.visual_time_seconds+=.04;await motion_capture(case_label,index,region);index+=1
		var seen_slots:Dictionary={}
		var required_key: String=case_label if not case_label.begins_with("step-") else "walk-"+case_label
		for sample in samples:
			if sample.direction==case_label and sample.key==required_key:seen_slots[sample.slot]=true
		check(seen_slots.size()==player.frames[required_key].size(),"complete intended locomotion cycle "+required_key)
		cases.append({"direction":case_label,"frames":index,"durationMs":index*1000.0/60.0,"start":[start.x,start.y],"target":[target.x,target.y],"arrived":arrived,"region":[region.position.x,region.position.y,400,400]})
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"samples":samples,"scope":"One actual normal168-unit east run with starts, walking slowdown and stop. Normal actor/controller/grid; deterministic60Hz simulation steps. Complete source hashes and rendered marker guard each native crop. Prescribed furnished cold-store routes, not autonomous chooser, real-time pacing or universal planted-foot acceptance."},"\t"));file.close()
	print("MARSH EAST RUN SMOOTH REVIEW: ",checks," checks, ",failures," failures")
	marker_layer.queue_free()
	await process_frame
	quit(1 if failures else 0)

func motion_capture(facing:String,index:int,region:Rect2i):
	var actor=game.marsh_npc
	var texture:Texture2D=game.grid_view._get_marsh_frame(game)
	var key:String=actor.animation_state()+"-"+actor.direction
	var slot:int=game.grid_view.marsh_player.frames[key].find(texture)
	check(slot>=0,"normal selected source slot present")
	var marker_index: int=samples.size()+1
	marker.color=Color8(marker_index%256,(marker_index/256)%256,150)
	game.grid_view.queue_redraw()
	var image:Image
	for attempt in range(20):
		await process_frame;await RenderingServer.frame_post_draw
		image=root.get_texture().get_image()
		if image.get_pixel(2,2).is_equal_approx(marker.color):break
	check(image.get_pixel(2,2).is_equal_approx(marker.color),"current rendered sample marker observed")
	check(game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"actual source frozen during sample render")
	check(Rect2i(Vector2i.ZERO,image.get_size()).encloses(region),"full native motion crop inside actual saved viewport")
	var name:String=facing+"-%03d.png"%index
	check(image.get_region(region).save_png(OUTPUT+name)==OK,"native sample saved")
	check(texture.get_image().save_png(OUTPUT+"source-"+name)==OK,"selected source sample saved")
	var position:Vector2=game.get_marsh_position()
	var canvas:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*(position+Vector2(0,game.get_cell_size()*.038))
	check(region.encloses(Rect2i(Vector2i(canvas)-Vector2i(60,130),Vector2i(120,160))),"whole actor margin inside fixed motion crop")
	samples.append({"direction":facing,"index":index,"file":name,"durationMs":1000.0/60.0,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"canvasPosition":[canvas.x,canvas.y],"region":[region.position.x,region.position.y,400,400],"actualViewportSize":[image.get_width(),image.get_height()],"paused":game.paused,"visualTime":game.visual_time_seconds,"playerPhase":game.grid_view.marsh_player.phase,"runActive":actor.run_motion_active(),"snapshotValid":Normal.valid_marsh_snapshot(actor.snapshot())})
