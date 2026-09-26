extends SceneTree
## Dedicated prebuilt station; real dispatch, airlock, actor and renderer paths.
const Trips=preload("res://scripts/crew_expedition.gd")
const Cycle=preload("res://scripts/airlock_cycle.gd")
const Save=preload("res://scripts/run_save.gd")
var HOME=Vector2i(20,19)
var TARGET=Vector2i(21,16)
var game
var failures:=0
var capture_dir:=""
var reports:=[]
var only_rotation:=-1
func _init():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="):capture_dir=arg.trim_prefix("--capture-dir=")
		if arg.begins_with("--rotation="):only_rotation=int(arg.trim_prefix("--rotation="))
	call_deferred("run")
func check(ok:bool,message:String):
	if not ok:failures+=1;push_error(message)
func run():
	game=load("res://scenes/main.tscn").instantiate()
	var stem="user://marsh_expedition_visual_%d"%OS.get_process_id()
	game.meta.save_path=stem+".meta";game.run_save_path=stem+".loop"
	game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.panel.hide();game.tick_timer.stop()
	if not capture_dir.is_empty():DirAccess.make_dir_recursive_absolute(capture_dir)
	if only_rotation>=0:await journey("delivery",only_rotation)
	else:
		for mode in ["delivery","recall-outbound","recall-loaded"]:await journey(mode)
		for rotation in [1,2,3]:await journey("delivery",rotation)
	if not capture_dir.is_empty():
		var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"failures":failures,"journeys":reports},"  "))
	game.free()
	if not FileAccess.file_exists("res://tests/test_marsh_expedition_presentation.gd.uid"):
		var uid=FileAccess.open("res://tests/test_marsh_expedition_presentation.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	for suffix in [".meta",".loop",".loop.bak",".loop.comms.json"]:
		if FileAccess.file_exists(stem+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(stem+suffix))
	print("MARSH EXPEDITION PRESENTATION: ",reports.size()," journeys; failures=",failures)
	quit(1 if failures else 0)
func journey(mode:String,rotation:int=0):
	game._start_reboot_cycle();game.tick_timer.stop();game.paused=false;game.Architects.advance_core(game,10)
	var outward:Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][rotation]
	var across:=Vector2i(-outward.y,outward.x)
	HOME=Vector2i(20,20)+outward;TARGET=Vector2i(20,20)+outward*4+across
	for step in range(1,5):
		for side in [0,1]:
			var cell:Vector2i=Vector2i(20,20)+outward*step+across*side
			# Crew wards belong to the checkpoint roster; route around them.
			if game.wrecks.get(cell,{}).get("kind","") not in ["cryo","charging"]:game.wrecks.erase(cell)
	game._place_room("airlock",HOME,true);game.occupied[HOME].rotation=rotation;game.powered_room_cells[HOME]=true
	game.resources.oxygen=0;game.resources.food=50;game.resources.metal=5;game.resources.data=0
	game.drone_fleet.sites={TARGET:game.drone_fleet.Sites.make_site("salvage",3)}
	game.drone_fleet.sites[TARGET].discovered=true;game.drone_fleet.sites_initialized=true
	var actor=game.marsh_npc
	check(Trips.dispatch(game,"marsh",HOME),mode+" dispatch")
	if actor.expedition.is_empty():return
	var phases:={};var pickup:={};var unload:={};var turns:={};var drain_frames:={};var samples:=[];var previous:="";var recalled:=false;var restored:=false;var drain_verified:=false;var capture_count:=0
	for tick in range(5400):
		if actor.expedition.is_empty():break
		var phase:String=actor.expedition.phase;var pose:String=actor.animation_state()
		phases[phase]=true
		if (mode=="recall-outbound" and phase=="outbound") or (mode=="recall-loaded" and phase=="return"):
			if not recalled:check(Trips.request_recall(game,actor),mode+" request");recalled=true
		var texture=game.grid_view._get_marsh_frame(game)
		check(texture!=null,mode+" missing texture "+phase)
		var key=pose+"-"+actor.direction
		if phase=="pickup":pickup[game.grid_view.marsh_player.frames[key].find(texture)]=true
		if phase=="unload" and not actor.expedition.cargo.is_empty():unload[game.grid_view.marsh_player.frames[key].find(texture)]=true
		var chamber:Dictionary=Cycle.state(game.occupied[HOME])
		var draining:bool=phase=="drain" and chamber.phase=="draining" and float(chamber.elapsed)>=1.6 and not actor.expedition.cargo.is_empty()
		if draining:
			drain_frames[game.grid_view.marsh_player.frames["cargo-drain-"+actor.direction].find(texture)]=true
			if mode=="delivery" and float(chamber.elapsed)>=2.1 and not drain_verified:
				check_drain_clock();actor=game.marsh_npc;drain_verified=true
		var turn:String=game.grid_view.marsh_player.motion.get("clip","")
		if turn.begins_with("swim-carry-turn-"):turns[turn]=true
		check(game.resources.metal==5 and game.resources.data==0,"Cargo credited before unloading finished")
		if mode=="delivery" and phase=="return" and not restored:
			var pixels=texture.get_image().get_data();var foot:Vector2=actor.foot
			check(Save.write(game,game.run_save_path)==OK,"Loaded expedition checkpoint writes")
			var disk:Dictionary=Save.read(game.run_save_path)
			var current:bool=not disk.is_empty() and not disk.get("_recovered_backup",false) and disk.get("crew",{}).get("marsh",{}).get("expedition",{}).get("home",Vector2i(-1,-1))==HOME
			check(current,"Loaded checkpoint is current, not backup: q%d / %s"%[rotation,Save.last_error])
			if not current:return
			check(Save.restore(game,disk),"Loaded expedition checkpoint restores")
			game.tick_timer.stop();game.paused=true;actor=game.marsh_npc
			check(game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"Loaded restore preserves visible pose")
			game._process(.2)
			check(actor.foot==foot,"Paused loaded return stays fixed")
			game.paused=false;restored=true
		var capture:bool=phase!=previous or (phase in ["pickup","unload"] and tick%2==0) or (not turn.is_empty() and tick%3==0) or (draining and float(chamber.elapsed)<=3.0 and tick%2==0)
		if capture and not capture_dir.is_empty() and DisplayServer.get_name()!="headless":
			game.selected_card_id="";game.hovered_card_id="";game.crew_comms.panel.hide()
			game._set_grid_zoom(.7,true,actor.foot/(384.0*40.0));game.grid_view.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var filename="q%d-%s-%03d-%s.png"%[rotation,mode,capture_count,phase]
			root.get_texture().get_image().save_png(capture_dir.path_join(filename));capture_count+=1
			samples.append({"file":filename,"phase":phase,"pose":pose,"direction":actor.direction,"elapsed":actor.expedition.elapsed,"medium":actor.movement_medium,"turn":turn})
		previous=phase;game.visual_time_seconds+=1.0/30.0
		Cycle.advance(game,1.0/30.0);game._update_test_walker(1.0/30.0)
	check(actor.expedition.is_empty() and not actor.dead and actor.movement_medium=="dry",mode+" completed dry and alive")
	var loaded:bool=mode!="recall-outbound"
	check(game.drone_fleet.sites[TARGET].units==(2 if loaded else 3),mode+" exact extraction count")
	check(game.resources.metal==(6 if loaded else 5) and game.resources.data==(1 if loaded else 0),mode+" exact delivery credit")
	if loaded:
		check(phases.size()==Trips.PHASES.size(),mode+" all expedition phases")
		check(pickup.size()==6 and not pickup.has(-1),mode+" plays all six pickup poses")
		check(unload.size()==4 and not unload.has(-1),mode+" plays all four unload poses")
		check(not turns.is_empty(),mode+" actual renderer plays cargo turn")
		check(drain_frames.size()==5 and not drain_frames.has(-1),mode+" all five drainage poses before first carry stride")
	else:check(pickup.is_empty() and unload.is_empty(),"Empty recall never picks up/unloads a case")
	reports.append({"mode":mode,"rotation":rotation,"phases":phases.keys(),"pickup_frames":pickup.keys(),"unload_frames":unload.keys(),"drain_frames":drain_frames.keys(),"turns":turns.keys(),"captures":samples})

func check_drain_clock():
	var actor=game.marsh_npc;var room:Dictionary=game.occupied[HOME]
	var original_direction:String=actor.direction;var original_cycle:Dictionary=room.airlock_cycle.duplicate()
	for direction in ["east","west","north","south"]:
		actor.direction=direction;var seen:={};var key="cargo-drain-"+direction
		for i in range(61):
			room.airlock_cycle={"phase":"draining","elapsed":1.6+i/50.0}
			var texture=game.grid_view._get_marsh_frame(game);seen[game.grid_view.marsh_player.frames[key].find(texture)]=true
		check(seen.size()==5 and not seen.has(-1),"Drain renderer covers all rising poses "+direction)
		room.airlock_cycle={"phase":"depressurizing","elapsed":.2}
		check(game.grid_view._get_marsh_frame(game)==game.grid_view.marsh_player.frames[key][4],"Drain holds planted pose "+direction)
	actor.direction=original_direction;room.airlock_cycle=original_cycle
	actor.dead=true
	check(game.grid_view._get_marsh_cargo_drain_frame(game)==null,"Drain never overrides death playback")
	actor.dead=false
	var held=game.grid_view._get_marsh_frame(game);var pixels=held.get_image().get_data()
	game.paused=true;game._process(.3)
	check(game.grid_view._get_marsh_frame(game)==held and room.airlock_cycle==original_cycle,"Pause holds drain pose and interlock")
	game.paused=false;game.powered_room_cells.erase(HOME);Cycle.advance(game,.3)
	check(game.grid_view._get_marsh_frame(game)==held and room.airlock_cycle==original_cycle,"Power loss holds drain pose and interlock")
	game.powered_room_cells[HOME]=true
	check(Save.write(game,game.run_save_path)==OK,"Drain checkpoint writes")
	check(Save.restore(game,Save.read(game.run_save_path)),"Drain checkpoint restores")
	game.tick_timer.stop();game.paused=false
	check(game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"Drain checkpoint preserves pose pixels")
