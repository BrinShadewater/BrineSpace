extends SceneTree
## Two-room snapshot probe from V33; stationary peer, not a full traffic replay.
const Database=preload("res://scripts/room_database.gd")
class GeometryProvider extends Control:
	var views: Dictionary={}
	func bill_room_geometry(room: Dictionary,sides: Array) -> Dictionary:
		var view=views[room.id]
		view.configure_embedded(int(room.rotation),sides,false,0.0)
		return {"layout":view.layout.duplicate(true),"props":view.props.duplicate(true),"edges":view.edges.duplicate(true)}
func _init() -> void: call_deferred("run")
func run() -> void:
	var game=load("res://scripts/main.gd").new()
	var provider:=GeometryProvider.new()
	for info in [["crew_lounge",Vector2i(25,19),1],["battery_array",Vector2i(25,20),0]]:
		var room: Dictionary=Database.get_room(info[0]).duplicate(true)
		room.pos=info[1]
		room.rotation=info[2]
		game.occupied[info[1]]=room
		var view=load("res://rooms/production-ten/"+info[0]+"_view.gd").new()
		view.embedded=true
		root.add_child(view)
		provider.views[info[0]]=view
	game.grid_view=provider
	var npc=load("res://scripts/bill_npc.gd").new()
	npc.rebuild(game)
	var origin:=Vector2(9782.3583984375,7671.2490234375)
	var peer:=Vector2(9767.9814453125,7655.72900390625)
	var target:=Vector2(9792,7488)
	var records: Array=[]
	var failures:=0
	for offset in [Vector2.ZERO,Vector2(8,0),Vector2(-8,0),Vector2(0,8),Vector2(0,-8)]:
		npc.foot=origin+offset
		npc.avoidance_positions=PackedVector2Array([peer])
		npc.path=PackedVector2Array([target])
		var nearest: int=npc.nearest_in_room(npc.foot,npc.cell_at(npc.foot))
		var join_clear: bool=nearest>=0 and npc.crew_clear(npc.foot,npc.graph.get_point_position(nearest))
		var offset_safe: bool=npc.segment_clear(origin,npc.foot) and (offset==Vector2.ZERO or npc.crew_clear(origin,npc.foot))
		var success: bool=npc.detour_around_crew()
		records.append({"offset":str(offset),"standable":npc.can_stand(npc.foot),"reachable_offset":offset_safe,"nearest_join_crew_clear":join_clear,"detour":success,"route":str(npc.path)})
	for with_peer in [false,true]:
		npc.foot=origin
		npc.avoidance_positions=PackedVector2Array([peer]) if with_peer else PackedVector2Array()
		npc.path=PackedVector2Array([target])
		npc.traffic_wait=0
		npc.traffic_retry=0
		for step in range(100):
			if npc.path.is_empty(): break
			var before: Vector2=npc.foot
			npc.move(0.1)
			if not npc.can_stand(npc.foot) or before.distance_to(npc.foot)>4.601 or not npc.crew_clear(before,npc.foot) and before!=npc.foot: failures+=1
		if not npc.foot.is_equal_approx(target): failures+=1
		records.append({"stationary_peer":with_peer,"arrived":npc.foot.is_equal_approx(target),"end":str(npc.foot),"activity":npc.activity})
	print(JSON.stringify({"controller_sha256":FileAccess.get_sha256("res://scripts/bill_npc.gd"),"scope":"V33 two-room stationary-peer snapshot; not complete three-crew reproduction","records":records},"\t"))
	for view in provider.views.values(): view.free()
	provider.free()
	game.free()
	print("LOUNGE TRAFFIC PROGRESS: ",failures," failures")
	quit(1 if "--require-progress" in OS.get_cmdline_user_args() and failures>0 else 0)
