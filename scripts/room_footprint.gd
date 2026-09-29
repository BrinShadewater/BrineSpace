extends RefCounted
class_name RoomFootprint

const RoomDatabaseScript = preload("res://scripts/room_database.gd")
const SIDES := ["north", "east", "south", "west"]

static func cells(anchor: Vector2i, size: Vector2i) -> Array[Vector2i]:
	var result: Array[Vector2i] = []
	for y in range(maxi(size.y, 0)):
		for x in range(maxi(size.x, 0)):
			result.append(anchor + Vector2i(x, y))
	return result

static func ports(room: Dictionary) -> Array[Dictionary]:
	var result: Array[Dictionary] = []
	var anchor: Vector2i = room.get("pos", Vector2i.ZERO)
	var size: Vector2i = room.get("size", Vector2i.ONE)
	var rotation: int = posmod(int(room.get("rotation", 0)), 4)
	var local_ports: Array = room.get("ports", [])
	if not room.has("ports") and size == Vector2i.ONE:
		var template: Dictionary = RoomDatabaseScript.get_room(str(room.get("id", "")))
		var layout: Dictionary = RoomDatabaseScript.get_layout(str(room.get("layout", template.get("layout", "cross"))))
		for side in layout.get("doors", []):
			local_ports.append({"cell": Vector2i.ZERO, "side": str(side)})
	for port in local_ports:
		if not port is Dictionary:
			continue
		var local: Vector2i = port.get("cell", Vector2i(-1, -1))
		var side := str(port.get("side", ""))
		if not SIDES.has(side) or not _on_edge(local, side, size):
			continue
		var rotated := local
		var rotated_size := size
		for _turn in range(rotation):
			rotated = Vector2i(rotated_size.y - 1 - rotated.y, rotated.x)
			rotated_size = Vector2i(rotated_size.y, rotated_size.x)
		result.append({"cell": anchor + rotated, "side": SIDES[(SIDES.find(side) + rotation) % 4]})
	return result

static func exterior_cells(room: Dictionary, side: String) -> Array[Vector2i]:
	var result: Array[Vector2i] = []
	var anchor: Vector2i = room.get("pos", Vector2i.ZERO)
	var size: Vector2i = room.get("size", Vector2i.ONE)
	if side == "north" or side == "south":
		var y := anchor.y - 1 if side == "north" else anchor.y + size.y
		for x in range(size.x):
			result.append(Vector2i(anchor.x + x, y))
	elif side == "west" or side == "east":
		var x := anchor.x - 1 if side == "west" else anchor.x + size.x
		for y in range(size.y):
			result.append(Vector2i(x, anchor.y + y))
	return result

static func room_at(occupied: Dictionary, cell: Vector2i) -> Dictionary:
	return occupied.get(cell, {})

static func _on_edge(cell: Vector2i, side: String, size: Vector2i) -> bool:
	if cell.x < 0 or cell.y < 0 or cell.x >= size.x or cell.y >= size.y:
		return false
	match side:
		"north": return cell.y == 0
		"east": return cell.x == size.x - 1
		"south": return cell.y == size.y - 1
		"west": return cell.x == 0
	return false
