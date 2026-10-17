extends SceneTree
const OUT := "res://character/james-workstation-arrival-polish-v1/"
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
	for rotation in range(4):
		game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear()
		for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
			var room:Dictionary=game.RoomDatabaseScript.get_room("life_support" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
			room.pos=cell+offset;room.rotation=rotation if offset==Vector2i.ZERO else 0;room.water_level=.95
			game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
		npc.rebuild(game);npc.active=true;npc.dead=false;npc.movement_medium="flooded";npc.direction="north"
		var stations:Array=npc.RoomActivity.stations(npc.geometry[cell]);check(stations.size()==1,"One authored console")
		if stations.is_empty():continue
		var station:Dictionary=stations[0];var data:Dictionary=npc.geometry[cell]
		for mode in ["bare","helmet"]:
			npc.helmet_equipped=mode=="helmet";var gear:String="" if mode=="bare" else "diving-helmet"
			npc.swim_segment_clear(center,center,"north","north")
			var original:Array=npc.swim_clearance[mode].north.duplicate();var kinds:Dictionary={"full_swim":original,"selected_tread":player.clip_extent("tread-north",gear)}
			var row:Array=player.frames["swim-north"] if gear.is_empty() else player.equipment_frames[gear]["swim-north"]
			var rect:Rect2=row[0].get_meta("crew_alpha_extent")
			kinds.selected_swim_neutral=[rect.position.x,rect.position.y,rect.end.x,rect.end.y]
			for incoming in ["east","west","south"]:
				var key:String="swim-turn-"+incoming+"-north";var extent:Array=player.clip_extent(key,gear);var outgoing:Array=npc.swim_clearance[mode][incoming]
				for axis in range(2):
					extent[axis]=minf(extent[axis],minf(original[axis],outgoing[axis]));extent[axis+2]=maxf(extent[axis+2],maxf(original[axis+2],outgoing[axis+2]))
				kinds[key]=extent
			var by_kind:Dictionary={}
			for kind in kinds:
				var extent:Array=kinds[kind];npc.swim_clearance[mode].north=extent
				var clear:Array=[]
				for y in range(-36,37,2):
					for x in range(-36,37,2):
						var point:Vector2=center+station.point+Vector2(x,y)
						if Vector2(x,y).length()>36 or not npc.can_stand(point):continue
						if npc.swim_segment_clear(point,point,"north","north"):
							clear.append({"x":point.x-center.x,"y":point.y-center.y,"stationDistance":Vector2(x,y).length()})
				by_kind[kind]={"extent":extent,"safePoints":clear}
			npc.swim_clearance[mode].north=original
			var contact:Vector2=center+station.point;var body:=Rect2(contact+Vector2(original[0],original[1]),Vector2(original[2]-original[0],original[3]-original[1]));var hits:Array=[]
			for blocker in data.get("swim_blockers",data.blockers):
				var obstacle:Rect2=blocker.grow(-maxf(0.0,float(data.get("blocker_padding",0.0))-2))
				if body.intersects(Rect2(obstacle.position+center,obstacle.size),true):hits.append({"x":obstacle.position.x,"y":obstacle.position.y,"width":obstacle.size.x,"height":obstacle.size.y})
			results.append({"rotation":rotation,"mode":mode,"station":str(station.point),"frontContactBlockers":hits,"kinds":by_kind})
	var file:=FileAccess.open(OUT+"space-probe-evidence.json",FileAccess.WRITE);file.store_string(JSON.stringify({"results":results,"scope":"Diagnostic only: actual James full swim vs intact selected neutral/tread footprints at2-unit samples within unchanged36-unit console service radius. Profiles temporarily replaced only in this scratch probe, not installed. No approach/journey or new pose acceptance."},"  "));file.close()
	print("JAMES SPACE PROBE: ",checks," checks; ",failures," failures; ",results.size()," geometry samples")
	quit(1 if failures else 0)
