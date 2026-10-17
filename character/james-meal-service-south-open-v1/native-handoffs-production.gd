extends SceneTree
const OUT := "res://character/james-meal-service-south-open-v1/"
const Service=preload("res://scripts/airlock_service.gd")

var game
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func capture(label:String,npc)->String:
	var screen:=Rect2();var visible:=false
	for attempt in range(120):
		var center:Vector2=npc.foot/384.0*game.get_cell_size()
		game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
		game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
		game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var world:=Rect2(npc.foot/384.0*game.get_cell_size()-Vector2.ONE*game.get_cell_size()*.45,Vector2.ONE*game.get_cell_size()*.9)
		screen=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
		var viewport:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
		if viewport.encloses(screen):visible=true;break
	check(visible,"Entire locker review region visibly inside station viewport")
	var screenshot:=root.get_texture().get_image()
	var image:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var path:String=OUT+"production-captures/"+label+".png"
	check(image.save_png(path)==OK,"Native locker capture")
	return path
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
	game.meta.save_path="user://james-locker.meta";game.run_save_path="user://james-locker.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={"room-galley/0":{"library/sp-galley-2":null,"library/sp-galley-4":null,"library/sp-generated-counter-galley-prep":[0.0,126.0]}};store.revision+=1;store.geometry_revision+=1;store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"production-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var npc=game.branforth_npc
	game.grid_view._get_branforth_frame_source(game)
	var player=game.grid_view.branforth_player;var results:Array=[]
	game.resources.food=1000;game.resources.oxygen=1000;game.running=true;game.paused=false
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-helmet-fitting-east-v1/manifest.json"))
	game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
	for offset in [Vector2i.ZERO,Vector2i.DOWN]:
		var room:Dictionary=game.RoomDatabaseScript.get_room("galley" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=cell+offset;room.rotation=0;room.water_level=0;room.fire=0
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	npc.rebuild(game);var prep:Dictionary=npc.geometry[cell].props.filter(func(prop):return prop.id=="library/sp-generated-counter-galley-prep")[0];check(Rect2(-184,-184,368,368).encloses(prep.rect),"Open prep counter floor footprint wholly inside hull");print("OPEN PREP RECT ",prep.rect," COLLISION ",prep.get("collision",[]));npc.dead=false;npc.active=true;npc.stage="";npc.path.clear();npc.goal="";npc.state="idle";npc.timer=0;npc.helmet_equipped=false;npc.movement_medium="dry";npc.expedition.clear();npc.avoidance_positions.clear()
	npc.foot=npc.graph.get_point_position(npc.nearest_in_room(center+Vector2(-32,-48),cell));npc.direction="south";npc.needs={"maintenance":0.0,"hunger":95.0,"fatigue":0.0,"curiosity":0.0};npc.decision_rng.seed=1;print("SOUTH START ",npc.foot-center," nodes=",npc.room_nodes[cell].size()," stand=",npc.can_stand(center+Vector2(112,64)));npc.choose_goal(game);print("SOUTH PLAN ",npc.goal," ",npc.goal_cell," ",npc.path)
	var reached:=false
	for tick in range(3000):
		game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
		if npc.stage=="life_eat":reached=true;break
	print("SOUTH ARRIVAL ",reached," ",npc.snapshot()," stations=",npc.RoomActivity.stations(npc.geometry[cell]))
	check(reached and npc.direction=="south","Normal chooser reaches actual South galley service")
	var arrival:Dictionary=npc.snapshot()
	var foot:Vector2=npc.foot;var frames:Dictionary={};var samples:Array=[];var last:Texture2D;var previous:String=""
	var manifest_states:Dictionary={}
	var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-meal-service-south-open-v1/handoffs-manifest.json"))
	for entry in pack.states:
		manifest_states[entry.id]=entry

	var normal_states:Array=["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"]
	var completed:=false;var normal_completion:Dictionary={}
	for tick in range(1200):
		var pose:String=npc.animation_state();var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
		if pose not in normal_states:
			normal_completion={"snapshot":npc.snapshot(),"pose":pose,"playerKey":player.current_key,"textureSize":texture.get_size(),"lastSize":last.get_size() if last!=null else Vector2.ZERO,"capture":await capture("normal-completion",npc)}
			print("ACTUAL NORMAL COMPLETION ",normal_completion)
			var registered_idle:=Image.create(256,256,false,Image.FORMAT_RGBA8)
			registered_idle.fill(Color(0,0,0,0))
			var pivot_delta:Vector2=last.get_meta("crew_pivot")-texture.get_meta("crew_pivot")
			registered_idle.blit_rect(texture.get_image(),Rect2i(Vector2i.ZERO,texture.get_image().get_size()),Vector2i(pivot_delta))
			check(last!=null and last.get_image().get_data()==registered_idle.get_data(),"Final deposit joins complete live idle image after metadata-pivot registration")
			completed=true;break
		var key:String=pose+"-south";var index:int=player.frames[key].find(texture)
		check(index>=0,"Actual drawer selects staged handoff/loop source")
		if previous!=pose and last!=null:check(last.get_image().get_data()==texture.get_image().get_data(),"Exact source join "+previous+" to "+pose)
		if not frames.has(key):frames[key]={}
		if not frames[key].has(index):
			check(npc.foot==foot and npc.direction=="south","Whole meal/drink source remains at supported contact")
			frames[key][index]=true;samples.append({"key":key,"index":index,"elapsed":npc.action_elapsed(),"capture":await capture("%s-%02d"%[pose,index],npc)})
		last=texture;previous=pose;game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120
	check(completed,"Actual Life.next progresses meal6s through drink3s to empty idle")
	for pose in normal_states:
		var key:String=pose+"-south";check(frames.has(key) and frames[key].size()==manifest_states[key].frameCount,"All candidate sources drawn "+key)
	var controlled_cuts:Array=[]
	for entry in pack.states:
		if not String(entry.id).begins_with("meal-return-"):continue
		await npc.restore_snapshot(game,arrival);game.powered_room_cells[cell]=true
		var source_key:String=entry.provenance.sourceState;var source_index:int=entry.provenance.sourceIndex
		var source:String=source_key.trim_suffix("-south");var source_time:=.00001
		for index in range(source_index):source_time+=float(manifest_states[source_key].frameDurationsMs[index])*.001
		npc.stage="life_eat" if source in ["meal-acquire","meal-deposit","eat"] else "life_drink"
		match source:
			"meal-acquire":npc.timer=6.0-source_time
			"meal-deposit","cup-deposit":npc.timer=.9-source_time
			"cup-acquire":npc.timer=3.0-source_time
			"eat":npc.timer=5.1-source_time/npc.meal_cycle_seconds("eat","south")*1.4
			"drink":npc.timer=2.1-source_time/npc.meal_cycle_seconds("drink","south")*1.2
		var before:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(before==player.frames[source_key][source_index],"Actual timer selects exact source "+entry.id)
		var hunger:float=npc.needs.hunger
		game.powered_room_cells.erase(cell);game._update_test_walker(.000001)
		var first:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(npc.meal_return_active() and npc.meal_return.index==source_index and npc.meal_return.facing=="south","Actual service loss selects facing/index return "+entry.id)
		check(first.get_image().get_data()==before.get_image().get_data(),"Actual return first pixels exact "+entry.id)
		check(first.get_meta("crew_depth_offset",0)==before.get_meta("crew_depth_offset",0),"Return cut depth exact "+entry.id)
		var snap:Dictionary=npc.snapshot()
		check(npc.valid_branforth_snapshot(snap),"Actual South return snapshot valid "+entry.id)
		var bad:Dictionary=snap.duplicate(true);bad.branforth_meal_return.index=manifest_states[source_key].frameCount
		check(not npc.valid_branforth_snapshot(bad),"Out of range index rejected "+entry.id)
		bad=snap.duplicate(true);bad.branforth_meal_return.erase("facing")
		check(not npc.valid_branforth_snapshot(bad),"Legacy implicit North does not accept South snapshot "+entry.id)
		await npc.restore_snapshot(game,snap)
		check(npc.snapshot()==snap,"Actual South return snapshot restores exactly "+entry.id)
		game.powered_room_cells[cell]=true
		if source=="cup-acquire" and source_index==7:
			game.paused=true;var clock:float=game.visual_time_seconds
			var save=preload("res://scripts/run_save.gd");var scratch_path:="user://james-south-return.loop"
			check(save.problem(save.capture(game)).is_empty(),"South eight-index checkpoint valid")
			check(save.write(game,scratch_path)==OK,"South return checkpoint writes")
			var data:Dictionary=save.read(scratch_path)
			root.remove_child(game);game.queue_free();await process_frame
			game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
			game.meta.save_path="user://james-locker.meta";game.run_save_path=scratch_path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
			root.add_child(game);current_scene=game
			while not game.startup_complete:await process_frame
			game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
			check(await save.restore_staged(game,data),"Fresh scene South index7 disk Continue")
			game.run_save_path=scratch_path;game.tick_timer.stop();game.set_process(false);game.crew_comms.set_process(false)
			npc=game.branforth_npc;player=game.grid_view.branforth_player
			check(npc.snapshot()==snap and game.paused and game.visual_time_seconds==clock,"Disk Continue actor clock pause exact")
			check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==first.get_image().get_data(),"Disk Continue source pixels exact")
			game._process(.5)
			check(npc.snapshot()==snap and game.visual_time_seconds==clock,"Paused South return does not advance")
			game.paused=false
		var duration:float=npc.meal_return_seconds(source,source_index,"south")
		var ticks:=0
		while npc.meal_return_active() and ticks<1200:
			check(npc.foot==foot and npc.direction=="south" and npc.goal=="" and npc.stage=="","Return holds physical contact "+entry.id)
			game._update_test_walker(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
		check(not npc.meal_return_active() and ticks<1200,"Actual return completes "+entry.id)
		check(npc.needs.hunger>=hunger,"Interrupted service awards no hunger relief "+entry.id)
		var terminal:Texture2D=game.grid_view._get_branforth_frame_source(game)
		var empty:=Image.create(256,256,false,Image.FORMAT_RGBA8);empty.fill(Color(0,0,0,0))
		var delta:Vector2=player.frames["meal-acquire-south"][0].get_meta("crew_pivot")-terminal.get_meta("crew_pivot")
		empty.blit_rect(terminal.get_image(),Rect2i(Vector2i.ZERO,terminal.get_image().get_size()),Vector2i(delta))
		if source=="meal-acquire" and source_index==0:
			print("RETURN TERMINAL DIAGNOSTIC ",npc.snapshot()," key=",player.current_key," size=",terminal.get_size()," pivot=",terminal.get_meta("crew_pivot"))
			empty.save_png(OUT+"return-terminal-diagnostic.png")
		check(empty.get_data()==player.frames["meal-acquire-south"][0].get_image().get_data(),"Actual return ends complete empty idle "+entry.id)
		controlled_cuts.append({"key":entry.id,"sourceIndex":source_index,"duration":duration,"firstExact":true,"lastExact":true,"actualServiceLoss":true})
	check(controlled_cuts.size()==44,"All44 actual service-loss returns exercised")

	var file:=FileAccess.open(OUT+"native-handoffs-production-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"foot":foot,"local":foot-center,"samples":samples,"controlledCuts":controlled_cuts,"frameCoverage":frames,"normalCompletion":normal_completion,"scope":"Normal production loader/controller, actual supported chooser/route and nine-second course, all44 phase sources, exact joins and idle.44 timer-selected source slots interrupted by actual power-loss policy; snapshots and bounds all44; fresh-scene disk Continue and pause at South cup-acquire index7. Dedicated open prep geometry only. No other hazard/gear/placement proof or owner visual acceptance."},"  "));file.close()
	if not FileAccess.file_exists(OUT+"native-handoffs-production.gd.uid"):
		var uid_file=FileAccess.open(OUT+"native-handoffs-production.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid_file.close()
	print("JAMES SOUTH HANDOFFS PRODUCTION: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)

