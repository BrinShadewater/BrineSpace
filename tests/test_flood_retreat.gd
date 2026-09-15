extends SceneTree
const Safety=preload("res://scripts/flood_safety.gd")
const Architects=preload("res://scripts/architects.gd")
var failures := 0
var game
func check(ok: bool,message: String):
	if not ok: failures+=1; push_error(message)
func _init(): call_deferred("run")
func run():
	game=load("res://scenes/main.tscn").instantiate()
	game.meta.save_path="user://retreat-%d.meta" % OS.get_process_id()
	game.run_save_path=game.meta.save_path+".loop"
	root.add_child(game)
	current_scene=game
	game.set_process(false)
	game.tick_timer.stop()
	game.crew_comms.set_process(false)
	game.architect_run={"selected":"bill"}
	game.recovered_crew=[{"architect_id":"bill","alive":true}]
	game.hardware.doors=false
	game.hardware.pumps=false
	game.running=true
	game.paused=false
	game.resources.food=100
	game.resources.oxygen=100
	game.placed_rooms.clear()
	game.occupied.clear()
	game.powered_room_cells.clear()
	game.wrecks.clear()
	game.drone_fleet.orders.clear()
	game.drone_fleet.sites.clear()
	for x in range(19,23):
		var name: String="airlock" if x==19 else "corridor" if x==21 else "storage_bay"
		var room: Dictionary=game.RoomDatabaseScript.get_room(name).duplicate(true)
		room.pos=Vector2i(x,20)
		room.rotation=3 if name=="airlock" else 1 if name=="corridor" else 0
		room.water_level=0.95 if x==21 else 0
		game.placed_rooms.append(room)
		game.occupied[room.pos]=room
		game.powered_room_cells[room.pos]=true
	var actor=game.bill_npc
	game.veld_npc.active=false
	game.branforth_npc.active=false
	actor.active=true
	actor.helmet_equipped=true
	actor.tank_oxygen=6
	actor.movement_medium="flooded"
	actor.direction="west"
	actor.rebuild(game)
	var desired := (Vector2(21,20)+Vector2.ONE*0.5)*384+Vector2(-140,0)
	var best := INF
	for node in actor.room_nodes.get(Vector2i(21,20),[]):
		var point: Vector2=actor.graph.get_point_position(node)
		if actor.swim_segment_clear(point,point,"west") and point.distance_to(desired)<best:
			best=point.distance_to(desired)
			actor.foot=point
	check(best<60,"Swimmer starts near real exit doorway")
	actor.goal=""
	actor.path.clear()
	check(Safety.advance(game,actor,0.1) and actor.goal=="flood-retreat","Low-air crew selects physical escape route")
	check(actor.valid_snapshot(actor.snapshot()),"Retreat snapshot validates")
	for i in range(150):
		game._update_test_walker(0.1)
		if actor.cell_at(actor.foot)!=Vector2i(21,20): break
	check(not actor.dead and actor.cell_at(actor.foot)!=Vector2i(21,20),"Crew crosses doorway to refuge before oxygen expires")
	for i in range(800):
		game._update_test_walker(0.1)
		if actor.tank_oxygen>=59.9: break
	check(not actor.dead and actor.tank_oxygen>=59.9,"Retreated crew reaches real locker and refills")
	# A refuge that floods mid-route must be re-routed, not swum into.
	actor.goal="";actor.path.clear();actor.state="idle"
	for room in game.placed_rooms: room.water_level=0.95 if room.pos==Vector2i(21,20) else 0.0
	actor.cancel_helmet_action();actor.locker_request.clear()
	actor.movement_medium="flooded";actor.direction="west"
	actor.helmet_equipped=true;actor.tank_oxygen=4
	actor.set_meta("flood_safety_wait",0.0);actor.set_meta("flood_retreat_check",0.0);actor.set_meta("flood_blocked_warning",false)
	var desired2 := (Vector2(21,20)+Vector2.ONE*0.5)*384+Vector2(-140,0)
	var best2 := INF
	for node in actor.room_nodes.get(Vector2i(21,20),[]):
		var point: Vector2=actor.graph.get_point_position(node)
		if actor.swim_segment_clear(point,point,"west") and point.distance_to(desired2)<best2:
			best2=point.distance_to(desired2)
			actor.foot=point
	check(best2<60,"Second retreat repositions near the corridor exit doorway")
	check(Safety.advance(game,actor,0.1) and actor.goal=="flood-retreat","Second retreat engages")
	var refuge: Vector2i=actor.goal_cell
	game.occupied[refuge].water_level=0.95
	for i in range(4):Safety.advance(game,actor,0.6)
	check(actor.goal_cell!=refuge and float(game.occupied.get(actor.goal_cell,{}).get("water_level",1))<0.25,"Flooded refuge is re-routed mid-retreat")
	# Water can catch crew beside a doorway, where they stood but their swim outline does not
	# fit in any facing. They used to find no escape there and drown in place (owner playtest).
	actor.goal="";actor.path.clear();actor.state="idle"
	for room in game.placed_rooms: room.water_level=0.95 if room.pos in [Vector2i(20,20),Vector2i(21,20)] else 0.0
	actor.cancel_helmet_action();actor.locker_request.clear()
	actor.movement_medium="flooded";actor.direction="east"
	actor.helmet_equipped=false;actor.breath_oxygen=30.0
	actor.set_meta("flood_safety_wait",0.0);actor.set_meta("flood_retreat_check",0.0);actor.set_meta("flood_blocked_warning",false)
	var doorway := Vector2(21,20.5)*384
	var stuck_node := -1
	var nodes: Array=actor.room_nodes.get(Vector2i(20,20),[]).duplicate()
	nodes.sort_custom(func(a,b): return actor.graph.get_point_position(a).distance_to(doorway)<actor.graph.get_point_position(b).distance_to(doorway))
	for node in nodes:
		var point: Vector2=actor.graph.get_point_position(node)
		if not actor.can_stand(point): continue
		var fits := false
		for facing in ["east","south","west","north"]: fits=fits or actor.swim_segment_clear(point,point,facing,facing)
		if not fits:
			stuck_node=node
			break
	check(stuck_node>=0,"Fixture finds a standable doorway spot where no swim outline fits")
	if stuck_node>=0:
		actor.foot=actor.graph.get_point_position(stuck_node)
		var started := Time.get_ticks_msec()
		var route: Dictionary=Safety.escape_route(game,actor)
		check(not route.is_empty() and route.squeeze.is_finite(),"Escape squeezes out of the tight spot: "+str(route.keys()))
		check(Time.get_ticks_msec()-started<1000,"Escape search finishes promptly: %d ms" % (Time.get_ticks_msec()-started))
		var reached := false
		for i in range(900):
			game._update_test_walker(0.1)
			if actor.dead: break
			if float(game.occupied.get(actor.cell_at(actor.foot),{}).get("water_level",1))<0.25:
				reached=true
				break
		check(not actor.dead and reached,"Crew caught beside a flooded doorway reach a dry refuge alive: %s at %s, air %.1f" % [actor.activity,actor.cell_at(actor.foot),actor.breath_oxygen])
	# River floating in the doorway walled off the retreat: crew waited behind her in the water
	# until they drowned (owner playtest). Crew fleeing for air now pass companions.
	if not actor.dead:
		actor.goal="";actor.path.clear();actor.state="idle";actor.squeeze_point=Vector2.INF
		for room in game.placed_rooms: room.water_level=0.95 if room.pos.x>=21 else 0.0
		actor.cancel_helmet_action();actor.locker_request.clear()
		actor.movement_medium="flooded";actor.direction="west"
		actor.helmet_equipped=true;actor.tank_oxygen=6
		actor.set_meta("flood_safety_wait",0.0);actor.set_meta("flood_retreat_check",0.0);actor.set_meta("flood_blocked_warning",false)
		var best3 := INF
		for node in actor.room_nodes.get(Vector2i(21,20),[]):
			var point: Vector2=actor.graph.get_point_position(node)
			if actor.swim_segment_clear(point,point,"west") and point.distance_to(desired)<best3:
				best3=point.distance_to(desired)
				actor.foot=point
		var planned: Dictionary=Safety.escape_route(game,actor)
		var river=game.companion_actors["river"]
		river.room_cache=actor.room_cache
		river.rebuild(game)
		river.water.mode="float"
		var from: Vector2=actor.foot
		for point in planned.get("route",PackedVector2Array()):
			for i in range(ceili(from.distance_to(point)/4.0)+1):
				var sample: Vector2=from.move_toward(point,4.0*i)
				if not river.active and actor.cell_at(sample)!=Vector2i(21,20):
					river.foot=sample
					river.active=true
			from=point
		check(river.active and river.foot.distance_to(actor.foot)>30,"Fixture floats River in the doorway on the escape route")
		var escaped := false
		for i in range(300):
			game._update_test_walker(0.1)
			if actor.dead: break
			if float(game.occupied.get(actor.cell_at(actor.foot),{}).get("water_level",1))<0.25:
				escaped=true
				break
		check(not actor.dead and escaped,"Crew retreating for air pass River in a flooded doorway: %s at %s, tank %.1f" % [actor.activity,actor.cell_at(actor.foot),actor.tank_oxygen])
		river.active=false
	print("FLOOD RETREAT ","PASS" if failures==0 else "FAIL"," / ",actor.activity," / ",actor.tank_oxygen)
	quit(0 if failures==0 else 1)
