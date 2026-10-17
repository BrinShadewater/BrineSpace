extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-water-turn-family-v1/"
const ORIGIN := Vector2i(20,20)
var game
var failures:=0
var checks:=0
var results: Array=[]
func check(ok: bool,message: String) -> void:
	checks+=1
	if not ok:failures+=1;push_error(message)
func _init() -> void:call_deferred("run")
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
	var file: String=OUT+"installed-route-captures/"+label+".png"
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
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-water-turn-routes.meta";game.run_save_path="user://james-water-turn-routes.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
	for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room: Dictionary=game.RoomDatabaseScript.get_room("maintenance_bay" if delta==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=ORIGIN+delta;room.rotation=0;room.water_level=.95
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1) # Disable the idle fallback demonstrator too.
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":ORIGIN}])
	var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
	npc.swim_clearance.clear();npc.tread_clearance.clear();npc.action_clearance.clear();npc.movement_medium="flooded"
	npc.swim_segment_clear(npc.foot,npc.foot,"east");npc.action_pose_clear("transition")
	var expected_clearance:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance.json"))
	for field in ["swim","tread","actions"]:
		var selected:Dictionary=npc.swim_clearance if field=="swim" else (npc.tread_clearance if field=="tread" else npc.action_clearance)
		check(selected==expected_clearance[field],"Actual NPC lazy selected "+field+" clearance")
	var player=game.grid_view.branforth_player
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
	await process_frame;game._center_grid_on_station_now();await process_frame
	DirAccess.make_dir_recursive_absolute(OUT+"installed-route-captures")
	var center: Vector2=(Vector2(ORIGIN)+Vector2.ONE*.5)*384.0
	var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"bare-manifest.json"))
	var deltas:Dictionary={"east":Vector2.RIGHT,"south":Vector2.DOWN,"west":Vector2.LEFT,"north":Vector2.UP}
	for mode in ["bare","helmet"]:
		npc.helmet_equipped=mode=="helmet";npc.movement_medium="flooded"
		for entry in manifest.states:
			var key:String=entry.id
			var first:String=key.get_slice("-",2);var last:String=key.get_slice("-",3)
			var gear:String="" if mode=="bare" else "diving-helmet"
			var frames:Dictionary=player.frames if mode=="bare" else player.equipment_frames[gear]
			var row:Array=frames[key]
			var corner:=Vector2.INF;var start:=Vector2.INF;var finish:=Vector2.INF
			for node in npc.graph.get_point_ids():
				var at:Vector2=npc.graph.get_point_position(node)
				var a:Vector2=at-deltas[first]*80;var b:Vector2=at+deltas[last]*80
				if not npc.swim_segment_clear(a,at,first,first,true):continue
				if not npc.swim_segment_clear(at,b,last,last,true):continue
				if not npc.swim_segment_clear(at,b,last,last,false,npc.action_clearance[mode]["transition-"+last]):continue
				if not npc.swim_segment_clear(a,at,first,first,false,npc.action_clearance[mode]["transition-"+first]):continue
				corner=at;start=a;finish=b;break
			check(corner.is_finite(),"Clear authored two-leg water path "+mode+key)
			if not corner.is_finite():results.append({"mode":mode,"clip":key,"routeUnavailable":true});continue
			npc.foot=start;npc.path=PackedVector2Array([corner,finish]);npc.stage="";npc.goal="curiosity";npc.goal_cell=ORIGIN;npc.state="walk";npc.direction=first;npc.timer=100;npc.expedition.clear()
			player.current_key="";player.current_equipment=gear;player.motion.clear();player.last_time=-1;player.phase=0
			game.visual_time_seconds=100.0
			game.grid_view._get_branforth_frame(game)
			var captured:Dictionary={};var seen:Dictionary={};var captures:Array=[];var sampled:=0;var completed:=false;var entered:=false
			for tick in range(400):
				if not npc.path.is_empty():npc.move(.04)
				game.visual_time_seconds+=.04
				var tex:Texture2D=game.grid_view._get_branforth_frame(game)
				check(tex!=null,"Normal grid selected water texture "+key)
				if tex==null:break
				var active:String=player.motion.get("clip","")
				if active==key:
					entered=true
					var slot:int=row.find(tex)
					check(slot>=0,"Actual route turn selected staged pose "+key)
					seen[slot]=true
					var used:Rect2i=tex.get_image().get_used_rect();var sc:float=65.28/148.0
					var body:=Rect2(npc.foot+(Vector2(used.position)-Vector2(128,128))*sc,Vector2(used.size)*sc)
					var extent:Array=[body.position.x-npc.foot.x,body.position.y-npc.foot.y,body.end.x-npc.foot.x,body.end.y-npc.foot.y]
					check(npc.swim_segment_clear(npc.foot,npc.foot,npc.direction,npc.direction,false,extent),"Actual turn alpha bounds clear navigation "+mode+key+str(tick));sampled+=1
					if not captured.has(slot):
						captured[slot]=true;captures.append(await capture(mode+"-"+key+"-"+str(slot).pad_zeros(3),npc))
				elif entered:
					completed=true;break
			check(entered,"Requested turn exercised by actual NPC move "+mode+key)
			check(seen.size()==row.size(),"All authored route turn poses observed "+mode+key)
			check(completed,"Actual moving turn completes "+mode+key)
			results.append({"mode":mode,"clip":key,"entered":entered,"completed":completed,"seenSlots":seen.keys(),"captures":captures,"envelopeSamples":sampled,"start":str(start),"corner":str(corner),"finish":str(finish)})
	var file:=FileAccess.open(OUT+"installed-route-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"24 explicitly authored collision-checked two-leg in-room paths through real NPC move and normal grid, actual installed manifests and NPC lazy clearance; all quarter/reverse/half poses; not pathfinder-generated cross-room, exterior or traffic proof","results":results},"\t"));file.close()
	print("JAMES WATER TURN INSTALLED ROUTES: ",checks," checks; ",failures," failures; ",results.size()," installed two-leg paths")
	quit(1 if failures else 0)
