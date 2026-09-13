extends RefCounted
const Fire=preload("res://scripts/room_fire.gd")
const Architects=preload("res://scripts/architects.gd")
const Route=preload("res://scripts/hull_repair.gd")

static func release(actor) -> void:
	actor.goal=""
	actor.path.clear()
	actor.stage=""
	actor.state="idle"
	actor.timer=0.5

static func safe(room: Dictionary) -> bool:
	return Fire.fault(room) and not Fire.burning(room) and room.get("suspended",false) and float(room.get("water_level",0))<0.25

static func advance(game,actor,dt: float) -> bool:
	if dt<=0 or not game.running or game.paused: return false
	if actor.dead or not actor.active or not actor.expedition.is_empty(): return false
	if actor.goal=="electrical-repair" and (not game.occupied.has(actor.goal_cell) or not safe(game.occupied[actor.goal_cell])):
		release(actor)
		return true
	if actor.goal not in ["","maintenance","electrical-repair"] or actor.helmet_action_active() or not actor.locker_request.is_empty(): return false
	for room in game.placed_rooms:
		if not safe(room): continue
		if actor.goal=="electrical-repair" and actor.goal_cell!=room.pos: continue
		var claimed := false
		for id in Architects.IDS:
			if not Architects.present(game,id): continue
			var peer=Architects.actor_for(game,id)
			if peer!=actor and not peer.dead and peer.goal=="electrical-repair" and peer.goal_cell==room.pos: claimed=true
		if claimed: continue
		if actor.goal!="electrical-repair":
			var found := Route.approach(actor,room.pos)
			if found.is_empty(): continue
			actor.path=found.route
			actor.goal="electrical-repair"
			actor.goal_cell=room.pos
			actor.stage=""
			actor.timer=0
		if not actor.path.is_empty():
			actor.activity="heading to isolated electrical fault"
			actor.move(dt)
			return true
		# Revalidate the worksite after save/load or a changed route.
		var found := Route.approach(actor,room.pos)
		if found.is_empty(): release(actor); return true
		if actor.foot.distance_to(found.point)>1:
			actor.path=found.route
			return true
		actor.state="repair"
		actor.direction="north"
		actor.activity="repairing isolated wiring"
		room.electrical_repair_progress=minf(8,float(room.get("electrical_repair_progress",0))+dt)
		if room.electrical_repair_progress>=8:
			room.electrical_fault=false
			room.fire_heat=0.0
			room.electrical_repair_progress=0.0
			release(actor)
			actor.activity="electrical fault repaired"
			game._log("WIRING REPAIRED // %s. Room remains suspended. Resume when ready." % room.display_name,false)
			game._refresh_all()
		return true
	return false
