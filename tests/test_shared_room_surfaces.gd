extends SceneTree
const Floor = preload("res://rooms/whole-room/room_floor.gd")
const Door = preload("res://rooms/whole-room/room_door.gd")
const Geometry = preload("res://tools/modular_room_geometry.gd")
func _init() -> void:
	assert(Floor.TILE==Geometry.FLOOR_TILE and Door.OPENING==Geometry.OPENING)
	for i in range(1,Floor.SEAMS.size()): assert(Floor.SEAMS[i]-Floor.SEAMS[i-1]==48)
	assert(Door.leaf_rects(1.0).is_empty())
	for frame in range(10):
		var amount := float(frame)/9
		var leaves := Door.leaf_rects(amount)
		if leaves.is_empty(): continue
		assert(is_equal_approx(leaves[0].position.x,-36))
		assert(is_equal_approx(leaves[1].end.x,36))
		assert(is_equal_approx(leaves[1].position.x-leaves[0].end.x,72*amount))
		assert(not leaves[0].intersects(leaves[1]))
	print("SHARED SURFACES PASS: one 48-unit grid, 72-unit aperture, 10 monotonic door frames, fully open leaves absent")
	quit()
