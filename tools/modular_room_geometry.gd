extends RefCounted
## Pilot-only structural contract. Units are world units, not texture pixels.
const CELL := 384.0
const WALL := 16.0
const OPENING := 72.0
const FLOOR_TILE := 48.0
const RADIUS := 7.0
const DIRS := [Vector2i.UP, Vector2i.RIGHT, Vector2i.DOWN, Vector2i.LEFT]
const MASKS := [[1, 2, 3], [0, 2], [0, 1, 2, 3], [2], [2, 3]] # kind 4: west/south corner
const RECIPE_PATH := "res://rooms/modular/nursery-room.json"
static var recipe: Dictionary = load_recipe()

static func load_recipe() -> Dictionary:
	var parsed: Variant = JSON.parse_string(FileAccess.get_file_as_string(RECIPE_PATH))
	return parsed if parsed is Dictionary else {}

static func recipe_errors(data: Dictionary) -> Array[String]:
	var errors: Array[String] = []
	if data.get("schema_version") != 1 or data.get("id") != "mycelium_nursery":
		errors.append("Unsupported or missing nursery recipe identity/version")
	var roots: Variant = data.get("asset_roots")
	if not roots is Array or roots.is_empty():
		errors.append("Asset roots must be a nonempty array")
	else:
		for art_root in roots:
			if not art_root is String or not art_root.begins_with("res://rooms/modular/") or not FileAccess.file_exists(art_root + "registration.json"):
				errors.append("Missing or invalid asset registration root")
	var doors: Variant = data.get("doors")
	if not doors is Array or doors.is_empty():
		errors.append("Doors must be a nonempty array")
	else:
		var seen_doors := {}
		for side in doors:
			if not (side is float or side is int) or side != int(side) or side < 0 or side > 3 or seen_doors.has(side):
				errors.append("Door sides must be unique integers 0..3")
			seen_doors[side] = true
	var entries: Variant = data.get("props")
	if not entries is Array or entries.is_empty():
		errors.append("Props must be a nonempty array")
		return errors
	var ids := {}
	var footprints: Array[Rect2] = []
	for entry in entries:
		if not entry is Dictionary:
			errors.append("Prop must be an object")
			continue
		var id: String = str(entry.get("id", ""))
		if id.is_empty() or ids.has(id):
			errors.append("Prop IDs must be nonempty and unique")
		ids[id] = true
		if not entry.get("kind", "") in ["rack", "bench", "tank", "filter"]:
			errors.append("Unknown prop renderer: " + id)
		var valid := true
		for key in ["center", "footprint"]:
			var pair: Variant = entry.get(key)
			if not pair is Array or pair.size() != 2:
				valid = false
			else:
				for component in pair:
					if not (component is float or component is int):
						valid = false
		if not valid:
			errors.append("Prop center/footprint must be numeric pairs: " + id)
			continue
		var center := Vector2(entry.center[0], entry.center[1])
		var size := Vector2(entry.footprint[0], entry.footprint[1])
		if not center.is_finite() or not size.is_finite() or size.x <= 0 or size.y <= 0:
			errors.append("Prop dimensions must be finite and positive: " + id)
			continue
		var rect := Rect2(center - size * 0.5, size)
		if not Rect2(-176, -176, 352, 352).encloses(rect):
			errors.append("Invalid or out-of-hull prop footprint: " + id)
		# Reserve the canonical cross aisle, including character clearance.
		if rect.grow(RADIUS).intersects(Rect2(-OPENING * 0.5, -192, OPENING, 384)) or rect.grow(RADIUS).intersects(Rect2(-192, -OPENING * 0.5, 384, OPENING)):
			errors.append("Prop obstructs reserved center aisle: " + id)
		for other in footprints:
			if other.intersects(rect):
				errors.append("Overlapping prop footprint: " + id)
		footprints.append(rect)
	return errors

static func turn(v: Vector2, quarter: int) -> Vector2:
	for unused in range(posmod(quarter, 4)):
		v = Vector2(-v.y, v.x)
	return v

static func rooms(quarter: int, individual: Array = [0, 0]) -> Array:
	return [
		{"cell": Vector2i.ZERO, "rotation": posmod(quarter + int(individual[0]), 4), "kind": 0},
		{"cell": Vector2i(turn(Vector2.DOWN, quarter)), "rotation": posmod(quarter + int(individual[1]), 4), "kind": 1}
	]

static func has_port(room: Dictionary, side: int) -> bool:
	if room.kind == 0:
		for port in recipe.doors:
			if int(port) == posmod(side - int(room.rotation), 4):
				return true
		return false
	return MASKS[room.kind].has(posmod(side - int(room.rotation), 4))

static func edges(layout: Array) -> Array:
	var result: Array = []
	var seen := {}
	for room in layout:
		for side in range(4):
			var cell: Vector2i = room.cell
			var next: Vector2i = cell + DIRS[side]
			var center := Vector2(cell) * CELL + Vector2(DIRS[side]) * CELL * 0.5
			var key := "%d:%d" % [roundi(center.x), roundi(center.y)]
			if seen.has(key):
				continue
			seen[key] = true
			var neighbor: Dictionary = {}
			for candidate in layout:
				if candidate.cell == next:
					neighbor = candidate
			var shared := not neighbor.is_empty()
			var opened := shared and has_port(room, side) and has_port(neighbor, (side + 2) % 4)
			result.append({"center": center, "horizontal": side % 2 == 0,
				"open": opened, "shared": shared, "port": has_port(room, side)})
	return result

static func wall_rects(edge: Dictionary) -> Array:
	var spans: Array = [[-CELL * 0.5, CELL]]
	if edge.open:
		var aperture: float = edge.get("aperture", OPENING)
		spans = [[-CELL * 0.5, (CELL - aperture) * 0.5], [aperture * 0.5, (CELL - aperture) * 0.5]]
	var result: Array = []
	for span in spans:
		var offset := Vector2(float(span[0]), -WALL * 0.5)
		var size := Vector2(float(span[1]), WALL)
		if not edge.horizontal:
			offset = Vector2(offset.y, offset.x)
			size = Vector2(size.y, size.x)
		result.append(Rect2(edge.center + offset, size))
	return result

static func jamb_rects(edge: Dictionary) -> Array:
	if not edge.open:
		return []
	var axis := Vector2.RIGHT if edge.horizontal else Vector2.DOWN
	var result: Array = []
	for sign_value in [-1, 1]:
		var center: Vector2 = edge.center + axis * (float(edge.get("aperture", OPENING)) + WALL) * 0.5 * sign_value
		result.append(Rect2(center - Vector2.ONE * WALL * 0.5, Vector2.ONE * WALL))
	return result

static func props(layout: Array) -> Array:
	var result: Array = []
	for room in layout:
		if room.kind == 0:
			for entry in recipe.props:
				var center := Vector2(room.cell) * CELL + turn(Vector2(entry.center[0], entry.center[1]), room.rotation)
				var size := Vector2(entry.footprint[0], entry.footprint[1])
				if int(room.rotation) % 2 == 1:
					size = Vector2(size.y, size.x)
				result.append({"id": entry.id, "kind": entry.kind, "rect": Rect2(center - size * 0.5, size), "facing": room.rotation,
					"sort_y": center.y + size.y * 0.5, "room": room.kind})
			continue
		var kinds := ["rack", "bench", "tank", "filter"] if room.kind == 0 else ["tank", "filter", "tank", "bench"]
		var offsets := [Vector2(-108, -100), Vector2(108, -100), Vector2(-108, 106), Vector2(108, 106)]
		for i in range(4):
			var center := Vector2(room.cell) * CELL + turn(offsets[i], room.rotation)
			var size := Vector2(102, 74) if kinds[i] != "tank" else Vector2(78, 78)
			if int(room.rotation) % 2 == 1:
				size = Vector2(size.y, size.x)
			result.append({"kind": kinds[i], "rect": Rect2(center - size * 0.5, size), "facing": room.rotation,
				"sort_y": center.y + size.y * 0.5, "room": room.kind})
	return result

static func can_stand(point: Vector2, layout: Array, furnishings: Array, structure: Array) -> bool:
	var inside := false
	for room in layout:
		if Rect2(Vector2(room.cell) * CELL - Vector2.ONE * CELL * 0.5, Vector2.ONE * CELL).has_point(point):
			inside = true
	if not inside:
		return false
	for edge in structure:
		for rect in wall_rects(edge):
			if rect.grow(RADIUS).has_point(point):
				return false
	for prop in furnishings:
		if prop.rect.grow(RADIUS).has_point(point):
			return false
	return true
