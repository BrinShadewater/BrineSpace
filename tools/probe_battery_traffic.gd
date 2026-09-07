extends SceneTree
## Recorded Battery Array snapshot; stationary Veld only, not a full tour replay.
const Database=preload("res://scripts/room_database.gd")
const Provider=preload("res://tools/probe_lounge_traffic.gd").GeometryProvider
func _init() -> void: call_deferred("run")
func run() -> void:
	var game=load("res://scripts/main.gd").new()
	var provider:=Provider.new()
	var view=load("res://rooms/production-ten/battery_array_view.gd").new()
	view.embedded=true
	root.add_child(view)
	provider.views["battery_array"]=view
	for cell in [Vector2i(24,20),Vector2i(25,20)]:
		var room: Dictionary=Database.get_room("battery_array").duplicate(true)
		room.pos=cell
		room.rotation=0
		game.occupied[cell]=room
	game.grid_view=provider
	var npc=load("res://tests/traced_bill_npc.gd").new()
	npc.rebuild(game)
	var origin:=Vector2(9614.982421875,7872)
	var peer:=Vector2(9635.5791015625,7878.26123046875)
	var destination:=Vector2(9792,7872)
	npc.foot=origin
	npc.avoidance_positions=PackedVector2Array([peer])
	var target: int=npc.nearest_in_room(destination,npc.cell_at(destination))
	var joins: Array=[]
	for id in npc.room_nodes[npc.cell_at(origin)]:
		var point: Vector2=npc.graph.get_point_position(id)
		if not npc.segment_clear(origin,point) or not npc.crew_clear(origin,point): continue
		var disabled: Array=[]
		for other in npc.graph.get_point_ids():
			if other!=id and npc.graph.get_point_position(other).distance_to(peer)<32:
				npc.graph.set_point_disabled(other,true)
				disabled.append(other)
		var path: PackedVector2Array=npc.graph.get_point_path(id,target)
		for other in disabled: npc.graph.set_point_disabled(other,false)
		var safe:=not path.is_empty()
		var previous:=origin
		for step in path:
			safe=safe and npc.segment_clear(previous,step) and npc.crew_clear(previous,step)
			previous=step
		joins.append({"id":id,"point":str(point),"distance":origin.distance_to(point),"route_nodes":path.size(),"safe_route":safe})
	joins.sort_custom(func(a,b): return a.distance<b.distance)
	var cases: Array=[]
	for with_peer in [false,true]:
		npc.foot=origin
		npc.avoidance_positions=PackedVector2Array([peer]) if with_peer else PackedVector2Array()
		npc.path=PackedVector2Array([destination])
		npc.traffic_wait=0
		npc.traffic_retry=0
		var violations:=0
		for tick in range(500):
			if npc.path.is_empty(): break
			var before: Vector2=npc.foot
			npc.move(0.1)
			if not npc.can_stand(npc.foot) or npc.traveled_distance()>4.601 or not npc.traveled_clear(): violations+=1
			var previous:=before
			for traveled in npc.traveled_points:
				if previous!=traveled and not npc.crew_clear(previous,traveled): violations+=1
				previous=traveled
		cases.append({"stationary_peer":with_peer,"arrived":npc.foot.is_equal_approx(destination),"end":str(npc.foot),"activity":npc.activity,"violations":violations})
	print(JSON.stringify({"scope":"Two adjacent Battery Arrays, recorded Bill/Veld positions, stationary peer; third crew and full station not reproduced","controller_sha256":FileAccess.get_sha256("res://scripts/bill_npc.gd"),"joins":joins,"cases":cases},"\t"))
	view.free()
	provider.free()
	game.free()
	var failures:=0
	for record in cases:
		if not record.arrived or record.violations>0: failures+=1
	print("BATTERY TRAFFIC PROGRESS: ",failures," failed cases")
	quit(1 if "--require-progress" in OS.get_cmdline_user_args() and failures>0 else 0)
