extends SceneTree
const Normal = preload("res://scripts/marsh_npc.gd")
const Loading = preload("res://scripts/loading_transition.gd")
const OUTPUT = "res://output/marsh-animation-audit/south-salvage-job-v2-2026-10-04/"
const Trips=preload("res://scripts/crew_expedition.gd")
const Cycle=preload("res://scripts/airlock_cycle.gd")
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
	var canvas_position: Vector2 = root.get_final_transform() * game.grid_view.get_global_transform_with_canvas() * (position + Vector2(0, game.get_cell_size() * .038))
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

	var home:=Vector2i(20,21);var target:=Vector2i(20,24)
	for y in range(21,25):
		for x in [19,20]:
			var cell=Vector2i(x,y)
			if game.wrecks.get(cell,{}).get("kind","") not in ["cryo","charging","recovery"]:game.wrecks.erase(cell)
	game._place_room("airlock",home,true);game.occupied[home].rotation=2;game.powered_room_cells[home]=true
	game.resources.oxygen=50;game.resources.food=50;game.resources.metal=5;game.resources.data=0
	game.drone_fleet.sites={target:game.drone_fleet.Sites.make_site("salvage",3)}
	game.drone_fleet.sites[target].discovered=true;game.drone_fleet.sites_initialized=true
	for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
	game.selected_card_id="";game.hovered_card_id="";game.selected_room_cell=home;game.hand_panel.hide();game._refresh_all()
	var player=game.grid_view.marsh_player
	check(game.marsh_npc.get_script()==Normal,"actual normal Marsh factory")
	check(Trips.dispatch(game,"marsh",home),"actual normal expedition dispatch; reason="+Trips.reason(game,"marsh",home))
	actor=game.marsh_npc
	if actor.expedition.is_empty():quit(1);return
	var south_slots:Dictionary={};var expected_work:Array=[]
	var work_manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/marsh-v2/supplemental/south-work-polish-v1/manifest.json"))
	for entry in work_manifest.states:
		if entry.id=="salvage-south":
			for path in entry.frameFiles:
				var image:=Image.new();check(image.load_png_from_buffer(FileAccess.get_file_as_bytes(path))==OK,"current selected South salvage source decodes");expected_work.append(image.get_data())
	var phases:Dictionary={};var seen:Dictionary={};var east:Dictionary={};var pickup:Dictionary={};var unload:Dictionary={};var drain:Dictionary={};var turns:Dictionary={}
	var joins:Array=[];var restores:=0;var previous_key:="";var previous_slot:=-1;var previous_phase:=""
	for step in range(9000):
		if actor.expedition.is_empty():break
		var phase:String=actor.expedition.phase;var pose:String=actor.animation_state();phases[phase]=true
		var texture:Texture2D=game.grid_view._get_marsh_frame(game)
		check(texture!=null,"actual water route has source")
		if texture==null:break
		var key:String=pose+"-"+actor.direction
		var chamber:Dictionary=Cycle.state(game.occupied[home])
		var draining:bool=phase=="drain" and chamber.phase=="draining" and float(chamber.elapsed)>=1.6 and not actor.expedition.cargo.is_empty()
		if game.grid_view._get_marsh_cargo_drain_frame(game)!=null:key="cargo-drain-"+actor.direction
		elif actor.action_elapsed()<0 and not str(player.motion.get("clip","")).is_empty():key=player.motion.clip
		check(player.frames.has(key),"declared source key exists "+key)
		if not player.frames.has(key):break
		var slot:int=player.frames[key].find(texture)
		check(slot>=0,"normal route texture belongs to actual clip "+key)
		if slot<0:break
		if key=="swim-carry-east":east[slot]=true
		if phase=="salvage":
			check(key=="salvage-south" and actor.direction=="south" and actor.movement_medium=="exterior","actual outbound route derives South exterior salvage pose")
			if key=="salvage-south":
				south_slots[slot]=true
				check(texture.get_image().get_data()==expected_work[slot],"actual production salvage draws exact revised normal PNG")
		if phase=="pickup":pickup[slot]=true
		if phase=="unload" and not actor.expedition.cargo.is_empty():unload[slot]=true
		if draining:drain[slot]=true
		if key.begins_with("swim-carry-turn-"):turns[key]=true
		check(game.resources.metal==5 and game.resources.data==0,"cargo not credited before complete unload")
		if previous_key!=key or previous_phase!=phase:
			joins.append({"fromPhase":previous_phase,"phase":phase,"fromKey":previous_key,"fromSlot":previous_slot,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction})
		var wanted:bool=phase in ["salvage","pickup"] or previous_phase!=phase
		var signature:String=(phase+"/" if phase!="salvage" and phase!="pickup" else "")+key+":"+str(slot)
		if wanted and not seen.has(signature):
			seen[signature]=true
			var camera:Vector2=actor.foot/(384.0*float(game.GRID_SIZE))
			game.paused=true;check(await settle_camera(camera),"native camera and layers settled")
			await capture(signature,slot);captures.back()["expectedKey"]=key;captures.back()["phase"]=phase
			var saved:Dictionary=actor.snapshot();var playback:Dictionary=player.snapshot()
			check(Normal.valid_marsh_snapshot(saved),"real expedition actor validates")
			var restored=Normal.new();game.marsh_npc=restored;await restored.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true);player.restore_snapshot(bytes_to_var(var_to_bytes(playback)))
			check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"actual water-route phase source/root restore")
			game._process(.5)
			check(restored.snapshot()==saved and game.grid_view._get_marsh_frame(game).get_image().get_data()==texture.get_image().get_data(),"actual water-route restored pause hold")
			actor=restored;restores+=1;game.paused=false
		samples.append({"step":step,"phase":phase,"key":key,"slot":slot,"direction":actor.direction,"medium":actor.movement_medium,"foot":[actor.foot.x,actor.foot.y],"routeLeft":actor.expedition.route.size(),"next":str(actor.expedition.route[0]) if not actor.expedition.route.is_empty() else "","chamber":chamber.phase,"battery":actor.battery})
		previous_key=key;previous_slot=slot;previous_phase=phase
		game.visual_time_seconds+=.02;Cycle.advance(game,.02);game._update_test_walker(.02)
	check(actor.expedition.is_empty() and not actor.dead and actor.movement_medium=="dry","actual expedition completed dry/alive")
	check(game.drone_fleet.sites[target].units==2 and game.resources.metal==6 and game.resources.data==1,"one extraction/one safe delivery credit")
	check(phases.size()==Trips.PHASES.size(),"all twelve real expedition phases")
	check(south_slots.size()==6 and pickup.size()==6,"all six real South salvage timing holds and six pickup holds")
	check(not turns.is_empty(),"actual loaded route turns selected")
	var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
	file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"phases":phases.keys(),"southSalvageSlots":south_slots.keys(),"pickupSlots":pickup.keys(),"unloadSlots":unload.keys(),"drainSlots":drain.keys(),"turns":turns.keys(),"joins":joins,"actorPlayerRestores":restores,"scope":"One actual normal dispatched q2 expedition to a prescribed South salvage site. Actual route derives South exterior salvage; every selected South work source exact at all six timing holds, pickup, return/drain/exit/unload and one resource credit. Authored airlock/site fixture, normal economy/failure flags, normal catalogue and production actor/Cycle/player, no state or art injection. Actor/player snapshot restore and pause at captured boundaries. Not all route rotations/fullRunSave/visibleTitleContinue/helmet/continuous motion/physical contact/full-set acceptance."},"\t"));file.close()
	print("MARSH SOUTH SALVAGE JOB: ",checks,"checks,",failures,"failures,",captures.size(),"captures,",samples.size(),"samples")
	quit(1 if failures else 0)
