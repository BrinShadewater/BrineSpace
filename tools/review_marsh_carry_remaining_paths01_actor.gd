extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-animation-audit/carry-remaining-paths-01-2026-10-02/"
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
	player.load_manifest(MANIFEST,true)
	var axes={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}
	var cases:Array=[]
	for pair in [["south","east"],["south","west"],["north","east"],["north","west"],["west","east"],["north","south"],["south","north"]]:
		var origin:String=pair[0];var dest:String=pair[1];var key:String="carry-turn-"+origin+"-"+dest
		var phases:int=player.frames[key].size();check(phases in [5,9],"quarter5 or opposite9 frames loaded")
		var origin_axis:Vector2=axes[origin];var dest_axis:Vector2=axes[dest]
		actor=Normal.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
		var route_start:=Vector2.INF;var route_probes:Array=[]
		for dy in range(-130,131,20):
			for dx in range(-120,121,20):
				var candidate:Vector2=desired+Vector2(dx,dy);var corner:Vector2=candidate+origin_axis*64
				var clear:bool=actor.segment_clear(candidate,corner) and actor.segment_clear(corner,corner+dest_axis*96)
				var blocked:=0
				for leg in range(2):
					for travel in range(0,65 if leg==0 else 97,4):
						var point:Vector2=candidate+origin_axis*travel if leg==0 else corner+dest_axis*travel
						for offset in [Vector2.ZERO,Vector2(-25,-45),Vector2(25,-45)]:
							if not actor.can_stand(point+offset):clear=false;blocked+=1
					route_probes.append({"candidate":[candidate.x,candidate.y],"blockedSamples":blocked,"clear":clear})
				if clear:route_start=candidate;break
			if route_start.is_finite():break
		check(route_start.is_finite(),key+" actual clear route with body envelope")
		if not route_start.is_finite():quit(1);return
		actor.foot=route_start;actor.state="idle";actor.direction=origin;actor.goal="";actor.stage="";actor.path=PackedVector2Array()
		check(is_equal_approx(player.cycle_seconds(key),.4 if phases==5 else .8),"exact quarter/opposite timing")
		check(player.frames[key][0].get_image().get_data()==player.frames["carry-"+origin][0].get_image().get_data(),"exact loaded origin endpoint")
		check(player.frames[key][phases-1].get_image().get_data()==player.frames["carry-"+dest][0].get_image().get_data(),"exact loaded destination endpoint")
		for slot in range(phases):check(player.frames[key][slot].get_image().get_data()==player.frames["carry-turn-"+dest+"-"+origin][phases-1-slot].get_image().get_data(),"reverse whole frame sequence exact")
		game.visual_time_seconds=100.0;player.current_key="";player.motion={};game.paused=true
		var first_capture:int=captures.size();var first_sample:int=samples.size()
		await capture(key+" selected origin idle",-1);captures.back()["expectedKey"]="idle-"+origin
		actor.state="walk";actor.goal="curiosity";actor.stage="workshop_carry";actor.activity="carrying recovered parts"
		actor.path=PackedVector2Array([route_start+origin_axis*64,route_start+origin_axis*64+dest_axis*96]);game.paused=false
		var turn_seen:Dictionary={};var dest_seen:Dictionary={};var origin_seen:=false;var returned:=false;var restores:=0;var last_key:="";var last_slot:=-1
		var steps:int=140 if phases==5 else 160
		for step in range(steps):
			var before:Vector2=actor.foot;actor.move(.02);game.visual_time_seconds=100.02+step*.02
			var texture:Texture2D=game.grid_view._get_marsh_frame(game);var actual_key:String=player.motion.get("clip","")
			if actual_key.is_empty():actual_key="carry-"+actor.direction
			var slot:int=player.frames[actual_key].find(texture)
			check(actor.animation_state()=="carry" and not actor.run_motion_active(),"actual cargo excludes running")
			check(actor.direction in [origin,dest] and actor.foot.distance_to(before)>0 and actor.foot.distance_to(before)<=46.0*.02+.001,"actual route advances within normal46rate")
			check(slot>=0,"normal renderer selects exact staged source")
			if actor.direction==origin and not origin_seen:
				origin_seen=true;check(actual_key=="carry-"+origin and slot==0,"origin cargo begins at0")
				await capture(key+" origin cargo",slot);captures.back()["expectedKey"]=actual_key
			if actual_key==key and not turn_seen.has(slot):
				check(slot==turn_seen.size(),"all turn phases advance in order")
				turn_seen[slot]=true;await capture(key+" turn%d"%slot,slot);captures.back()["expectedKey"]=actual_key
				var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
				check(Normal.valid_marsh_snapshot(saved),"movingturn actor snapshot valid")
				var restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"restore exact root/source")
				game.paused=true;restored.update(game,.5)
				check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"pause restored root/source")
				game.paused=false;actor=restored;restores+=1
			if actual_key=="carry-"+dest and not dest_seen.has(slot):
				if not returned:returned=true;check(turn_seen.size()==phases and slot==0,"exact destination0return after all turn phases")
				dest_seen[slot]=true;await capture(key+" destination%d"%slot,slot);captures.back()["expectedKey"]=actual_key
			last_key=actual_key;last_slot=slot;samples.append({"case":key,"elapsed":(step+1)*.02,"key":actual_key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"playerPhase":player.phase,"animationState":actor.animation_state(),"running":actor.run_motion_active()})
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		check(origin_seen and returned and turn_seen.size()==phases and dest_seen.size()==4 and restores==phases,"all real turn/destination phases and restores covered")
		game.paused=true;var held:Dictionary=actor.snapshot();var held_texture:Texture2D=game.grid_view._get_marsh_frame(game);actor.update(game,.5)
		check(actor.snapshot()==held and game.grid_view._get_marsh_frame(game).get_image().get_data()==held_texture.get_image().get_data(),"final pause root/source")
		await capture(key+" finalpaused destination",last_slot);captures.back()["expectedKey"]=last_key
		cases.append({"key":key,"origin":origin,"destination":dest,"phaseCount":phases,"samples":steps,"actorRestores":restores,"turnSlots":turn_seen.keys(),"destinationSlots":dest_seen.keys(),"captureStart":first_capture,"captureCount":captures.size()-first_capture,"sampleStart":first_sample,"routeProbes":route_probes})
		print("CASE DONE "+key+" phases="+str(phases)+" captures="+str(captures.size()-first_capture))
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures,"samples":samples,"scope":"Seven actual normal Marsh.move workshop_carry paths:four reverse quarters400ms andthree opposites800ms,normalfactory/main/grid/player with stagedcardinals+family. Exact orderedturn phases,actor-player restores/pause,destination0return,all4destinationphases andfinalpause. Dedicatedfree furnished fixture,normalflagsfalse. NotfullRunSave/visibleTitleContinue/completepickup-unload/continuouscontact/fullsetacceptance."},"\t"));file.close()
	print("MARSH REMAINING PATHS: %dchecks,%dviews,%dfailures"%[checks,captures.size(),failures]);quit(1 if failures else 0)
