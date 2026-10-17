extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-animation-audit/south-work-polish-v2-2026-10-04/"
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
	var starts:Dictionary={}
	var routes:Dictionary={"east":Vector2(96,0),"west":Vector2(-96,0),"north":Vector2(0,-96)}
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
	var start:Vector2=starts.east
	actor.foot = start; actor.direction = "east"; actor.state = "idle"; actor.goal = ""; actor.stage = ""; actor.timer = 10
	actor.path = PackedVector2Array()
	actor.needs = {"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
	game.selected_room_cell = cell; game.paused = true; game._refresh_all(); game.hand_panel.hide()
	var camera: Vector2 = (Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
	check(await settle_camera(camera), "camera and room layers observably settled")
	var player=game.grid_view.marsh_player

	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-south-work-polish-v1/candidate-manifest.json"))
	var original:Dictionary={}
	for entry in manifest.states:
		var key:String=entry.id;original[key]=player.frames[key].duplicate()
		check(player.timing[key].durations==entry.frameDurationsMs and player.timing[key].loop==entry.loop,"original action timing retained "+key)
	for variant in ["selected","candidate"]:
		if variant=="candidate":
			for entry in manifest.states:
				var key:String=entry.id;var textures:Array=[]
				for index in range(entry.frameFiles.size()):
					var image:=Image.new();check(image.load_png_from_buffer(FileAccess.get_file_as_bytes(entry.frameFiles[index]))==OK,"candidate whole-source decoded")
					var texture:=ImageTexture.create_from_image(image)
					for meta in original[key][index].get_meta_list():texture.set_meta(meta,original[key][index].get_meta(meta))
					textures.append(texture)
				player.frames[key]=textures
		for entry in manifest.states:
			var key:String=entry.id;actor.state=key.trim_suffix("-south");actor.direction="south";actor.goal="";actor.stage="";actor.path=PackedVector2Array();actor.foot=start;game.paused=true
			for index in range(entry.frameFiles.size()):
				player.current_key="";player.motion={};game.grid_view._get_marsh_frame(game)
				player.phase=index*.15+.02;player.started=game.visual_time_seconds-player.phase;player.last_time=game.visual_time_seconds
				var texture:Texture2D=game.grid_view._get_marsh_frame(game)
				check(texture==player.frames[key][index],"normal renderer presents exact held working slot")
				check(texture.get_meta("crew_pivot")==Vector2(92,172) and texture.get_meta("crew_standing_height")==148,"original source density/pivot retained")
				var previous:Dictionary=actor.snapshot();actor.update(game,.5);check(actor.snapshot()==previous,"pause holds whole actor")
				await capture(variant+"/"+key,index)
	for key in original:player.frames[key]=original[key]
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"scope":"Staged texture family comparison in actual normal main scene renderer. Two actions/six slots before and after, matching pivot/density/timing, paused actor and whole source parity across render. In-memory textures only; actor states prescribed for held-source capture. Not normal catalogue admission, autonomous repair/inspection dispatch, complete continuous playback or SaveContinue."},"\t"));file.close()
	print("MARSH SOUTH WORK STAGED REVIEW: ",checks," checks, ",failures," failures")
	quit(1 if failures else 0)
