extends SceneTree
const OUT := "res://character/james-console-water-turn-v1/"
var game
var checks := 0
var failures := 0
func check(ok: bool, message: String) -> void:
	checks += 1
	if not ok: failures += 1; push_error(message)
func _init() -> void: call_deferred("run")
func run() -> void:
	check("brine-james-native-" in OS.get_environment("APPDATA"), "Scratch profile")
	if failures: quit(2); return
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://james-space.meta";game.run_save_path="user://james-space.loop"
	game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
	root.add_child(game);current_scene=game
	while not game.startup_complete:await process_frame
	game.set_process(false);game.tick_timer.stop();game.paused=true;game.crew_comms.set_process(false);game.crew_comms.dismiss()
	var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={};store.defaults_path="res://rooms/full-wall-v1/default-layouts.json"
	for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
	game.test_walker_cell=Vector2i(-1,-1)
	var cell:=Vector2i(20,20);var center:Vector2=(Vector2(cell)+Vector2.ONE*.5)*384
	var npc=game.branforth_npc;var player=game.grid_view.branforth_player;var results:Array=[]
	player.load_manifest(OUT+"bare-manifest.json",true,false);player.load_equipment_manifest("diving-helmet",OUT+"helmet-manifest.json")
	for rotation in range(4):
		game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
		for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("life_support" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=rotation if offset==Vector2i.ZERO else 0;room.water_level=.95
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="flooded";npc.flood_speed=1.0;npc.stage="";npc.expedition.clear();npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
		var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(stations.size()==1,"One authored console")
		if stations.is_empty():continue
		var contact:Vector2=center+stations[0].point+Vector2(0,6)
		var lane:Vector2=center+Vector2(36.7,contact.y-center.y)
		var gate_id:int=npc.nearest_in_room(center+Vector2(16,128),cell,false)
		for mode in ["bare","helmet"]:
			npc.helmet_equipped=mode=="helmet";var gear:String="" if mode=="bare" else "diving-helmet"
			for offset in [Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
				npc.foot=center+Vector2(offset)*384;npc.direction={Vector2i.LEFT:"east",Vector2i.RIGHT:"west",Vector2i.UP:"south",Vector2i.DOWN:"north"}[offset]
				var start:int=npc.nearest_in_room(npc.foot,cell+offset,false)
				var route:PackedVector2Array=npc.route_between(start,gate_id,false,"east")
				var entry:Dictionary={"kind":"approach","rotation":rotation,"mode":mode,"from":str(offset),"rawPoints":route.size(),"gate":str(npc.graph.get_point_position(gate_id)-center)}
				if not route.is_empty():
					route.append(lane);route.append(contact)
					var planned:PackedVector2Array=npc._smooth_route(route,Vector2.INF,true)
					entry.plannedPoints=planned.size();entry.route=[]
					for point in planned:entry.route.append(str(point-center))
					if not planned.is_empty():entry.motion=walk_route(npc,player,planned,gear,center)
				results.append(entry)
			# Contact first facesNorth; the reverse must finish here before graph travel.
			for offset in [Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
				npc.foot=contact;npc.direction="west";npc.path.clear()
				var start:int=npc.nearest_in_room(center+Vector2(32,144),cell,false)
				var target:int=npc.nearest_in_room(center+Vector2(offset)*384,cell+offset,false)
				var route:PackedVector2Array=npc.route_between(start,target)
				var entry:Dictionary={"kind":"departureAfterStationaryNorthWest","rotation":rotation,"mode":mode,"to":str(offset),"rawPoints":route.size(),"join":str(npc.graph.get_point_position(start)-center)}
				if not route.is_empty():
					route.insert(0,lane)
					var planned:PackedVector2Array=npc._smooth_route(route,Vector2.INF,true)
					entry.plannedPoints=planned.size();entry.route=[]
					for point in planned:entry.route.append(str(point-center))
					if not planned.is_empty():entry.motion=walk_route(npc,player,planned,gear,center)
				results.append(entry)
	var file:=FileAccess.open(OUT+"egress-probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"results":results,"scope":"Scratch candidate manifests, actual James navigation and move plus normal grid player sampled at120Hz. Fine contact/lane supplied explicitly; exact turn envelope used only in scratch action gate. Diagnostics record canceled turns and body intersections rather than concealing them. No production route integration, safety update loop, console activity, save or owner acceptance."},"  "));file.close()
	print("JAMES CONSOLE EGRESS PROBE: ",checks," checks; ",failures," failures; ",results.size()," diagnostic routes")
	quit(1 if failures else 0)
func walk_route(npc,player,route:PackedVector2Array,gear:String,center:Vector2)->Dictionary:
	var before_profiles:Dictionary=npc.action_clearance.duplicate(true)
	npc.path=route; npc.goal="";npc.timer=0;npc.stage="";npc.state="walk";npc.activity="diagnostic route"
	player.motion.clear();player.current_key="";player.last_time=-1;player.current_equipment=gear
	game.visual_time_seconds=100
	game.grid_view._get_branforth_frame(game)
	var ticks:=0;var bad:Array=[];var canceled:Array=[];var turns:Array=[]
	while not npc.path.is_empty() and ticks<12000:
		var previous:Vector2=npc.foot;var incoming:String=npc.direction
		npc.move(1.0/120);ticks+=1;game.visual_time_seconds=100+float(ticks)/120
		var key:String="swim-turn-"+incoming+"-"+npc.direction
		if incoming!=npc.direction:
			turns.append({"key":key,"point":str(npc.foot-center)})
			var extent:Array=player.clip_extent(key,gear)
			if not extent.is_empty():
				npc.action_pose_clear("transition")
				npc.action_clearance["bare" if gear.is_empty() else "helmet"]["transition-"+npc.direction]=extent
		var texture:Texture2D=game.grid_view._get_branforth_frame(game)
		if incoming!=npc.direction and player.motion.get("clip","")!=key:canceled.append({"key":key,"point":str(npc.foot-center)})
		if texture!=null:
			var used:Rect2=texture.get_meta("crew_alpha_extent");var extent:Array=[used.position.x,used.position.y,used.end.x,used.end.y]
			if not npc.swim_segment_clear(previous,npc.foot,npc.direction,incoming,false,extent) and bad.size()<10:bad.append({"tick":ticks,"key":player.motion.get("clip",""),"point":str(npc.foot-center),"extent":extent})
	npc.action_clearance=before_profiles
	return {"ticks":ticks,"arrived":npc.path.is_empty() and npc.activity!="route obstructed","point":str(npc.foot-center),"direction":npc.direction,"bodyIntersections":bad,"canceledTurns":canceled,"turns":turns}
