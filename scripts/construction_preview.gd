extends RefCounted
## Advisory only. Never queues work, assigns an actor, or changes placement costs.
const Crew=preload("res://scripts/crew_construction.gd")
const Architects=preload("res://scripts/architects.gd")
const Routes=preload("res://scripts/drone_routes.gd")
const CACHE_MSEC:=250
var _key:Array=[]
var _checked_at:=-CACHE_MSEC
var _result:Dictionary={}

func inspect(game,room_id:String,cell:Vector2i,rotation:int)->Dictionary:
	var key:Array=[room_id,cell,rotation,game.hardware.power,game.hardware.doors,game.powered_room_cells.hash(),game.drone_fleet.route_blockers.hash()]
	for id in Architects.IDS:
		var actor=Architects.actor_for(game,id)
		key.append([Architects.present(game,id),actor.active,actor.dead,actor.signature,actor.cell_at(actor.foot),actor.movement_medium,actor.helmet_equipped,actor.fire_cells.hash()])
	for drone in game.drone_fleet.drones.values():
		key.append([drone.kind,drone.bootstrap,drone.home,drone.phase])
	var now:=Time.get_ticks_msec()
	if key==_key and now-_checked_at<CACHE_MSEC:return _result.duplicate()
	_key=key;_checked_at=now
	_result=_inspect(game,room_id,cell,rotation)
	return _result.duplicate()

func _inspect(game,room_id:String,cell:Vector2i,rotation:int)->Dictionary:
	var order:Dictionary={"id":room_id,"pos":cell,"rotation":rotation}
	# Busy, hungry or resting crew can still have a route. Do not confuse a
	# scheduling delay with isolation, or call advance() to claim hypothetical work.
	for id in Architects.IDS:
		var actor=Architects.actor_for(game,id)
		if not Architects.present(game,id) or not actor.active or actor.dead or actor.movement_medium!="dry" or not Crew.equipment_allowed(actor):continue
		if actor.fire_cells.has(actor.cell_at(actor.foot)):continue # Evacuation takes priority.
		if not Crew.approach(game,actor,order).is_empty():return {"warning":false,"text":""}
	for drone in game.drone_fleet.drones.values():
		if drone.kind!="construction" or drone.bootstrap or not game.hardware.power or game.hardware.doors or not game.powered_room_cells.has(drone.home):continue
		if not Routes.find_path(drone.home,cell,game.drone_fleet.route_blockers).is_empty():
			return {"warning":false,"text":"DRONE ACCESS // Powered construction drone can reach this site; work waits for its availability."}
	var message:="WARNING // NO SAFE CREW ROUTE\nChoose a reachable site or restore safe access. Placing still spends normal materials."
	if room_id=="desalination_unit":message+="\nEmergency Water must wait until a builder can reach and finish this unit."
	return {"warning":true,"text":message}
