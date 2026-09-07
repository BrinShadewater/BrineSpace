extends RefCounted
## Finite extraction targets. Decorative seabed sprites remain decorative.
const NAMES := {"mining":"Mineral Nodule Deposit", "salvage":"Service Scrap Pile"}
const LOADS := {"mining":{"metal":2}, "salvage":{"metal":1,"data":1}}
const WORK_SECONDS := 6.0
const CAPACITY := 12

static func seed_sites(rooms: Array, wrecks: Dictionary) -> Dictionary:
	var occupied := {}
	for room in rooms: occupied[room.pos] = true
	var result := {}
	# Fixed authored sites, avoiding immediate Core expansion and existing obstacles.
	var cells := [Vector2i(18,21),Vector2i(22,20),Vector2i(19,22),Vector2i(22,19),
		Vector2i(15,18),Vector2i(25,21),Vector2i(18,15),Vector2i(24,25),
		Vector2i(13,24),Vector2i(27,16),Vector2i(20,11),Vector2i(17,28),
		Vector2i(11,18),Vector2i(29,23),Vector2i(24,12),Vector2i(27,29)]
	for i in range(cells.size()):
		var cell: Vector2i = cells[i]
		if occupied.has(cell) or preload("res://scripts/wreck_field.gd").blocks(wrecks,cell): continue
		result[cell] = make_site("mining" if i%2==0 else "salvage")
	discover(result,rooms)
	return result

static func make_site(kind: String, units: int = CAPACITY) -> Dictionary:
	return {"kind":kind,"units":units,"capacity":units,"progress":0.0,"discovered":false,"active":true}

static func discover(sites: Dictionary, rooms: Array) -> void:
	for cell in sites:
		if sites[cell].discovered: continue
		for room in rooms:
			if Vector2(cell).distance_to(Vector2(room.pos)) <= 5.0:
				sites[cell].discovered = true
				break

static func blocks(sites: Dictionary, cell: Vector2i) -> bool:
	return sites.has(cell) and sites[cell].units > 0

static func valid(sites: Variant) -> bool:
	if not sites is Dictionary or sites.size()>1600: return false
	for cell in sites:
		if not cell is Vector2i or cell.x<0 or cell.y<0 or cell.x>=40 or cell.y>=40: return false
		var site = sites[cell]
		if not site is Dictionary or not NAMES.has(site.get("kind")): return false
		if not site.get("units") is int or not site.get("capacity") is int: return false
		if site.capacity<1 or site.capacity>1000 or site.units<0 or site.units>site.capacity: return false
		if not site.get("progress") is float or not is_finite(site.progress) or site.progress<0 or site.progress>=WORK_SECONDS: return false
		if not site.get("discovered") is bool or not site.get("active") is bool: return false
	return true
