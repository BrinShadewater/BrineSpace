extends RefCounted
## Door apertures are derived from one phase, never independent mutable flags.
const DURATIONS={"sealing_inner":1.0,"flooding":4.0,"equalizing":2.0,"opening_outer":1.0,"sealing_outer":1.0,"draining":4.0,"depressurizing":2.0,"opening_inner":1.0}
const NEXT={"sealing_inner":"flooding","flooding":"equalizing","equalizing":"opening_outer","opening_outer":"exterior","sealing_outer":"draining","draining":"depressurizing","depressurizing":"opening_inner","opening_inner":"dry"}
const LABELS={"dry":"DRY / INNER DOOR OPEN","sealing_inner":"SEALING INNER DOOR","flooding":"FLOODING CHAMBER","equalizing":"EQUALIZING PRESSURE","opening_outer":"OPENING OUTER HATCH","exterior":"FLOODED / OUTER HATCH OPEN","sealing_outer":"SEALING OUTER HATCH","draining":"DRAINING CHAMBER","depressurizing":"RESTORING STATION PRESSURE","opening_inner":"OPENING INNER DOOR"}

static func state(room: Dictionary) -> Dictionary:
	return room.get("airlock_cycle",{"phase":"dry","elapsed":0.0})

static func pose(room: Dictionary) -> Dictionary:
	var s:=state(room)
	var phase: String=s.phase
	var t:=clampf(float(s.elapsed)/float(DURATIONS.get(phase,1.0)),0,1)
	var inner:=1.0 if phase=="dry" else (1.0-t if phase=="sealing_inner" else (t if phase=="opening_inner" else 0.0))
	var outer:=1.0 if phase=="exterior" else (1.0-t if phase=="sealing_outer" else (t if phase=="opening_outer" else 0.0))
	var water:=t if phase=="flooding" else (1.0-t if phase=="draining" else (1.0 if phase in ["equalizing","opening_outer","exterior","sealing_outer"] else 0.0))
	var pressure:=t if phase=="equalizing" else (1.0-t if phase=="depressurizing" else (1.0 if phase in ["opening_outer","exterior","sealing_outer","draining"] else 0.0))
	return {"inner":inner,"outer":outer,"water":water,"pressure":pressure,"phase":phase}

static func exterior_clear(game,room: Dictionary) -> bool:
	var offset: Vector2i=[Vector2i.UP,Vector2i.RIGHT,Vector2i.DOWN,Vector2i.LEFT][posmod(int(room.rotation),4)]
	var cell: Vector2i=room.pos+offset
	return cell.x>=0 and cell.y>=0 and cell.x<40 and cell.y<40 and not game.occupied.has(cell) and not game.wrecks.has(cell)

static func request(game,cell: Vector2i,outward: bool) -> bool:
	if not preload("res://scripts/airlock_service.gd").ready(game,cell): return false
	var room: Dictionary=game.occupied[cell]
	if state(room).phase!=("dry" if outward else "exterior"): return false
	if outward and not exterior_clear(game,room): return false
	room.airlock_cycle={"phase":"sealing_inner" if outward else "sealing_outer","elapsed":0.0}
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
