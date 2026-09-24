extends RefCounted
## Test-player routing only. Production placement remains the final authority.
const Generator = preload("res://scripts/site_generator.gd")
const Wrecks = preload("res://scripts/wreck_field.gd")
const Sites = preload("res://scripts/harvest_sites.gd")

static func distances(target: Vector2i, occupied: Dictionary, wrecks: Dictionary, sites: Dictionary) -> Dictionary:
	var result := {}
	var queue: Array[Vector2i] = []
	for direction in [Vector2i.UP, Vector2i.DOWN]:
		var cell: Vector2i = target + direction
		if buildable(cell, occupied, wrecks, sites):
			result[cell] = 0
			queue.append(cell)
	var cursor := 0
	while cursor < queue.size():
		var cell := queue[cursor]
		cursor += 1
		for direction in Generator.DIRECTIONS:
			var next: Vector2i = cell + direction
			if result.has(next) or not buildable(next, occupied, wrecks, sites): continue
			result[next] = int(result[cell]) + 1
			queue.append(next)
	return result

static func buildable(cell: Vector2i, occupied: Dictionary, wrecks: Dictionary, sites: Dictionary) -> bool:
	return Generator.inside(cell) and not occupied.has(cell) and not Wrecks.blocks(wrecks, cell) and not Sites.blocks(sites, cell)

static func preserves_route(cell: Vector2i, exits: Array, field: Dictionary) -> bool:
	if not field.has(cell): return false
	if int(field[cell]) == 0: return true # Caller checks the chamber-facing door.
	for direction in exits:
		if int(field.get(cell + direction, 10000)) < int(field[cell]): return true
	return false
