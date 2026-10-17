extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-east-cargo-heads-v3/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:
	print("JAMES WORKSHOP BOOT")
	call_deferred("run")
func endpoint(npc,desired: Vector2,cell: Vector2i,d: String) -> int:
	var best: int=-1;var distance: float=INF
	for node in npc.room_nodes.get(cell,[]):
		var at: Vector2=npc.graph.get_point_position(node)
		if not npc.swim_segment_clear(at,at,d,d,true):continue
		if not npc.swim_segment_clear(at,at,d,d,false,npc.action_clearance["helmet" if npc.helmet_equipped else "bare"]["transition-"+d]):continue
		if at.distance_squared_to(desired)<distance:best=node;distance=at.distance_squared_to(desired)
	return best
func capture(label: String,npc) -> String:
	var center: Vector2=npc.foot/384.0*game.get_cell_size()
	game.grid_scroll.scroll_horizontal=maxi(0,int(center.x-game.grid_scroll.size.x*.5))
	game.grid_scroll.scroll_vertical=maxi(0,int(center.y-game.grid_scroll.size.y*.5))
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var file: String=OUT+"arrival-captures/"+label+".png"
	check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
	check(crop.save_png(file)==OK,"Save route capture")
	if label.ends_with("-000"):
		var texture: Texture2D=game.grid_view._get_branforth_frame(game)
		var used: Rect2i=texture.get_image().get_used_rect();var sc: float=cell_size*.17/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot")
		var actor_world:=Rect2(center+(Vector2(used.position)-pivot)*sc,Vector2(used.size)*sc).grow(3)
		var actor_screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*actor_world
		var roi:=Rect2i(actor_screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size())))
		var before: PackedByteArray=screenshot.get_region(roi).get_data()
		npc.active=false;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
		var after: PackedByteArray=root.get_texture().get_image().get_region(roi).get_data();var differences:=0
		for i in range(mini(before.size(),after.size())):
			if absi(int(before[i])-int(after[i]))>=5:differences+=1
		check(differences>25,"Actor on/off render difference "+label)
		npc.active=true;game.grid_view.queue_redraw();await process_frame
	return file
func run() -> void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch user directory")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-workshop.meta";game.run_save_path="user://james-workshop.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	game.running=true;game.paused=false;game.Architects.advance_core(game,10)
	check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Actual core release supplies valid roster")
	game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();pass # Preserve normal architect/wreck registry for valid disk saves.
	for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room: Dictionary=game.RoomDatabaseScript.get_room("salvage_workshop" if delta==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=ORIGIN+delta;room.rotation=0;room.water_level=.95
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1) # Disable the idle fallback demonstrator too.
	check(not game.recovered_crew.is_empty(),"Normal recovered roster retained")
	var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
	npc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear();npc.movement_medium="flooded"
	var player=game.grid_view.branforth_player
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
	await process_frame;game._center_grid_on_station_now();await process_frame
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	var center: Vector2=(Vector2(ORIGIN)+Vector2.ONE*.5)*384.0

	for room in game.placed_rooms:room.water_level=0.0
	npc.movement_medium="dry"
	var stations:Array=npc.RoomActivity.stations(npc.geometry[ORIGIN])
	check(not stations.is_empty(),"Default workshop has real station")
	if stations.is_empty():quit(2);return
	var contact:Vector2=center+stations[0].point
	var facing:String=stations[0].facing
	var start:=Vector2.INF
	for node in npc.room_nodes.get(ORIGIN,[]):
		var at:Vector2=npc.graph.get_point_position(node)
		if at.distance_to(contact)<8 or at.distance_to(contact)>100:continue
		if npc.travel_segment_clear(at,contact,npc.travel_heading(at,contact,facing)):start=at;break
	check(start.is_finite(),"Collision-clear actual workshop approach")
	if not start.is_finite():quit(2);return
	for mode in ["bare","helmet"]:
		npc=game.branforth_npc;player=game.grid_view.branforth_player
		npc.helmet_equipped=mode=="helmet";npc.active=true;npc.dead=false;npc.expedition.clear();npc.stage="";npc.state="walk";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.timer=0;npc.needs.curiosity=90
		npc.foot=start;npc.direction=facing;npc.path=PackedVector2Array([contact]);npc.movement_medium="dry";npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		game.visual_time_seconds=100;game.paused=false;player.current_key="";player.motion.clear();player.last_time=-1
		var saved_stages:Dictionary={};var seen_stages:Dictionary={};var poses:Dictionary={};var previous_stage:="";var elapsed:=0.0;var captures:Array=[]
		for tick in range(2500):
			npc.update(game,.02);game.visual_time_seconds+=.02;elapsed+=.02
			var tex:Texture2D=game.grid_view._get_branforth_frame(game)
			check(tex!=null,"Actual workshop selected texture")
			if npc.stage!=previous_stage:
				print("JAMES WORKSHOP STAGE: ",mode," / ",npc.stage," / ",npc.direction," / ",npc.timer," / path",npc.path.size())
				previous_stage=npc.stage
			if npc.stage.begins_with("workshop_"):
				seen_stages[npc.stage]=true;poses[npc.animation_state()]=true
				check(npc.helmet_equipped==(mode=="helmet") and npc.goal=="curiosity","Workshop gear/goal retained")
			if npc.stage in ["workshop_pickup","workshop_carry","workshop_unload"] and not saved_stages.has(npc.stage):
				if npc.stage=="workshop_pickup" and npc.timer>.27:continue
				if npc.stage=="workshop_unload" and npc.timer>1.02:continue
				var stage:String=npc.stage;captures.append(await capture(mode+"-"+stage+"-000",npc));game.paused=true
				var actor:Dictionary=npc.snapshot();var playback:Dictionary=player.snapshot();var pixels:PackedByteArray=tex.get_image().get_data();var clock:float=game.visual_time_seconds
				var save=preload("res://scripts/run_save.gd");var data:Dictionary=save.capture(game);var problem:String=save.problem(data)
				check(problem.is_empty(),"Actual workshop checkpoint valid: "+problem)
				if not problem.is_empty():quit(2);return
				var path:="user://james-workshop.loop";check(save.write(game,path)==OK,"Workshop disk checkpoint writes");data=save.read(path)
				root.remove_child(game);game.queue_free();await process_frame
				game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true);game.meta.save_path="user://james-workshop.meta";game.run_save_path=path;game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
				root.add_child(game);current_scene=game
				while not game.startup_complete:await process_frame
				game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
				check(await save.restore_staged(game,data),"Workshop fresh-main disk Continue")
				game.run_save_path=path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false)
				npc=game.branforth_npc;player=game.grid_view.branforth_player
				check(npc.snapshot()==actor,"Workshop Continue actor exact");check(player.snapshot()==playback,"Workshop Continue playback exact");check(game.visual_time_seconds==clock and game.paused,"Workshop Continue pause/clock exact")
				check(game.grid_view._get_branforth_frame(game).get_image().get_data()==pixels,"Workshop Continue source exact")
				game._process(.5);check(npc.snapshot()==actor and game.visual_time_seconds==clock,"Paused workshop Continue stays fixed")
				game.paused=false;saved_stages[stage]=true
			if seen_stages.has("workshop_unload") and npc.stage.is_empty():break
		check(seen_stages.size()==5,"Actual inspect/work/pickup/carry/unload stages")
		check(saved_stages.size()==3,"Actual pickup/carry/unload fresh disk checkpoints")
		check(npc.goal.is_empty() and npc.needs.curiosity<35,"Workshop completes with normal curiosity relief")
		results.append({"mode":mode,"stages":seen_stages.keys(),"poses":poses.keys(),"savedStages":saved_stages.keys(),"elapsed":elapsed,"captures":captures})
		print("JAMES WORKSHOP CASE: ",mode," checks",checks," failures",failures)
	var report:=FileAccess.open(OUT+"native-workshop-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Default rotation0 workshop, prescribed collision-clear approach/curiosity goal, actual NPC.update/arrival/RoomActivity inspect-work-pickup-generated carrying route-unload; both initial gears; three ordinary disk/fresh-main Continues per gear. Main simulation otherwise paused/actor-stepped, not natural scheduling or full cardinal turns/interruptions."},"  "))
	if not FileAccess.file_exists(OUT+"native-workshop.gd.uid"):
		var uid:=FileAccess.open(OUT+"native-workshop.gd.uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
	print("JAMES WORKSHOP: ",checks,"checks; ",failures,"failures")
	quit(1 if failures else 0)
