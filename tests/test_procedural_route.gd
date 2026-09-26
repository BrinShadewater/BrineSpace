extends SceneTree
const Route = preload("res://tests/procedural_route.gd")
var failures := 0
func check(ok: bool, label: String):
	if not ok: failures += 1; push_error(label)
func _init():
	var target := Vector2i(23,15)
	var occupied := {Vector2i(23,17): {"id":"corridor"}}
	var sites := {Vector2i(22,17): {"units":0}, Vector2i(24,17): {"units":12}}
	var wrecks := {target: {"cleared":false}}
	var field := Route.distances(target,occupied,wrecks,sites)
	check(not field.has(Vector2i(23,17)),"Occupied rooms cannot shortcut the water route")
	check(field.has(Vector2i(22,17)),"Exhausted deposits permit construction")
	check(not field.has(Vector2i(24,17)),"Live deposits block construction")
	check(field[Vector2i(23,18)]>2,"Route must detour around the existing room")
	check(not Route.preserves_route(Vector2i(23,18),[Vector2i.UP],field),"Door into occupied room cannot be an onward route")
	check(Route.preserves_route(Vector2i(23,18),[Vector2i.LEFT],field),"Side door can follow the open detour")
	check(not Route.preserves_route(Vector2i(23,18),[Vector2i.DOWN],field),"Door away from target cannot cap the best frontier")
	check(Route.preserves_route(Vector2i(23,16),[],field),"Destination delegates chamber door compatibility to placement")
	occupied[Vector2i(23,16)]={"id":"galley"}
	field=Route.distances(target,occupied,wrecks,sites)
	check(not field.has(Vector2i(23,16)) and field.get(Vector2i(23,14))==0,"Occupied approach leaves the opposite approach available")
	occupied[Vector2i(23,14)]={"id":"galley"}
	check(Route.distances(target,occupied,wrecks,sites).is_empty(),"Two occupied approaches cannot seed a phantom route")
	field=Route.distances(Vector2i.ZERO,{}, {Vector2i.ZERO:{"cleared":false}}, {})
	check(not field.has(Vector2i.UP) and field.get(Vector2i.DOWN)==0,"Boundary approach stays inside the grid")
	print("PROCEDURAL ROUTE: failures=",failures)
	quit(0 if failures==0 else 1)
