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
var checks:=0
var north_route:=false
var expedition_kind:="salvage"
func observe_action(_water:Dictionary):pass
func _init():
	for arg in OS.get_cmdline_user_args():
		if arg.begins_with("--capture-dir="):capture_dir=arg.trim_prefix("--capture-dir=")
		if arg.begins_with("--rotation="):only_rotation=int(arg.trim_prefix("--rotation="))
	call_deferred("run")
func check(ok:bool,message:String):
	checks+=1
	if not ok:failures+=1;push_error(message)
func run():
	if not OS.get_environment("APPDATA").contains("marsh-water-actions"):quit(2);return
	if DisplayServer.get_name()=="headless":quit(2);return
	root.size=Vector2i(1600,900)
	seed(20261015)
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
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
		for rotation in range(4):
			await journey("delivery",rotation)
			await journey("recall-outbound",rotation)
	if not capture_dir.is_empty():
		var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"journeys":reports},"  "))
	game.free()
	if not FileAccess.file_exists("res://tests/test_marsh_expedition_presentation.gd.uid"):
		var uid=FileAccess.open("res://tests/test_marsh_expedition_presentation.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	for suffix in [".meta",".loop",".loop.bak",".loop.comms.json"]:
		if FileAccess.file_exists(stem+suffix):DirAccess.remove_absolute(ProjectSettings.globalize_path(stem+suffix))
	print("MARSH WATER ACTIONS NATIVE: ",checks," checks; ",reports.size()," journeys; failures=",failures)
	quit(1 if failures else 0)
func journey(mode:String,rotation:int=0):
	game._start_reboot_cycle();game.tick_timer.stop();game.paused=false;game.Architects.advance_core(game,10)
	var outward:Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][rotation]
	var across:=Vector2i(-outward.y,outward.x)
	HOME=Vector2i(20,20)+outward;TARGET=Vector2i(20,20)+outward*4+across
	for step in range(1,5):
		for side in [0,1]:
			var cell:Vector2i=Vector2i(20,20)+outward*step+across*side
			# Crew wards belong to the checkpoint roster; route around them. Unidentified wards
			# ("recovery") too: erasing one on the random route made the saved site invalid, so
			# the checkpoint fell back to its backup about one run in three (Sept 26; site seeds 1, 6).
			if game.wrecks.get(cell,{}).get("kind","") not in ["cryo","charging","recovery"]:game.wrecks.erase(cell)
	game._place_room("airlock",HOME,true);game.occupied[HOME].rotation=rotation;game.powered_room_cells[HOME]=true
	game.resources.oxygen=0;game.resources.food=50;game.resources.metal=5;game.resources.data=0
	game.drone_fleet.sites={TARGET:game.drone_fleet.Sites.make_site(expedition_kind,3)}
	game.drone_fleet.sites[TARGET].discovered=true;game.drone_fleet.sites_initialized=true
	if north_route:
		# Fixture obstacle forces the last real sea-route leg northward. Production
		# pathfinding and actor facing still choose the route; no direction override.
		game._place_room("corridor",TARGET+Vector2i.RIGHT,true)
	var actor=game.marsh_npc
	var water_frames:Dictionary={};var water_restores:Dictionary={};var captured:Dictionary={}
	check(Trips.dispatch(game,"marsh",HOME,expedition_kind),mode+" dispatch")
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
		var water:Dictionary=preload("res://scripts/marsh_water_actions.gd").clock(actor,game.occupied)
		observe_action(water)
		if not water.is_empty():
			key=water.key
			var slot:int=game.grid_view.marsh_player.frames[key].find(texture)
			check(slot>=0,"actual renderer selects water action "+key)
			if not water_frames.has(key):water_frames[key]={}
			water_frames[key][slot]=true
			check(texture==game.grid_view.marsh_player.frame_at_elapsed(key,water.elapsed),"saved water/work clock selects exact source")
			var restore_kind:String="lift" if key.begins_with("water-lift-") else "settle" if key.begins_with("water-settle-") else "work" if key.begins_with("water-salvage-") and not key.begins_with("water-salvage-enter-") else ""
			if key=="water-mine-"+actor.direction:restore_kind="work"
			if not restore_kind.is_empty() and slot==1 and not water_restores.has(restore_kind):
				var pixels:PackedByteArray=texture.get_image().get_data();var saved:Dictionary=actor.snapshot()
				check(Save.write(game,game.run_save_path)==OK,"water action checkpoint writes")
				var disk:Dictionary=Save.read(game.run_save_path)
				check(not disk.is_empty() and not disk.get("_recovered_backup",false),"water checkpoint current")
				check(Save.restore(game,disk),"water action checkpoint restores")
				game.tick_timer.stop();game.paused=true;actor=game.marsh_npc
				check(actor.foot==Vector2(saved.foot),"water restore preserves physical contact")
				check(game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"water restore preserves source pixels")
				var held:Dictionary=actor.snapshot();game._process(.2)
				check(actor.snapshot()==held,"pause preserves water action and service clock")
				game.paused=false;water_restores[restore_kind]=true
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
		var slot:int=game.grid_view.marsh_player.frames.get(key,[]).find(texture)
		var tag:String=phase+"/"+key+"/"+str(slot)
		var capture:bool=not captured.has(tag) and (not water.is_empty() or phase in ["pickup","unload"] or phase!=previous or draining)
		if capture and not capture_dir.is_empty():
			captured[tag]=true
			game.selected_card_id="";game.hovered_card_id="";game.crew_comms.panel.hide()
			game._set_grid_zoom(.7,true,actor.foot/(384.0*40.0));game.grid_view.queue_redraw()
			await process_frame;await RenderingServer.frame_post_draw
			var image:Image=root.get_texture().get_image()
			var at:Vector2=game.get_marsh_position()+Vector2(0,game.get_cell_size()*.038)
			var canvas:Vector2=root.get_final_transform()*game.grid_view.get_global_transform_with_canvas()*at
			var corner:=Vector2i(clampi(roundi(canvas.x)-300,0,image.get_width()-600),clampi(roundi(canvas.y)-280,0,image.get_height()-480))
			var filename="q%d-%s-%03d-%s.png"%[rotation,mode,capture_count,phase]
			check(image.get_region(Rect2i(corner,Vector2i(600,480))).save_png(capture_dir.path_join(filename))==OK,"current room crop saved")
			check(texture.get_image().save_png(capture_dir.path_join("source-"+filename))==OK,"actual source saved")
			capture_count+=1
			samples.append({"file":filename,"phase":phase,"pose":pose,"key":key,"slot":slot,"direction":actor.direction,"elapsed":actor.expedition.elapsed,"medium":actor.movement_medium,"turn":turn})
		previous=phase;game.visual_time_seconds+=1.0/30.0
		Cycle.advance(game,1.0/30.0);game._update_test_walker(1.0/30.0)
	check(actor.expedition.is_empty() and not actor.dead and actor.movement_medium=="dry",mode+" completed dry and alive")
	check(water_restores.has("lift"),"lift actual disk restore exercised")
	var lift_key:String="water-lift-"+actor.direction
	# Facing can change on exit; coverage is grouped by the actual clock key.
	var lifts:Array=water_frames.keys().filter(func(k):return str(k).begins_with("water-lift-"))
	check(lifts.size()==1 and water_frames[lifts[0]].size()==4,"all four flooding lift holds")
	if mode=="recall-outbound":
		var settles:Array=water_frames.keys().filter(func(k):return str(k).begins_with("water-settle-"))
		check(settles.size()==1 and water_frames[settles[0]].size()==4,"all four empty-handed settling holds")
		check(water_restores.has("settle"),"empty drain actual disk restore exercised")
	else:
		var family:String="water-mine-" if expedition_kind=="mining" else "water-salvage-"
		var works:Array=water_frames.keys().filter(func(k):return str(k) in [family+"north",family+"south",family+"east",family+"west"])
		check(works.size()==1 and water_frames[works[0]].size()==(5 if expedition_kind=="mining" else 6),"all underwater working holds")
		if expedition_kind=="mining" and works.size()==1:
			var facing:String=str(works[0]).trim_prefix(family)
			for action in ["water-mine-draw-","water-mine-stow-"]:check(water_frames.get(action+facing,{}).size()==4,"all mining tool handoff holds "+action+facing)
		if north_route:check(works==[family+"north"],"real final sea-route leg reaches north work")
		check(water_restores.has("work"),"underwater work actual disk restore exercised")
	var loaded:bool=mode!="recall-outbound"
	check(game.drone_fleet.sites[TARGET].units==(2 if loaded else 3),mode+" exact extraction count")
	var reward:Dictionary=game.drone_fleet.Sites.LOADS[expedition_kind] if loaded else {}
	check(game.resources.metal==5+reward.get("metal",0) and game.resources.data==reward.get("data",0),mode+" exact delivery credit")
	if loaded:
		check(phases.size()==Trips.PHASES.size(),mode+" all expedition phases")
		check(pickup.size()==6 and not pickup.has(-1),mode+" plays all six pickup poses")
		check(unload.size()==4 and not unload.has(-1),mode+" plays all four unload poses")
		check(not turns.is_empty(),mode+" actual renderer plays cargo turn")
		check(drain_frames.size()==5 and not drain_frames.has(-1),mode+" all five drainage poses before first carry stride")
	else:check(pickup.is_empty() and unload.is_empty(),"Empty recall never picks up/unloads a case")
	reports.append({"mode":mode,"rotation":rotation,"phases":phases.keys(),"pickup_frames":pickup.keys(),"unload_frames":unload.keys(),"drain_frames":drain_frames.keys(),"turns":turns.keys(),"captures":samples,"water_holds":water_frames,"water_restores":water_restores})

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
