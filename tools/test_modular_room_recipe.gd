extends SceneTree
const Geometry = preload("res://tools/modular_room_geometry.gd")

func _init() -> void:
	var failures: Array[String] = []
	if not Geometry.recipe_errors(Geometry.recipe).is_empty():
		failures.append("Valid production recipe rejected")
	var invalid_cases: Array[Dictionary] = []
	for field in ["doors", "props", "asset_roots"]:
		var missing := Geometry.recipe.duplicate(true)
		missing.erase(field)
		invalid_cases.append(missing)
	var duplicate := Geometry.recipe.duplicate(true)
	duplicate.props[1].id = duplicate.props[0].id
	invalid_cases.append(duplicate)
	var blocked := Geometry.recipe.duplicate(true)
	blocked.props[0].center = [0, 0]
	invalid_cases.append(blocked)
	var outside := Geometry.recipe.duplicate(true)
	outside.props[0].center = [190, 190]
	invalid_cases.append(outside)
	var negative := Geometry.recipe.duplicate(true)
	negative.props[0].footprint = [-1, 74]
	invalid_cases.append(negative)
	var malformed := Geometry.recipe.duplicate(true)
	malformed.props[0].center = ["bad", 0]
	invalid_cases.append(malformed)
	var wrong_port := Geometry.recipe.duplicate(true)
	wrong_port.doors = [1.5]
	invalid_cases.append(wrong_port)
	var duplicate_port := Geometry.recipe.duplicate(true)
	duplicate_port.doors = [1, 1]
	invalid_cases.append(duplicate_port)
	var unknown := Geometry.recipe.duplicate(true)
	unknown.props[0].kind = "unimplemented"
	invalid_cases.append(unknown)
	for i in range(invalid_cases.size()):
		if Geometry.recipe_errors(invalid_cases[i]).is_empty():
			failures.append("Invalid recipe accepted: case %d" % i)
	for q in range(4):
		var props := Geometry.props(Geometry.rooms(q))
		for index in range(Geometry.recipe.props.size()):
			var entry: Dictionary = Geometry.recipe.props[index]
			var actual: Dictionary = props[index]
			var expected := Geometry.turn(Vector2(entry.center[0], entry.center[1]), q)
			if actual.id != entry.id or actual.rect.get_center() != expected:
				failures.append("Recipe placement did not rotate with the room")
	if not failures.is_empty():
		push_error(str(failures))
		quit(1)
		return
	print("RECIPE PASS: valid recipe, %d rejected mutations, 16 registered prop placements" % invalid_cases.size())
	quit(0)
