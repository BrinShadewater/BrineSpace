extends SceneTree
const OUT := "res://character/james-meal-service-south-open-v1/"
const Service=preload("res://scripts/airlock_service.gd")
class CandidateJames extends "res://scripts/branforth_npc.gd":
	var preview_key:String=""
	var preview_elapsed:float=0.0
	var cycle_lengths:Dictionary={"eat":1.5,"drink":3.0}
	func animation_state()->String:
		if not preview_key.is_empty():return preview_key.trim_suffix("-south")
		if active and not dead and not helmet_equipped and movement_medium=="dry" and direction=="south":
			if stage=="life_eat":
				if timer>5.1:return "meal-acquire"
				return "meal-deposit" if timer<=.9 else "eat"
			if stage=="life_drink":
				if timer>2.1:return "cup-acquire"
				return "cup-deposit" if timer<=.9 else "drink"
		return super.animation_state()
	func action_elapsed()->float:
		if not preview_key.is_empty():return preview_elapsed
		var pose=animation_state()
		if pose=="meal-acquire":return 6.0-timer
		if pose=="cup-acquire":return 3.0-timer
		if pose in ["meal-deposit","cup-deposit"]:return .9-timer
		if pose=="eat" and stage=="life_eat":return fposmod(6.0-timer-.9,1.4)/1.4*float(cycle_lengths.eat)
		if pose=="drink" and stage=="life_drink":return (3.0-timer-.9)/1.2*float(cycle_lengths.drink)
		return super.action_elapsed()

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
	var path:String=OUT+"handoff-captures/"+label+".png"
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
	DirAccess.make_dir_recursive_absolute(OUT+"handoff-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Real core-release roster")
	var saved:Dictionary=game.branforth_npc.snapshot();var npc=CandidateJames.new();npc.restore_snapshot(game,saved);game.branforth_npc=npc
	var player=game.grid_view.branforth_player;player.load_manifest("res://character/james-meal-service-south-open-v1/handoffs-manifest.json",true);var results:Array=[]
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
	var foot:Vector2=npc.foot;var frames:Dictionary={};var samples:Array=[];var last:Texture2D;var previous:String=""
	var manifest_states:Dictionary={}
	var pack:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/james-meal-service-south-open-v1/handoffs-manifest.json"))
	for entry in pack.states:
		manifest_states[entry.id]=entry
		if entry.id in ["eat-south","drink-south"]:
			var duration:=0.0
			for ms in entry.frameDurationsMs:duration+=float(ms)*.001
			npc.cycle_lengths[entry.id.trim_suffix("-south")]=duration
	var normal_states:Array=["meal-acquire","eat","meal-deposit","cup-acquire","drink","cup-deposit"]
	var completed:=false;var normal_completion:Dictionary={}
	for tick in range(1200):
		var pose:String=npc.animation_state();var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
		if pose not in normal_states:
			normal_completion={"snapshot":npc.snapshot(),"pose":pose,"playerKey":player.current_key,"textureSize":texture.get_size(),"lastSize":last.get_size() if last!=null else Vector2.ZERO,"capture":await capture("normal-completion",npc)}
			print("ACTUAL NORMAL COMPLETION ",normal_completion)
			check(last!=null and last.get_image().get_region(Rect2i(36,52,184,192)).get_data()==texture.get_image().get_data(),"Final deposit joins actual selected empty idle after common-pivot crop")
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
	npc.stage="";npc.goal="";npc.path.clear();npc.state="idle";npc.direction="south";npc.foot=foot
	for entry in pack.states:
		if not String(entry.id).begins_with("meal-return-"):continue
		var source_key:String=entry.provenance.sourceState;var source_index:int=entry.provenance.sourceIndex
		var source_time:=.00001
		for index in range(source_index):source_time+=float(manifest_states[source_key].frameDurationsMs[index])*.001
		npc.preview_key=source_key;npc.preview_elapsed=source_time
		var before:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(before.get_image().get_data()==player.frames[source_key][source_index].get_image().get_data(),"Controlled source clock selects exact interruption pose "+entry.id)
		npc.preview_key=entry.id;npc.preview_elapsed=0.0
		var first:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(first.get_image().get_data()==before.get_image().get_data(),"Actual return drawer begins with exact current pixels "+entry.id)
		check(first.get_meta("crew_depth_offset",0)==before.get_meta("crew_depth_offset",0),"Return cut retains exact depth "+entry.id)
		var duration:=0.0
		for ms in entry.frameDurationsMs:duration+=float(ms)*.001
		npc.preview_elapsed=duration+.00001
		var terminal:Texture2D=game.grid_view._get_branforth_frame_source(game)
		check(terminal.get_image().get_data()==player.frames["meal-acquire-south"][0].get_image().get_data(),"Return clamps to exact empty standing "+entry.id)
		controlled_cuts.append({"key":entry.id,"sourceIndex":source_index,"duration":duration,"firstExact":true,"lastExact":true})
	check(controlled_cuts.size()==44,"All44 source-index return variants dispatched")
	npc.preview_key=""

	var file:=FileAccess.open(OUT+"native-handoffs-candidate-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"foot":foot,"local":foot-center,"samples":samples,"controlledCuts":controlled_cuts,"frameCoverage":frames,"normalCompletion":normal_completion,"scope":"Candidate manifest and temporary CandidateJames presentation subclass, normal actual South chooser/in-room route/service and unchanged timer. Dedicated in-memory open prep counter at[0,126], North-only raised-backboard counters omitted. Registered open counter supports both service sides; no owner layout edit. Staged complete9second South meal/drink presentation via temporary CandidateJames subclass. Normal actual Life.next and supported chooser/route; all6phase textures and exact joins. Return variants are controlled drawer/source-index dispatch, NOT actual hazard/clearance decision, snapshot/Continue or normal-loader proof. Cup contact/body projection remains visual review pending. Source/contact review only; production controller/loader unchanged. No Continue or production selection claim."},"  "));file.close()
	if not FileAccess.file_exists(OUT+"native-handoffs-candidate.gd.uid"):
		var uid_file=FileAccess.open(OUT+"native-handoffs-candidate.gd.uid",FileAccess.WRITE);uid_file.store_line(ResourceUID.id_to_text(ResourceUID.create_id()));uid_file.close()
	print("JAMES SOUTH HANDOFFS CANDIDATE: ",checks," checks; ",failures," failures")
	quit(1 if failures else 0)
