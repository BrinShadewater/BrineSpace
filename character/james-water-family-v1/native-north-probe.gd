extends SceneTree
## Candidate clips through real James navigation, move(), water selection and grid drawing.
const OUT := "res://character/james-water-family-v1/"
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
	game.grid_view.queue_redraw()
	await process_frame
	await RenderingServer.frame_post_draw
	var screenshot:=root.get_texture().get_image()
	var cell_size: float=game.get_cell_size()
	var world: Rect2=Rect2(npc.foot/384.0*cell_size-Vector2.ONE*cell_size*.55,Vector2.ONE*cell_size*1.1)
	var screen: Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world
	var crop:=screenshot.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,screenshot.get_size()))))
	var file: String=OUT+"route-captures/"+label+".png"
	check(crop.get_width()>0 and crop.get_height()>0,"Visible route capture "+label)
	check(crop.save_png(file)==OK,"Save route capture")
	return file
func run() -> void:
	check("brine-james-native-" in OS.get_environment("APPDATA"),"Scratch profile required")
	check(OS.get_user_data_dir().replace("\\","/").to_lower().begins_with(OS.get_environment("APPDATA").replace("\\","/").to_lower()+"/"),"Resolved scratch user directory")
	if failures:quit(2);return
	root.size=Vector2i(1600,900)
	game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://james-water-routes.meta";game.run_save_path="user://james-water-routes.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path=OUT+"no-layout-overrides.json"
	game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
	for delta in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		var room: Dictionary=game.RoomDatabaseScript.get_room("maintenance_bay" if delta==Vector2i.ZERO else "storage_bay").duplicate(true)
		room.pos=ORIGIN+delta;room.rotation=0;room.water_level=.95
		game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.recovered_crew.assign([{"architect_id":"branforth","alive":true,"id":"architect_branforth","name":"James","origin":ORIGIN}])
	var npc=game.branforth_npc;npc.rebuild(game);npc.active=true;npc.dead=false;npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
	var clearance: Dictionary=JSON.parse_string(FileAccess.get_file_as_string(OUT+"clearance.json"));npc.swim_clearance=clearance.swim;npc.tread_clearance=clearance.tread;npc.action_clearance=clearance.actions
	var player=game.grid_view.branforth_player;player.load_manifest(OUT+"bare-manifest.json",true);check(player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json"),"Candidate shared helmets")
	game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all();game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.9)
	await process_frame;game._center_grid_on_station_now();await process_frame
	DirAccess.make_dir_recursive_absolute(OUT+"route-captures")
	var center: Vector2=(Vector2(ORIGIN)+Vector2.ONE*.5)*384.0
	for mode in ["bare","helmet"]:
		npc.helmet_equipped=mode=="helmet";npc.movement_medium="flooded"
		for d in ["north"]:
			var step: Vector2i={"east":Vector2i.RIGHT,"south":Vector2i.DOWN,"west":Vector2i.LEFT,"north":Vector2i.UP}[d]
			var start:=endpoint(npc,center-Vector2(step)*80,ORIGIN,d)
			var target:=endpoint(npc,center+Vector2(step)*384,ORIGIN+step,d)
			check(start>=0 and target>=0,"Furnished endpoints "+mode+d)
			if start<0 or target<0:continue
			npc.foot=npc.graph.get_point_position(start);npc.path.clear();npc.stage="";npc.goal="";npc.state="idle";npc.direction=d;npc.timer=100;npc.expedition.clear()
			player.current_key="";player.current_equipment="diving-helmet" if npc.helmet_equipped else "";player.motion.clear();player.last_time=-1;player.phase=0
			game.visual_time_seconds=100.0
			check(npc.animation_state()=="tread","Clear start selects tread "+d)
			game.grid_view._get_branforth_frame(game)
			var route: PackedVector2Array=npc.smooth_route(npc.route_between(start,target));check(not route.is_empty(),"Real collision-aware route "+mode+d)
			if route.is_empty():
				var old_swim: Dictionary=npc.swim_clearance;var old_tread: Dictionary=npc.tread_clearance
				var retained: Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/chief-engineer-branforth-v2/clearance.json"))
				npc.swim_clearance=retained.swim;npc.tread_clearance=retained.tread
				npc.swim_link_cache.clear();npc.swim_reach_scope=null
				var old_route: PackedVector2Array=npc.route_between(start,target)
				npc.swim_clearance=old_swim;npc.tread_clearance=old_tread
				npc.swim_link_cache.clear();npc.swim_reach_scope=null
				print("JAMES ROUTE DIAGNOSTIC ",mode,d," start=",npc.foot," target=",npc.graph.get_point_position(target)," retainedRoute=",old_route.size()," extent=",npc.swim_clearance[mode][d])
				results.append({"mode":mode,"initialFacing":d,"routeUnavailable":true,"retainedRoutePoints":old_route.size(),"start":str(npc.foot),"target":str(npc.graph.get_point_position(target))})
				continue
			var route_points: int=route.size()
			npc.path=route.duplicate();npc.goal="curiosity";npc.goal_cell=ORIGIN+step;npc.state="walk"
			var captures: Array=[];var clips: Dictionary={};var ticks: int=0;var pixels_checked: int=0;var overlaps: Array=[]
			for tick in range(600):
				var moving: bool=not npc.path.is_empty()
				if moving:npc.move(.06)
				else:npc.state="idle"
				game.visual_time_seconds+=.06
				var texture: Texture2D=game.grid_view._get_branforth_frame(game)
				check(texture!=null,"Normal grid water texture")
				var clip: String=player.motion.get("clip","")
				if clip.is_empty():clip=player.current_key
				clips[clip]=true
				if tick<11 or tick%30==0 or not moving:
					captures.append(await capture(mode+"-"+d+"-"+str(tick).pad_zeros(3),npc))
					# Conservative selected bounding envelope checked at actual foot along route.
					var image:=texture.get_image();var rect: Rect2i=image.get_used_rect();var sc: float=65.28/float(texture.get_meta("crew_standing_height"));var pivot: Vector2=texture.get_meta("crew_pivot");var body:=Rect2(npc.foot+(Vector2(rect.position)-pivot)*sc,Vector2(rect.size)*sc)
					for cell in npc.geometry:
						var origin: Vector2=(Vector2(cell)+Vector2.ONE*.5)*384.0
						for prop in npc.geometry[cell].get("props",[]):
							var obstacle: Rect2=Rect2(prop.rect.position+origin,prop.rect.size)
							if body.intersects(obstacle):overlaps.append({"tick":tick,"cell":str(cell),"prop":prop.get("id","unknown"),"clip":clip})
					pixels_checked+=1
				if not moving and str(player.motion.get("clip","")).is_empty():break
				ticks+=1
			var arrived: bool=npc.foot.distance_to(npc.graph.get_point_position(target))<.01
			check(arrived,"Cross-room route completes "+mode+d);check(npc.animation_state()=="tread","Clear destination treads "+mode+d)
			check(overlaps.is_empty(),"No selected envelope/prop overlap "+mode+d)
			results.append({"mode":mode,"initialFacing":d,"routePoints":route_points,"ticks":ticks,"arrived":arrived,"seenClips":clips.keys(),"captures":captures,"envelopeSamples":pixels_checked,"propEnvelopeOverlaps":overlaps})
	var report:=FileAccess.open(OUT+"north-probe-evidence.json",FileAccess.WRITE);report.store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"Staged candidates on real James furnished five-room navigation and normal grid selection/render; one cross-room route per initial facing/mode; not exterior/concurrent traffic","results":results},"\t"));report.close()
	print("JAMES WATER ROUTES: ",checks," checks; ",failures," failures; ",results.size()," staged real routes")
	quit(1 if failures else 0)
