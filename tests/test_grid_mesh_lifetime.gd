extends SceneTree
func _init() -> void:
	var grid = preload("res://scripts/grid_canvas.gd").new()
	var mesh: ArrayMesh = grid._foundation_contact_mesh(96.0, false)
	var live: WeakRef = weakref(mesh)
	mesh = null
	var retained := live.get_ref() != null
	grid.free()
	var released := live.get_ref() == null
	print("GRID MESH LIFETIME ", "PASS" if retained and released else "FAIL")
	quit(0 if retained and released else 1)
