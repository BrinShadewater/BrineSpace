extends SceneTree
const Branch=preload("res://scripts/station_branch.gd")
func _init() -> void:
	var linked:=func(_a: Dictionary,_b: Dictionary,_direction: Vector2i)->bool:return true
	var rooms: Array=[{"id":"brine_core","pos":Vector2i(0,0)},{"id":"corridor","pos":Vector2i(1,0)},{"id":"storage_bay","pos":Vector2i(2,0)}]
	var before:=var_to_bytes(rooms)
	var result:=Branch.plan(rooms,Vector2i(1,0),Vector2i(0,0),linked)
	assert(result.ok and result.cells.size()==2)
	assert(var_to_bytes(rooms)==before,"Planning must not mutate the station")
	assert(not Branch.plan(rooms,Vector2i(0,0),Vector2i(1,0),linked).ok)
	assert(not Branch.plan(rooms,Vector2i(0,0),Vector2i(2,0),linked).ok)
	assert(not Branch.plan(rooms,Vector2i(1,0),Vector2i(0,0),func(_a,_b,_d):return false).ok)
	rooms.append_array([{"id":"corridor","pos":Vector2i(0,1)},{"id":"corridor","pos":Vector2i(1,1)}])
	assert(not Branch.plan(rooms,Vector2i(1,0),Vector2i(0,0),linked).ok,"Loops must not be misidentified as isolated branches")
	print("STATION BRANCH PASS: bridge selection, core protection, loops, closed doors, immutable planning")
	quit()
