extends "res://character/james-construction-controller-v2/validate.gd"
const Motion = preload("res://scripts/james_construction_motion.gd")
var output: String
var serial := 0
func directions() -> Array: return [0]
func lane() -> String: return "north"
func access(mode: String, blocked: bool):
	game.hardware.power = not blocked if mode == "power" else true
	game.hardware.doors = blocked if mode == "doors" else false
func observe(label: String, actor, previous: String) -> String:
	var source: Texture2D = game.grid_view._get_branforth_frame_source(game)
	var pixels: String = source.get_image().get_data().hex_encode().sha256_text()
	var phase: String = actor.construction_motion.get("phase", "work")
	var token := phase + ":" + pixels
	if token != previous:
		var path := output + "native/" + label + "-%04d.png" % serial; serial += 1
		game.grid_view.queue_redraw(); await process_frame; await RenderingServer.frame_post_draw
		check(root.get_texture().get_image().save_png(path) == OK, "Motion source capture")
		var key: String = actor.animation_state() + "-" + actor.direction
		var index: int = game.grid_view.branforth_player.equipment_frames["diving-helmet"].get(key, []).find(source)
		if not actor.construction_motion.is_empty():
			var m: Dictionary = actor.construction_motion
			var row: Array = m.home.back() if phase == "hold" else m.sequence[Motion.slot(m.sequence, m.elapsed)]
			key = row[0]; index = row[1]
		check(index >= 0 and game.grid_view.branforth_player.equipment_frames["diving-helmet"][key][index].get_image().get_data() == source.get_image().get_data(), "Whole selected original pose")
		records.append({"label":label,"capture":path,"phase":phase,"key":key,"index":index,"timer":actor.timer,"elapsed":actor.construction_motion.get("elapsed",0),"helmet":actor.helmet_equipped,"foot":[actor.foot.x,actor.foot.y],"footViewport":[(root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)).x,(root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot*game.get_cell_size()/384.0)).y],"sourceHash":pixels,"sparks":Effects.torch_actors(game).has(actor)})
	return token
func run():
	if DisplayServer.get_name() == "headless": quit(2); return
	var expected := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\", "/")
	if OS.get_user_data_dir().replace("\\", "/").to_lower() != expected.to_lower(): quit(3); return
	output = "res://character/james-construction-helmet-v1/" + lane() + "/"
	DirAccess.make_dir_recursive_absolute(output + "native")
	game = load("res://scenes/main.tscn").instantiate(); game.meta.save_path = "user://james-construction-motion.meta"; game.run_save_path = "user://james-construction-motion.loop"
	game.meta.unlocked_architect_ids = {"bill":true,"branforth":true}; game.meta.selected_architect = "branforth"
	root.add_child(game); current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game.running = true; game.paused = false; game.crew_comms.dismiss(); game.crew_comms.set_process(false)
	game.Architects.advance_core(game,10)
	if lane()=="south" and not game.hand_collapsed:game._toggle_hand_collapsed()
	var actor = game.branforth_npc; check(actor.active,"Genuine core release")
	var initial: Vector2 = actor.foot; var core := Vector2i(20,20); var core_room: Dictionary = game.occupied[core].duplicate(true)
	for side in directions():
		var direction: String = ["north","east","south","west"][side]
		game.placed_rooms.assign([core_room.duplicate(true)]); game.occupied.clear(); game.occupied[core] = game.placed_rooms[0]; game.drone_fleet.restore(null); game.drone_fleet.sites_initialized = true
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
		actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.signature="";actor.foot=initial;check(actor.set_helmet_equipped(true),"Prescribed worn helmet");actor.construction_motion.clear()
		var target: Vector2i = core + Construction.DIRS[side]; game.wrecks.erase(target); game.drone_fleet.sites.erase(target)
		game.hand.assign(["life_support"]); game._on_card_pressed("life_support")
		for rotation in range(4):
			game.selected_rotation=rotation
			if game.get_placement_problem("life_support",target).is_empty():break
		game._on_grid_clicked(target);check(game.drone_fleet.reserved(target),"Real paid motion job")
		game.selected_card_id="";game.selected_room_cell=target;game._refresh_all();game._set_grid_zoom(1.2,true,(Vector2(target)+Vector2(core)+Vector2.ONE)/80.0)
		for attempt in range(120):
			game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
			if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing:break
		for threshold in [.4,2.75,9.68]:
			for step in range(2400):
				game._process(1.0/60.0);game.grid_view._get_branforth_frame_source(game)
				if actor.goal=="construction" and actor.state=="weld" and actor.timer>=threshold:break
			check(actor.goal=="construction" and actor.state=="weld","Reach actual motion phase")
			var phase: String = actor.animation_state()
			for mode in ["power","doors"]:
				var label: String = direction + "-" + phase + "-" + mode
				var previous: String = await observe(label,actor,"")
				var foot: Vector2 = actor.foot; var work: float = actor.timer; var order: Dictionary = game.drone_fleet.order_at(target).duplicate(true)
				access(mode,true)
				var did_repeat := false; var restored := false; var pause_checked := false
				for step in range(300):
					game._process(1.0/60.0)
					if step % 30 == 0: print("JAMES MOTION TRACE ",label," step=",step," state=",actor.state," phase=",actor.construction_motion.get("phase","empty")," elapsed=",actor.construction_motion.get("elapsed",-1)," timer=",actor.timer," power=",game.hardware.power," doors=",game.hardware.doors)
					check(actor.foot==foot and actor.timer==work and game.drone_fleet.order_at(target)==order,"Tool motion preserves paid work and contact")
					check(not Effects.torch_actors(game).has(actor),"No sparks during interrupted motion")
					check(actor.valid_branforth_snapshot(actor.snapshot()),"Motion checkpoint admissible")
					if failures>0:quit(2);return
					previous=await observe(label,actor,previous)
					if not pause_checked and not actor.construction_motion.is_empty():
						var snapshot:Dictionary=actor.snapshot();var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data();var clock:float=game.visual_time_seconds
						game.paused=true;game._process(.25)
						check(actor.snapshot()==snapshot and game.visual_time_seconds==clock,"Pause freezes motion and work")
						check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Pause retains exact whole source")
						game.paused=false;pause_checked=true
					if actor.construction_motion.get("phase","")=="hold":
						access(mode,false);restored=true
					if mode=="power" and phase=="weld" and not did_repeat and actor.construction_motion.get("phase","")=="return" and actor.construction_motion.elapsed>=.1:
						var pixels:PackedByteArray=game.grid_view._get_branforth_frame_source(game).get_image().get_data()
						access(mode,true);game._process(1.0/60.0)
						check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==pixels,"Second loss reverses current return pose exactly")
						previous=await observe(label,actor,previous);did_repeat=true;restored=false
					if actor.construction_motion.get("phase","")=="done":break
				check(restored and actor.construction_motion.get("phase","")=="done","Exit hold return completes")
				if not restored or actor.construction_motion.get("phase","")!="done": print("JAMES MOTION FAILED DATA ",actor.snapshot());quit(2);return
				game._process(1.0/60.0)
				check(actor.construction_motion.is_empty() and actor.state=="weld" and actor.timer>work,"Paid work resumes after torch ready")
				previous=await observe(label,actor,previous)
				cases.append({"direction":direction,"phase":phase,"mode":mode,"repeatedLoss":did_repeat,"workBefore":work,"workAfter":actor.timer})
		for step in range(120):
			game._process(1.0/60.0)
			if game.occupied.has(target):break
		check(game.occupied.has(target) and not game.drone_fleet.reserved(target),"Motion job completes once")
		print("JAMES CONSTRUCTION MOTION CASE ",direction," captures=",serial," completed=",game.occupied.has(target))
	var report:=FileAccess.open(output+"evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"cases":cases,"scope":"Real paid construction, normal60Hz updates, arbitrary actual source-derived exit/hold/reverse return, power/door holds in draw/weld/stow, repeated loss mid-return for held power case, pause/source/snapshot/contact/progress/sparks checks. All source changes during reviewed interruptions captured. Bare only; no fresh Continue inside new motion yet."},"  "))
	for path in ["res://scripts/james_construction_motion.gd",get_script().resource_path]:
		if not FileAccess.file_exists(path+".uid"):
			var uid:=FileAccess.open(path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES HELMET CONSTRUCTION MOTION: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
