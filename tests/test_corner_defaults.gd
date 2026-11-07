extends SceneTree
const Geometry=preload("res://rooms/underwater/corridor_geometry.gd")
const Turn=preload("res://tools/modular_room_geometry.gd")
func _init() -> void:
	var uid="res://tests/test_corner_defaults.gd.uid"
	if not FileAccess.file_exists(uid):
		var f=FileAccess.open(uid,FileAccess.WRITE)
		f.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
	assert(Geometry.next_corner_rotation([],[])==0)
	assert(Geometry.next_corner_rotation([],[{"id":"corner"}])==3)
	assert(Geometry.next_corner_rotation([{"id":"corner","rotation":2}],[])==3)
	assert(Geometry.next_corner_rotation([{"id":"corner"}],[{"id":"corner"}])==0)
	assert(Geometry.next_corner_rotation([{"id":"corridor"}],[{"id":"tee_corridor"}])==0)
	assert(Turn.turn(Vector2.LEFT,3)==Vector2.DOWN and Turn.turn(Vector2.DOWN,3)==Vector2.RIGHT)
	var main=preload("res://scripts/main.gd").new()
	main.placed_rooms=[{"id":"corner","rotation":2}]
	assert(main._default_card_rotation("corner")==3)
	assert(main.placed_rooms[0].rotation==2,"Existing corner rotation preserved")
	main.drone_fleet.orders=[{"id":"corner","rotation":3}]
	assert(main._default_card_rotation("corner")==0,"Queued construction counts before completion")
	main.free()
	print("CORNER DEFAULTS PASS: alternating left/right, queued jobs, unrelated rooms and existing rotation preservation")
	quit()
