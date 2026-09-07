extends RefCounted
## Wrecks and rocks occupy placement cells but never join the operational room graph.
const DURATION := 18.0
const TYPES := ["engineering", "medical", "habitation", "hydroponics"]
const NAMES := {"engineering":"Engineering Wreck", "medical":"Medical Wreck", "habitation":"Habitation Wreck", "hydroponics":"Hydroponics Wreck", "basalt":"Basalt Outcrop", "cryo":"Derelict Cryo Ward"}
const YIELDS := {"engineering":12, "medical":8, "habitation":6, "hydroponics":10, "basalt":4}

static func initial() -> Dictionary:
	var result := {}
	var positions := [Vector2i(18,18),Vector2i(22,18),Vector2i(18,22),Vector2i(22,22)]
	for i in range(TYPES.size()):
		result[positions[i]] = {"kind":TYPES[i], "progress":0.0, "active":false, "cleared":false}
	# Connected shelves leave all four immediate core expansion cells open.
	for cell in [Vector2i(17,19),Vector2i(17,20),Vector2i(17,21),Vector2i(16,20),Vector2i(16,21),Vector2i(23,19),Vector2i(23,20),Vector2i(23,21),Vector2i(24,19),Vector2i(19,17),Vector2i(20,17),Vector2i(21,17),Vector2i(20,23),Vector2i(21,23),Vector2i(21,24)]:
		result[cell] = {"kind":"basalt", "progress":0.0, "active":false, "cleared":false}
	preload("res://scripts/cryo_recovery.gd").seed(result)
	return result

static func blocks(wrecks: Dictionary, cell: Vector2i) -> bool:
	return wrecks.has(cell) and not wrecks[cell].cleared

static func reachable(occupied: Dictionary, cell: Vector2i) -> bool:
	for offset in [Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
		if occupied.has(cell+offset):
			return true
	return false

static func busy(wrecks: Dictionary, except_cell: Vector2i) -> bool:
	for cell in wrecks:
		if cell != except_cell and wrecks[cell].active:
			return true
	return false

static func advance(wrecks: Dictionary, occupied: Dictionary, delta: float, drone_work: Variant = null) -> Array:
	var completed := []
	for cell in wrecks:
		var wreck: Dictionary = wrecks[cell]
		if wreck.cleared or not wreck.active or not reachable(occupied,cell):
			continue
		var work_delta: float = delta if drone_work == null or wreck.kind == "cryo" else float(drone_work.get(cell,0.0))
		wreck.progress = minf(DURATION,float(wreck.progress)+maxf(0.0,work_delta))
		if wreck.progress >= DURATION:
			wreck.cleared = true
			wreck.active = false
			completed.append(cell)
		break # One basic salvage rig; no parallel rewards from malformed state.
	return completed

static func valid(value: Variant, occupied: Dictionary) -> bool:
	if not value is Dictionary or value.size()>1600:
		return false
	var active_count := 0
	for cell in value:
		if not cell is Vector2i or cell.x<0 or cell.y<0 or cell.x>=40 or cell.y>=40:
			return false
		var w = value[cell]
		if not w is Dictionary or not NAMES.has(w.get("kind")):
			return false
		if not w.get("progress") is float or not is_finite(w.progress) or w.progress<0 or w.progress>DURATION:
			return false
		if not w.get("active") is bool or not w.get("cleared") is bool:
			return false
		if w.kind == "cryo" and not preload("res://scripts/cryo_recovery.gd").valid_ward(w):
			return false
		if w.cleared != (w.progress == DURATION) or (w.cleared and w.active):
			return false
		if not w.cleared and occupied.has(cell):
			return false
		active_count += int(w.active)
	return active_count<=1
