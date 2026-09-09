extends RefCounted
## Fractions of a compartment, per simulation second. Closed bulkheads seal water.
const Architects = preload("res://scripts/architects.gd")
const Service = preload("res://scripts/airlock_service.gd")
const MEDIUM := 0.25
const HIGH := 0.55
const CRITICAL := 0.85
const STARVATION_SECONDS := 90.0

static func level(room: Dictionary) -> float:
	return float(room.get("water_level", 1.0 if room.get("flooded",false) else 0.0))

static func stage(water: float) -> String:
	if water >= CRITICAL: return "CRITICAL"
	if water >= HIGH: return "HIGH / SWIMMING"
	if water >= MEDIUM: return "MEDIUM / WADING"
	return "LOW" if water > 0.001 else "DRY"

static func advance(game, delta: float) -> void:
	if not is_finite(delta) or delta <= 0 or not game.running or game.paused: return
	# Bounded steps keep transfers conservative and independent of room iteration order.
	var remaining := delta
	while remaining > 0.00001:
		var dt := minf(remaining,0.1)
		step_water(game,dt)
		for id in Architects.IDS:
			var actor = Architects.actor_for(game,id)
			if Architects.present(game,id) and actor.active and not actor.dead:
				step_crew(game,actor,id,dt)
		remaining -= dt

static func step_water(game, dt: float) -> void:
	# Resolve external sources/sinks first. A pump cannot drain borrowed water,
	# and a saturated leak cannot cancel water leaving through a doorway.
	var levels := {}
	var changes := {}
	var pumps: bool = game.hardware.power and game.hardware.pumps
	for room in game.placed_rooms:
		var leak := float(room.get("hull_crack",0.0))*0.04
		if room.get("flooded",false) and room.has("branch_owner"): leak += 0.04
		var pump := 0.008 if pumps and game.powered_room_cells.has(room.pos) and not room.get("suspended",false) else 0.0
		levels[room.pos] = clampf(level(room)+(leak-pump)*dt,0,1)
		changes[room.pos] = 0.0
	for pair in connected_pairs(game):
		var cell: Vector2i=pair[0]
		var next: Vector2i=pair[1]
		var difference: float=levels[cell]-levels[next]
		if is_zero_approx(difference): continue
		if game.occupied[cell].get("isolated",false) or game.occupied[next].get("isolated",false): continue
		var aperture := clampf(float(game.grid_view._door_frame_for_pair(game,cell,next))/float(game.grid_view.DOOR_OPEN_FRAMES-1),0,1)
		var flow := difference*0.18*aperture*dt
		changes[cell] -= flow
		changes[next] += flow
	for room in game.placed_rooms:
		room.water_level = clampf(float(levels[room.pos])+float(changes[room.pos]),0,1)

static func connected_pairs(game) -> Array:
	var signature := []
	for room in game.placed_rooms:
		signature.append([room.pos,room.id,room.get("rotation",0),room.get("branch_owner",Vector2i(-1,-1))])
	var key := hash(signature)
	if game.grid_view.get_meta("flood_topology",-1)==key:
		return game.grid_view.get_meta("flood_pairs",[])
	var pairs := []
	for room in game.placed_rooms:
		for offset in [Vector2i.RIGHT,Vector2i.DOWN]:
			var next: Vector2i=room.pos+offset
			if game.occupied.has(next) and game._placed_rooms_connected(room,game.occupied[next],offset): pairs.append([room.pos,next])
	game.grid_view.set_meta("flood_topology",key)
	game.grid_view.set_meta("flood_pairs",pairs)
	return pairs

static func step_crew(game, actor, id: String, dt: float) -> void:
	var cell: Vector2i = actor.cell_at(actor.foot)
	var water := level(game.occupied.get(cell,{}))
	var exterior: bool = actor.movement_medium == "exterior" or not game.occupied.has(cell)
	if actor.expedition.is_empty() and not exterior:
		if water >= HIGH:
			actor.cancel_helmet_action()
			if not actor.locker_request.is_empty():
				actor.goal=""
				actor.path.clear()
				actor.state="idle"
			actor.locker_request.clear()
		actor.movement_medium = "flooded" if water >= HIGH else "dry"
	elif not actor.expedition.is_empty() and actor.expedition.phase in ["pressurize","drain"]:
		water = maxf(water,preload("res://scripts/airlock_cycle.gd").pose(game.occupied.get(actor.expedition.home,{})).water)
		exterior=false
		actor.movement_medium="flooded" if water>=HIGH else "dry"
	actor.flood_speed = 0.55 if water >= HIGH else (0.65 if water >= MEDIUM else 1.0)
	if not actor.needs_air():
		actor.helmet_equipped=false
		actor.air_recovery=0.0;actor.air_was_low=false
		actor.drain_battery(dt)
	else:
		var unsafe_air: bool = exterior or water >= CRITICAL or int(game.resources.oxygen)<=0
		if exterior and not actor.helmet_equipped:
			actor.movement_medium="exterior"
			kill(game,actor,id,"unprotected exterior exposure")
			return
		actor.air_recovery=maxf(0,actor.air_recovery-dt)
		if unsafe_air:
			if (actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen)<=(12 if actor.helmet_equipped else 5): actor.air_was_low=true
			if actor.helmet_equipped: actor.tank_oxygen = maxf(0,actor.tank_oxygen-dt)
			else: actor.breath_oxygen = maxf(0,actor.breath_oxygen-dt)
			if (actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen) <= 0.00001:
				kill(game,actor,id,"oxygen exhausted")
				return
		else:
			if actor.air_was_low: actor.air_recovery=3.0;actor.air_was_low=false
			actor.breath_oxygen = 15.0
			if actor.helmet_equipped and Service.ready(game,cell):
				var locker := Service.locker(game,cell)
				if not locker.is_empty() and actor.foot.distance_to(locker.interaction_point)<=12:
					actor.tank_oxygen = minf(60,actor.tank_oxygen+dt*12)
	actor.starvation = minf(STARVATION_SECONDS,actor.starvation+dt) if int(game.resources.food)<=0 else maxf(0,actor.starvation-dt*2)
	if actor.starvation >= STARVATION_SECONDS: kill(game,actor,id,"starvation")

static func kill(game,actor,id: String,cause: String) -> void:
	actor.die()
	game.crew_count = maxi(0,game.crew_count-1)
	for member in game.recovered_crew:
		if member.get("architect_id","")==id: member.alive=false
	game._log("%s lost: %s. The station keeps count." % [Architects.NAMES[id],cause],true)
	game._check_fail_conditions()

static func inspector(game,room: Dictionary) -> String:
	var text := "WATER %d%% // %s" % [roundi(level(room)*100),stage(level(room))]
	if level(room)>0 or float(room.get("hull_crack",0))>0:
		text += "\nHull crack: %d%% severity. Pumps drain 0.8%%/s when powered." % roundi(float(room.get("hull_crack",0))*100)
	if float(room.get("hull_crack",0))>0:
		var repairs = preload("res://scripts/hull_repair.gd")
		var index: int=repairs.variant(room)
		text += "\n%s / %.1f%% water per second" % [repairs.NAMES[index],float(room.hull_crack)*4]
		if room.has("leak_repair"):
			text += "\nRepair / %d%% / Metal allocated" % roundi(float(room.leak_repair.progress)/float(room.leak_repair.duration)*100)
			text += "\n"+str(room.leak_repair.get("status","Waiting for crew"))
			var refund := int(floor(float(room.leak_repair.cost)*(1-float(room.leak_repair.progress)/float(room.leak_repair.duration))))
			text += "\n[url=floodcancel:%d:%d]Cancel / return %d Metal[/url]" % [room.pos.x,room.pos.y,refund]
			for id in Architects.IDS:
				if Architects.present(game,id): text += "\n[url=floodassign:%d:%d:%s]Assign %s[/url]" % [room.pos.x,room.pos.y,id,Architects.NAMES[id]]
		else:
			text += "\n[url=floodrepair:%d:%d]Send crew to weld — %d Metal / %.0fs work[/url]" % [room.pos.x,room.pos.y,repairs.COSTS[index],repairs.SECONDS[index]]

	for id in Architects.IDS:
		var actor = Architects.actor_for(game,id)
		if not actor.active or actor.dead or actor.cell_at(actor.foot)!=room.pos: continue
		text += "\nMarsh // "+actor.battery_status() if not actor.needs_air() else "\n%s // %s %.0fs" % [Architects.NAMES[id],"TANK" if actor.helmet_equipped else "BREATH",actor.tank_oxygen if actor.helmet_equipped else actor.breath_oxygen]
		if actor.starvation>0: text += " / %s %.0fs" % ["STARVING" if int(game.resources.food)<=0 else "RECOVERING",STARVATION_SECONDS-actor.starvation]
	return text

static func valid_rooms(rooms: Array) -> bool:
	for room in rooms:
		if room.has("leak_repair") and not preload("res://scripts/hull_repair.gd").valid(room.leak_repair): return false
		for key in ["water_level","hull_crack"]:
			if not room.has(key): continue
			if not (room[key] is float or room[key] is int) or not is_finite(float(room[key])) or room[key]<0 or room[key]>1: return false
	return true

static func draw(canvas,game,rooms: Array,size: float) -> void:
	preload("res://scripts/flood_visuals.gd").draw_front(canvas,game,rooms,size)
