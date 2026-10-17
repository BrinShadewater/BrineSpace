extends SceneTree
const OUT := "res://character/james-console-water-exit-turn-v1/"
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
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
func run()->void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch profile")
	if failures:quit(2);return
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-workstation-routes.meta";game.run_save_path="user://james-workstation-routes.loop";game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	DirAccess.make_dir_recursive_absolute(OUT+"arrival-captures")
	game._set_grid_zoom(1.256,true,Vector2(.5125,.5125));game._refresh_all()
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":cell}])
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	player.load_manifest("res://character/james-console-water-turn-v1/bare-manifest.json",true,false);player.load_equipment_manifest("diving-helmet","res://character/james-console-water-turn-v1/helmet-manifest.json")
	player.load_manifest(OUT+"bare-manifest.json",true,false);player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json")
	for q in range(4):
		game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
		for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("life_support" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=q if offset==Vector2i.ZERO else 0;room.water_level=.95
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="flooded";npc.flood_speed=1;npc.stage="";npc.expedition.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(stations.size()==1,"Console fixture")
		if stations.is_empty():continue
		var contact:Vector2=center+stations[0].point+Vector2(0,6);var lane:Vector2=center+Vector2(36.7,contact.y-center.y)
		for mode in ["bare","helmet"]:
			npc.helmet_equipped=mode=="helmet";var gear:String="" if mode=="bare" else "diving-helmet";var captures:Array=[]
			npc.foot=center+Vector2(0,384);npc.direction="north";npc.goal="";npc.goal_cell=cell;npc.path.clear();npc.state="walk";npc.timer=0;npc.activity="staged console journey"
			player.motion.clear();player.current_key="";player.last_time=-1;player.current_equipment=gear;game.visual_time_seconds=100
			game.grid_view._get_branforth_frame(game)
			var start:int=npc.nearest_in_room(npc.foot,cell+Vector2i.DOWN,false);var gate:int=npc.nearest_in_room(center+Vector2(16,128),cell,false)
			var route:PackedVector2Array=npc.route_between(start,gate,false,"east");check(not route.is_empty(),"Actual approach graph route")
			if route.is_empty():continue
			route.append(lane);route.append(contact);npc.path=npc._smooth_route(route,Vector2.INF,true);check(not npc.path.is_empty(),"Heading-preserving fine connector")
			var approach_ticks:int=traverse(npc,player,gear)
			check(npc.foot.distance_to(contact)<.01 and npc.direction=="east","Actual move reaches console facingEast")
			if q==0:captures.append(await capture("journey-"+mode+"-approach",npc))
			npc.state="interact";npc.direction="north"
			await turn(npc,player,"swim-turn-east-north",gear,q==0,"journey-"+mode+"-entry")
			var fixed:Vector2=npc.foot
			for tick in range(720):
				game.visual_time_seconds+=1.0/120
				selected_clear(npc,game.grid_view._get_branforth_frame(game))
				check(npc.foot==fixed,"Stationary six-second flooded console dwell")
				if q==0 and tick==360:captures.append(await capture("journey-"+mode+"-console",npc))
			npc.direction="west"
			await turn(npc,player,"swim-turn-north-west",gear,q==0,"journey-"+mode+"-exit")
			check(npc.foot==fixed,"Departure quarter finishes before translating")
			start=npc.nearest_in_room(center+Vector2(32,144),cell,false)
			var target:int=npc.nearest_in_room(center+Vector2(0,384),cell+Vector2i.DOWN,false)
			route=npc.route_between(start,target);check(not route.is_empty(),"Actual departure graph route")
			route.insert(0,lane);npc.path=npc._smooth_route(route,Vector2.INF,true);check(not npc.path.is_empty(),"Fine egress connector")
			var departure_ticks:int=traverse(npc,player,gear)
			check(npc.foot.distance_to(center+Vector2(0,384))<.01,"Actual move returns to storage")
			if q==0:captures.append(await capture("journey-"+mode+"-returned",npc))
			results.append({"rotation":q,"mode":mode,"approachTicks":approach_ticks,"departureTicks":departure_ticks,"consoleDwellTicks":720,"contact":str(contact-center),"captures":captures})
	var file:=FileAccess.open(OUT+"native-journey-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Eight staged South-storage approach/console/return journeys with actual facing-aware navigation, smoothing, move and normal grid player at120Hz. Every selected pose/body clear, both stationary520ms compact quarters and six-second console dwell. Candidate manifests and exact turn gates injected in scratch; explicit fixture turn holds, NOT production update/safety/save/controller integration or owner acceptance."},"  "));file.close()
	print("JAMES CONSOLE STAGED JOURNEY: ",checks," checks; ",failures," failures; ",results.size()," actual move journeys")
	quit(1 if failures else 0)
func selected_clear(npc,texture:Texture2D)->void:
	check(texture!=null,"Native selected frame")
	if texture==null:return
	var used:Rect2=texture.get_meta("crew_alpha_extent");var extent:Array=[used.position.x,used.position.y,used.end.x,used.end.y]
	check(npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,false,extent),"Selected pose and full body clear actual geometry")
func gate_turn(npc,player,key:String,gear:String)->void:
	npc.action_pose_clear("transition")
	npc.action_clearance["bare" if gear.is_empty() else "helmet"]["transition-"+npc.direction]=player.clip_extent(key,gear)
func traverse(npc,player,gear:String)->int:
	var ticks:=0
	while not npc.path.is_empty() and ticks<12000:
		var previous:String=npc.direction;npc.move(1.0/120);game.visual_time_seconds+=1.0/120;ticks+=1
		var key:String="swim-turn-"+previous+"-"+npc.direction
		if previous!=npc.direction:gate_turn(npc,player,key,gear)
		selected_clear(npc,game.grid_view._get_branforth_frame(game))
		if previous!=npc.direction:check(player.motion.get("clip","")==key,"Route direction changes animate without cancellation")
	check(ticks<12000,"Finite traversal")
	return ticks
func turn(npc,player,key:String,gear:String,visible:bool,label:String)->void:
	gate_turn(npc,player,key,gear);var fixed:Vector2=npc.foot
	var start_time:float=game.visual_time_seconds
	var texture:Texture2D=game.grid_view._get_branforth_frame(game)
	check(player.motion.get("clip","")==key,"Stationary compact quarter starts")
	for tick in range(64):
		game.visual_time_seconds=start_time+float(tick)/120
		texture=game.grid_view._get_branforth_frame(game);selected_clear(npc,texture)
		check(npc.foot==fixed,"Quarter holds foot position")
		if tick<63:
			var expected:Texture2D=player.frame_at_elapsed(key,float(tick)/120,gear)
			check(texture.get_image().get_data()==expected.get_image().get_data(),"Normal player uses exact quarter clock")
		if visible and tick==30:await capture(label,npc)
	check(player.motion.get("clip","")=="","Finite quarter completes before next move")
