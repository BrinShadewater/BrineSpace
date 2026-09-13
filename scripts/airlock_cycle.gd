extends RefCounted
## Door apertures are derived from one phase, never independent mutable flags.
const DURATIONS={"sealing_inner":1.0,"flooding":4.0,"equalizing":2.0,"opening_outer":1.0,"sealing_outer":1.0,"sealing_departed":1.0,"draining":4.0,"depressurizing":2.0,"opening_inner":1.0}
const NEXT={"sealing_inner":"flooding","flooding":"equalizing","equalizing":"opening_outer","opening_outer":"exterior","sealing_outer":"draining","sealing_departed":"sealed_exterior","draining":"depressurizing","depressurizing":"opening_inner","opening_inner":"dry"}
const LABELS={"dry":"DRY / INNER DOOR OPEN","sealing_inner":"SEALING INNER DOOR","flooding":"FLOODING CHAMBER","equalizing":"EQUALIZING PRESSURE","opening_outer":"OPENING OUTER HATCH","exterior":"FLOODED / OUTER HATCH OPEN","sealing_outer":"SEALING OUTER HATCH","sealing_departed":"SEALING DEPARTURE HATCH","sealed_exterior":"FLOODED / AWAITING RETURN","draining":"DRAINING CHAMBER","depressurizing":"RESTORING STATION PRESSURE","opening_inner":"OPENING INNER DOOR"}

static func state(room: Dictionary) -> Dictionary:
	return room.get("airlock_cycle",{"phase":"dry","elapsed":0.0})

static func pose(room: Dictionary) -> Dictionary:
	var s:=state(room)
	var phase: String=s.phase
	var t:=clampf(float(s.elapsed)/float(DURATIONS.get(phase,1.0)),0,1)
	var inner:=1.0 if phase=="dry" else (1.0-t if phase=="sealing_inner" else (t if phase=="opening_inner" else 0.0))
	var outer:=1.0 if phase=="exterior" else (1.0-t if phase in ["sealing_outer","sealing_departed"] else (t if phase=="opening_outer" else 0.0))
	var water:=t if phase=="flooding" else (1.0-t if phase=="draining" else (1.0 if phase in ["equalizing","opening_outer","exterior","sealing_outer","sealing_departed","sealed_exterior"] else 0.0))
	var pressure:=t if phase=="equalizing" else (1.0-t if phase=="depressurizing" else (1.0 if phase in ["opening_outer","exterior","sealing_outer","sealing_departed","sealed_exterior","draining"] else 0.0))
	return {"inner":inner,"outer":outer,"water":water,"pressure":pressure,"phase":phase}

static func exterior_clear(game,room: Dictionary) -> bool:
	return exterior_problem(game,room).is_empty()

static func exterior_problem(game,room: Dictionary) -> String:
	var offset: Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][posmod(int(room.rotation),4)]
	var cell: Vector2i=room.pos+offset
	var reason: String=""
	if cell.x<0 or cell.y<0 or cell.x>=40 or cell.y>=40: reason="map edge"
	elif game.occupied.has(cell): reason="station room"
	elif preload("res://scripts/wreck_field.gd").blocks(game.wrecks,cell): reason="rock or wreck"
	elif game.drone_fleet.Sites.blocks(game.drone_fleet.sites,cell): reason="resource deposit"
	elif game.drone_fleet.reserved(cell): reason="queued construction"
	return "" if reason.is_empty() else "Exterior hatch blocked by %s at (%d, %d)."%[reason,cell.x,cell.y]

static func request(game,cell: Vector2i,outward: bool) -> bool:
	if not preload("res://scripts/airlock_service.gd").ready(game,cell): return false
	var room: Dictionary=game.occupied[cell]
	if not outward and state(room).phase=="sealed_exterior":
		room.airlock_cycle={"phase":"draining","elapsed":0.0}
		return true
	if state(room).phase!=("dry" if outward else "exterior"): return false
	if outward and not exterior_clear(game,room): return false
	room.airlock_cycle={"phase":"sealing_inner" if outward else "sealing_outer","elapsed":0.0}
	return true

static func seal_departure(game,cell: Vector2i) -> bool:
	if not preload("res://scripts/airlock_service.gd").ready(game,cell): return false
	var room: Dictionary=game.occupied[cell]
	if state(room).phase!="exterior": return false
	room.airlock_cycle={"phase":"sealing_departed","elapsed":0.0}
	return true

static func open_for_return(game,cell: Vector2i) -> bool:
	if not preload("res://scripts/airlock_service.gd").ready(game,cell): return false
	var room: Dictionary=game.occupied[cell]
	if state(room).phase!="sealed_exterior": return false
	room.airlock_cycle={"phase":"opening_outer","elapsed":0.0}
	return true

static func advance(game,delta: float) -> void:
	if not game.running or game.paused: return
	for room in game.placed_rooms:
		if room.id!="airlock" or not preload("res://scripts/airlock_service.gd").ready(game,room.pos): continue
		var s:=state(room).duplicate()
		var remaining:=maxf(0,delta)
		while DURATIONS.has(s.phase) and remaining>0:
			var step:=minf(remaining,float(DURATIONS[s.phase])-float(s.elapsed))
			s.elapsed+=step
			remaining-=step
			if s.elapsed>=float(DURATIONS[s.phase]):
				s={"phase":NEXT[s.phase],"elapsed":0.0}
		room.airlock_cycle=s

static func valid_rooms(rooms: Array) -> bool:
	for room in rooms:
		if not room is Dictionary: return false
		if not room.has("airlock_cycle"): continue # Older airlocks start dry.
		var s=room.airlock_cycle
		if room.get("id")!="airlock" or not s is Dictionary or not s.get("phase") is String: return false
		if not LABELS.has(s.phase) or not (s.get("elapsed") is float or s.get("elapsed") is int): return false
		var elapsed:=float(s.elapsed)
		if not is_finite(elapsed) or elapsed<0 or elapsed>float(DURATIONS.get(s.phase,0.0)): return false
	return true
