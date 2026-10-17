extends "res://character/james-construction-controller-v2/validate.gd"
const Motion = preload("res://scripts/james_construction_motion.gd")
var output: String
var serial := 0
func directions() -> Array: return [2]
func lane() -> String: return "safety"
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
		var index: int = game.grid_view.branforth_player.frames.get(key, []).find(source)
		if not actor.construction_motion.is_empty():
			var m: Dictionary = actor.construction_motion
			var row: Array = m.home.back() if phase == "hold" else m.sequence[Motion.slot(m.sequence, m.elapsed)]
			key = row[0]; index = row[1]
		check(index >= 0 and game.grid_view.branforth_player.frames[key][index].get_image().get_data() == source.get_image().get_data(), "Whole selected original pose")
		records.append({"label":label,"capture":path,"phase":phase,"key":key,"index":index,"timer":actor.timer,"elapsed":actor.construction_motion.get("elapsed",0),"foot":[actor.foot.x,actor.foot.y],"sourceHash":pixels,"sparks":Effects.torch_actors(game).has(actor)})
	return token
func run():
	if DisplayServer.get_name() == "headless": quit(2); return
	var expected := OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\", "/")
	if OS.get_user_data_dir().replace("\\", "/").to_lower() != expected.to_lower(): quit(3); return
	output = "res://character/james-construction-motion-v1/" + lane() + "/"
	DirAccess.make_dir_recursive_absolute(output + "native")
	game = load("res://scenes/main.tscn").instantiate(); game.meta.save_path = "user://james-construction-motion.meta"; game.run_save_path = "user://james-construction-motion.loop"
	game.meta.unlocked_architect_ids = {"bill":true,"branforth":true}; game.meta.selected_architect = "branforth"
	root.add_child(game); current_scene = game
	while not game.startup_complete: await process_frame
	game.set_process(false); game.tick_timer.stop(); game.running = true; game.paused = false; game.crew_comms.dismiss(); game.crew_comms.set_process(false)
	game.Architects.advance_core(game,10)
	var actor = game.branforth_npc; check(actor.active,"Genuine core release")
	var initial: Vector2 = actor.foot; var core := Vector2i(20,20); var core_room: Dictionary = game.occupied[core].duplicate(true)
	for event in ["cancel","death","flood"]:
		var side:int=2
		var direction: String = ["north","east","south","west"][side]
		game.placed_rooms.assign([core_room.duplicate(true)]); game.occupied.clear(); game.occupied[core] = game.placed_rooms[0]; game.drone_fleet.restore(null); game.drone_fleet.sites_initialized = true
		game.resources.metal=100;game.resources.power=100;game.resources.oxygen=100;game.resources.food=100
		for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
		actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.signature="";actor.foot=initial;actor.helmet_equipped=false;actor.construction_motion.clear()
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
		for step in range(2400):
			game._process(1.0/60.0);game.grid_view._get_branforth_frame_source(game)
			if actor.goal=="construction" and actor.state=="weld" and actor.timer>=2.75:break
		game.hardware.power=false
		for step in range(10):game._process(1.0/60.0)
		check(not actor.construction_motion.is_empty(),"Actual safety case has partial torch retraction")
		await observe(event+"-before",actor,"")
		if event=="cancel":game.drone_fleet.orders.clear()
		elif event=="death":
			actor.die()
			check(not Motion.eligible(actor),"Death immediately invalidates torch motion")
			var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
			check(source!=null and game.grid_view.branforth_player.frames["death-ground-south"].has(source),"Immediate death renders death source before another update")
		else:game.occupied[core].water_level=.9
		for step in range(10):game._process(1.0/60.0)
		print("JAMES MOTION SAFETY TRACE ",event," goal=",actor.goal," medium=",actor.movement_medium," dead=",actor.dead," motion=",actor.construction_motion)
		check(actor.construction_motion.is_empty(),"Safety preemption clears tool motion "+event)
		check(actor.goal!="construction" and not Effects.torch_actors(game).has(actor),"Safety preemption replaces work and extinguishes sparks "+event)
		cases.append({"event":event,"goal":actor.goal,"medium":actor.movement_medium,"dead":actor.dead})
		game.hardware.power=true;game.hardware.doors=false;actor.dead=false;actor.active=true;actor.movement_medium="dry"
	var report:=FileAccess.open(output+"evidence.json",FileAccess.WRITE)
	report.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"cases":cases,"scope":"Three actual South paid-job retractions preempted by removed order, death and critical room flooding. Immediate death source before another update and normal safety/controller cleanup. No other safety context claim."},"  "))
	for path in ["res://scripts/james_construction_motion.gd",get_script().resource_path]:
		if not FileAccess.file_exists(path+".uid"):
			var uid:=FileAccess.open(path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES CONSTRUCTION SAFETY: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
